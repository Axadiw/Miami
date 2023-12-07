import asyncio
import logging
from datetime import datetime, timedelta
from queue import Queue
from typing import Type, Callable

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from data_harvesters.consts import GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND
from data_harvesters.database import get_session
from data_harvesters.harvester_core.common_harvester import fetch_list_of_symbols, fetch_exchange_entry, \
    get_subset_of_timeframes
from models.exchange import Exchange
from models.funding import Funding
from models.ohlcv import OHLCV
from models.open_interests import OpenInterest
from models.symbol import Symbol
from models.timeframe import Timeframe


class RealtimeHarvester:
    exchange: Type[Exchange]

    def __init__(self, exchange_name: str, client_generator: Callable, queue: Queue,
                 ohlcv_timeframe_names: list[str]):
        logging.info('[Realtime Harvester Watcher] Initializing ')
        self.queue = queue
        self.exchange_connector_generator = client_generator
        self.should_refresh_candle_symbols = True
        self.should_refresh_tickers_symbols = True
        self.exchange_name = exchange_name
        self.symbols: list[Type[Symbol]] = []
        self.timeframes: list[Type[Timeframe]] = []
        self.newest_candles: dict = {}
        self.supported_ohlcv_timeframes_names = ohlcv_timeframe_names

    async def watch_candles(self):
        logging.info(f'[Realtime Harvester Watcher] Will start watching for candles')
        exchange_connector = self.exchange_connector_generator()
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
                    await asyncio.create_task(self.handle_candles(candles))
                else:
                    await asyncio.sleep(1)  # empty subscriptions array
            except Exception as e:
                logging.critical(f'[Realtime Harvester Watcher] Error watch_candles {e}')

    async def handle_candles(self, candles):
        async with get_session() as db_session:
            ohlcv_candles_to_save = []
            for received_symbol in candles.items():
                for received_timeframes_and_data in received_symbol[1].items():
                    candle_symbol = received_symbol[0]
                    candle_timeframe = received_timeframes_and_data[0]
                    candle_data = received_timeframes_and_data[1]

                    # if candle_symbol == 'BTC/USDT:USDT':
                    #     pass
                    # if candle_symbol == '10000NFT/USDT:USDT':
                    #     pass
                    # print(f'Adding ohlcv for {candle_symbol}')
                    # ohlcv_candles_to_save.append(
                    #     await self.convert_candle_data_to_ohlcv_object(db_session, candle_symbol,
                    #                                                    candle_timeframe,
                    #                                                    candle_data[0]))
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
                                print(
                                    f'New Realtime candle for {candle_symbol} {candle_timeframe} {datetime.fromtimestamp(old_candle[0] / 1000.0)}')
                    self.newest_candles[candle_symbol][candle_timeframe] = candle_data  # save new candle as current
            if len(ohlcv_candles_to_save) > 0:
                await db_session.execute(
                    insert(OHLCV).values(ohlcv_candles_to_save).on_conflict_do_nothing())
                await db_session.commit()

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
                await db_session.rollback()
                logging.error(f'[Realtime HarvesterWatcher] convert_candle_data_to_ohlcv_object error {e}')
                await asyncio.sleep(1)

    async def watch_tickers(self):
        exchange_connector = self.exchange_connector_generator()
        logging.info(f'[Realtime Harvester Watcher] Will start watching for ticker')
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
                    await asyncio.create_task(self.handle_tickers(ticker))
                else:
                    await asyncio.sleep(1)  # empty subscriptions array
            except Exception as e:
                logging.critical(f'[Realtime Harvester Watcher] Error watch_tickers {e}')

    async def handle_tickers(self, ticker):
        async with get_session() as db_session:
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
                await db_session.execute(insert(Funding).values(funding).on_conflict_do_nothing())
                await db_session.execute(insert(OpenInterest).values(oi).on_conflict_do_nothing())
                await db_session.commit()

    async def start_queue_loop(self):
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, self.queue.get)

            if command == GLOBAL_QUEUE_START_COMMAND:
                self.timeframes = await get_subset_of_timeframes(self.supported_ohlcv_timeframes_names)
                self.exchange = await fetch_exchange_entry(self.exchange_name)
            elif command == GLOBAL_QUEUE_REFRESH_COMMAND:
                self.symbols = await fetch_list_of_symbols(self.exchange)
                self.should_refresh_candle_symbols = True
                self.should_refresh_tickers_symbols = True

    async def start(self):
        await asyncio.gather(*[self.start_queue_loop(), self.watch_candles(), self.watch_tickers()])
