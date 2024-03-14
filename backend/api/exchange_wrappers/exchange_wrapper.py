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
    def get_balance(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        pass
