import asyncio
import concurrent
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import wraps
from time import sleep
from typing import Type

from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker

from consts_secrets import db_username, db_password, db_name
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchanges import Exchanges
from models.ohlcv import OHLCV
from models.symbols import Symbols
from models.timeframes import Timeframes

EXCHANGE_NAME = 'bybit'
MAX_TIME_BETWEEN_SYMBOLS_FETCH = 3600
MAX_TIME_BETWEEN_ALL_OHLCV_FETCH = 60


async def semaphore_gather(num, coros, return_exceptions=False):
    semaphore = asyncio.Semaphore(num)

    async def _wrap_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(
        *(_wrap_coro(coro) for coro in coros), return_exceptions=return_exceptions
    )


class BybitHarvester:

    @staticmethod
    def get_session():
        return sessionmaker(create_engine(url=f'postgresql://{db_username}:{db_password}@db/{db_name}'))()

    def __init__(self, client: BaseExchangeConnector):
        logging.info('[Bybit Harvester] Initializing ')
        self.exchange_connector = client
        self.db_session = self.get_session()
        self.time_of_last_symbols_update = datetime.fromtimestamp(0)
        self.time_of_last_all_ohlcv_update = datetime.fromtimestamp(0)
        self.exchange = self.create_exchange_entry()
        self.create_supported_timeframes()

    def create_supported_timeframes(self):
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
            existing_timeframe = self.db_session.query(Timeframes).filter_by(name=timeframe['name']).first()
            if existing_timeframe is None:
                new_timeframes.append(Timeframes(name=timeframe['name'], seconds=timeframe['seconds']))

        self.db_session.bulk_save_objects(new_timeframes)
        self.db_session.commit()
        logging.info(
            f'[Bybit Harvester] Updated list of supported timeframes ({len(new_timeframes)} new timeframes added)')

    def create_exchange_entry(self):
        existing_entry = self.db_session.query(Exchanges).filter_by(name=EXCHANGE_NAME).first()

        if existing_entry is not None:
            return existing_entry
        else:
            new_entry = Exchanges(name=EXCHANGE_NAME)
            self.db_session.add(new_entry)
            self.db_session.commit()
            return self.db_session.query(Exchanges).filter_by(name=EXCHANGE_NAME).first()

    async def update_list_of_symbols(self):
        if (datetime.now() - self.time_of_last_symbols_update).total_seconds() < MAX_TIME_BETWEEN_SYMBOLS_FETCH:
            return 0

        existing_symbols = list(map(lambda x: x.name, self.db_session.query(Symbols).all()))

        fetched_symbols = await self.exchange_connector.fetch_tickers()
        new_symbols_to_add = []
        for symbol in fetched_symbols:
            if symbol.name not in existing_symbols:
                new_symbols_to_add.append(symbol)

        self.db_session.bulk_save_objects(new_symbols_to_add)
        self.db_session.commit()

        self.time_of_last_symbols_update = datetime.now()
        new_symbols_count = len(new_symbols_to_add)
        logging.info(f'[Bybit Harvester] Updated list of symbols ({new_symbols_count} new added)')
        return new_symbols_count

    async def update_all_ohlcv(self):
        if (datetime.now() - self.time_of_last_all_ohlcv_update).total_seconds() < MAX_TIME_BETWEEN_ALL_OHLCV_FETCH:
            return 0

        start_all_symbols = time.time()
        existing_symbols = self.db_session.query(Symbols).all()
        existing_timeframes = self.db_session.query(Timeframes).all()
        i = 1

        new_candles_for_all_symbols_count = 0
        for symbol_index, symbol in enumerate(existing_symbols):
            for timeframe_index, timeframe in enumerate(existing_timeframes):
                new_candles = await self.update_single_ohlcv(symbol=symbol, timeframe=timeframe, current_fetch=i,
                                                             all_fetches=len(existing_symbols) * len(
                                                                 existing_timeframes))
                self.db_session.bulk_save_objects(new_candles)
                self.db_session.commit()
                new_candles_for_all_symbols_count += len(new_candles)
                i += 1

        self.time_of_last_all_ohlcv_update = datetime.now()
        end_all_symbols = time.time()
        logging.info(
            f'[Bybit Harvester] Finished updating OHLCV history for all {len(existing_symbols)} symbols '
            f'in {len(existing_timeframes)} timeframes. '
            f'Added {new_candles_for_all_symbols_count} new entries '
            f'Took {"{:.2f}".format(end_all_symbols - start_all_symbols)} seconds')
        return new_candles_for_all_symbols_count

    async def update_single_ohlcv(self, symbol: Type[Symbols], timeframe: Type[Timeframes], current_fetch: int,
                                  all_fetches: int):
        start_single_symbol = time.time()
        success = False
        new_candles = []
        while not success:
            try:
                since = int(
                    datetime.timestamp(self.get_newest_ohlcv_timestamp(symbol.id, timeframe_id=timeframe.id))) + 1
                new_candles = await self.exchange_connector.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since,
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

    def get_newest_ohlcv_timestamp(self, symbol_id: int, timeframe_id: int):
        last_item = self.db_session.query(OHLCV).filter_by(exchange=self.exchange.id, symbol=symbol_id,
                                                           timeframe=timeframe_id).order_by(
            desc(OHLCV.timestamp)).limit(1).first()

        if last_item is None:
            return datetime.fromtimestamp(0)
        else:
            return last_item.timestamp

    async def try_webhooks(self):
        existing_symbols = self.db_session.query(Symbols).all()
        existing_timeframes = self.db_session.query(Timeframes).all()
        subscriptions = []
        for timeframe in existing_timeframes:
            for symbol in existing_symbols:
                subscriptions.append([symbol.name, timeframe.name])
            # subscriptions.append(symbol.name)
        while True:
            try:
                # candles = await self.exchange_connector.watch_ohlcv(subscriptions)
                candles = await self.exchange_connector.watch_ohlcv(subscriptions)
                logging.debug(f'[Bybit Harvester] {candles}')
            except Exception as e:
                print(e)
                # stop the loop on exception or leave it commented to retry
                # raise e

    async def start_loop(self):
        await self.update_list_of_symbols()
        await self.update_all_ohlcv()
        # await self.try_webhooks()
