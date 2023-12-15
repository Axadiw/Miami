import asyncio
import logging
from datetime import datetime, timedelta
from queue import Queue
from typing import Type, Any, Callable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from data_harvesters.consts import MAX_CONCURRENT_FETCHES, MAX_CANDLES_HISTORY_TO_FETCH, \
    GLOBAL_QUEUE_START_COMMAND
from data_harvesters.data_to_fetch import DataToFetch
from data_harvesters.database import pg_bulk_insert, async_session_generator, get_session
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from data_harvesters.harvester_core.common_harvester import fetch_list_of_symbols, fetch_exchange_entry, \
    get_subset_of_timeframes
from data_harvesters.helpers.semaphore_gather import semaphore_gather
from models.exchange import Exchange
from models.last_fetched_date import LastFetchedDate
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe
from timer import elapsed_timer


def sort_data_to_fetch_by_start_key(e: DataToFetch):
    return e.start


def sort_ohlcv_by_timestamp_key(e: OHLCV):
    return e.timestamp


class HistoricalHarvester:
    symbol_start_dates: dict[Any, Any]
    exchange: Type[Exchange]
    temporary_gaps_finding_db_sessions: list[AsyncSession]
    temporary_ohlcv_fetching_db_sessions: list[AsyncSession]
    temporary_ohlcv_fetching_exchange_connectors: list[BaseExchangeConnector]

    def __init__(self, exchange_name: str, client_generator: Callable, queue: Queue,
                 ohlcv_timeframe_names: list[str]):
        logging.info('[Historical Harvester] Initializing ')

        self.exchange_name = exchange_name
        self.exchange_connector_generator = client_generator
        self.queue = queue
        self.supported_ohlcv_timeframes_names = ohlcv_timeframe_names
        self.configured = False

    async def fetch_all_ohlcv(self, data_to_fetch: list[DataToFetch]) -> object:
        self.temporary_ohlcv_fetching_db_sessions = [async_session_generator()() for _ in
                                                     range(0, MAX_CONCURRENT_FETCHES)]
        self.temporary_ohlcv_fetching_exchange_connectors = [self.exchange_connector_generator() for _ in
                                                             range(0, MAX_CONCURRENT_FETCHES)]
        with elapsed_timer() as elapsed:
            new_candles_counts = await semaphore_gather(MAX_CONCURRENT_FETCHES,
                                                        [self.fetch_and_save_single_ohlcv(data=data,
                                                                                          current_fetch=index + 1,
                                                                                          all_fetches=len(
                                                                                              data_to_fetch))
                                                         for index, data in enumerate(data_to_fetch)])
            new_candles_for_all_symbols_count = 0
            for count in new_candles_counts:
                new_candles_for_all_symbols_count += count

            for session in self.temporary_ohlcv_fetching_db_sessions:
                await session.close()
            for connector in self.temporary_ohlcv_fetching_exchange_connectors:
                await connector.close()
            self.temporary_ohlcv_fetching_db_sessions = []
            self.temporary_ohlcv_fetching_exchange_connectors = []
            logging.info(
                f'[Historical Harvester] Finished updating history for all symbols in all timeframes. '
                f'Added {new_candles_for_all_symbols_count} new entries '
                f'Took {"{:.2f}".format(elapsed())} seconds')
            return new_candles_for_all_symbols_count

    async def fetch_and_save_single_ohlcv(self, data: DataToFetch, current_fetch: int,
                                          all_fetches: int):
        with elapsed_timer() as elapsed:
            new_candles: list[OHLCV] = await self.fetch_single_ohlcv(data=data, current_fetch=current_fetch,
                                                                     all_fetches=all_fetches)
            fetch_length = elapsed()
            await self.save_candles(data, new_candles)
            logging.info(
                f'Handled {len(new_candles)} new entries for\t{data}\t({current_fetch} / {all_fetches}).\t'
                f'Fetch {"{:.2f}".format(fetch_length)} s, save {"{:.2f}".format(elapsed() - fetch_length)} s. Total {"{:.2f}".format(elapsed())} s')
            return len(new_candles)

    async def save_candles(self, data, new_candles):
        db_session = self.temporary_ohlcv_fetching_db_sessions.pop()

        def conflict_passer(statement: Insert):
            return statement.on_conflict_do_nothing()

        if len(new_candles) > 0:
            success = False
            while not success:
                try:
                    await pg_bulk_insert(session=db_session, table=OHLCV, data=new_candles,
                                         statement_modifier=conflict_passer)
                    await db_session.commit()
                    await db_session.flush()
                    await self.update_last_fetched_date(data=data, db_session=db_session)
                    success = True
                except Exception as e:
                    await db_session.rollback()
                    logging.error(
                        f'fetch_and_save_single_ohlcv insert new error {data.symbol.name} {data.timeframe.name} {e}')
                    await asyncio.sleep(1)
        self.temporary_ohlcv_fetching_db_sessions.append(db_session)

    async def update_last_fetched_date(self, data: DataToFetch, db_session: AsyncSession):
        existing_date_entry = (await db_session.execute(
            select(LastFetchedDate).filter_by(exchange=self.exchange.id, symbol=data.symbol.id,
                                              timeframe=data.timeframe.id))).scalar_one_or_none()

        if existing_date_entry is None:
            db_session.add(LastFetchedDate(exchange=self.exchange.id, symbol=data.symbol.id,
                                           timeframe=data.timeframe.id, last_fetched=data.end))
        else:
            existing_date_entry.last_fetched = data.end
        await db_session.commit()

    async def fetch_single_ohlcv(self, data: DataToFetch, current_fetch: int,
                                 all_fetches: int):
        success = False
        new_candles = []
        exchange_connector = self.temporary_ohlcv_fetching_exchange_connectors.pop()
        while not success:
            try:
                new_candles = await exchange_connector.fetch_ohlcv(data=data, exchange=self.exchange)
                success = True
            except Exception as e:
                logging.error(f'Update Single fetch_single_ohlcv {data.symbol.name} {data.timeframe.name} {e}')
                await asyncio.sleep(1)
        self.temporary_ohlcv_fetching_exchange_connectors.append(exchange_connector)
        return new_candles

    def get_earliest_possible_date_for_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe]) -> datetime:
        return max(self.symbol_start_dates[symbol.name],
                   max(datetime.fromtimestamp(0),
                       datetime.now() - timedelta(seconds=timeframe.seconds * MAX_CANDLES_HISTORY_TO_FETCH)))

    async def find_data_to_fetch(self, current_symbols) -> list[DataToFetch]:
        with elapsed_timer() as elapsed:
            data_to_fetch = []
            exchange_connector = self.exchange_connector_generator()  # TODO: figure out how to use context there
            end_time: datetime = await exchange_connector.get_server_time()
            await exchange_connector.close()
            async with get_session() as db_session:
                last_fetched_dates = {}
                for entry in list((await db_session.execute(
                        select(LastFetchedDate).filter_by(exchange=self.exchange.id))).scalars()):
                    last_fetched_dates[f'{entry.symbol}_{entry.timeframe}'] = entry.last_fetched

                for timeframe in await get_subset_of_timeframes(self.supported_ohlcv_timeframes_names):
                    for symbol in current_symbols:
                        pair_id = f'{symbol.id}_{timeframe.id}'
                        start_time = last_fetched_dates[
                            pair_id] if pair_id in last_fetched_dates else self.get_earliest_possible_date_for_ohlcv(
                            symbol, timeframe)

                        data_to_fetch.append(
                            DataToFetch(symbol=symbol, timeframe=timeframe, start=start_time, end=end_time))
            logging.info(
                f'Calculated date ranges to fetch '
                f'Took {"{:.2f}".format(elapsed())} seconds')
            return data_to_fetch

    async def configure(self):
        exchange_connector = self.exchange_connector_generator()  # TODO: figure out how to use context there
        self.exchange = await fetch_exchange_entry(self.exchange_name)
        self.symbol_start_dates = await exchange_connector.fetch_start_dates()
        await exchange_connector.close()
        self.configured = True

    async def start_queue_loop(self):
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, self.queue.get)

            if command == GLOBAL_QUEUE_START_COMMAND:
                await self.configure()

    async def fetch_candles(self):
        while True:
            if self.configured:
                current_symbols = await fetch_list_of_symbols(self.exchange)
                ohlcv_data_to_fetch = await self.find_data_to_fetch(current_symbols)
                await self.fetch_all_ohlcv(ohlcv_data_to_fetch)
            await asyncio.sleep(1)

    async def start(self):
        await asyncio.gather(*[self.start_queue_loop(), self.fetch_candles()])
