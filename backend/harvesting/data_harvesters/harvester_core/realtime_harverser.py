import asyncio
import decimal
import logging
from datetime import datetime, timedelta
from queue import Queue
from typing import Type, Callable

from pybit.unified_trading import WebSocket
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from harvesting.data_harvesters.consts import GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND
from harvesting.data_harvesters.database import get_session
from harvesting.data_harvesters.harvester_core.common_harvester import fetch_list_of_symbols, fetch_exchange_entry, \
    get_subset_of_timeframes
from shared.models.exchange import Exchange
from shared.models.funding import Funding
from shared.models.ohlcv import OHLCV
from shared.models.open_interests import OpenInterest
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe

ws = WebSocket(
    testnet=False,
    channel_type="linear",
)


def handle_klines(message):
    # I will be called every time there is new orderbook data!
    print(message)
    orderbook_data = message["data"]


ws.kline_stream(60, ['1000000VINUUSDT',
                     '10000LADYSUSDT',
                     '10000NFTUSDT',
                     '10000SATSUSDT',
                     '10000STARLUSDT',
                     '1000BONKUSDT',
                     '1000BTTUSDT',
                     '1000FLOKIUSDT',
                     '1000LUNCUSDT',
                     '1000PEPEUSDT'], handle_klines)


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
        self.supported_ohlcv_timeframes_names = ohlcv_timeframe_names
        self.added_tickers_count = 0
        self.tickers_counter_timer = datetime.now()
        self.added_candles_count = 0
        self.candles_counter_timer = datetime.now()

    async def watch_candles(self):
        logging.info(f'[Realtime Harvester Watcher] Will start watching for candles')
        exchange_connector = self.exchange_connector_generator()
        subscriptions = []

        async with get_session(app_name='watch_candles') as db_session:
            while True:
                try:
                    if self.should_refresh_candle_symbols:
                        subscriptions = []
                        for timeframe in self.timeframes:
                            for symbol in self.symbols:
                                subscriptions.append([symbol.name, timeframe.name])
                        self.should_refresh_candle_symbols = False

                    if (datetime.now() - self.candles_counter_timer).total_seconds() > 60:
                        logging.info(
                            f'[Realtime Harvester Watcher]: In the last minute processed {self.added_candles_count} new candles')
                        self.candles_counter_timer = datetime.now()
                        self.added_candles_count = 0

                    if len(subscriptions) > 0:
                        candles: dict = await exchange_connector.watch_ohlcv(subscriptions)
                        await asyncio.create_task(self.handle_candles(candles, db_session=db_session))
                    else:
                        await asyncio.sleep(1)  # empty subscriptions array
                except Exception as e:
                    logging.critical(f'[Realtime Harvester Watcher] Error watch_candles {e}')
                    await asyncio.sleep(1)

    async def handle_candles(self, candles, db_session: AsyncSession):
        # async with get_session(app_name='handle_candles_realtime') as db_session:
        ohlcv_candles_to_save = []
        for received_symbol in candles.items():
            for received_timeframes_and_data in received_symbol[1].items():
                candle_symbol = received_symbol[0]
                candle_timeframe = received_timeframes_and_data[0]
                candle_data = received_timeframes_and_data[1]

                for candle in candle_data:
                    if candle[6]:
                        ohlcv_candles_to_save.append(
                            await self.convert_candle_data_to_ohlcv_object(db_session, candle_symbol,
                                                                           candle_timeframe, candle))
                        # logging.warning(
                        #     f'New Realtime candle for {candle_symbol} {candle_timeframe} {datetime.fromtimestamp(candle[0] / 1000.0)}')
        if len(ohlcv_candles_to_save) > 0:
            self.added_candles_count += len(ohlcv_candles_to_save)
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
                        "timestamp": datetime.fromtimestamp(candle_data[0] / 1000.0 + timeframe.seconds),
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

        async with get_session(app_name='watch_tickers') as db_session:
            while True:
                try:
                    if self.should_refresh_tickers_symbols:
                        subscriptions = []
                        for symbol in self.symbols:
                            subscriptions.append(symbol.name)
                        self.should_refresh_tickers_symbols = False

                    if (datetime.now() - self.tickers_counter_timer).total_seconds() > 60:
                        logging.info(
                            f'[Realtime Harvester Watcher]: In the last minute processed {self.added_tickers_count} new tickers')
                        self.tickers_counter_timer = datetime.now()
                        self.added_tickers_count = 0

                    if len(subscriptions) > 0:
                        ticker: dict = await exchange_connector.watch_tickers(subscriptions)
                        await asyncio.create_task(self.handle_tickers(ticker, db_session=db_session))
                    else:
                        await asyncio.sleep(1)  # empty subscriptions array
                except Exception as e:
                    logging.critical(f'[Realtime Harvester Watcher] Error watch_tickers {e}')
                    await asyncio.sleep(1)

    async def handle_tickers(self, ticker, db_session: AsyncSession):
        # async with get_session(app_name='handle_tickers_realtime') as db_session:
        symbol = (await db_session.execute(select(Symbol).filter_by(name=ticker['symbol']))).scalar()
        timestamp = datetime.fromtimestamp(ticker['timestamp'] / 1000.0)
        count = (await db_session.execute(select(func.count(Funding.id)).filter_by(symbol=symbol.id).filter(
            Funding.timestamp > timestamp - timedelta(seconds=30)))).scalar()
        if count == 0:
            if 'fundingRate' in ticker['info']:
                funding = {"exchange": self.exchange.id, "symbol": symbol.id,
                           "timestamp": timestamp,
                           "value": decimal.Decimal(ticker['info']['fundingRate'])}
                self.added_tickers_count += 1
                await db_session.execute(insert(Funding).values(funding).on_conflict_do_nothing())
            if 'openInterest' in ticker['info']:
                oi = {"exchange": self.exchange.id, "symbol": symbol.id,
                      "timestamp": timestamp,
                      "value": decimal.Decimal(ticker['info']['openInterest'])}
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
