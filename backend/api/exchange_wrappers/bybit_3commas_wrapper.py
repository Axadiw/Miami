import json
from json import JSONDecodeError
from typing import Optional

from flask import jsonify, make_response
from py3cw.request import Py3CW

from api.exchange_wrappers.exchange_wrapper import ExchangeWrapper


class Bybit3CommasWrapper(ExchangeWrapper):

    def __init__(self, serialized_account_details: str):
        details = json.loads(serialized_account_details)
        self.accountId = details['accountId']

        self.p3cw = Py3CW(
            key=details['apiKey'],
            secret=details['apiSecret'],
            request_options={
                'request_timeout': 10,
                'nr_of_retries': 5,
                'retry_status_codes': [502],
                'retry_backoff_factor': 0.1
            }
        )

    @staticmethod
    def get_name():
        return 'bybit_3commas'

    def create_market(self, side: str, symbol: str, position_size: float, take_profits: dict, stop_loss: float,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: Optional[str]):
        pass

    def get_balance(self):

        error, data = self.p3cw.request(
            entity='accounts',
            action='load_balances',
            action_id=self.accountId
        )

        if error:
            return make_response(jsonify(error), 500)

        return jsonify({'balance': float(data['usd_amount'])})

    @staticmethod
    def validate_account_details(serialized_account_details: str) -> bool:
        try:
            details = json.loads(serialized_account_details)
            return 'accountId' in details and 'apiKey' in details and 'apiSecret' in details
        except JSONDecodeError:
            return False
