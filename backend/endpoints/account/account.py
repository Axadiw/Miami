from flask import jsonify, request, Blueprint

from database import db
from endpoints.consts import USER_CONFIG_SAVED_RESPONSE
from endpoints.session.token_required import token_required
from models.user_configs import UserConfig
from models.user import User

ALLOWED_USER_CONFIG_KEYS = ['3commas_account', '3commas_api_key', '3commas_secret', 'bybit_api_key', 'bybit_api_secret']

account_routes = Blueprint('account_routes', __name__)


@account_routes.route('/save_config', methods=['POST'])
@token_required
def save_config(user):
    data = request.get_json()

    for key in data.keys():
        if key in ALLOWED_USER_CONFIG_KEYS:
            current_value = db.session.query(UserConfig).filter_by(user_id=user.id, key=key).first()
            if current_value:
                current_value.value = data[key]
            else:
                db.session.add(UserConfig(user_id=user.id, key=key, value=data[key]))
        db.session.commit()

    return jsonify(USER_CONFIG_SAVED_RESPONSE)


@account_routes.route('/account_info', methods=['GET'])
@token_required
def account_info(user):
    user = db.session.query(User).filter_by(public_id=user.public_id).first()
    configs = db.session.query(UserConfig).filter_by(user_id=user.id).all()

    def convert_to_json(config):
        return {'key': config.key, 'value': config.value}

    configs = list(map(convert_to_json, configs))
    return jsonify({'email': user.email, 'config_keys': configs})
