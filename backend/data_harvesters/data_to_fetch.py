from dataclasses import dataclass
from datetime import datetime
from typing import Type

from models.symbol import Symbol
from models.timeframe import Timeframe


@dataclass
class DataToFetch:
    symbol: Type[Symbol]
    timeframe: Type[Timeframe]
    start: datetime
    end: datetime

    def length(self):
        return self.end - self.start

    def __repr__(self):
        return f'{self.symbol.name} {self.timeframe.name} {self.start}\t-\t{self.end}\tlength: {self.length()}'
