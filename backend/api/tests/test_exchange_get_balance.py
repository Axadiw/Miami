import json

from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.exchange_shared_test_helpers import create_exchange_account
from api.tests.test_session import get_test_user_token


def test_should_fail_for_non_existing_account(client, user1_token):
    response = client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": user1_token})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_fail_when_account_not_provided(client, user1_token):
    response = client.get('/exchange_get_balance', headers={"x-access-tokens": user1_token})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_should_fail_for_different_user_account(client, user2_token):
    create_exchange_account(client, user2_token)

    response = client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_good_get_balance(client, mocker, user1_token):
    get_balance_spy = mocker.patch.object(Bybit3CommasWrapper, 'get_balance', return_value='dummy-value')
    create_exchange_account(client, user1_token)

    response = client.get('/exchange_get_balance?account=1', headers={"x-access-tokens": user1_token})
    assert response.data == b'dummy-value'
    assert get_balance_spy.call_count == 1
