import base64
import json

from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
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
