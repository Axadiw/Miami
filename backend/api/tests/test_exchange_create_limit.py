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

common_limit_params = {'account_id': 1,
                       'symbol': 'SYMBOL_NAME',
                       'limit_price': 7,
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
    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
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

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'soft_stop_loss_timeout': '-1',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'soft_stop_loss_timeout': '-1',
                                 'helper_url': 'this_is_helper_url'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'limit_price': 7,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_side(client, mocker, user1_token):
    should_handle_properly_side(client, mocker, user1_token, common_limit_params, 'create_limit',
                                "/exchange_create_limit_position")


def test_should_handle_properly_symbol(client, mocker, user1_token):
    should_handle_properly_symbol(client, mocker, user1_token, common_limit_params, 'create_limit',
                                  "/exchange_create_limit_position")


def test_should_handle_properly_position_size(client, mocker, user1_token):
    should_handle_properly_numeric_parameter(client, mocker, user1_token, common_limit_params, 'create_limit',
                                             "/exchange_create_limit_position", 'position_size')


def test_should_handle_properly_limit_price(client, mocker, user1_token):
    should_handle_properly_numeric_parameter(client, mocker, user1_token, common_limit_params, 'create_limit',
                                             "/exchange_create_limit_position", 'limit_price')


def test_should_handle_properly_take_profits(client, mocker, user1_token):
    should_handle_properly_take_profits(client, mocker, user1_token, common_limit_params, 'create_limit',
                                        "/exchange_create_limit_position")


def test_should_handle_properly_stop_loss(client, mocker, user1_token):
    should_handle_properly_stop_loss(client, mocker, user1_token, common_limit_params, 'create_limit',
                                     "/exchange_create_limit_position")


def test_should_handle_properly_soft_stop_loss(client, mocker, user1_token):
    should_handle_properly_soft_stop_loss(client, mocker, user1_token, common_limit_params, 'create_limit',
                                          "/exchange_create_limit_position")


def test_should_handle_properly_comment(client, mocker, user1_token):
    should_handle_properly_comment(client, mocker, user1_token, common_limit_params, 'create_limit',
                                   "/exchange_create_limit_position")


def test_should_handle_properly_move_sl_to_be(client, mocker, user1_token):
    should_handle_properly_move_sl_to_be(client, mocker, user1_token, common_limit_params, 'create_limit',
                                         "/exchange_create_limit_position")


def test_should_handle_properly_helper_url(client, mocker, user1_token):
    should_handle_properly_move_sl_to_be(client, mocker, user1_token, common_limit_params, 'create_limit',
                                         "/exchange_create_limit_position")


def test_fail_when_non_existing_account_provided(client, user1_token):
    fail_when_non_existing_account_provided(client, user1_token, common_limit_params, 'create_limit',
                                            "/exchange_create_limit_position")


def test_fail_for_account_from_different_user(client, user1_token, user2_token):
    fail_for_account_from_different_user(client, user1_token, user2_token, common_limit_params, 'create_limit',
                                         "/exchange_create_limit_position")


def test_should_have_at_least_2tps_when_moveto_be_set(client, mocker, user1_token):
    should_have_at_least_2tps_when_moveto_be_set(client, mocker, user1_token, common_limit_params, 'create_limit',
                                                 "/exchange_create_limit_position")


def test_can_have_single_tp_when_dont_need_to_move_sl_to_be(client, mocker, user1_token):
    can_have_single_tp_when_dont_need_to_move_sl_to_be(client, mocker, user1_token, common_limit_params,
                                                       'create_limit',
                                                       "/exchange_create_limit_position")


def test_check_if_params_passed_to_wrapper(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    create_limit_spy = mocker.patch.object(Bybit3CommasWrapper, 'create_limit',
                                           return_value='dummy_create_limit_response')

    side = 'Long'
    symbol = 'SYMBOL_NAME'
    limit_price = 7
    position_size = 10
    take_profits = [[10, 30], [20, 20], [30, 50]]
    stop_loss = 5
    comment = 'my_comment'
    move_sl_to_breakeven_after_tp1 = True
    helper_url = 'this_is_helper_url'
    soft_stop_loss_timeout = 100

    response = client.post("/exchange_create_limit_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': symbol,
                                 'limit_price': limit_price,
                                 'position_size': position_size,
                                 'take_profits': take_profits,
                                 'stop_loss': stop_loss,
                                 'comment': comment,
                                 'move_sl_to_breakeven_after_tp1': move_sl_to_breakeven_after_tp1,
                                 'helper_url': helper_url,
                                 'soft_stop_loss_timeout': soft_stop_loss_timeout,
                                 'side': side})
    assert response.data == b'dummy_create_limit_response'
    assert create_limit_spy.call_count == 1
    create_limit_spy.assert_called_once_with(side=side,
                                             symbol=symbol,
                                             limit_price=limit_price,
                                             position_size=position_size,
                                             take_profits=take_profits,
                                             stop_loss=stop_loss,
                                             soft_stop_loss_timeout=soft_stop_loss_timeout,
                                             comment=comment,
                                             move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1,
                                             helper_url=helper_url)
