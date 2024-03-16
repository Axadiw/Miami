import json
import os
from typing import Type

from flask import Blueprint, jsonify, request, make_response

from api.database import db
from api.endpoints.consts import PARAMS_INVALID_RESPONSE
from api.endpoints.session.token_required import token_required
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.exchange_wrappers.exchange_wrapper import ExchangeWrapper
from shared.consts_tpl import miami_version_env_key
from shared.models.exchange_account import ExchangeAccount

exchange_routes = Blueprint('exchange_routes', __name__)

wrapper_map: dict[str: Type[ExchangeWrapper]] = {Bybit3CommasWrapper.get_name(): Bybit3CommasWrapper}


@exchange_routes.route('/exchange_get_balance', methods=['GET'])
@token_required
def get_balance(user):
    if 'account' not in request.args:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    account = db.session.query(ExchangeAccount).filter_by(id=request.args['account'], user_id=user.id).first()

    if account is None:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if account.type not in wrapper_map:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    wrapper: ExchangeWrapper = wrapper_map[account.type](account.details)
    return wrapper.get_balance()


@exchange_routes.route('/exchange_create_market_position', methods=['POST'])
@token_required
def create_market_position(user):
    data = request.get_json()

    account_id = data['account_id']
    side = data['side']
    symbol = data['symbol']
    position_size = data['position_size']
    take_profits = data['take_profits']
    stop_loss = data['stop_loss']
    comment = data['comment']
    move_sl_to_breakeven_after_tp1 = data['move_sl_to_breakeven_after_tp1']
    helper_url = data['helper_url'] if 'helper_url' in data else None

    account = db.session.query(ExchangeAccount).filter_by(id=account_id, user_id=user.id).first()
    wrapper = Bybit3CommasWrapper(account.details)

    return wrapper.create_market(side=side, symbol=symbol, position_size=position_size, take_profits=take_profits,
                                 stop_loss=stop_loss, comment=comment,
                                 move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1, helper_url=helper_url)
