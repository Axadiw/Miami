import datetime
import uuid

import jwt
from flask import jsonify, make_response, request, Blueprint
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from consts_tpl import flask_api_secret
from database import db
from endpoints.consts import PARAMS_INVALID_RESPONSE, USER_EXISTS_RESPONSE, INCORRECT_CREDENTIALS_RESPONSE, \
    TOKEN_MISSING_RESPONSE, TOKEN_VALID_RESPONSE, TOKEN_EXPIRED_RESPONSE, TOKEN_INVALID_RESPONSE, \
    TOKEN_VALIDITY_IN_DAYS, REGISTRATION_SUCCESS_RESPONSE, EMAIL_IN_USE_RESPONSE, MINIMUM_USERNAME_LENGTH, \
    MINIMUM_PASSWORD_LENGTH, PASSWORD_CHANGED_RESPONSE
from endpoints.session.token_required import token_required
from models.users import Users
import re

session_routes = Blueprint('session_routes', __name__)


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def valid_username(email):
    return bool(re.search(r"^[a-z0-9_]*$", email))


@session_routes.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    if 'username' not in data or 'password' not in data or 'email' not in data:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    invalid_email = not valid_email(data['email'])
    invalid_username = not valid_username(data['username']) or len(data['username']) < MINIMUM_USERNAME_LENGTH
    invalid_password = len(data['password']) < MINIMUM_PASSWORD_LENGTH

    if invalid_email or invalid_username or invalid_password:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if db.session.query(Users).filter_by(username=data['username']).count() > 0:
        return make_response(jsonify(USER_EXISTS_RESPONSE), 400)

    if db.session.query(Users).filter_by(email=data['email']).count() > 0:
        return make_response(jsonify(EMAIL_IN_USE_RESPONSE), 400)

    hashed_password = generate_password_hash(data['password'])

    new_user = Users(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=False,
                     email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(REGISTRATION_SUCCESS_RESPONSE)


@session_routes.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify(INCORRECT_CREDENTIALS_RESPONSE), 400)

    user = db.session.query(Users).filter_by(username=auth.username).first()

    if user is None:
        return make_response(jsonify(INCORRECT_CREDENTIALS_RESPONSE), 400)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=TOKEN_VALIDITY_IN_DAYS)},
            flask_api_secret, "HS256")

        return jsonify({'token': token})

    return make_response(jsonify(INCORRECT_CREDENTIALS_RESPONSE), 400)


@session_routes.route('/is_valid_token', methods=['POST'])
def is_valid_token():
    data = request.get_json()
    if 'token' not in data:
        return make_response(jsonify(TOKEN_MISSING_RESPONSE), 400)
    token = data['token']

    try:
        jwt.decode(token, flask_api_secret, algorithms=["HS256"])
        return make_response(jsonify(TOKEN_VALID_RESPONSE), 200)
    except ExpiredSignatureError:
        return make_response(jsonify(TOKEN_EXPIRED_RESPONSE), 400)
    except:
        return make_response(jsonify(TOKEN_INVALID_RESPONSE), 400)


@session_routes.route('/change_password', methods=['POST'])
@token_required
def change_password(user):
    data = request.get_json()
    user = db.session.query(Users).filter_by(public_id=user.public_id).first()

    if 'old_password' not in data or 'new_password' not in data:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if not check_password_hash(user.password, data['old_password']):
        return make_response(jsonify(INCORRECT_CREDENTIALS_RESPONSE), 400)

    if len(data['new_password']) < MINIMUM_PASSWORD_LENGTH:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    user.password = generate_password_hash(data['new_password'])
    db.session.commit()

    return make_response(jsonify(PASSWORD_CHANGED_RESPONSE), 200)
