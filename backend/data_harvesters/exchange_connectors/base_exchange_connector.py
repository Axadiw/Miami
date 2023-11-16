from abc import ABC, abstractmethod
from typing import List, Type, Optional

from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol
from models.timeframe import Timeframe


class BaseExchangeConnector(ABC):

    @abstractmethod
    def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        pass

    @abstractmethod
    def fetch_ohlcv(self, symbol: Type[Symbol], timeframe: Type[Timeframe], exchange: Type[Exchange],
                    since: int) \
            -> List[OHLCV]:
        pass

    @abstractmethod
    async def watch_ohlcv(self, symbolsAndTimeframes: List[List[str]], since: Optional[int] = None,
                          limit: Optional[int] = None, params={}):
        pass

    @abstractmethod
    def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None, params={}):
        pass
