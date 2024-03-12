import base64
import json

from api.database import db
from api.endpoints.account.account import ALLOWED_USER_CONFIG_KEYS
from api.endpoints.consts import USER_CONFIG_SAVED_RESPONSE, DEFAULT_ADMIN_EMAIL, EXCHANGE_ACCOUNT_ADDED, \
    EXCHANGE_ACCOUNT_REMOVED, PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.test_session import get_test_user_token
from shared.models.exchange_account import ExchangeAccount
from shared.models.user import User


def test_should_return_email_in_account_info(client):
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert 'email' in response.json
    assert response.json['email'] == 'email1@gmail.com'


def test_save_and_get_proper_values(client):
    client.post("/save_config", headers={"x-access-tokens": get_test_user_token(client)},
                json={ALLOWED_USER_CONFIG_KEYS[0]: 'val1', ALLOWED_USER_CONFIG_KEYS[1]: 'val2'})
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert 'config_keys' in response.json
    assert response.json['email'] == 'email1@gmail.com'

    key1_value = None
    key2_value = None
    for item in response.json['config_keys']:
        if item['key'] == ALLOWED_USER_CONFIG_KEYS[0]:
            key1_value = item['value']
        if item['key'] == ALLOWED_USER_CONFIG_KEYS[1]:
            key2_value = item['value']
    assert key1_value is not None
    assert key2_value is not None


def test_save_values_returns_correct_value(client):
    response = client.post("/save_config", headers={"x-access-tokens": get_test_user_token(client)},
                           json={ALLOWED_USER_CONFIG_KEYS[0]: 'val1', ALLOWED_USER_CONFIG_KEYS[1]: 'val2'})
    assert response.status_code == 200
    assert response.json == USER_CONFIG_SAVED_RESPONSE


def test_save_unsupported_value(client):
    unsupported = 'unsupported'
    client.post("/save_config", headers={"x-access-tokens": get_test_user_token(client)},
                json={ALLOWED_USER_CONFIG_KEYS[0]: 'val1', unsupported: 'val2'})
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert 'config_keys' in response.json

    key1_value = None
    for item in response.json['config_keys']:
        if item['key'] == unsupported:
            key1_value = item['value']
    assert key1_value is None


def test_check_if_default_email_is_an_admin(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'axadiw@gmail.com'})
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert response.json['is_admin'] is True


def test_check_if_non_default_email_is_an_admin(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'anyemail@yahoo.com'})
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert response.json['is_admin'] is False


def test_check_if_non_default_email_marked_as_admin_is_an_admin(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'anyemail@yahoo.com'})
    user = db.session.query(User).filter_by(username='user1').first()
    user.admin = True
    response = client.get('/account_info', headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert response.json['is_admin'] is True


def test_adding_new_exchange_account_should_be_visible_in_db(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    user2_token = response.json['token']

    test_account_name = 'account 1'
    test_account2_name = 'account 2'
    test_account_type = 'bybit_3commas'
    test_account_details = json.dumps({'accountId': '123', 'apiKey': 'abcd', 'apiSecret': 'def'})
    test_account2_details = json.dumps({'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'defg'})

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': test_account_type,
                                 'name': test_account_name,
                                 'details': test_account_details})
    response2 = client.post('/add_new_exchange_account', headers={"x-access-tokens": user2_token},
                            json={'type': 'bybit_3commas',
                                  'name': test_account2_name,
                                  'details': test_account2_details})

    user1 = db.session.query(User).filter_by(username='user1').first()
    user_other = db.session.query(User).filter_by(username='other_user').first()
    user_1_accounts = db.session.query(ExchangeAccount).filter_by(user_id=user1.id).all()
    other_user_accounts = db.session.query(ExchangeAccount).filter_by(user_id=user_other.id).all()
    assert response.status_code == 200
    assert response2.status_code == 200
    assert len(user_1_accounts) == 1
    assert len(other_user_accounts) == 1
    assert user_1_accounts[0].name == test_account_name
    assert user_1_accounts[0].type == test_account_type
    assert user_1_accounts[0].details == test_account_details
    assert other_user_accounts[0].name == test_account2_name
    assert other_user_accounts[0].type == test_account_type
    assert other_user_accounts[0].details == test_account2_details


def test_added_exchange_account_should_have_all_necessary_fields(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'name': 'name', 'details': json.dumps(
                               {'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'secret'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'details': json.dumps(
                               {'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'secret'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'name': 'name', 'type': Bybit3CommasWrapper.get_name()})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_added_exchange_account_should_not_allow_creating_exchange_of_unsupported_type(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': 'unknown', 'name': 'name', 'details': json.dumps(
                               {'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'secret'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_added_exchange_account_3commas_bybit_should_have_necessary_details_fields(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': json.dumps(
                               {'apiKey': 'abcde', 'apiSecret': 'secret'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': json.dumps(
                               {'accountId': '1234', 'apiSecret': 'secret'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': json.dumps(
                               {'accountId': '1234', 'apiKey': 'abcde'})})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': ''})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': 'abcd'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                           json={'type': Bybit3CommasWrapper.get_name(), 'name': 'name', 'details': json.dumps(
                               {'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'secret'})})
    assert response.status_code == 200
    assert response.json == EXCHANGE_ACCOUNT_ADDED


def test_list_exchange_account_should_return_accounts_for_correct_users(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    user2_token = response.json['token']

    test_account_name = 'account 1'
    test_account2_name = 'account 2'
    test_account_type = 'bybit_3commas'
    test_account_details = json.dumps({'accountId': '1234', 'apiKey': 'abcde', 'apiSecret': 'secret'})
    test_account2_details = json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'})

    add_response_1 = client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                                 json={'type': test_account_type,
                                       'name': test_account_name,
                                       'details': test_account_details})
    add_response_2 = client.post('/add_new_exchange_account', headers={"x-access-tokens": user2_token},
                                 json={'type': 'bybit_3commas',
                                       'name': test_account2_name,
                                       'details': test_account2_details})
    assert add_response_1.status_code == 200
    assert add_response_2.status_code == 200
    assert add_response_1.json == EXCHANGE_ACCOUNT_ADDED
    assert add_response_2.json == EXCHANGE_ACCOUNT_ADDED

    response = client.get('/list_exchange_accounts', headers={"x-access-tokens": get_test_user_token(client)})
    response2 = client.get('/list_exchange_accounts', headers={"x-access-tokens": user2_token})
    assert response.status_code == 200
    assert response2.status_code == 200

    assert len(response.json['accounts']) == 1
    assert response.json['accounts'][0]['id'] == 1
    assert response.json['accounts'][0]['name'] == test_account_name
    assert response.json['accounts'][0]['type'] == test_account_type
    assert ('details' not in response.json['accounts'][0]) is True

    assert len(response2.json['accounts']) == 1
    assert response2.json['accounts'][0]['id'] == 2
    assert response2.json['accounts'][0]['name'] == test_account2_name
    assert response2.json['accounts'][0]['type'] == test_account_type
    assert ('details' not in response2.json['accounts'][0]) is True


def test_removing_exchange_account_should_work(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    user2_token = response.json['token']

    test_account_name = 'account 1'
    test_account2_name = 'account 2'
    test_account_type = 'bybit_3commas'
    test_account_details = json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'})
    test_account2_details = json.dumps({'accountId': '123456', 'apiKey': 'abcdefg', 'apiSecret': 'secret3'})

    client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                json={'type': test_account_type,
                      'name': test_account_name,
                      'details': test_account_details})
    client.post('/add_new_exchange_account', headers={"x-access-tokens": user2_token},
                json={'type': 'bybit_3commas',
                      'name': test_account2_name,
                      'details': test_account2_details})

    delete_response = client.post('/remove_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                                  json={'id': 1})
    assert delete_response.status_code == 200
    assert delete_response.json == EXCHANGE_ACCOUNT_REMOVED

    response = client.get('/list_exchange_accounts', headers={"x-access-tokens": get_test_user_token(client)})
    response2 = client.get('/list_exchange_accounts', headers={"x-access-tokens": user2_token})
    assert response.status_code == 200
    assert response2.status_code == 200
    assert len(response.json['accounts']) == 0

    assert len(response2.json['accounts']) == 1
    assert response2.json['accounts'][0]['id'] == 2
    assert response2.json['accounts'][0]['name'] == test_account2_name
    assert response2.json['accounts'][0]['type'] == test_account_type
    assert ('details' not in response2.json['accounts'][0]) is True


def test_removing_exchange_account_without_id_should_fail(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})

    delete_response = client.post('/remove_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                                  json={})
    assert delete_response.status_code == 400
    assert delete_response.json == PARAMS_INVALID_RESPONSE


def test_removing_exchange_account_from_different_user_should_fail(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    user2_token = response.json['token']

    test_account_name = 'account 1'
    test_account2_name = 'account 2'
    test_account_type = 'bybit_3commas'
    test_account_details = json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'})
    test_account2_details = json.dumps({'accountId': '123456', 'apiKey': 'abcdefg', 'apiSecret': 'secret3'})

    client.post('/add_new_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                json={'type': test_account_type,
                      'name': test_account_name,
                      'details': test_account_details})
    client.post('/add_new_exchange_account', headers={"x-access-tokens": user2_token},
                json={'type': 'bybit_3commas',
                      'name': test_account2_name,
                      'details': test_account2_details})

    delete_response = client.post('/remove_exchange_account', headers={"x-access-tokens": get_test_user_token(client)},
                                  json={'id': 2})
    assert delete_response.status_code == 400
    assert delete_response.json == PARAMS_INVALID_RESPONSE
