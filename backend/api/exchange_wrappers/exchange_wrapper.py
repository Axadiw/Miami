from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Type

from harvesting.data_harvesters.data_to_fetch import DataToFetch
from shared.models.exchange import Exchange
from shared.models.symbol import Symbol


class ExchangeWrapper(ABC):
    @abstractmethod
    def __init__(self, serialized_account_details: str):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        pass
