import datetime
import uuid
from functools import wraps

import jwt
from flask import jsonify, make_response, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from backend.src.consts_tpl import flask_api_secret
from backend.src.database import db
from backend.src.models.users import Users

session_routes = Blueprint('session_routes', __name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, flask_api_secret, algorithms=["HS256"])
            current_user = db.session.query(Users).filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@session_routes.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    if 'username' not in data or 'password' not in data or 'email' not in data:
        return make_response(jsonify({'error': 'parameters invalid'}), 400)

    if db.session.query(Users).filter_by(username=data['username']).count() > 0:
        return make_response(jsonify({'error': 'user already exists'}), 400)

    hashed_password = generate_password_hash(data['password'])

    new_user = Users(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=False,
                     email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})


@session_routes.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = db.session.query(Users).filter_by(username=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            flask_api_secret, "HS256")

        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})
