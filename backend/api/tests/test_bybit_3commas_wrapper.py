import json

from py3cw.request import Py3CW

from api.endpoints.consts import MAXIMUM_COMMENT_LENGTH, MAXIMUM_HELPER_URL_LENGTH, MARKET_POSITION_CREATED, \
    UNKNOWN_3COMMAS_ERROR
from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper


def test_should_pass_correct_params_to_py3w_with_3_tps(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, 'dummy_value_py3w'))
    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_market(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10,
                                     take_profits=[[10, 30], [20, 20], [30, 50]],
                                     stop_loss=5, comment='my_comment',
                                     move_sl_to_breakeven_after_tp1=True,
                                     soft_stop_loss_timeout=0,
                                     helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.json == MARKET_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'market', 'type': 'buy',
                                                           'units': {'value': 10}},
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
                                   return_value=(None, 'dummy_value_py3w'))
    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_market(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10,
                                     take_profits=[[10, 30], [20, 20], [30, 50]],
                                     stop_loss=5, comment='my_comment',
                                     move_sl_to_breakeven_after_tp1=True,
                                     soft_stop_loss_timeout=10,
                                     helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.json == MARKET_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'market', 'type': 'buy',
                                                           'units': {'value': 10}},
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
                                   return_value=(None, 'dummy_value_py3w'))
    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_market(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10,
                                     take_profits=[[10, 30], [20, 70]],
                                     stop_loss=5, comment='my_comment',
                                     move_sl_to_breakeven_after_tp1=True,
                                     soft_stop_loss_timeout=0,
                                     helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.status_code == 200
    assert response.json == MARKET_POSITION_CREATED
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'market', 'type': 'buy',
                                                           'units': {'value': 10}},
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
    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_market(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10,
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
    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))

    response = wrapper.create_market(side='Long', symbol='SYMBOL_NAME/USDT:USDT', position_size=10,
                                     take_profits=[[10, 30], [20, 70]],
                                     stop_loss=5, soft_stop_loss_timeout=0, comment='my_comment',
                                     move_sl_to_breakeven_after_tp1=True,
                                     helper_url='this_is_helper_url')

    assert py3w_spy.call_count == 1
    assert response.status_code == 400
    assert response.json == {'error': UNKNOWN_3COMMAS_ERROR}
