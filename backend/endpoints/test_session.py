PARAMS_INVALID_RESPONSE = dict(error='parameters invalid')
SUCCESS_RESPONSE = dict(message='registered successfully')
USER_EXISTS_RESPONSE = dict(error='user already exists')


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
