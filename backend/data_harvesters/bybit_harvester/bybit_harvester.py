import asyncio
import logging
from datetime import datetime, timedelta
from math import floor
from typing import Type, Any, Callable

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from data_harvesters.bybit_harvester.bybit_harverser_watcher import BybitHarvesterWatcher
from data_harvesters.consts import MAX_CONCURRENT_FETCHES, MAX_CANDLES_HISTORY_TO_FETCH, \
    MAX_CONCURRENT_GAPS_CALCULATIONS
from data_harvesters.data_to_fetch import DataToFetch
from data_harvesters.database import get_session, pg_bulk_insert, async_session_generator
from data_harvesters.helpers.semaphore_gather import semaphore_gather
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe
from timer import elapsed_timer

EXCHANGE_NAME = 'bybit'


def sort_data_to_fetch_by_start_key(e: DataToFetch):
    return e.start


def sort_ohlcv_by_timestamp_key(e: OHLCV):
    return e.timestamp


class BybitHarvester:
    watcher: BybitHarvesterWatcher
    symbol_start_dates: dict[Any, Any]
    exchange: Type[Exchange]
    timeframes: list[Type[Timeframe]]
    temporary_gaps_finding_db_sessions: list[AsyncSession]
    temporary_ohlcv_fetching_db_sessions: list[AsyncSession]

    def __init__(self, client_generator: Callable):
        logging.info('[Bybit Harvester] Initializing ')

        self.exchange_connector_generator = client_generator

    async def configure(self):
        self.exchange = await self.create_exchange_entry()
        self.timeframes = await self.create_supported_timeframes()
        self.watcher = BybitHarvesterWatcher(client_generator=self.exchange_connector_generator, exchange=self.exchange)
        self.watcher.update_timeframes(self.get_ohlcv_supported_timeframes())
        self.symbol_start_dates = {}

    def get_ohlcv_supported_timeframes(self) -> list[Type[Timeframe]]:
        return list(filter(lambda timeframe: timeframe.name in ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w'],
                           self.timeframes))

    def get_open_interest_supported_timeframes(self) -> list[Type[Timeframe]]:
        return list(filter(lambda timeframe: timeframe.name in ['5m', '15m', '30m', '1h' '4h', '1d'], self.timeframes))

    @staticmethod
    async def create_supported_timeframes() -> list[Type[Timeframe]]:
        async with get_session() as db_session:
            supported_timeframes = [
                {'name': '1m', 'seconds': 60},
                {'name': '5m', 'seconds': 60 * 5},
                {'name': '15m', 'seconds': 60 * 15},
                {'name': '30m', 'seconds': 60 * 30},
                {'name': '1h', 'seconds': 60 * 60},
                {'name': '4h', 'seconds': 60 * 60 * 4},
                {'name': '1d', 'seconds': 60 * 60 * 24},
                {'name': '1w', 'seconds': 60 * 60 * 24 * 7},
            ]

            new_timeframes = []
            for timeframe in supported_timeframes:
                existing_timeframe = (
                    await db_session.execute(select(Timeframe).filter_by(name=timeframe['name']))).scalar()
                if existing_timeframe is None:
                    new_timeframes.append(Timeframe(name=timeframe['name'], seconds=timeframe['seconds']))
            if len(new_timeframes) > 0:
                await db_session.add_all(new_timeframes)
                await db_session.commit()
            logging.info(
                f'[Bybit Harvester] Updated list of supported timeframes ({len(new_timeframes)} new timeframes added)')

            return list((await db_session.execute(select(Timeframe))).scalars())

    @staticmethod
    async def create_exchange_entry() -> Type[Exchange]:
        async with get_session() as db_session:
            existing_entry = (await db_session.execute(select(Exchange).filter_by(name=EXCHANGE_NAME))).scalar()

            if existing_entry is not None:
                return existing_entry
            else:
                new_entry = Exchange(name=EXCHANGE_NAME)
                await db_session.add(new_entry)
                await db_session.commit()
                return (await db_session.execute(select(Exchange).filter_by(name=EXCHANGE_NAME))).scalar()

    async def update_list_of_symbols(self) -> list[Type[Symbol]]:
        exchange_connector = self.exchange_connector_generator()
        logging.info(f'[Bybit Harvester] Starting updating list of symbols')
        async with get_session() as db_session:
            while True:  # should finish after first round because of return at the end
                try:
                    existing_symbols = list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                    fetched_symbols = await exchange_connector.fetch_tickers(self.exchange)
                    fetched_symbols_names = list(map(lambda x: x.name, fetched_symbols))
                    existing_symbols_names = list(map(lambda x: x.name, existing_symbols))

                    for symbol in existing_symbols:
                        if symbol.name not in fetched_symbols_names:
                            await db_session.delete(symbol)

                    new_symbols_to_add = []
                    for symbol in fetched_symbols:
                        if symbol.name not in existing_symbols_names:
                            new_symbols_to_add.append(symbol)
                    db_session.add_all(new_symbols_to_add)
                    await db_session.commit()

                    new_symbols_count = len(new_symbols_to_add)

                    self.symbol_start_dates = await exchange_connector.fetch_start_dates()
                    logging.info(f'[Bybit Harvester] Updated list of symbols ({new_symbols_count} new added)')
                    await exchange_connector.close()
                    return list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                except Exception as e:
                    logging.error(f'[Bybit Harvester] Fetch list of symbols error {e}')
                    await asyncio.sleep(1)

    async def fetch_all_ohlcv(self, data_to_fetch: list[DataToFetch]) -> object:
        self.temporary_ohlcv_fetching_db_sessions = [async_session_generator()() for i in
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
            self.temporary_ohlcv_fetching_db_sessions = []
            logging.info(
                f'[Bybit Harvester] Finished updating history for all symbols in all timeframes. '
                f'Added {new_candles_for_all_symbols_count} new entries '
                f'Took {"{:.2f}".format(elapsed())} seconds')
            return new_candles_for_all_symbols_count

    async def fetch_and_save_single_ohlcv(self, data: DataToFetch, current_fetch: int, all_fetches: int):
        db_session = self.temporary_ohlcv_fetching_db_sessions.pop()
        new_candles: list[OHLCV] = await self.fetch_single_ohlcv(data=data, current_fetch=current_fetch,
                                                                 all_fetches=all_fetches)

        if len(new_candles) > 0:
            expected_candles_count = floor((data.end - data.start).total_seconds() / data.timeframe.seconds)
            if expected_candles_count != len(new_candles):
                new_candles += self.generate_missing_candles_in_front(candles=new_candles, start_time=data.start,
                                                                      timeframe=data.timeframe)
            success = False
            while not success:
                try:
                    def conflict_passer(statement: Insert):
                        return statement.on_conflict_do_nothing()

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
                    success = True
                except Exception as e:
                    logging.error(f'fetch_and_save_single_ohlcv error {data.symbol.name} {data.timeframe.name} {e}')
                    await asyncio.sleep(1)
        self.temporary_ohlcv_fetching_db_sessions.append(db_session)
        return len(new_candles)

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

    async def fetch_single_ohlcv(self, data: DataToFetch, current_fetch: int, all_fetches: int):
        with elapsed_timer() as elapsed:
            success = False
            new_candles = []
            exchange_connector = self.exchange_connector_generator()
            while not success:
                try:
                    new_candles = await exchange_connector.fetch_ohlcv(data=data, exchange=self.exchange)
                    logging.info(
                        f'Fetched {len(new_candles)} new entries for\t{data}\t({current_fetch} / {all_fetches}).\t'
                        f'Took {"{:.2f}".format(elapsed())} seconds')
                    success = True
                except Exception as e:
                    logging.error(f'Update Single fetch_single_ohlcv {data.symbol.name} {data.timeframe.name} {e}')
                    await asyncio.sleep(1)
            await exchange_connector.close()
            return new_candles

    def get_earliest_possible_date_for_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe]) -> datetime:
        return max(self.symbol_start_dates[symbol.name],
                   max(datetime.fromtimestamp(0),
                       datetime.now() - timedelta(seconds=timeframe.seconds * MAX_CANDLES_HISTORY_TO_FETCH)))

    async def find_all_gaps(self, current_symbols) -> list[DataToFetch]:
        logging.info(f'[Bybit Harvester] Starting to look for gaps in OHLCV data')
        exchange_connector = self.exchange_connector_generator()
        with elapsed_timer() as elapsed:
            all_gaps = []
            end_time = await exchange_connector.get_server_time()
            find_gap_coroutines = []
            self.temporary_gaps_finding_db_sessions = [async_session_generator()() for i in
                                                       range(0, MAX_CONCURRENT_GAPS_CALCULATIONS)]

            for timeframe in self.get_ohlcv_supported_timeframes():
                for symbol in current_symbols:
                    find_gap_coroutines.append(self.gap_finder(symbol=symbol, timeframe=timeframe, end_time=end_time))

            for gap in await semaphore_gather(MAX_CONCURRENT_GAPS_CALCULATIONS, find_gap_coroutines):
                all_gaps += gap
            logging.info(f'[Bybit Harvester] Found {len(all_gaps)} gaps. Took {"{:.2f}".format(elapsed())} seconds')
            for session in self.temporary_gaps_finding_db_sessions:
                await session.close()
            self.temporary_gaps_finding_db_sessions = []
            await exchange_connector.close()
            return all_gaps

    async def gap_finder(self, symbol: Type[Symbol], timeframe: Type[Timeframe], end_time: datetime):
        start_time = self.get_earliest_possible_date_for_ohlcv(symbol, timeframe)

        gaps_to_merge = await self.find_gaps(symbol, timeframe, start_time, end_time)
        gaps_to_merge.sort(key=sort_data_to_fetch_by_start_key)

        merged_gaps: list[DataToFetch] = []
        while len(gaps_to_merge) > 0:
            current_gap = gaps_to_merge.pop(0)
            while len(gaps_to_merge) > 0:
                if (gaps_to_merge[
                        0].start - current_gap.end).total_seconds() - 5 * timeframe.seconds and \
                        gaps_to_merge[0].end >= current_gap.end:
                    current_gap.end = gaps_to_merge.pop(0).end
                else:
                    break
            if current_gap.length().total_seconds() > current_gap.timeframe.seconds:
                merged_gaps.append(current_gap)

        if len(merged_gaps) > 0:
            merged_gaps[len(merged_gaps) - 1].is_last_to_fetch = True
        return merged_gaps

    async def find_gaps(self, symbol, timeframe, start_time, end_time):
        db_session = self.temporary_gaps_finding_db_sessions.pop()
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
                     f'		raw.differ != {timeframe.seconds}*\'1 sec\'::interval')
        results = (await db_session.execute(query)).all()
        gaps = list(map(lambda x: DataToFetch(symbol=symbol, timeframe=timeframe, start=x[0] - x[1], end=x[0],
                                              is_last_to_fetch=False), results))

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
            gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=start_time, end=first_timestamp,
                                    is_last_to_fetch=False))

        if last_timestamp is not None and (end_time - last_timestamp).total_seconds() > timeframe.seconds:
            gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=last_timestamp, end=end_time,
                                    is_last_to_fetch=False))
        self.temporary_gaps_finding_db_sessions.append(db_session)
        return gaps

    async def start_watching(self):
        return await asyncio.gather(*[self.watcher.watch_candles(), self.watcher.watch_tickers()])

    async def fetch_candles(self):

        while True:
            current_symbols = await self.update_list_of_symbols()

            self.watcher.update_symbols(current_symbols)
            self.watcher.refresh()

            ohlcv_data_to_fetch = await self.find_all_gaps(current_symbols)  # move below
            await self.fetch_all_ohlcv(ohlcv_data_to_fetch)
            await asyncio.sleep(3600)

    async def start_loop(self):
        await asyncio.gather(*[self.start_watching(), self.fetch_candles()])
