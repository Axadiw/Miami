import datetime
import uuid
from functools import wraps

import jwt
from flask import jsonify, make_response, request, Blueprint
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from consts_tpl import flask_api_secret
from database import db
from models.users import Users

session_routes = Blueprint('session_routes', __name__)

# success
REGISTRATION_SUCCESS_RESPONSE = dict(message='Registered successfully')
TOKEN_VALID_RESPONSE = dict(message='Token valid')

# error
PARAMS_INVALID_RESPONSE = dict(error='Parameters invalid')
USER_EXISTS_RESPONSE = dict(error='User already exists')
INCORRECT_CREDENTIALS_RESPONSE = dict(error='Incorrect credentials')
TOKEN_MISSING_RESPONSE = dict(error='A valid token is missing')
TOKEN_INVALID_RESPONSE = dict(error='Invalid token')
TOKEN_EXPIRED_RESPONSE = dict(error='Expired token')

TOKEN_VALIDITY_IN_DAYS = 30


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response(jsonify(TOKEN_MISSING_RESPONSE), 400)
        try:
            data = jwt.decode(token, flask_api_secret, algorithms=["HS256"])
            current_user = db.session.query(Users).filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify(TOKEN_INVALID_RESPONSE), 400)

        return f(current_user, *args, **kwargs)

    return decorator


@session_routes.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    if 'username' not in data or 'password' not in data or 'email' not in data:
        return make_response(jsonify(PARAMS_INVALID_RESPONSE), 400)

    if db.session.query(Users).filter_by(username=data['username']).count() > 0:
        return make_response(jsonify(USER_EXISTS_RESPONSE), 400)

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
