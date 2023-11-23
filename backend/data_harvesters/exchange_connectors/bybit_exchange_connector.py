from datetime import datetime
from typing import List, Optional, Type

import ccxt
import ccxt.pro as ccxtpro
from ccxt.base.types import Trade

from data_harvesters.bybit_harvester.bybit_harvester import MAX_CANDLES_HISTORY_TO_FETCH
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.open_interests import OpenInterest
from models.symbol import Symbol
from models.timeframe import Timeframe


class BybitConnectorCCXT(BaseExchangeConnector):

    def __init__(self):
        self.connector_pro = ccxtpro.bybit()
        self.connector = ccxt.bybit()

    async def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        self.connector.load_markets(True)
        response = await self.connector_pro.fetch_tickers()
        return list(map(lambda x: Symbol(name=x[1]['symbol'], exchange=exchange.id), response.items()))

    async def fetch_ohlcv(self, symbol: Symbol, timeframe: Timeframe, exchange: Exchange, since: int) -> List[OHLCV]:
        response = await self.connector_pro.fetch_ohlcv(symbol.name, timeframe.name, since,
                                                        limit=MAX_CANDLES_HISTORY_TO_FETCH,
                                                        params={"paginate": True,
                                                                "paginationCalls": int(
                                                                    MAX_CANDLES_HISTORY_TO_FETCH / 1000),
                                                                'until': datetime.now().timestamp() * 1000,
                                                                'maxRetries': 10})
        new_items = list(
            map(lambda x: OHLCV(timestamp=datetime.fromtimestamp(x[0] / 1000.0),
                                exchange=exchange.id,
                                symbol=symbol.id,
                                timeframe=timeframe.id,
                                open=x[1],
                                high=x[2],
                                low=x[3],
                                close=x[4],
                                volume=x[5]), response))
        if len(new_items) > 0:
            new_items.pop()  # Remove last, not finished candle
        return new_items

    async def watch_ohlcv(self, symbolsAndTimeframes: List[List[str]], since: Optional[int] = None,
                          limit: Optional[int] = None, params={}):
        return await self.connector_pro.watch_ohlcv_for_symbols(symbolsAndTimeframes, since, limit, params)

    async def watch_tickers(self, symbols: List[str]):
        return await self.connector_pro.watch_tickers(symbols, {})

    async def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None,
                           params={}):
        return await self.connector_pro.watch_trades_for_symbols(symbols, since, limit, params)

    def build(self, trades: List[Trade], timeframe: str = '1m', since: float = 0, limit: float = 2147483647):
        return self.connector_pro.build_ohlcvc(trades, timeframe, since, limit)

    async def fetch_start_dates(self):
        return {i[0]: int(i[1]) for i in list(map(lambda x: [x['symbol'], x['info']['launchTime']],
                                                  await self.connector_pro.fetch_future_markets(
                                                      {'category': 'linear'})))}

    async def fetch_funding_history(self, symbol: str, since: int):
        resp = await self.connector_pro.fetch_funding_history()
        return await self.connector_pro.fetch_funding_rate_history(symbol=symbol, since=since, limit=200,
                                                                   params={"paginate": True,
                                                                           "paginationCalls": 100,
                                                                           'until': datetime.now().timestamp() * 1000,
                                                                           'maxRetries': 10})

    async def fetch_open_interest_history(self, symbol: Symbol, timeframe: Timeframe, since: int,
                                          exchange: Type[Exchange]) -> List[OpenInterest]:
        response = await self.connector_pro.fetch_open_interest_history(symbol=symbol.name, timeframe=timeframe.name,
                                                                        since=since,
                                                                        limit=MAX_CANDLES_HISTORY_TO_FETCH,
                                                                        params={"paginate": True,
                                                                                "paginationCalls": int(
                                                                                    MAX_CANDLES_HISTORY_TO_FETCH / 200),
                                                                                'until': datetime.now().timestamp() * 1000,
                                                                                'maxRetries': 10,
                                                                                'maxEntriesPerRequest': 200})
        new_items = list(
            map(lambda x: OpenInterest(timestamp=datetime.fromtimestamp(x['timestamp'] / 1000.0),
                                       exchange=exchange.id,
                                       symbol=symbol.id,
                                       timeframe=timeframe.id,
                                       value=x['openInterestValue']), response))
        if len(new_items) > 0:
            new_items.pop()  # Remove last, not finished candle
        return new_items
