from datetime import datetime

from api.database import db
from api.endpoints.consts import PARAMS_INVALID_RESPONSE
from shared.models.exchange import Exchange
from shared.models.ohlcv import OHLCV
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe


def populate_objects():
    db.session.add_all([Exchange(name='bybit'),
                        Exchange(name='mexc'),
                        Exchange(name='binance')])
    db.session.commit()

    bybit_exchange = db.session.query(Exchange).filter_by(name='bybit').first()
    mexc_exchange = db.session.query(Exchange).filter_by(name='mexc').first()

    db.session.add_all([Symbol(name='A', exchange=bybit_exchange.id),
                        Symbol(name='B', exchange=bybit_exchange.id),
                        Symbol(name='C', exchange=bybit_exchange.id),
                        Symbol(name='D', exchange=mexc_exchange.id)])
    symbol_a = db.session.query(Symbol).filter_by(name='A').first()
    symbol_b = db.session.query(Symbol).filter_by(name='B').first()
    symbol_c = db.session.query(Symbol).filter_by(name='C').first()
    symbol_d = db.session.query(Symbol).filter_by(name='D').first()

    db.session.add_all([Timeframe(name='1m', seconds=60),
                        Timeframe(name='5m', seconds=5 * 60),
                        Timeframe(name='15m', seconds=15 * 60)])
    timeframe_1m = db.session.query(Timeframe).filter_by(name='1m').first()
    timeframe_5m = db.session.query(Timeframe).filter_by(name='5m').first()
    timeframe_15m = db.session.query(Timeframe).filter_by(name='15m').first()

    db.session.add_all([OHLCV(id=0, exchange=bybit_exchange.id, symbol=symbol_a.id, timeframe=timeframe_1m.id,
                              timestamp=datetime.fromtimestamp(0), open=0, high=1, low=0, close=1, volume=0),
                        OHLCV(id=1, exchange=bybit_exchange.id, symbol=symbol_a.id, timeframe=timeframe_1m.id,
                              timestamp=datetime.fromtimestamp(60), open=2, high=4, low=2, close=4, volume=60),
                        OHLCV(id=2, exchange=bybit_exchange.id, symbol=symbol_b.id, timeframe=timeframe_1m.id,
                              timestamp=datetime.fromtimestamp(0), open=10, high=10, low=0, close=10, volume=10),
                        OHLCV(id=3, exchange=bybit_exchange.id, symbol=symbol_c.id, timeframe=timeframe_5m.id,
                              timestamp=datetime.fromtimestamp(0), open=0, high=1, low=0, close=1, volume=10),
                        OHLCV(id=4, exchange=mexc_exchange.id, symbol=symbol_d.id, timeframe=timeframe_15m.id,
                              timestamp=datetime.fromtimestamp(0), open=0, high=1, low=0, close=1, volume=10)])


def test_get_of_exchanges(client):
    populate_objects()
    response = client.get("/exchanges")

    assert response.status_code == 200
    assert response.json == {'exchanges': ['binance', 'bybit', 'mexc']}


def test_get_list_of_symbols(client):
    populate_objects()
    response = client.get("/symbols?exchange=bybit")

    assert response.status_code == 200
    assert response.json == {'symbols': ['A', 'B', 'C']}

    response = client.get("/symbols?exchange=mexc")
    assert response.status_code == 200
    assert response.json == {'symbols': ['D']}

    response = client.get("/symbols?exchange=binance")
    assert response.status_code == 200
    assert response.json == {'symbols': []}


def test_get_list_of_symbols_incorrect_data(client):
    populate_objects()
    response = client.get("/symbols?exchange=wat")

    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_get_list_of_ohlcv_timeframes(client):
    populate_objects()
    response = client.get("/ohlcv_timeframes?exchange=bybit")

    assert response.status_code == 200
    assert response.json == {'timeframes': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']}


def test_get_list_of_ohlcv_timeframes_incorrect_data(client):
    populate_objects()
    response = client.get("/ohlcv_timeframes?exchange='wat'")

    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_get_ohlcv(client):
    populate_objects()
    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A&limit=1000")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': [{"open": 0, "high": 1, "low": 0, "close": 1, "volume": 0, "time": 0},
                                        {"open": 2, "high": 4, "low": 2, "close": 4, "volume": 60, "time": 60}]}

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A&limit=1")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': [{"open": 2, "high": 4, "low": 2, "close": 4, "volume": 60, "time": 60}]}

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=B&limit=1000")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': [{"open": 10, "high": 10, "low": 0, "close": 10, "volume": 10, "time": 0}]}

    response = client.get("/ohlcv?exchange=bybit&tf=5m&symbol=C&limit=1000")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': [{"open": 0, "high": 1, "low": 0, "close": 1, "volume": 10, "time": 0}]}

    response = client.get("/ohlcv?exchange=mexc&tf=15m&symbol=D&limit=1000")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': [{"open": 0, "high": 1, "low": 0, "close": 1, "volume": 10, "time": 0}]}

    response = client.get("/ohlcv?exchange=mexc&tf=5m&symbol=A&limit=1000")
    assert response.status_code == 200
    assert response.json == {'ohlcvs': []}


def test_get_ohlcv_incorrect_data(client):
    populate_objects()
    response = client.get("/ohlcv?exchange=wat&tf=1m&symbol=A&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=11m&symbol=A&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=WAT&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A&limit=WAT")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A&limit=-1")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A&limit=0")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?tf=1m&symbol=A&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&symbol=A&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&limit=1000")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.get("/ohlcv?exchange=bybit&tf=1m&symbol=A")
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE
