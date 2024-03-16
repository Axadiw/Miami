import json

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


def create_exchange_account(client, token):
    client.post('/add_new_exchange_account', headers={"x-access-tokens": token},
                json={'type': 'bybit_3commas',
                      'name': 'account 1',
                      'details': (json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))})


def test_should_check_if_all_params_are_provided(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'helper_url': 'this_is_helper_url',
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'side': 'Long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': 'SYMBOL_NAME',
                                 'position_size': 10,
                                 'take_profits': [[10, 30], [20, 20], [30, 50]],
                                 'stop_loss': 5,
                                 'comment': 'my_comment',
                                 'move_sl_to_breakeven_after_tp1': True,
                                 'helper_url': 'this_is_helper_url'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_side(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'Long'})
    assert response.data == b'dummy_create_market_response'

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'Short'})
    assert response.data == b'dummy_create_market_response'

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'short'})
    assert response.status_code == 400

    assert response.json == PARAMS_INVALID_RESPONSE
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'wrong'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_symbol(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'symbol': ''})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_position_size(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'position_size': '123'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'position_size': 0})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'position_size': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # int value
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'position_size': 10})
    assert response.data == b'dummy_create_market_response'

    # float value
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'position_size': 10.1})
    assert response.data == b'dummy_create_market_response'


def test_should_handle_properly_take_profits(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': []})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': 'abc'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 2, 3]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # single tp not 100%
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 99]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [['a', 99]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[-1, 100]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[0, 100]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # single tp 100%
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 100]]})
    assert response.data == b'dummy_create_market_response'

    # floats
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 40.5], [2, 59.5]]})
    assert response.data == b'dummy_create_market_response'

    # ints
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 40], [2, 60]]})
    assert response.data == b'dummy_create_market_response'

    # need to sum up to 100
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 20], [2, 30]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # tp prices can't duplicate
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 50], [2, 30], [2, 20]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_stop_loss(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 'abc'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 0})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # int value
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 10})
    assert response.data == b'dummy_create_market_response'

    # float value
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 10.1})
    assert response.data == b'dummy_create_market_response'


def test_should_handle_properly_comment(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # empty comment is correct
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': ''})
    assert response.data == b'dummy_create_market_response'

    # too long comment
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': "a" * (MAXIMUM_COMMENT_LENGTH + 1)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_handle_properly_move_sl_to_be(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': 'True'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': True})
    assert response.data == b'dummy_create_market_response'

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': False})
    assert response.data == b'dummy_create_market_response'


def test_should_handle_properly_helper_url(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='dummy_create_market_response')

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # empty url is correct
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': ''})
    assert response.data == b'dummy_create_market_response'

    # too long url
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': "a" * (MAXIMUM_HELPER_URL_LENGTH + 1)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_fail_when_non_existing_account_provided(client, user1_token):
    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={**common_params, 'account_id': 10})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_fail_for_account_from_different_user(client, user1_token, user2_token):
    create_exchange_account(client, user1_token)

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user2_token},
                           json=common_params)
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_check_if_params_passed_to_wrapper(client, mocker, user1_token):
    create_exchange_account(client, user1_token)
    create_market_spy = mocker.patch.object(Bybit3CommasWrapper, 'create_market',
                                            return_value='dummy_create_market_response')

    side = 'Long'
    symbol = 'SYMBOL_NAME'
    position_size = 10
    take_profits = [[10, 30], [20, 20], [30, 50]]
    stop_loss = 5
    comment = 'my_comment'
    move_sl_to_breakeven_after_tp1 = True
    helper_url = 'this_is_helper_url'

    response = client.post("/exchange_create_market_position", headers={"x-access-tokens": user1_token},
                           json={'account_id': 1,
                                 'symbol': symbol,
                                 'position_size': position_size,
                                 'take_profits': take_profits,
                                 'stop_loss': stop_loss,
                                 'comment': comment,
                                 'move_sl_to_breakeven_after_tp1': move_sl_to_breakeven_after_tp1,
                                 'helper_url': helper_url,
                                 'side': side})
    assert response.data == b'dummy_create_market_response'
    assert create_market_spy.call_count == 1
    create_market_spy.assert_called_once_with(side=side,
                                              symbol=symbol,
                                              position_size=position_size,
                                              take_profits=take_profits,
                                              stop_loss=stop_loss,
                                              comment=comment,
                                              move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1,
                                              helper_url=helper_url)
