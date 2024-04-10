from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Type, Optional

from ccxt.base.types import Trade
from harvesting.data_harvesters.data_to_fetch import DataToFetch
from shared.models.exchange import Exchange
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe


class BaseExchangeConnector(ABC):

    @abstractmethod
    async def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        pass

    @abstractmethod
    async def load_markets(self):
        pass

    @abstractmethod
    async def fetch_ohlcv(self, exchange: Type[Exchange], data: DataToFetch, trim_to_range: bool = True) -> \
            List[tuple]:
        pass

    @abstractmethod
    def build_ohlcv(self, last_ohlcv: Optional[list], trades: List[Trade], timeframe: Type[Timeframe]):
        pass

    @abstractmethod
    async def watch_trades(self, symbols_and_time_frames: List[str]):
        pass

    @abstractmethod
    async def watch_ohlcv(self, symbols_and_time_frames: List[List[str]]):
        pass

    @abstractmethod
    async def watch_tickers(self, symbols: List[str]):
        pass

    @abstractmethod
    async def fetch_start_dates(self):
        pass

    @abstractmethod
    async def get_server_time(self) -> datetime:
        pass

    @abstractmethod
    async def close(self):
        pass
