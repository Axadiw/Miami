from flask import jsonify, request, Blueprint

from api.database import db
from api.endpoints.consts import USER_CONFIG_SAVED_RESPONSE, DEFAULT_ADMIN_EMAIL, EXCHANGE_ACCOUNT_ADDED, \
    EXCHANGE_ACCOUNT_REMOVED
from api.endpoints.session.token_required import token_required
from shared.models.exchange_account import ExchangeAccount
from shared.models.user_configs import UserConfig
from shared.models.user import User

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
    is_admin = user.admin or user.email == DEFAULT_ADMIN_EMAIL
    return jsonify({'email': user.email, 'is_admin': is_admin, 'config_keys': configs})


@account_routes.route('/add_new_exchange_account', methods=['POST'])
@token_required
def add_new_exchange_account(user):
    data = request.get_json()
    db.session.add(ExchangeAccount(type=data['type'], name=data['name'], details=data['details'], user_id=user.id))
    db.session.commit()
    return jsonify(EXCHANGE_ACCOUNT_ADDED)


@account_routes.route('/remove_exchange_account', methods=['POST'])
@token_required
def remove_exchange_account(user):
    data = request.get_json()
    account_to_delete = db.session.query(ExchangeAccount).filter_by(id=data['id']).one()
    db.session.delete(account_to_delete)
    db.session.commit()
    return jsonify(EXCHANGE_ACCOUNT_REMOVED)


@account_routes.route('/list_exchange_accounts', methods=['GET'])
@token_required
def list_exchange_account(user):
    accounts = db.session.query(ExchangeAccount).filter_by(user_id=user.id).all()
    return jsonify({'accounts': list(map(lambda x: {'id': x.id, 'name': x.name, 'type': x.type}, accounts))})
