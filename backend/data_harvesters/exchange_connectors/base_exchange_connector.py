from abc import ABC, abstractmethod
from typing import List, Type, Optional

from models.exchanges import Exchanges
from models.ohlcv import OHLCV
from models.symbols import Symbols
from models.timeframes import Timeframes


class BaseExchangeConnector(ABC):

    @abstractmethod
    async def fetch_tickers(self) -> List[Symbols]:
        pass

    @abstractmethod
    async def fetch_ohlcv(self, symbol: Type[Symbols], timeframe: Type[Timeframes], exchange: Type[Exchanges],
                          since: int) \
            -> List[OHLCV]:
        pass

    def watch_ohlcv(self, symbolsAndTimeframes: List[List[str]], since: Optional[int] = None,
                    limit: Optional[int] = None, params={}):
        pass

    def watch_trades(self, symbols: List[str], since: Optional[int] = None, limit: Optional[int] = None, params={}):
        pass
