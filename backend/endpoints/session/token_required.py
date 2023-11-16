from functools import wraps

import jwt
from flask import jsonify, make_response, request, Blueprint

from consts_tpl import flask_api_secret
from database import db
from endpoints.consts import TOKEN_MISSING_RESPONSE, TOKEN_INVALID_RESPONSE
from models.user import User


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
            current_user = db.session.query(User).filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify(TOKEN_INVALID_RESPONSE), 400)

        return f(current_user, *args, **kwargs)

    return decorator
