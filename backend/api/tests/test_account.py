from api.database import db
from api.endpoints.account.account import ALLOWED_USER_CONFIG_KEYS
from api.endpoints.consts import USER_CONFIG_SAVED_RESPONSE, DEFAULT_ADMIN_EMAIL
from api.tests.test_session import get_test_user_token
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
