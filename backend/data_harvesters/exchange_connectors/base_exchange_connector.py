from abc import ABC, abstractmethod
from typing import List, Type, Optional

from ccxt.base.types import Trade

from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe


class BaseExchangeConnector(ABC):

    @abstractmethod
    async def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        pass

    @abstractmethod
    async def fetch_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe], exchange: Type[Exchange],
                          since: int) \
            -> List[OHLCV]:
        pass

    @abstractmethod
    async def watch_ohlcv(self, symbolsAndTimeframes: List[List[str]], since: Optional[int] = None,
                          limit: Optional[int] = None, params={}):
        pass

    @abstractmethod
    async def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None,
                           params={}):
        pass

    @abstractmethod
    def build(self, trades: List[Trade], timeframe: str = '1m', since: float = 0, limit: float = 2147483647):
        pass

    @abstractmethod
    async def fetch_start_dates(self):
        pass
