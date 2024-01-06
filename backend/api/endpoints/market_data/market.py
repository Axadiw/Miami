import datetime
import uuid

import jwt
from flask import jsonify, make_response, request, Blueprint
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from harvesting.data_harvesters.exchanges.bybit.bybit_harvesters import bybit_ohlcv_timeframes
from shared.consts_tpl import flask_api_secret
from api.database import db
from api.endpoints.consts import PARAMS_INVALID_RESPONSE, USER_EXISTS_RESPONSE, INCORRECT_CREDENTIALS_RESPONSE, \
    TOKEN_MISSING_RESPONSE, TOKEN_VALID_RESPONSE, TOKEN_EXPIRED_RESPONSE, TOKEN_INVALID_RESPONSE, \
    TOKEN_VALIDITY_IN_DAYS, REGISTRATION_SUCCESS_RESPONSE, EMAIL_IN_USE_RESPONSE, MINIMUM_USERNAME_LENGTH, \
    MINIMUM_PASSWORD_LENGTH, PASSWORD_CHANGED_RESPONSE
from api.endpoints.session.token_required import token_required
from shared.models.exchange import Exchange
from shared.models.ohlcv import OHLCV
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe
from shared.models.user import User
import re

market_routes = Blueprint('market_routes', __name__)


@market_routes.route('/exchanges', methods=['GET'])
def get_exchanges():
    exchanges = list(map(lambda x: x.name, db.session.query(Exchange).order_by(Exchange.name).all()))
    return jsonify({'exchanges': exchanges})


@market_routes.route('/symbols', methods=['GET'])
def get_symbols():
    if 'exchange' not in request.args:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    exchange = db.session.query(Exchange).filter_by(name=request.args['exchange']).first()
    if exchange is None:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    symbols = list(map(lambda x: x.name, db.session.query(Symbol).filter_by(exchange=exchange.id).all()))
    return jsonify({'symbols': symbols})


@market_routes.route('/ohlcv_timeframes', methods=['GET'])
def get_ohlcv_timeframes():
    if 'exchange' not in request.args:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if request.args['exchange'] == 'bybit':
        return jsonify({'timeframes': bybit_ohlcv_timeframes})
    # elif rest of the exchanges
    else:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)


@market_routes.route('/ohlcv', methods=['GET'])
def get_ohlcv():
    if 'exchange' not in request.args or 'tf' not in request.args or 'symbol' not in request.args or 'limit' not in request.args:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not request.args['limit'].isnumeric():
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    limit = int(request.args['limit'])

    if limit <= 0:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    exchange = db.session.query(Exchange).filter_by(name=request.args['exchange']).first()
    timeframe = db.session.query(Timeframe).filter_by(name=request.args['tf']).first()
    symbol = db.session.query(Symbol).filter_by(name=request.args['symbol']).first()
    if exchange is None or timeframe is None or symbol is None:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    ohlcvs = list(map(lambda x: {"open": x.open, "high": x.high, "low": x.low, "close": x.close, "volume": x.volume,
                                 "time": x.timestamp.timestamp()},
                      db.session.query(OHLCV).filter_by(exchange=exchange.id, timeframe=timeframe.id,
                                                        symbol=symbol.id).limit(limit).all()))
    return jsonify({'ohlcvs': ohlcvs})
