import base64

from endpoints.session import PARAMS_INVALID_RESPONSE, SUCCESS_RESPONSE, USER_EXISTS_RESPONSE, \
    INCORRECT_CREDENTIALS_RESPONSE


def test_simple_registration(client):
    response = client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
    assert response.json == SUCCESS_RESPONSE


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
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
    response = client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
    assert response.status_code == 400
    assert response.json == USER_EXISTS_RESPONSE


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
    client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})

    user_credentials = base64.b64encode(b"user1:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 200
    assert 'token' in response.json
    assert len(response.json['token']) > 0

