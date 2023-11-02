import base64
import datetime

from endpoints.consts import EMAIL_IN_USE_RESPONSE
from endpoints.session.session import PARAMS_INVALID_RESPONSE, REGISTRATION_SUCCESS_RESPONSE, USER_EXISTS_RESPONSE, \
    INCORRECT_CREDENTIALS_RESPONSE, TOKEN_VALIDITY_IN_DAYS, TOKEN_VALID_RESPONSE, TOKEN_INVALID_RESPONSE, \
    TOKEN_EXPIRED_RESPONSE
from freezegun import freeze_time


# REGISTER
def get_test_user_token(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1@gmail.com'})
    user_credentials = base64.b64encode(b"user1:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    return response.json['token']


def test_simple_registration(client):
    response = client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1@gmail.com'})
    assert response.json == REGISTRATION_SUCCESS_RESPONSE

    response = client.post("/register", json={"username": "user2", 'password': 'Apass1', 'email': 'email2@gmail.com'})
    assert response.json == REGISTRATION_SUCCESS_RESPONSE


def test_register_without_email(client):
    response = client.post("/register", json={"username": "user1", 'password': 'pass1'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_register_without_password(client):
    response = client.post("/register", json={"username": "user1", 'email': 'email1'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_register_without_username(client):
    response = client.post("/register", json={'email': 'email1', 'password': 'pass1'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_dont_allow_duplicate_registrations(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1@gmail.com'})
    response = client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1@gmail.com'})
    assert response.status_code == 400
    assert response.json == USER_EXISTS_RESPONSE


def test_show_duplicated_email_during_registration(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email@gmail.com'})
    response = client.post("/register", json={"username": "user2", 'password': 'pass1', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == EMAIL_IN_USE_RESPONSE


def test_incorrect_email(client):
    response = client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'not_an_email'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_too_short_username(client):
    response = client.post("/register", json={"username": "aa", 'password': 'pass1', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_zero_length_params(client):
    response = client.post("/register", json={"username": "", 'password': 'pass1', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/register", json={"username": "aaaaa", 'password': '', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/register", json={"username": "bbbbb", 'password': 'pass1', 'email': ''})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def test_incorrect_chars_in_params(client):
    response = client.post("/register",
                           json={"username": "akjasd asd", 'password': 'pass1', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/register", json={"username": "sad@as", 'password': '', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post("/register", json={"username": "aaa#$@aaa", 'password': 'pass1', 'email': 'email@gmail.com'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


# LOGIN
def test_show_incorrect_credentials_when_unknown_user_selected_during_login(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})

    user_credentials = base64.b64encode(b"non_existing_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 400
    assert response.json == INCORRECT_CREDENTIALS_RESPONSE


def test_show_incorrect_credentials_when_incorrect_password_selected(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})

    user_credentials = base64.b64encode(b"user1:nonpass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 400
    assert response.json == INCORRECT_CREDENTIALS_RESPONSE


def test_inform_when_auth_data_not_present(client):
    response = client.post("/login")
    assert response.status_code == 400
    assert response.json == INCORRECT_CREDENTIALS_RESPONSE


def test_inform_when_auth_username_not_present(client):
    user_credentials = base64.b64encode(b":pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 400
    assert response.json == INCORRECT_CREDENTIALS_RESPONSE


def test_inform_when_auth_password_not_present(client):
    user_credentials = base64.b64encode(b"user:").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 400
    assert response.json == INCORRECT_CREDENTIALS_RESPONSE


def test_show_token_when_correct_credentials_passed(client):
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1@gmail.com'})

    user_credentials = base64.b64encode(b"user1:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 200
    assert 'token' in response.json
    assert len(response.json['token']) > 0


# is_valid_token
def test_valid_token_should_be_marked_as_valid(client):
    initial_datetime = datetime.datetime(year=2000, month=1, day=1)
    with freeze_time(initial_datetime):
        token = get_test_user_token(client)

    with freeze_time(initial_datetime + datetime.timedelta(days=TOKEN_VALIDITY_IN_DAYS / 2)):
        response = client.post("/is_valid_token", json={"token": token})
        assert response.status_code == 200
        assert response.json == TOKEN_VALID_RESPONSE


def test_invalid_token_should_be_marked_as_invalid(client):
    token = get_test_user_token(client)
    response = client.post("/is_valid_token", json={"token": token + 'abcd'})
    assert response.status_code == 400
    assert response.json == TOKEN_INVALID_RESPONSE


def test_missing_token_should(client):
    response = client.post("/is_valid_token")
    assert response.status_code == 415


def test_expired_token_should_be_marked_as_invalid(client):
    initial_datetime = datetime.datetime(year=2000, month=1, day=1)
    with freeze_time(initial_datetime):
        token = get_test_user_token(client)

    with freeze_time(initial_datetime + datetime.timedelta(days=TOKEN_VALIDITY_IN_DAYS + 1)):
        response = client.post("/is_valid_token", json={"token": token})
        assert response.status_code == 400
        assert response.json == TOKEN_EXPIRED_RESPONSE
