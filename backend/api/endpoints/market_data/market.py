from operator import attrgetter

from flask import jsonify, make_response, request, Blueprint
from sqlalchemy import desc

from api.database import db
from api.endpoints.consts import PARAMS_INVALID_RESPONSE
from shared.consts import bybit_ohlcv_timeframes
from shared.models.exchange import Exchange
from shared.models.ohlcv import OHLCV
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe

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

    ohlcvs = list(
        map(lambda x: {"open": float(x.open), "high": float(x.high), "low": float(x.low), "close": float(x.close),
                       "volume": float(x.volume),
                       "time": x.timestamp.timestamp()},
            sorted(db.session.query(OHLCV).filter_by(exchange=exchange.id, timeframe=timeframe.id,
                                                     symbol=symbol.id).order_by(desc(OHLCV.timestamp))
                   .limit(limit)
                   .all(), key=attrgetter('timestamp'))
            ))
    return jsonify({'ohlcvs': ohlcvs})
