from endpoints.account.account import ALLOWED_USER_CONFIG_KEYS
from endpoints.consts import USER_CONFIG_SAVED_RESPONSE
from endpoints.session.test_session import get_test_user_token


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
