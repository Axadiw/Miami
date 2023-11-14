from datetime import datetime
from typing import List, Optional

import ccxt.pro as ccxtpro
from ccxt.base.types import Trade

from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchanges import Exchanges
from models.ohlcv import OHLCV
from models.symbols import Symbols
from models.timeframes import Timeframes


class BybitConnectorCCXT(BaseExchangeConnector):

    def __init__(self):
        self.connector = ccxtpro.bybit()

    async def fetch_tickers(self) -> List[Symbols]:
        response = await self.connector.fetch_tickers()
        return list(map(lambda x: Symbols(name=x[1]['symbol']), response.items()))

    async def fetch_ohlcv(self, symbol: Symbols, timeframe: Timeframes, exchange: Exchanges, since: int) -> List[OHLCV]:
        response = await self.connector.fetch_ohlcv(symbol.name, timeframe.name, since * 1000, limit=20000,
                                                    params={"paginate": True, "paginationCalls": 20})
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
        new_items.pop()  # Remove last, not finished candle
        return new_items

    def watch_ohlcv(self, symbolsAndTimeframes: List[List[str]], since: Optional[int] = None,
                    limit: Optional[int] = None, params={}):
        return self.connector.watch_ohlcv_for_symbols(symbolsAndTimeframes, since, limit, params)

    def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None, params={}):
        return self.connector.watch_trades_for_symbols(symbols, since, limit, params)

    def build(self, trades: List[Trade], timeframe: str = '1m', since: float = 0, limit: float = 2147483647):
        return self.connector.build_ohlcvc(trades, timeframe, since, limit)
