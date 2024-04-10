import json
import uuid
from datetime import datetime
from json import JSONDecodeError

from flask import jsonify, make_response
from py3cw.request import Py3CW

from api.database import db
from api.endpoints.consts import MARKET_POSITION_CREATED, UNKNOWN_3COMMAS_ERROR
from api.exchange_wrappers.exchange_wrapper import ExchangeWrapper
from shared.models.order import Order, STOP_LOSS_ORDER_TYPE, CREATED_ORDER_STATE, TAKE_PROFIT_ORDER_TYPE, \
    STANDARD_ORDER_TYPE, FILLED_ORDER_STATE
from shared.models.position import Position, SHORT_SIDE, LONG_SIDE, serialize_side, CREATED_POSITION_STATE


class Bybit3CommasWrapper(ExchangeWrapper):

    def __init__(self, account_id: int, serialized_account_details: str):
        details = json.loads(serialized_account_details)
        self.accountId = account_id
        self.three_commas_account_id = details['accountId']

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

    def create_market(self, side: str, symbol: str, position_size: float,
                      take_profits: list[list[int | float]],
                      stop_loss: float, soft_stop_loss_timeout: int,
                      comment: str, move_sl_to_breakeven_after_tp1: bool, helper_url: str):
        error, data = self.p3cw.request(
            entity='smart_trades_v2',
            action='new',
            payload={
                "account_id": self.three_commas_account_id,
                "pair": "USDT_{}USDT".format(symbol.split('/')[0].upper()),
                "note": comment,
                "position": {
                    "type": 'buy' if side == 'Long' else 'sell',
                    "units": {
                        "value": position_size
                    },
                    "order_type": "market"
                },
                "take_profit": {
                    "enabled": "true",
                    "steps": [
                        {
                            "order_type": "limit",
                            "price": {
                                "value": take_profit[0],
                                "type": "bid"
                            },
                            "volume": take_profit[1]
                        } for take_profit in take_profits
                    ]
                },
                "stop_loss": {
                    "enabled": "true",
                    "breakeven": "true" if move_sl_to_breakeven_after_tp1 else 'false',
                    "order_type": "market",
                    'timeout': {'enabled': 'true', 'value': soft_stop_loss_timeout} if soft_stop_loss_timeout > 0 else {
                        'enabled': 'false'},
                    "conditional": {
                        "price": {
                            "value": stop_loss,
                            "type": "bid"
                        }
                    },
                }
            }
        )
        if error:
            error_message = UNKNOWN_3COMMAS_ERROR
            if 'msg' in error:
                error_message = error['msg']
            return make_response(jsonify(dict(error=error_message)), 400)

        size = data['position']['units']['value']
        open_price = data['position']['price']['value']
        '2024-04-04T21:13:37.782Z'
        create_date = datetime.fromisoformat(data['data']['created_at'])
        position_external_id = str(uuid.uuid4())
        symbol = symbol  # TBD czy to pwinien byc string czy id
        new_position = Position(side=serialize_side(side), size=size, account_id=self.accountId, comment=comment,
                                position_external_id=position_external_id, helper_url=helper_url, symbol=symbol,
                                state=CREATED_POSITION_STATE,
                                create_date=create_date,
                                move_sl_to_be=move_sl_to_breakeven_after_tp1,
                                soft_stop_loss_timeout=soft_stop_loss_timeout)
        db.session.add(new_position)
        db.session.commit()

        sl_order = Order(type=STOP_LOSS_ORDER_TYPE, state=CREATED_ORDER_STATE, create_date=create_date,
                         name=(str(uuid.uuid4())), price=stop_loss, position_id=new_position.id)

        db.session.add_all([Order(type=TAKE_PROFIT_ORDER_TYPE, state=CREATED_ORDER_STATE, create_date=create_date,
                                  name=str(uuid.uuid4()), price=take_profit[0], amount=take_profit[1],
                                  position_id=new_position.id)
                            for take_profit in take_profits])

        db.session.add(Order(type=STANDARD_ORDER_TYPE, state=FILLED_ORDER_STATE, create_date=create_date,
                             name=str(uuid.uuid4()), price=open_price, amount=position_size,
                             position_id=new_position.id))

        db.session.add(sl_order)
        db.session.commit()

        return jsonify(MARKET_POSITION_CREATED)

    def get_balance(self):

        error, data = self.p3cw.request(
            entity='accounts',
            action='load_balances',
            action_id=self.three_commas_account_id
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
