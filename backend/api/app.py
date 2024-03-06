import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from api.database import db
from api.endpoints.account.account import account_routes
from api.endpoints.general.general import general_routes
from api.endpoints.market_data.market import market_routes
from api.endpoints.session.session import session_routes
from api.realtime_candles.handle_ohlcv_realtime_candles import handle_ohlcv_realtime_candles
from api.tests.test_token_required import token_required_test_routes
from shared.consts_secrets import db_username, db_password, db_name, miami_version_env_key
from shared.consts_tpl import flask_api_secret

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

if not db_username or not db_password or not db_name:
    logging.critical('No database creds detected')
    exit()

is_debug = True if os.environ.get(miami_version_env_key) in ['local', None] else False


def register_extensions(app):
    app.register_blueprint(account_routes)
    app.register_blueprint(session_routes)
    app.register_blueprint(general_routes)
    app.register_blueprint(token_required_test_routes)
    app.register_blueprint(market_routes)


def prepare_app():
    app = Flask(__name__)

    CORS(app)
    app.config['SECRET_KEY'] = flask_api_secret
    app.config['MQTT_BROKER_URL'] = 'localhost' if is_debug else 'mqtt'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@db/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.app_context().push()

    register_extensions(app)

    return app


def create_app():
    app = prepare_app()
    mqtt = Mqtt(app)
    socketio_instance = SocketIO(app, cors_allowed_origins='*')
    db.init_app(app)
    mqtt.init_app(app)
    handle_ohlcv_realtime_candles(socketio_instance, mqtt)
    return app


gunicorn_app = create_app()
