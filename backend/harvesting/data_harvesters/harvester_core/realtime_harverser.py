import asyncio
import decimal
import logging
from datetime import datetime, timedelta
from queue import Queue
from typing import Type, Callable, List
from ccxt.base.types import Trade
from gmqtt import Client as MQTTClient
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

import ccxt
from harvesting.data_harvesters.consts import GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND, \
    MAX_CONCURRENT_FETCHES
from harvesting.data_harvesters.data_to_fetch import DataToFetch
from harvesting.data_harvesters.database import get_session
from harvesting.data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from harvesting.data_harvesters.harvester_core.common_harvester import fetch_list_of_symbols, fetch_exchange_entry, \
    get_subset_of_timeframes
from harvesting.data_harvesters.helpers.semaphore_gather import semaphore_gather
from shared.models.exchange import Exchange
from shared.models.funding import Funding
from shared.models.ohlcv import OHLCV
from shared.models.open_interests import OpenInterest
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe


class RealtimeHarvester:
    exchange: Type[Exchange]
    temporary_ohlcv_fetching_exchange_connectors: list[BaseExchangeConnector]

    def __init__(self, exchange_name: str, client_generator: Callable, queue: Queue,
                 ohlcv_timeframe_names: list[str]):
        logging.info('[Realtime Harvester Watcher] Initializing ')
        self.queue = queue
        self.exchange_connector_generator = client_generator
        self.is_initialized = False
        self.exchange_name = exchange_name
        self.symbols: list[Type[Symbol]] = []
        self.symbols_dict: dict[str:Type[Symbol]] = {}
        self.timeframes: list[Type[Timeframe]] = []
        self.supported_ohlcv_timeframes_names = ohlcv_timeframe_names
        self.added_tickers_count = 0
        self.tickers_counter_timer = datetime.now()
        self.added_candles_count = 0
        self.mqtt_client = MQTTClient(f'{exchange_name}-realtime-harvester')
        self.candles_counter_timer = datetime.now()
        self.latest_candles = {}
        self.last_candles_mqtt_emit_dates: dict[str:datetime] = {}

    async def fetch_latest_candles(self):
        logging.info(f'[Realtime Harvester Watcher] Will start fetching initial candles')
        self.temporary_ohlcv_fetching_exchange_connectors = [self.exchange_connector_generator() for _ in
                                                             range(0, MAX_CONCURRENT_FETCHES)]
        tmp_connector = self.exchange_connector_generator()
        current_time: datetime = await tmp_connector.get_server_time()
        await tmp_connector.close()

        data_to_fetch = []
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                data_to_fetch.append(
                    DataToFetch(symbol=symbol, timeframe=timeframe,
                                start=current_time - timedelta(seconds=timeframe.seconds + 1), end=current_time))

        await semaphore_gather(MAX_CONCURRENT_FETCHES, [self.fetch_and_save_single_ohlcv(data=data) for index, data in
                                                        enumerate(data_to_fetch)])

        for connector in self.temporary_ohlcv_fetching_exchange_connectors:
            await connector.close()

        self.temporary_ohlcv_fetching_exchange_connectors = []
        logging.info(f'[Realtime Harvester Watcher] Finished fetching initial candles')

    async def fetch_and_save_single_ohlcv(self, data: DataToFetch):
        new_candles: list[OHLCV] = await self.fetch_single_ohlcv(data=data)
        if len(new_candles) > 0:
            last_candle = new_candles[-1]
            self.latest_candles[f'{data.symbol.name}_{data.timeframe.name}'] = [datetime.timestamp(last_candle[0]),
                                                                                last_candle[4], last_candle[5],
                                                                                last_candle[6], last_candle[7],
                                                                                last_candle[8]]

    async def fetch_single_ohlcv(self, data: DataToFetch):
        success = False
        new_candles = []
        exchange_connector = self.temporary_ohlcv_fetching_exchange_connectors.pop()
        while not success:
            try:
                new_candles = await exchange_connector.fetch_ohlcv(data=data, exchange=self.exchange,
                                                                   trim_to_range=False)
                success = True
            except Exception as e:
                logging.error(f'Fetch initial single realtime ohlcv {data.symbol.name} {data.timeframe.name} {e}')
                await asyncio.sleep(1)
        self.temporary_ohlcv_fetching_exchange_connectors.append(exchange_connector)
        return new_candles

    async def watch_trades(self):
        while not self.is_initialized:
            await asyncio.sleep(1)

        exchange_connector = self.exchange_connector_generator()
        async with get_session(app_name='watch_trades') as db_session:
            while True:
                try:
                    subscriptions: list[str] = []
                    for symbol in self.symbols:
                        subscriptions.append(symbol.name)

                    if len(subscriptions) > 0:
                        trades: List[Trade] = await exchange_connector.watch_trades(subscriptions)
                        await asyncio.create_task(
                            self.handle_trades(exchange_connector=exchange_connector, trades=trades,
                                               db_session=db_session))
                    else:
                        await asyncio.sleep(1)
                except ccxt.BadSymbol as e:
                    logging.critical(f'Bad symbol {e}')
                    await exchange_connector.load_markets()
                except Exception as e:
                    logging.critical(f'[Realtime Harvester Watcher] Error watch_candles {e}')
                    await asyncio.sleep(1)

    async def handle_trades(self, exchange_connector: BaseExchangeConnector, trades: List[Trade],
                            db_session: AsyncSession):
        if len(trades) == 0:
            return
        symbol_name = trades[0]['symbol']
        symbol_id = self.symbols_dict[symbol_name].id
        candles_to_save = []

        for timeframe in self.timeframes:
            pair_identifier = f'{symbol_name}_{timeframe.name}'
            if pair_identifier in self.latest_candles:
                new_candles = exchange_connector.build_ohlcv(last_ohlcv=self.latest_candles[pair_identifier],
                                                             trades=trades,
                                                             timeframe=timeframe)

                if len(new_candles) > 0:
                    converted_candle = self.convert_candle(new_candles[-1], symbol_id, timeframe.id)
                    pair_identifier = f'{symbol_name}_{timeframe.name}'
                    if pair_identifier not in self.last_candles_mqtt_emit_dates or datetime.now() - \
                            self.last_candles_mqtt_emit_dates[pair_identifier] > timedelta(seconds=1):
                        to_emit = {**converted_candle,
                                   'timestamp': datetime.timestamp(converted_candle['timestamp']),
                                   'exchange': self.exchange.name,
                                   'symbol': symbol_name,
                                   'timeframe': timeframe.name}
                        self.mqtt_client.publish('ohlcv', to_emit)
                        # logging.info(f'Updating candle {symbol_name} {timeframe.name}')
                        self.last_candles_mqtt_emit_dates[pair_identifier] = datetime.now()

                    if len(new_candles) > 1:
                        # logging.info(f'Adding new candle {symbol_name} {timeframe.name}')
                        self.added_candles_count += 1
                        candles_to_save.append(self.convert_candle(new_candles[-2], symbol_id, timeframe.id))

                    self.latest_candles[pair_identifier] = new_candles[-1]
                else:
                    logging.critical(
                        f'[Realtime Harvester Watcher] Received trade for {symbol_name} that '
                        f'have not produced any candles')
            else:
                logging.critical(
                    f'[Realtime Harvester Watcher] Received trade for unknown symbol_name: {symbol_name}')

        if len(candles_to_save) > 0:
            await db_session.execute(insert(OHLCV).values(candles_to_save).on_conflict_do_nothing())
            await db_session.commit()

    def convert_candle(self, candle, symbol_id, timeframe_id):
        return {"exchange": self.exchange.id,
                "symbol": symbol_id,
                "timeframe": timeframe_id,
                "timestamp": datetime.fromtimestamp(candle[0]),
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]}

    async def watch_tickers(self):
        exchange_connector = self.exchange_connector_generator()
        logging.info(f'[Realtime Harvester Watcher] Will start watching for ticker')

        async with get_session(app_name='watch_tickers') as db_session:
            while True:
                try:
                    subscriptions = []
                    for symbol in self.symbols:
                        subscriptions.append(symbol.name)

                    if len(subscriptions) > 0:
                        ticker: dict = await exchange_connector.watch_tickers(subscriptions)
                        await asyncio.create_task(self.handle_tickers(ticker, db_session=db_session))
                    else:
                        await asyncio.sleep(1)  # empty subscriptions array
                except ccxt.BadSymbol as e:
                    logging.critical(f'Bad symbol {e}')
                    await exchange_connector.load_markets()
                except Exception as e:
                    logging.critical(f'[Realtime Harvester Watcher] Error watch_tickers {e}')
                    await asyncio.sleep(1)

    async def handle_tickers(self, ticker, db_session: AsyncSession):
        try:
            symbol = (await db_session.execute(select(Symbol).filter_by(name=ticker['symbol']))).scalar()
            timestamp = datetime.fromtimestamp(ticker['timestamp'] / 1000.0)
            count = (await db_session.execute(select(func.count(Funding.id)).filter_by(symbol=symbol.id).filter(
                Funding.timestamp > timestamp - timedelta(seconds=30)))).scalar()
            if count == 0:
                if 'fundingRate' in ticker['info'] and ticker['info']['fundingRate']:
                    funding = {"exchange": self.exchange.id, "symbol": symbol.id,
                               "timestamp": timestamp,
                               "value": decimal.Decimal(ticker['info']['fundingRate'])}
                    self.added_tickers_count += 1
                    await db_session.execute(insert(Funding).values(funding).on_conflict_do_nothing())
                if 'openInterest' in ticker['info'] and ticker['info']['openInterest']:
                    oi = {"exchange": self.exchange.id, "symbol": symbol.id,
                          "timestamp": timestamp,
                          "value": decimal.Decimal(ticker['info']['openInterest'])}
                    await db_session.execute(insert(OpenInterest).values(oi).on_conflict_do_nothing())
                await db_session.commit()
        except Exception as e:
            logging.critical(f'[Realtime Harvester Watcher] Error handle_tickers {e}')

    async def start_queue_loop(self):
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, self.queue.get)

            if command == GLOBAL_QUEUE_START_COMMAND:
                self.timeframes = await get_subset_of_timeframes(self.supported_ohlcv_timeframes_names)
                self.exchange = await fetch_exchange_entry(self.exchange_name)
                self.symbols = await fetch_list_of_symbols(self.exchange)
                await self.fetch_latest_candles()
                self.is_initialized = True
            elif command == GLOBAL_QUEUE_REFRESH_COMMAND:
                self.symbols = await fetch_list_of_symbols(self.exchange)

            self.symbols_dict = {symbol.name: symbol for symbol in self.symbols}

    async def start(self):
        await self.mqtt_client.connect('mqtt', 1883, keepalive=60)
        await asyncio.gather(*[self.start_queue_loop(), self.watch_trades(), self.watch_tickers()])
