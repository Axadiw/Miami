import json

from api.endpoints.consts import MAXIMUM_COMMENT_LENGTH, MAXIMUM_HELPER_URL_LENGTH
from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.exchange_create_position_test_helpers import should_handle_properly_side, should_handle_properly_symbol, \
    should_handle_properly_take_profits, should_handle_properly_stop_loss, \
    should_handle_properly_soft_stop_loss, should_handle_properly_comment, should_handle_properly_move_sl_to_be, \
    fail_when_non_existing_account_provided, fail_for_account_from_different_user, \
    should_have_at_least_2tps_when_moveto_be_set, can_have_single_tp_when_dont_need_to_move_sl_to_be, \
    create_exchange_account, should_handle_properly_numeric_parameter

common_scaled_params = {'account_id': 1,
                        'symbol': 'SYMBOL_NAME',
                        'upper_price': 9,
                        'lower_price': 6,
                        'orders_count': 4,
                        'position_size': 10,
                        'take_profits': [[10, 30], [20, 20], [30, 50]],
                        'stop_loss': 5,
                        'comment': 'my_comment',
                        'move_sl_to_breakeven_after_tp1': True,
                        'helper_url': 'this_is_helper_url',
                        'soft_stop_loss_timeout': 0,
                        'side': 'Long'}


def test_should_check_if_all_params_are_provided(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'soft_stop_loss_timeout': '-1',
                                 'helper_url': 'this_is_helper_url'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'upper_price': 9,
                                 'lower_price': 6,
                                 'orders_count': 4,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_side(client, mocker, user1_token):
    should_handle_properly_side(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                "/exchange_create_scaled_position")


def test_should_handle_properly_symbol(client, mocker, user1_token):
    should_handle_properly_symbol(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                  "/exchange_create_scaled_position")


def test_should_handle_properly_position_size(client, mocker, user1_token):
    should_handle_properly_numeric_parameter(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                             "/exchange_create_scaled_position", 'position_size')


def test_should_handle_properly_orders_count(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_scaled', return_value='dummy_create_response')

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'orders_count': '123'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'orders_count': 2})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'orders_count': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'orders_count': 5.5})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'orders_count': 3})
    assert response.data == b'dummy_create_response'


def test_should_handle_properly_upper_lower_prices(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_scaled', return_value='dummy_create_response')

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'upper_price': '9'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': '6'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': -2, 'upper_price': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE
    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': 0, 'upper_price': 3})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': 20, 'upper_price': 10})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': 20, 'upper_price': 20})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': 10, 'upper_price': 20})
    assert response.data == b'dummy_create_response'

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={**common_scaled_params, 'lower_price': 10.5, 'upper_price': 20.5})
    assert response.data == b'dummy_create_response'


def test_should_handle_properly_take_profits(client, mocker, user1_token):
    should_handle_properly_take_profits(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                        "/exchange_create_scaled_position")


def test_should_handle_properly_stop_loss(client, mocker, user1_token):
    should_handle_properly_stop_loss(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                     "/exchange_create_scaled_position")


def test_should_handle_properly_soft_stop_loss(client, mocker, user1_token):
    should_handle_properly_soft_stop_loss(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                          "/exchange_create_scaled_position")


def test_should_handle_properly_comment(client, mocker, user1_token):
    should_handle_properly_comment(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                   "/exchange_create_scaled_position")


def test_should_handle_properly_move_sl_to_be(client, mocker, user1_token):
    should_handle_properly_move_sl_to_be(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                         "/exchange_create_scaled_position")


def test_should_handle_properly_helper_url(client, mocker, user1_token):
    should_handle_properly_move_sl_to_be(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                         "/exchange_create_scaled_position")


def test_fail_when_non_existing_account_provided(client, user1_token):
    fail_when_non_existing_account_provided(client, user1_token, common_scaled_params, 'create_scaled',
                                            "/exchange_create_scaled_position")


def test_fail_for_account_from_different_user(client, user1_token, user2_token):
    fail_for_account_from_different_user(client, user1_token, user2_token, common_scaled_params, 'create_scaled',
                                         "/exchange_create_scaled_position")


def test_should_have_at_least_2tps_when_moveto_be_set(client, mocker, user1_token):
    should_have_at_least_2tps_when_moveto_be_set(client, mocker, user1_token, common_scaled_params, 'create_scaled',
                                                 "/exchange_create_scaled_position")


def test_can_have_single_tp_when_dont_need_to_move_sl_to_be(client, mocker, user1_token):
    can_have_single_tp_when_dont_need_to_move_sl_to_be(client, mocker, user1_token, common_scaled_params,
                                                       'create_scaled',
                                                       "/exchange_create_scaled_position")


def test_check_if_params_passed_to_wrapper(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    create_scaled_spy = mocker.patch.object(Bybit3CommasWrapper, 'create_scaled',
                                            return_value='dummy_create_scaled_response')

    side = 'Long'
    symbol = 'SYMBOL_NAME'
    upper_price = 9
    lower_price = 6
    orders_count = 4
    position_size = 10
    take_profits = [[10, 30], [20, 20], [30, 50]]
    stop_loss = 5
    comment = 'my_comment'
    move_sl_to_breakeven_after_tp1 = True
    helper_url = 'this_is_helper_url'
    soft_stop_loss_timeout = 100

    response = client.post("/exchange_create_scaled_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': symbol,
                                 'upper_price': upper_price,
                                 'lower_price': lower_price,
                                 'orders_count': orders_count,
                                 'position_size': position_size,
                                 'take_profits': take_profits,
                                 'stop_loss': stop_loss,
                                 'comment': comment,
                                 'move_sl_to_breakeven_after_tp1': move_sl_to_breakeven_after_tp1,
                                 'helper_url': helper_url,
                                 'soft_stop_loss_timeout': soft_stop_loss_timeout,
                                 'side': side})
    assert response.data == b'dummy_create_scaled_response'
    assert create_scaled_spy.call_count == 1
    create_scaled_spy.assert_called_once_with(side=side,
                                              symbol=symbol,
                                              upper_price=upper_price,
                                              lower_price=lower_price,
                                              orders_count=orders_count,
                                              position_size=position_size,
                                              take_profits=take_profits,
                                              stop_loss=stop_loss,
                                              soft_stop_loss_timeout=soft_stop_loss_timeout,
                                              comment=comment,
                                              move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1,
                                              helper_url=helper_url)
