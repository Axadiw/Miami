import asyncio
import logging
from datetime import datetime, timedelta
from math import floor
from queue import Queue
from typing import Type, Any, Callable

from sqlalchemy import select, text, func
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from data_harvesters.consts import MAX_CONCURRENT_FETCHES, MAX_CANDLES_HISTORY_TO_FETCH, \
    MAX_CONCURRENT_GAPS_CALCULATIONS, GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND
from data_harvesters.data_to_fetch import DataToFetch
from data_harvesters.database import pg_bulk_insert, async_session_generator
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from data_harvesters.harvester_core.common_harvester import fetch_list_of_symbols, fetch_exchange_entry, \
    get_subset_of_timeframes
from data_harvesters.helpers.semaphore_gather import semaphore_gather
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.skipped_gap import SkippedGap
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
        self.requires_refetch = True
        self.configured = False

    async def fetch_all_ohlcv(self, data_to_fetch: list[DataToFetch]) -> object:
        self.temporary_ohlcv_fetching_db_sessions = [async_session_generator()() for i in
                                                     range(0, MAX_CONCURRENT_FETCHES)]
        self.temporary_ohlcv_fetching_exchange_connectors = [self.exchange_connector_generator() for i in
                                                             range(0, MAX_CONCURRENT_FETCHES)]
        connector = self.exchange_connector_generator()
        time_before_fetch = await connector.get_server_time()
        await connector.close()
        with elapsed_timer() as elapsed:
            new_candles_counts = await semaphore_gather(MAX_CONCURRENT_FETCHES,
                                                        [self.fetch_and_save_single_ohlcv(data=data,
                                                                                          time_before_fetch=time_before_fetch,
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

    async def fetch_and_save_single_ohlcv(self, data: DataToFetch, time_before_fetch: datetime, current_fetch: int,
                                          all_fetches: int):
        db_session = self.temporary_ohlcv_fetching_db_sessions.pop()
        new_candles: list[OHLCV] = await self.fetch_single_ohlcv(data=data, time_before_fetch=time_before_fetch,
                                                                 current_fetch=current_fetch,
                                                                 all_fetches=all_fetches)

        def conflict_passer(statement: Insert):
            # return statement
            return statement.on_conflict_do_nothing()

        if len(new_candles) > 0:
            expected_candles_count = floor((data.end - data.start).total_seconds() / data.timeframe.seconds)
            if expected_candles_count != len(new_candles):
                new_candles += self.generate_missing_candles_in_front(candles=new_candles, start_time=data.start,
                                                                      timeframe=data.timeframe)
            success = False
            while not success:
                try:
                    await pg_bulk_insert(session=db_session, table=OHLCV, data=[{"exchange": candle.exchange,
                                                                                 "symbol": candle.symbol,
                                                                                 "timeframe": candle.timeframe,
                                                                                 "timestamp": candle.timestamp,
                                                                                 "open": candle.open,
                                                                                 "high": candle.high,
                                                                                 "low": candle.low,
                                                                                 "close": candle.close,
                                                                                 "volume": candle.volume} for candle
                                                                                in
                                                                                new_candles],
                                         statement_modifier=conflict_passer)
                    await db_session.commit()
                    await db_session.flush()

                    success = True
                except Exception as e:
                    await db_session.rollback()
                    logging.error(
                        f'fetch_and_save_single_ohlcv insert new error {data.symbol.name} {data.timeframe.name} {e}')
                    await asyncio.sleep(1)
        else:
            await self.create_skipped_gap(conflict_passer, data, db_session)
        self.temporary_ohlcv_fetching_db_sessions.append(db_session)
        return len(new_candles)

    async def create_skipped_gap(self, conflict_passer, data, db_session):
        try:
            await pg_bulk_insert(session=db_session, table=SkippedGap, data=[{"exchange": self.exchange.id,
                                                                              "symbol": data.symbol.id,
                                                                              "timeframe": data.timeframe.id,
                                                                              "start": data.start,
                                                                              "end": data.end}],
                                 statement_modifier=conflict_passer)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            logging.error(
                f'fetch_and_save_single_ohlcv create gap error {data.symbol.name} {data.timeframe.name} {e}')
            await asyncio.sleep(1)

    @staticmethod
    def generate_missing_candles_in_front(candles: list[OHLCV], start_time: datetime, timeframe: Type[Timeframe]):
        candles_to_add = []
        candles.sort(key=sort_ohlcv_by_timestamp_key)
        first_candle = candles[0]
        candles_missing_in_front = floor(
            (first_candle.timestamp - start_time).total_seconds() / timeframe.seconds)
        if candles_missing_in_front > 0:
            for i in range(1, candles_missing_in_front + 1):
                candles_to_add.append(OHLCV(timestamp=first_candle.timestamp - timedelta(seconds=i * timeframe.seconds),
                                            exchange=first_candle.exchange, symbol=first_candle.symbol,
                                            timeframe=first_candle.timeframe, open=first_candle.open,
                                            high=first_candle.open,
                                            low=first_candle.open, close=first_candle.open, volume=0))
        return candles_to_add

    async def fetch_single_ohlcv(self, data: DataToFetch, time_before_fetch: datetime, current_fetch: int,
                                 all_fetches: int):
        with elapsed_timer() as elapsed:
            success = False
            new_candles = []
            exchange_connector = self.temporary_ohlcv_fetching_exchange_connectors.pop()
            while not success:
                try:
                    new_candles = await exchange_connector.fetch_ohlcv(data=data, exchange=self.exchange,
                                                                       time_before_fetch=time_before_fetch)
                    logging.info(
                        f'Fetched {len(new_candles)} new entries for\t{data}\t({current_fetch} / {all_fetches}).\t'
                        f'Took {"{:.2f}".format(elapsed())} seconds')
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

    async def find_all_gaps(self, current_symbols) -> list[DataToFetch]:
        logging.info(f'[Historical Harvester] Starting to look for gaps in OHLCV data')
        exchange_connector = self.exchange_connector_generator()

        with elapsed_timer() as elapsed:
            all_gaps = []

            end_time: datetime = await exchange_connector.get_server_time()
            end_time = datetime(year=end_time.year, month=end_time.month, day=end_time.day, hour=end_time.hour,
                                minute=end_time.minute) - timedelta(seconds=1)
            find_gap_coroutines = []
            self.temporary_gaps_finding_db_sessions = [async_session_generator()() for i in
                                                       range(0, MAX_CONCURRENT_GAPS_CALCULATIONS)]

            for timeframe in await get_subset_of_timeframes(self.supported_ohlcv_timeframes_names):
                for symbol in current_symbols:
                    find_gap_coroutines.append(self.gap_finder(symbol=symbol, timeframe=timeframe, end_time=end_time))

            for gap in await semaphore_gather(MAX_CONCURRENT_GAPS_CALCULATIONS, find_gap_coroutines):
                all_gaps += gap

            logging.info(
                f'[Historical Harvester] Found {len(all_gaps)} gaps. Took {"{:.2f}".format(elapsed())} seconds')
            for session in self.temporary_gaps_finding_db_sessions:
                await session.close()
            self.temporary_gaps_finding_db_sessions = []
            await exchange_connector.close()
            return all_gaps

    async def gap_finder(self, symbol: Type[Symbol], timeframe: Type[Timeframe], end_time: datetime):
        start_time = self.get_earliest_possible_date_for_ohlcv(symbol, timeframe)
        db_session = self.temporary_gaps_finding_db_sessions.pop()
        gaps_to_merge = await self.find_gaps(symbol, timeframe, start_time, end_time, db_session)

        gaps_to_merge.sort(key=sort_data_to_fetch_by_start_key)
        merged_gaps: list[DataToFetch] = []
        while len(gaps_to_merge) > 0:
            current_gap = gaps_to_merge.pop(0)
            while len(gaps_to_merge) > 0:
                if (gaps_to_merge[0].start - current_gap.end).total_seconds() < 5 * timeframe.seconds and \
                        gaps_to_merge[0].end >= current_gap.end:
                    current_gap.end = gaps_to_merge.pop(0).end
                else:
                    break
            if current_gap.length().total_seconds() > current_gap.timeframe.seconds:
                merged_gaps.append(current_gap)

        gaps_with_skipped_filtered_out = []
        for gap_to_check in merged_gaps:
            if (await db_session.execute(select(func.count(SkippedGap.id)).filter_by(exchange=self.exchange.id,
                                                                                     symbol=gap_to_check.symbol.id,
                                                                                     timeframe=gap_to_check.timeframe.id,
                                                                                     start=gap_to_check.start,
                                                                                     end=gap_to_check.end))).scalar() == 0:
                gaps_with_skipped_filtered_out.append(gap_to_check)

        self.temporary_gaps_finding_db_sessions.append(db_session)
        return gaps_with_skipped_filtered_out

    async def find_gaps(self, symbol, timeframe, start_time, end_time, db_session: AsyncSession):
        query = text(f''
                     f'SELECT'
                     f'	*'
                     f'FROM ('
                     f'	SELECT'
                     f'		"OHLCV".timestamp AS START,'
                     f'		"OHLCV".timestamp - lag("OHLCV".timestamp) OVER (ORDER BY "OHLCV"."timestamp" ASC) AS differ'
                     f'	FROM'
                     f'		"OHLCV"'
                     f'	WHERE'
                     f'		"OHLCV"."exchange" = {self.exchange.id}'
                     f'		AND "OHLCV"."symbol" = {symbol.id}'
                     f'		AND "OHLCV"."timeframe" = {timeframe.id}'
                     f'		AND "OHLCV"."timestamp" > \'{str(start_time)}\''
                     f'		AND "OHLCV"."timestamp" <= \'{str(end_time)}\' ORDER BY'
                     f'			"OHLCV"."timestamp" ASC) as raw'
                     f'	WHERE'
                     f'		MOD(EXTRACT(EPOCH FROM raw.differ)::int,{timeframe.seconds}) = 0 and'  # filter out gaps that are probably because of the time change
                     f'		raw.differ != {timeframe.seconds}*\'1 sec\'::interval')
        results = (await db_session.execute(query)).all()
        gaps = list(
            map(lambda x: DataToFetch(symbol=symbol, timeframe=timeframe, start=x[0] - x[1], end=x[0]), results))

        for gap in gaps:
            gap.start += timedelta(seconds=1)
            gap.end -= timedelta(seconds=1)

        first_timestamp = (await db_session.execute(select(OHLCV.timestamp).filter_by(exchange=self.exchange.id,
                                                                                      symbol=symbol.id,
                                                                                      timeframe=timeframe.id)
                                                    .filter(OHLCV.timestamp > start_time)
                                                    .filter(OHLCV.timestamp <= end_time)
                                                    .order_by(OHLCV.timestamp.asc()).limit(1))).scalar()

        last_timestamp = (await db_session.execute(select(OHLCV.timestamp).filter_by(exchange=self.exchange.id,
                                                                                     symbol=symbol.id,
                                                                                     timeframe=timeframe.id)
                                                   .filter(OHLCV.timestamp > start_time)
                                                   .filter(OHLCV.timestamp <= end_time)
                                                   .order_by(OHLCV.timestamp.desc()).limit(1))).scalar()

        if first_timestamp is not None and (first_timestamp - start_time).total_seconds() > timeframe.seconds:
            gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=start_time,
                                    end=first_timestamp - timedelta(seconds=1)))

        if last_timestamp is not None and (end_time - last_timestamp).total_seconds() > timeframe.seconds:
            gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=last_timestamp + timedelta(seconds=1),
                                    end=end_time))

        if first_timestamp is None and last_timestamp is None:
            gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=start_time,
                                    end=end_time))
        return gaps

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
                ohlcv_data_to_fetch = await self.find_all_gaps(current_symbols)
                await self.fetch_all_ohlcv(ohlcv_data_to_fetch)
            await asyncio.sleep(1)

    async def start(self):
        await asyncio.gather(*[self.start_queue_loop(), self.fetch_candles()])
