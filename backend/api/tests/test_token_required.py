import datetime

from flask import Blueprint
from flask import make_response
from freezegun import freeze_time

from api.endpoints.consts import TOKEN_INVALID_RESPONSE, TOKEN_MISSING_RESPONSE, TOKEN_VALIDITY_IN_DAYS
from api.tests.test_session import get_test_user_token
from api.endpoints.session.token_required import token_required

token_required_test_routes = Blueprint('token_required_test_routes', __name__)


@token_required_test_routes.route('/test_token_required', methods=['GET'])
@token_required
def dummy_token_required(client):
    return make_response('ok', 200)


def test_passing_valid_token(client):
    response = client.get("/test_token_required", headers={"x-access-tokens": get_test_user_token(client)})
    assert response.status_code == 200
    assert response.data == b'ok'


def test_passing_invalid_token(client):
    response = client.get("/test_token_required", headers={"x-access-tokens": 'aa'})
    assert response.status_code == 400
    assert response.json == TOKEN_INVALID_RESPONSE


def test_passing_expired_token(client):
    initial_datetime = datetime.datetime(year=2000, month=1, day=1)
    with freeze_time(initial_datetime):
        token = get_test_user_token(client)

    with freeze_time(initial_datetime + datetime.timedelta(days=TOKEN_VALIDITY_IN_DAYS / 2)):
        response = client.get("/test_token_required", headers={"x-access-tokens": token})
        assert response.status_code == 200
        assert response.data == b'ok'

    with freeze_time(initial_datetime + datetime.timedelta(days=TOKEN_VALIDITY_IN_DAYS + 1)):
        response = client.get("/test_token_required", headers={"x-access-tokens": token})
        assert response.status_code == 400
        assert response.json == TOKEN_INVALID_RESPONSE


def test_missing_token(client):
    response = client.get("/test_token_required", headers={"x-access-tokens": ''})
    assert response.status_code == 400
    assert response.json == TOKEN_MISSING_RESPONSE

    response = client.get("/test_token_required")
    assert response.status_code == 400
    assert response.json == TOKEN_MISSING_RESPONSE
