import base64
import json
from unittest import mock
from unittest.mock import patch

from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.test_session import get_test_user_token


def test_get_balance_should_fail_for_non_existing_account(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'axadiw@gmail.com'})
    response = client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_get_balance_should_fail_when_account_not_provided(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'axadiw@gmail.com'})
    response = client.get('/exchange_get_balance', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_get_balance_should_fail_for_different_user_account(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    user2_token = response.json['token']

    test_account_name = 'account 1'
    test_account_type = 'bybit_3commas'
    test_account_details = json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'})

    client.post('/add_new_exchange_account', headers={"x-access-tokens": user2_token},
                json={'type': test_account_type,
                      'name': test_account_name,
                      'details': test_account_details})

    response = client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_good_get_balance(client, mocker):
    get_balance_spy = mocker.patch.object(Bybit3CommasWrapper, 'get_balance')
    user_token = get_test_user_token(client)

    client.post('/add_new_exchange_account', headers={"x-access-tokens": user_token},
                json={'type': 'bybit_3commas',
                      'name': 'account 1',
                      'details': (json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))})
    client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": user_token})
    assert get_balance_spy.call_count == 1


def test_create_market_fail_if_not_all_required_params_provided(client):
    pass


def test_create_market_not_fail_if_havent_provided_helper_url(client):
    pass


def test_create_market_fail_for_account_from_different_user(client):
    pass


def test_create_market_check_if_params_passed(client, mocker):
    user_token = get_test_user_token(client)

    client.post('/add_new_exchange_account', headers={"x-access-tokens": user_token},
                json={'type': 'bybit_3commas',
                      'name': 'account 1',
                      'details': (json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))})
    create_market_spy = mocker.patch.object(Bybit3CommasWrapper, 'create_market', return_value='')
    side = 'long'
    symbol = 'SYMBOL_NAME'
    position_size = 10
    take_profits = [[10, 30], [20, 20], [30, 50]]
    stop_loss = 5
    comment = 'my_comment'
    move_sl_to_breakeven_after_tp1 = True
    helper_url = 'this_is_helper_url'

    client.post("/exchange_create_market_position", headers={"x-access-tokens": user_token},
                json={'account_id': 1,
                      'symbol': symbol,
                      'position_size': position_size,
                      'take_profits': take_profits,
                      'stop_loss': stop_loss,
                      'comment': comment,
                      'move_sl_to_breakeven_after_tp1': move_sl_to_breakeven_after_tp1,
                      'helper_url': helper_url,
                      'side': side})
    assert create_market_spy.call_count == 1
    create_market_spy.assert_called_once_with(side=side,
                                              symbol=symbol,
                                              position_size=position_size,
                                              take_profits=take_profits,
                                              stop_loss=stop_loss,
                                              comment=comment,
                                              move_sl_to_breakeven_after_tp1=move_sl_to_breakeven_after_tp1,
                                              helper_url=helper_url)
