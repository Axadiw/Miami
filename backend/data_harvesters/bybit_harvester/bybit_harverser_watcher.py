import asyncio
import logging
from datetime import datetime
from typing import Type

from sqlalchemy import create_engine
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

    def __init__(self, exchange: Type[Exchange], client: BaseExchangeConnector):
        logging.info('[Bybit Harvester Watcher] Initializing ')
        self.exchange_connector = client
        self.db_session = self.get_session()
        self.should_refresh_symbols = True
        self.exchange = exchange
        self.symbols: list[Type[Symbol]] = []
        self.timeframes: list[Type[Timeframe]] = []
        self.newest_candles: dict = {}

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

                if len(subscriptions) > 0:
                    candles: dict = await self.exchange_connector.watch_ohlcv(subscriptions)
                    ohlcv_candles_to_save = self.parse_candles(candles)
                    if len(ohlcv_candles_to_save) > 0:
                        self.db_session.execute(insert(OHLCV).values(ohlcv_candles_to_save).on_conflict_do_nothing())
                        self.db_session.commit()

                    if len(ohlcv_candles_to_save):
                        logging.debug(f'[Bybit Harvester Watcher] Added {len(ohlcv_candles_to_save)} candles')

                else:
                    await asyncio.sleep(1)  # empty subscriptions array
            except Exception as e:
                logging.critical(f'[Bybit Harvester Watcher] Error {e}')

    def parse_candles(self, candles):
        ohlcv_candles_to_save = []
        for received_symbol in candles.items():
            for received_timeframes_and_data in received_symbol[1].items():
                candle_symbol = received_symbol[0]
                candle_timeframe = received_timeframes_and_data[0]
                candle_data = received_timeframes_and_data[1]

                if candle_symbol not in self.newest_candles:
                    self.newest_candles[candle_symbol] = {}

                if candle_timeframe not in self.newest_candles[candle_symbol]:
                    self.newest_candles[candle_symbol][candle_timeframe] = candle_data  # save first candle

                if self.newest_candles[candle_symbol][candle_timeframe] is not None:  # should be always True
                    if len(candle_data) > 0 and len(self.newest_candles[candle_symbol][candle_timeframe]) > 0:
                        new_candle = candle_data[0]
                        old_candle = self.newest_candles[candle_symbol][candle_timeframe][0]
                        if new_candle > old_candle:
                            ohlcv_candles_to_save.append(
                                self.convert_candle_data_to_ohlcv_object(candle_symbol, candle_timeframe,
                                                                         old_candle))
                self.newest_candles[candle_symbol][candle_timeframe] = candle_data  # save new candle as current
        return ohlcv_candles_to_save

    def convert_candle_data_to_ohlcv_object(self, symbol_name: str, timeframe_name: str, candle_data: list):
        symbol = self.db_session.query(Symbol).filter_by(name=symbol_name).first()
        timeframe = self.db_session.query(Timeframe).filter_by(name=timeframe_name).first()

        if symbol is None or timeframe is None or len(candle_data) < 5:
            raise Exception('Not enough data to generate OHLCV candle')

        return {"exchange": self.exchange.id,
                "symbol": symbol.id,
                "timeframe": timeframe.id,
                "timestamp": datetime.fromtimestamp(candle_data[0] / 1000.0),
                "open": candle_data[1],
                "high": candle_data[2],
                "low": candle_data[3],
                "close": candle_data[4],
                "volume": candle_data[5]}
