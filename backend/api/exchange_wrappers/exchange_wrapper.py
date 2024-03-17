from abc import ABC, abstractmethod


class ExchangeWrapper(ABC):
    @abstractmethod
    def __init__(self, serialized_account_details: str):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def create_market(self, side: str, symbol: str, position_size: float, take_profits: list[list[int | float]],
                      stop_loss: float,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: str):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        pass
