import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep
from typing import Type

from sqlalchemy import desc, create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from consts_secrets import db_username, db_password, db_name
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe


class BybitHarvesterWatcher:

    @staticmethod
    def get_session():
        return sessionmaker(create_engine(url=f'postgresql://{db_username}:{db_password}@db/{db_name}'))()

    def __init__(self, client: BaseExchangeConnector):
        logging.info('[Bybit Harvester Watcher] Initializing ')
        self.exchange_connector = client
        self.db_session = self.get_session()
        self.should_refresh_symbols = True
        self.symbols: list[Type[Symbol]] = []
        self.timeframes: list[Type[Timeframe]] = []

    def refresh(self):
        self.should_refresh_symbols = True

    def update_symbols(self, symbols: list[Type[Symbol]]):
        self.symbols = symbols

    def update_timeframes(self, timeframes: list[Type[Timeframe]]):
        self.timeframes = timeframes

    async def watch_candles(self):
        logging.info(f'[Bybit Harvester Watcher] Will start watching for candles')

        subscriptions = []
        while True:
            try:
                if self.should_refresh_symbols:
                    subscriptions = []
                    for timeframe in self.timeframes:
                        for symbol in self.symbols:
                            subscriptions.append([symbol.name, timeframe.name])
                    self.should_refresh_symbols = False

                candles = await self.exchange_connector.watch_ohlcv(subscriptions)
                logging.info(f'[Bybit Harvester Watcher] {candles}')
            except Exception as e:
                logging.critical(f'[Bybit Harvester Watcher] {e}')
