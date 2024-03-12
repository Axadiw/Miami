import json
from json import JSONDecodeError

from api.exchange_wrappers.exchange_wrapper import ExchangeWrapper


class Bybit3CommasWrapper(ExchangeWrapper):

    @staticmethod
    def get_name():
        return 'bybit_3commas'

    def get_balance(self):
        return 0

    @staticmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        try:
            details = json.loads(serialized_account_details)
            return 'accountId' in details and 'apiKey' in details and 'apiSecret' in details
        except JSONDecodeError:
            return False
