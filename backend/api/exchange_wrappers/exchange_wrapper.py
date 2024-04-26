from abc import ABC, abstractmethod

from shared.models.position import SHORT_SIDE, LONG_SIDE


class ExchangeWrapper(ABC):
    @abstractmethod
    def __init__(self, account_id: int, serialized_account_details: str):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def create_market(self, side: str, symbol: str, position_size: float,
                      take_profits: list[list[int | float]],
                      stop_loss: float, soft_stop_loss_timeout: int,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: str):
        pass

    @abstractmethod
    def create_limit(self, side: str, symbol: str, position_size: float, limit_price: float,
                     take_profits: list[list[int | float]],
                     stop_loss: float, soft_stop_loss_timeout: int,
                     comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: str):
        pass

    @abstractmethod
    def create_scaled(self, side: str, symbol: str, position_size: float, upper_price: float, lower_price: float,
                      orders_count: int,
                      take_profits: list[list[int | float]],
                      stop_loss: float, soft_stop_loss_timeout: int,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: str):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        pass
