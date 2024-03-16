from abc import ABC, abstractmethod
from typing import Optional


class ExchangeWrapper(ABC):
    @abstractmethod
    def __init__(self, serialized_account_details: str):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def create_market(self, side: str, symbol: str, position_size: float, take_profits: dict, stop_loss: float,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: Optional[str]):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        pass
