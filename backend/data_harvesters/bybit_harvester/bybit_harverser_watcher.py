import asyncio
import logging
from datetime import datetime, timedelta
from typing import Type, Callable

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from data_harvesters.database import get_session
from models.exchange import Exchange
from models.funding import Funding
from models.ohlcv import OHLCV
from models.open_interests import OpenInterest
from models.symbol import Symbol
from models.timeframe import Timeframe


class BybitHarvesterWatcher:

    def __init__(self, exchange: Type[Exchange], client_generator: Callable):
        logging.info('[Bybit Harvester Watcher] Initializing ')
        self.exchange_connector_generator = client_generator
        self.should_refresh_candle_symbols = True
        self.should_refresh_tickers_symbols = True
        self.exchange = exchange
        self.symbols: list[Type[Symbol]] = []
        self.timeframes: list[Type[Timeframe]] = []
        self.newest_candles: dict = {}

    def refresh(self):
        self.should_refresh_candle_symbols = True
        self.should_refresh_tickers_symbols = True

    def update_symbols(self, symbols: list[Type[Symbol]]):
        self.symbols = symbols

    def update_timeframes(self, timeframes: list[Type[Timeframe]]):
        self.timeframes = timeframes

    async def watch_candles(self):
        logging.info(f'[Bybit Harvester Watcher] Will start watching for candles')
        exchange_connector = self.exchange_connector_generator()
        async with get_session() as db_session:
            subscriptions = []
            while True:
                try:
                    if self.should_refresh_candle_symbols:
                        subscriptions = []
                        for timeframe in self.timeframes:
                            for symbol in self.symbols:
                                subscriptions.append([symbol.name, timeframe.name])
                        self.should_refresh_candle_symbols = False

                    if len(subscriptions) > 0:
                        candles: dict = await exchange_connector.watch_ohlcv(subscriptions)
                        ohlcv_candles_to_save = await self.handle_candles(db_session, candles)
                        if len(ohlcv_candles_to_save) > 0:
                            logging.info(f'Will save {ohlcv_candles_to_save}')
                            await db_session.execute(
                                insert(OHLCV).values(ohlcv_candles_to_save).on_conflict_do_nothing())
                            await db_session.commit()
                    else:
                        await asyncio.sleep(1)  # empty subscriptions array
                except Exception as e:
                    logging.critical(f'[Bybit Harvester Watcher] Error watch_candles {e}')

    async def handle_candles(self, db_session: AsyncSession, candles):
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
                                await self.convert_candle_data_to_ohlcv_object(db_session, candle_symbol,
                                                                               candle_timeframe,
                                                                               old_candle))
                self.newest_candles[candle_symbol][candle_timeframe] = candle_data  # save new candle as current
        return ohlcv_candles_to_save

    async def convert_candle_data_to_ohlcv_object(self, db_session: AsyncSession, symbol_name: str,
                                                  timeframe_name: str,
                                                  candle_data: list):
        while True:
            try:
                symbol = (await db_session.execute(select(Symbol).filter_by(name=symbol_name))).scalar()
                timeframe = (await db_session.execute(select(Timeframe).filter_by(name=timeframe_name))).scalar()

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
            except Exception as e:
                logging.error(f'[Bybit HarvesterWatcher] convert_candle_data_to_ohlcv_object error {e}')
                await asyncio.sleep(1)

    async def watch_tickers(self):
        exchange_connector = self.exchange_connector_generator()
        async with get_session() as db_session:
            logging.info(f'[Bybit Harvester Watcher] Will start watching for ticker')
            subscriptions = []
            while True:
                try:
                    if self.should_refresh_tickers_symbols:
                        subscriptions = []
                        for symbol in self.symbols:
                            subscriptions.append(symbol.name)
                        self.should_refresh_tickers_symbols = False

                    if len(subscriptions) > 0:
                        ticker: dict = await exchange_connector.watch_tickers(subscriptions)
                        funding_to_save, oi_to_save = await self.handle_tickers(db_session, ticker)

                        if funding_to_save and oi_to_save:
                            await db_session.execute(insert(Funding).values(funding_to_save).on_conflict_do_nothing())
                            await db_session.execute(insert(OpenInterest).values(oi_to_save).on_conflict_do_nothing())
                            await db_session.commit()
                    else:
                        await asyncio.sleep(1)  # empty subscriptions array
                except Exception as e:
                    logging.critical(f'[Bybit Harvester Watcher] Error watch_tickers {e}')

    async def handle_tickers(self, db_session: AsyncSession, ticker):
        symbol = (await db_session.execute(select(Symbol).filter_by(name=ticker['symbol']))).scalar()
        timestamp = datetime.fromtimestamp(ticker['timestamp'] / 1000.0)
        count = (await db_session.execute(select(func.count(Funding.id)).filter_by(symbol=symbol.id).filter(
            Funding.timestamp > timestamp - timedelta(seconds=30)))).scalar()
        if count == 0:
            funding = {"exchange": self.exchange.id, "symbol": symbol.id,
                       "timestamp": timestamp,
                       "value": ticker['info']['fundingRate']}
            oi = {"exchange": self.exchange.id, "symbol": symbol.id,
                  "timestamp": timestamp,
                  "value": ticker['info']['openInterest']}
            return funding, oi
        else:
            return None, None
