from typing import Type

from flask import Blueprint, jsonify, request, make_response

from api.database import db
from api.endpoints.consts import PARAMS_INVALID_RESPONSE, POSITION_SIDES, MAXIMUM_COMMENT_LENGTH, \
    MAXIMUM_HELPER_URL_LENGTH
from api.endpoints.session.token_required import token_required
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.exchange_wrappers.exchange_wrapper import ExchangeWrapper
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

    wrapper: ExchangeWrapper = wrapper_map[account.type](account.id, account.details)
    return wrapper.get_balance()


@exchange_routes.route('/exchange_create_market_position', methods=['POST'])
@token_required
def create_market_position(user):
    data = request.get_json()

    if 'account_id' not in data \
            or 'side' not in data \
            or 'symbol' not in data \
            or 'position_size' not in data \
            or 'take_profits' not in data \
            or 'stop_loss' not in data \
            or 'comment' not in data \
            or 'move_sl_to_breakeven_after_tp1' not in data \
            or 'soft_stop_loss_timeout' not in data \
            or 'helper_url' not in data:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    account_id = data['account_id']
    side = data['side']
    symbol = data['symbol']
    position_size = data['position_size']
    take_profits = data['take_profits']
    stop_loss = data['stop_loss']
    comment = data['comment']
    soft_stop_loss_timeout = data['soft_stop_loss_timeout']
    move_sl_to_breakeven_after_tp1 = data['move_sl_to_breakeven_after_tp1']
    helper_url = data['helper_url']

    account = db.session.query(ExchangeAccount).filter_by(id=account_id, user_id=user.id).first()

    if not account:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if account.type not in wrapper_map:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if side not in POSITION_SIDES:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not isinstance(symbol, str) or len(symbol) <= 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if (not isinstance(position_size, int) and not isinstance(position_size, float)) or position_size <= 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if (not isinstance(stop_loss, int) and not isinstance(stop_loss, float)) or stop_loss <= 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if (not isinstance(soft_stop_loss_timeout, int)) or soft_stop_loss_timeout < 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not isinstance(take_profits, list) or len(take_profits) <= 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    for take_profit in take_profits:
        if not isinstance(take_profit, list) or len(take_profit) != 2:
            return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

        for entry in take_profit:
            if (not isinstance(entry, int) and not isinstance(entry, float)) or entry <= 0:
                return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    sum_of_tp_volumes = 0
    tp_dict = {}
    for take_profit in take_profits:
        sum_of_tp_volumes += take_profit[1]
        if take_profit[0] in tp_dict:
            return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)
        tp_dict[take_profit[0]] = True
    if sum_of_tp_volumes != 100:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if move_sl_to_breakeven_after_tp1 and len(take_profits) < 2:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not isinstance(comment, str) or len(comment) > MAXIMUM_COMMENT_LENGTH:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not isinstance(move_sl_to_breakeven_after_tp1, bool):
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not isinstance(helper_url, str) or len(helper_url) > MAXIMUM_HELPER_URL_LENGTH:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    wrapper: ExchangeWrapper = wrapper_map[account.type](account.id, account.details)
    return wrapper.create_market(side=side, symbol=symbol, position_size=position_size, take_profits=take_profits,
                                 stop_loss=stop_loss, soft_stop_loss_timeout=soft_stop_loss_timeout, comment=comment,
                                 move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1, helper_url=helper_url)
