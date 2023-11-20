import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from multiprocessing import Process
from time import sleep
from typing import Type

from sqlalchemy import desc, create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from consts_secrets import db_username, db_password, db_name
from data_harvesters.bybit_harvester.bybit_harverser_watcher import BybitHarvesterWatcher
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe

EXCHANGE_NAME = 'bybit'
MAX_CANDLES_HISTORY_TO_FETCH = 100000
MAX_CONCURRENT_FETCHES = 15


@dataclass
class DataToFetch:
    symbol: Type[Symbol]
    timeframe: Type[Timeframe]
    since: float


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
        self.watcher.update_timeframes(self.timeframes)
        self.symbol_start_dates = {}

    def create_supported_timeframes(self) -> list[Type[Timeframe]]:
        supported_timeframes = [
            {'name': '1m', 'seconds': 60},
            {'name': '5m', 'seconds': 60 * 5},
            {'name': '15m', 'seconds': 60 * 15},
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
            except Exception as e:
                logging.error(f'[Bybit Harvester] Fetch list of symbols error {e}')
                sleep(1)

    async def fetch_all_ohlcv(self, data_to_fetch: list[DataToFetch]):
        start_all_symbols = time.time()
        new_candles_counts = await semaphore_gather(MAX_CONCURRENT_FETCHES,
                                                    [self.fetch_and_save_single_ohlcv(symbol=data.symbol,
                                                                                      timeframe=data.timeframe,
                                                                                      since=data.since,
                                                                                      current_fetch=index + 1,
                                                                                      all_fetches=len(
                                                                                          data_to_fetch))
                                                     for index, data in enumerate(data_to_fetch)])
        new_candles_for_all_symbols_count = 0
        for count in new_candles_counts:
            new_candles_for_all_symbols_count += count

        end_all_symbols = time.time()
        logging.info(
            f'[Bybit Harvester] Finished updating OHLCV history for all symbols in all timeframes. '
            f'Added {new_candles_for_all_symbols_count} new entries '
            f'Took {"{:.2f}".format(end_all_symbols - start_all_symbols)} seconds')
        return new_candles_for_all_symbols_count

    async def fetch_and_save_single_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe], since: int,
                                          current_fetch: int,
                                          all_fetches: int):
        new_candles = await self.fetch_single_ohlcv(symbol=symbol, timeframe=timeframe, since=since,
                                                    current_fetch=current_fetch,
                                                    all_fetches=all_fetches)
        if len(new_candles) > 0:
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
        return len(new_candles)

    async def fetch_single_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe], since: int,
                                 current_fetch: int,
                                 all_fetches: int):
        start_single_symbol = time.time()
        success = False
        new_candles = []
        while not success:
            try:
                new_candles = await self.exchange_connector.fetch_ohlcv(symbol=symbol,
                                                                        timeframe=timeframe,
                                                                        since=since + 1,
                                                                        exchange=self.exchange)
                end_single_symbol = time.time()
                logging.info(
                    f'[Bybit Harvester] Finished updating OHLCV history for {symbol.name} in {timeframe.name} timeframe'
                    f' ({current_fetch} / {all_fetches}). '
                    f'Added {len(new_candles)} new entries '
                    f'Took {"{:.2f}".format(end_single_symbol - start_single_symbol)} seconds')
                success = True
            except Exception as e:
                logging.error(f'Update Single OHLCV {e}')
                sleep(1)

        return new_candles

    def get_newest_ohlcv_timestamp(self, symbols: list[Type[Symbol]], timeframes: list[Type[Timeframe]]) \
            -> list[DataToFetch]:
        symbols_timeframes_and_timestamps = []
        for symbol in symbols:
            for timeframe in timeframes:
                last_item = self.db_session.query(OHLCV).filter_by(exchange=self.exchange.id, symbol=symbol.id,
                                                                   timeframe=timeframe.id).order_by(
                    desc(OHLCV.timestamp)).limit(1).first()

                last_item_timestamp = max(
                    self.symbol_start_dates[symbol.name], max(0, 1000 * (datetime.now().timestamp() -
                                                                         timeframe.seconds * MAX_CANDLES_HISTORY_TO_FETCH))) \
                    if last_item is None else last_item.timestamp.timestamp()

                symbols_timeframes_and_timestamps.append(DataToFetch(symbol, timeframe, last_item_timestamp))

        logging.info(f'[Bybit Harvester] Finished calculating timestamps for further database refresh')
        return symbols_timeframes_and_timestamps

    async def start_watching(self):
        return await self.watcher.watch_candles()

    async def fetch_candles(self):
        while True:
            current_symbols = await self.update_list_of_symbols()
            data_to_fetch = self.get_newest_ohlcv_timestamp(current_symbols, self.timeframes)
            self.watcher.update_symbols(current_symbols)
            self.watcher.refresh()

            await self.fetch_all_ohlcv(data_to_fetch)
            await asyncio.sleep(3600)

    async def start_loop(self):
        await asyncio.gather(*[self.start_watching(), self.fetch_candles()])
