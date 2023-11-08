from flask import Flask
from flask_cors import CORS
from consts_secrets import db_username, db_password, db_name
from consts_tpl import flask_api_secret
from data_harvesters.data_harversters import run_data_harvesters
from database import db
from endpoints.account.account import account_routes
from endpoints.general.general import general_routes
from endpoints.session.session import session_routes
from endpoints.session.test_token_required import token_required_test_routes

if not db_username or not db_password or not db_name:
    print('No database creds detected')
    exit()


def register_extensions(app):
    app.register_blueprint(account_routes)
    app.register_blueprint(session_routes)
    app.register_blueprint(general_routes)
    app.register_blueprint(token_required_test_routes)


def prepare_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = flask_api_secret
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@db/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.app_context().push()

    register_extensions(app)

    return app


def create_app():
    application = prepare_app()
    db.init_app(application)
    run_data_harvesters()
    return application
