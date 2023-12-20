import os

from flask import Blueprint, jsonify

from shared.consts_tpl import miami_version_env_key

general_routes = Blueprint('general_routes', __name__)


@general_routes.route('/version', methods=['GET'])
def get_version():
    return jsonify({'message': os.environ.get(miami_version_env_key) or ''})
