import json

from py3cw.request import Py3CW

from api.endpoints.consts import MAXIMUM_COMMENT_LENGTH, MAXIMUM_HELPER_URL_LENGTH
from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper

common_params = {'account_id': 1,
                 'symbol': 'SYMBOL_NAME',
                 'position_size': 10,
                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                 'stop_loss': 5,
                 'comment': 'my_comment',
                 'move_sl_to_breakeven_after_tp1': True,
                 'helper_url': 'this_is_helper_url',
                 'side': 'Long'}


def test_should_pass_correct_params_to_py3w(mocker):
    py3w_spy = mocker.patch.object(Py3CW, 'request',
                                   return_value=(None, 'dummy_value_py3w'))

    wrapper = Bybit3CommasWrapper(
        serialized_account_details=json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))
    side = 'Long'
    symbol = 'SYMBOL_NAME'
    position_size = 10
    take_profits = [[10, 30], [20, 20], [30, 50]]
    stop_loss = 5
    comment = 'my_comment'
    move_sl_to_breakeven_after_tp1 = True
    helper_url = 'this_is_helper_url'

    wrapper.create_market(side=side, symbol=symbol, position_size=position_size, take_profits=take_profits,
                          stop_loss=stop_loss, comment=comment,
                          move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1,
                          helper_url=helper_url)

    assert py3w_spy.call_count == 1
    py3w_spy.assert_called_once_with(entity='smart_trades_v2',
                                     action='new',
                                     payload={'account_id': '12345',
                                              'note': 'my_comment',
                                              'pair': 'USDT_SYMBOL_NAMEUSDT',
                                              'position': {'order_type': 'market',
                                                           'type': 'buy',
                                                           'units':
                                                               {'value': 10}},
                                              'stop_loss':
                                                  {'breakeven': 'true',
                                                   'conditional':
                                                       {'price':
                                                            {'type': 'bid', 'value': 5}},
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

# TODO add test for symbol splitting
# TODO add test different set of take profits
