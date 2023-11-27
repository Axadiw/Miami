import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import ceil
from typing import Type

from sqlalchemy import create_engine, Row
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import sessionmaker, load_only

from consts_secrets import db_username, db_password, db_name
from data_harvesters.bybit_harvester.bybit_harverser_watcher import BybitHarvesterWatcher
from data_harvesters.data_to_fetch import DataToFetch
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe

EXCHANGE_NAME = 'bybit'
MAX_CANDLES_HISTORY_TO_FETCH = 100000
MAX_CONCURRENT_FETCHES = 3


def sort_data_to_fetch_by_start_key(e):
    return e.start


async def semaphore_gather(num, coros, return_exceptions=False):
    semaphore = asyncio.Semaphore(num)

    async def _wrap_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(_wrap_coro(coro) for coro in coros), return_exceptions=return_exceptions)


class BybitHarvester:

    @staticmethod
    def get_session():
        return sessionmaker(create_engine(url=f'postgresql://{db_username}:{db_password}@db/{db_name}'))()

    def __init__(self, client: BaseExchangeConnector):
        logging.info('[Bybit Harvester] Initializing ')

        self.exchange_connector = client
        self.db_session = self.get_session()
        self.exchange = self.create_exchange_entry()
        self.timeframes = self.create_supported_timeframes()
        self.watcher = BybitHarvesterWatcher(client=client, exchange=self.exchange)
        self.watcher.update_timeframes(self.get_ohlcv_supported_timeframes())
        self.symbol_start_dates = {}

    def get_ohlcv_supported_timeframes(self) -> list[Type[Timeframe]]:
        return list(
            filter(lambda timeframe: timeframe.name in ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w'],
                   self.timeframes))

    def get_open_interest_supported_timeframes(self) -> list[Type[Timeframe]]:
        return list(filter(lambda timeframe: timeframe.name in ['5m', '15m', '30m', '1h' '4h', '1d'], self.timeframes))

    def create_supported_timeframes(self) -> list[Type[Timeframe]]:
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
            existing_timeframe = self.db_session.query(Timeframe).filter_by(name=timeframe['name']).first()
            if existing_timeframe is None:
                new_timeframes.append(Timeframe(name=timeframe['name'], seconds=timeframe['seconds']))

        self.db_session.bulk_save_objects(new_timeframes)
        self.db_session.commit()
        logging.info(
            f'[Bybit Harvester] Updated list of supported timeframes ({len(new_timeframes)} new timeframes added)')

        return list(self.db_session.query(Timeframe).all())

    def create_exchange_entry(self) -> Type[Exchange]:
        existing_entry = self.db_session.query(Exchange).filter_by(name=EXCHANGE_NAME).first()

        if existing_entry is not None:
            return existing_entry
        else:
            new_entry = Exchange(name=EXCHANGE_NAME)
            self.db_session.add(new_entry)
            self.db_session.commit()
            return self.db_session.query(Exchange).filter_by(name=EXCHANGE_NAME).first()

    async def update_list_of_symbols(self) -> list[Type[Symbol]]:
        while True:  # should finish after first round because of return at the end
            try:
                existing_symbols = list(self.db_session.query(Symbol).filter_by(exchange=self.exchange.id).all())
                fetched_symbols = await self.exchange_connector.fetch_tickers(self.exchange)
                fetched_symbols_names = list(map(lambda x: x.name, fetched_symbols))
                existing_symbols_names = list(map(lambda x: x.name, existing_symbols))

                for symbol in existing_symbols:
                    if symbol.name not in fetched_symbols_names:
                        self.db_session.delete(symbol)

                new_symbols_to_add = []
                for symbol in fetched_symbols:
                    if symbol.name not in existing_symbols_names:
                        new_symbols_to_add.append(symbol)

                self.db_session.bulk_save_objects(new_symbols_to_add),
                self.db_session.commit()

                new_symbols_count = len(new_symbols_to_add)

                self.symbol_start_dates = await self.exchange_connector.fetch_start_dates()
                logging.info(f'[Bybit Harvester] Updated list of symbols ({new_symbols_count} new added)')

                return list(self.db_session.query(Symbol).filter_by(exchange=self.exchange.id).all())
            except PendingRollbackError as e:
                logging.error(f'[Bybit Harvester] Fetch list rollback error {e}')
                self.db_session.rollback()
                await asyncio.sleep(1)
            except Exception as e:
                logging.error(f'[Bybit Harvester] Fetch list of symbols error {e}')
                await asyncio.sleep(1)

    async def fetch_all_ohlcv(self, data_to_fetch: list[DataToFetch]) -> object:
        start_all_symbols = time.time()
        new_candles_counts = await semaphore_gather(MAX_CONCURRENT_FETCHES,
                                                    [self.fetch_and_save_single_ohlcv(data=data,
                                                                                      current_fetch=index + 1,
                                                                                      all_fetches=len(data_to_fetch))
                                                     for index, data in enumerate(data_to_fetch)])
        new_candles_for_all_symbols_count = 0
        for count in new_candles_counts:
            new_candles_for_all_symbols_count += count

        end_all_symbols = time.time()
        logging.info(
            f'[Bybit Harvester] Finished updating fetch_and_save_single_ohlcv history for all symbols in all timeframes. '
            f'Added {new_candles_for_all_symbols_count} new entries '
            f'Took {"{:.2f}".format(end_all_symbols - start_all_symbols)} seconds')
        return new_candles_for_all_symbols_count

    async def fetch_and_save_single_ohlcv(self, data: DataToFetch, current_fetch: int, all_fetches: int):
        new_candles = await self.fetch_single_ohlcv(data=data, current_fetch=current_fetch, all_fetches=all_fetches)
        if len(new_candles) > 0:
            success = False
            while not success:
                try:
                    self.db_session.execute(insert(OHLCV).values([{"exchange": candle.exchange,
                                                                   "symbol": candle.symbol,
                                                                   "timeframe": candle.timeframe,
                                                                   "timestamp": candle.timestamp,
                                                                   "open": candle.open,
                                                                   "high": candle.high,
                                                                   "low": candle.low,
                                                                   "close": candle.close,
                                                                   "volume": candle.volume} for candle in
                                                                  new_candles]).on_conflict_do_nothing())
                    self.db_session.commit()
                    success = True
                except PendingRollbackError as e:
                    logging.error(f'[Bybit Harvester] fetch_and_save_single_ohlcv rollback error {e}')
                    self.db_session.rollback()
                    await asyncio.sleep(1)
        return len(new_candles)

    async def fetch_single_ohlcv(self, data: DataToFetch, current_fetch: int, all_fetches: int):
        start_single_symbol = time.time()
        success = False
        new_candles = []
        while not success:
            try:
                new_candles = await self.exchange_connector.fetch_ohlcv(data=data, exchange=self.exchange)
                end_single_symbol = time.time()
                logging.info(
                    f'[Bybit Harvester] Finished fetching fetch_single_ohlcv history for {data} '
                    f' ({current_fetch} / {all_fetches}). Fetched {len(new_candles)} new entries '
                    f'Took {"{:.2f}".format(end_single_symbol - start_single_symbol)} seconds')
                success = True
            except Exception as e:
                logging.error(f'Update Single fetch_single_ohlcv {data.symbol.name} {data.timeframe.name} {e}')
                await asyncio.sleep(1)

        return new_candles

    def get_earliest_possible_date_for_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe]) -> datetime:
        return max(self.symbol_start_dates[symbol.name],
                   max(datetime.fromtimestamp(0),
                       datetime.now() - timedelta(seconds=timeframe.seconds * MAX_CANDLES_HISTORY_TO_FETCH)))

    async def find_all_gaps(self, current_symbols) -> list[DataToFetch]:
        all_gaps = []
        end_time = await self.exchange_connector.get_server_time()
        for timeframe in self.get_ohlcv_supported_timeframes():
            for symbol in current_symbols:
                start_time = self.get_earliest_possible_date_for_ohlcv(symbol, timeframe)

                query = self.db_session.query(OHLCV.timestamp).filter_by(exchange=self.exchange.id, symbol=symbol.id,
                                                                         timeframe=timeframe.id) \
                    .filter(OHLCV.timestamp > start_time) \
                    .filter(OHLCV.timestamp <= end_time) \
                    .order_by(OHLCV.timestamp.asc())

                timestamps = list(query.all())

                gaps_to_merge = self.find_gaps(symbol, timeframe, start_time, end_time, timestamps)
                gaps_to_merge.sort(key=sort_data_to_fetch_by_start_key)

                merged_gaps: list[DataToFetch] = []
                while len(gaps_to_merge) > 0:
                    current_gap = gaps_to_merge.pop(0)
                    while len(gaps_to_merge) > 0:
                        if (gaps_to_merge[0].start - current_gap.end).total_seconds() - 5 * timeframe.seconds and \
                                gaps_to_merge[0].end >= current_gap.end:
                            current_gap.end = gaps_to_merge.pop(0).end
                        else:
                            break
                    if current_gap.length().total_seconds() > current_gap.timeframe.seconds:
                        merged_gaps.append(current_gap)

                if len(merged_gaps) > 0:
                    merged_gaps[len(merged_gaps) - 1].is_last_to_fetch = True

                all_gaps += merged_gaps
                logging.info(
                    f'[Bybit Harvester] Found {len(merged_gaps)} gaps for {symbol.name} {timeframe.name}')
        return all_gaps

    def find_gaps(self, symbol: Type[Symbol], timeframe: Type[Timeframe], start_time: datetime, end_time: datetime,
                  timestamps: list[Row]) -> list[DataToFetch]:
        gaps = []
        for index, timestamp in enumerate(timestamps):
            if index > 0:
                previous_timestamp = timestamps[index - 1][0]
                current_timestamp = timestamp[0]
                if previous_timestamp + timedelta(seconds=timeframe.seconds) != current_timestamp:
                    gaps.append(
                        DataToFetch(symbol=symbol, timeframe=timeframe, start=previous_timestamp, end=current_timestamp,
                                    is_last_to_fetch=False))

        if len(timestamps) > 0:
            first_timestamp = timestamps[0][0]
            last_timestamp = timestamps[len(timestamps) - 1][0]
            if (first_timestamp - start_time).total_seconds() > timeframe.seconds:
                gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=start_time, end=first_timestamp,
                                        is_last_to_fetch=False))

            if (end_time - last_timestamp).total_seconds() > timeframe.seconds:
                gaps.append(DataToFetch(symbol=symbol, timeframe=timeframe, start=last_timestamp, end=end_time,
                                        is_last_to_fetch=False))

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
