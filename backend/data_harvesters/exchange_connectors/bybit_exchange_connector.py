from datetime import datetime
from typing import List, Optional, Type

import ccxt
import ccxt.pro as ccxtpro
from ccxt.base.types import Trade

from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe


class BybitConnectorCCXT(BaseExchangeConnector):

    def __init__(self):
        self.connector_pro = ccxtpro.bybit()
        self.connector = ccxt.bybit()

    def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        self.connector.load_markets(True)
        response = self.connector.fetch_tickers()
        return list(map(lambda x: Symbol(name=x[1]['symbol'], exchange=exchange.id), response.items()))

    def fetch_ohlcv(self, symbol: Symbol, timeframe: Timeframe, exchange: Exchange, since: int) -> List[OHLCV]:
        response = self.connector.fetch_ohlcv(symbol.name, timeframe.name, since * 1000, limit=20000,
                                              params={"paginate": True, "paginationCalls": 50,
                                                      'until': datetime.now().timestamp() * 1000})
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

    def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None, params={}):
        return self.connector_pro.watch_trades_for_symbols(symbols, since, limit, params)

    def build(self, trades: List[Trade], timeframe: str = '1m', since: float = 0, limit: float = 2147483647):
        return self.connector_pro.build_ohlcvc(trades, timeframe, since, limit)
