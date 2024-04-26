import json

from py3cw.request import Py3CW

from api.database import db
from api.endpoints.consts import UNKNOWN_3COMMAS_ERROR, LIMIT_POSITION_CREATED
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.bybit_3commas_wrapper.bybit_3commas_create_position_test_helpers import example_response
from shared.models.order import Order, STOP_LOSS_ORDER_TYPE, TAKE_PROFIT_ORDER_TYPE, CREATED_ORDER_STATE, \
    STANDARD_ORDER_TYPE
from shared.models.position import Position, LONG_SIDE


def test_should_pass_correct_params_to_py3w_with_3_tps(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, example_response))
    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                                    take_profits=[[10, 30], [20, 20], [30, 50]],
                                    stop_loss=5, comment='my_comment',
                                    move_sl_to_breakeven_after_tp1=True,
                                    soft_stop_loss_timeout=0,
                                    helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.json == LIMIT_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'limit', 'type': 'buy',
                                                           'units': {'value': 10}, "price": {"value": 7.0}},
                                              'stop_loss':
                                                  {'breakeven': 'true',
                                                   'conditional': {'price': {'type': 'bid', 'value': 5}},
                                                   'enabled': 'true',
                                                   'timeout': {'enabled': 'false'},
                                                   'order_type': 'market'},
                                              'take_profit': {'enabled': 'true',
                                                              'steps': [{'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 10},
                                                                         'volume': 30},
                                                                        {'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 20},
                                                                         'volume': 20},
                                                                        {'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 30},
                                                                         'volume': 50}]}})


def test_should_pass_soft_sl_correctly(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, example_response))
    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                                    take_profits=[[10, 30], [20, 20], [30, 50]],
                                    stop_loss=5, comment='my_comment',
                                    move_sl_to_breakeven_after_tp1=True,
                                    soft_stop_loss_timeout=10,
                                    helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.json == LIMIT_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'limit', 'type': 'buy',
                                                           'units': {'value': 10}, "price": {"value": 7.0}},
                                              'stop_loss':
                                                  {'breakeven': 'true',
                                                   'conditional': {'price': {'type': 'bid', 'value': 5}},
                                                   'timeout': {'enabled': 'true', 'value': 10},
                                                   'enabled': 'true',
                                                   'order_type': 'market'},
                                              'take_profit': {'enabled': 'true',
                                                              'steps': [{'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 10},
                                                                         'volume': 30},
                                                                        {'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 20},
                                                                         'volume': 20},
                                                                        {'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 30},
                                                                         'volume': 50}]}})


def test_should_pass_correct_params_to_py3w_with_2_tps(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, example_response))
    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                                    take_profits=[[10, 30], [20, 70]],
                                    stop_loss=5, comment='my_comment',
                                    move_sl_to_breakeven_after_tp1=True,
                                    soft_stop_loss_timeout=0,
                                    helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.status_code == 200
    assert response.json == LIMIT_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'limit', 'type': 'buy',
                                                           'units': {'value': 10}, "price": {"value": 7.0}},
                                              'stop_loss':
                                                  {'breakeven': 'true',
                                                   'conditional': {'price': {'type': 'bid', 'value': 5}},
                                                   'enabled': 'true',
                                                   'timeout': {'enabled': 'false'},
                                                   'order_type': 'market'},
                                              'take_profit': {'enabled': 'true',
                                                              'steps': [{'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 10},
                                                                         'volume': 30},
                                                                        {'order_type': 'limit',
                                                                         'price': {'type': 'bid', 'value': 20},
                                                                         'volume': 70}]}})


def test_should_pass_3commas_error(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=({'msg': 'dummy_error'}, 'dummy_value_py3w'))
    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                                    take_profits=[[10, 30], [20, 70]],
                                    stop_loss=5, comment='my_comment',
                                    move_sl_to_breakeven_after_tp1=True, soft_stop_loss_timeout=0,
                                    helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.status_code == 400
    assert response.json == {'error': 'dummy_error'}


def test_should_pass_unknown_error(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=('dummy_error', 'dummy_value_py3w'))
    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                                    take_profits=[[10, 30], [20, 70]],
                                    stop_loss=5, soft_stop_loss_timeout=0, comment='my_comment',
                                    move_sl_to_breakeven_after_tp1=True,
                                    helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.status_code == 400
    assert response.json == {'error': UNKNOWN_3COMMAS_ERROR}


def test_should_create_position_and_order_objects(app, mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, example_response))

    wrapper = Bybit3CommasWrapper(account_id=0,
                                  serialized_account_details=json.dumps(
                                      {'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    positions = db.session.query(Position).all()
    assert len(positions) == 0
    orders = db.session.query(Order).all()
    assert len(orders) == 0

    wrapper.create_limit(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10, limit_price=7,
                         take_profits=[[10, 30], [20, 70]],
                         stop_loss=5, comment='my_comment',
                         move_sl_to_breakeven_after_tp1=True,
                         soft_stop_loss_timeout=60,
                         helper_url='this_is_helper_url')

    positions = list(db.session.query(Position).all())
    assert len(positions) == 1
    positions[0].side = LONG_SIDE
    positions[0].size = 10
    positions[0].account_id = 0
    positions[0].comment = 'my_comment'
    positions[0].helper_url = 'this_is_helper_url'
    positions[0].symbol = 'SYMBOL_NAME/USDT:USDT'
    positions[0].move_sl_to_be = True
    positions[0].soft_stop_loss_timeout = 60

    sls = db.session.query(Order).filter_by(type=STOP_LOSS_ORDER_TYPE).all()
    assert len(sls) == 1
    assert sls[0].type == STOP_LOSS_ORDER_TYPE
    assert sls[0].state == CREATED_ORDER_STATE
    assert sls[0].price == 5
    assert sls[0].amount is None
    assert sls[0].position_id == positions[0].id

    tps = db.session.query(Order).filter_by(type=TAKE_PROFIT_ORDER_TYPE).order_by(Order.price).all()
    assert len(tps) == 2
    assert tps[0].type == TAKE_PROFIT_ORDER_TYPE
    assert tps[0].state == CREATED_ORDER_STATE
    assert tps[0].price == 10
    assert tps[0].amount == 30
    assert tps[0].position_id == positions[0].id

    assert tps[1].type == TAKE_PROFIT_ORDER_TYPE
    assert tps[1].state == CREATED_ORDER_STATE
    assert tps[1].price == 20
    assert tps[1].amount == 70
    assert tps[1].position_id == positions[0].id

    stds = db.session.query(Order).filter_by(type=STANDARD_ORDER_TYPE).order_by(Order.price).all()
    assert len(stds) == 1
    assert stds[0].type == STANDARD_ORDER_TYPE
    assert stds[0].state == CREATED_ORDER_STATE
    assert stds[0].price == 6
    assert stds[0].amount == 10
    assert stds[0].position_id == positions[0].id
