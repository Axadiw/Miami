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


def register_extensions(app_to_register):
    app_to_register.register_blueprint(account_routes)
    app_to_register.register_blueprint(session_routes)
    app_to_register.register_blueprint(general_routes)
    app_to_register.register_blueprint(token_required_test_routes)
    app_to_register.register_blueprint(market_routes)


def prepare_app():
    prepared_app = Flask(__name__)

    CORS(prepared_app)
    prepared_app.config['SECRET_KEY'] = flask_api_secret
    prepared_app.config['MQTT_BROKER_URL'] = 'mqtt'
    prepared_app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@db/{db_name}'
    prepared_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    prepared_app.app_context().push()

    register_extensions(prepared_app)

    return prepared_app


def create_app():
    prepared_app = prepare_app()
    mqtt = Mqtt(prepared_app)
    socketio_instance = SocketIO(prepared_app, cors_allowed_origins='*')
    db.init_app(prepared_app)
    mqtt.init_app(prepared_app)
    handle_ohlcv_realtime_candles(socketio_instance, mqtt)
    return prepared_app


def gunicorn_create(wsgi, response):
    create_app()
