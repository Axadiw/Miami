from flask import Flask

from backend.src.consts_secrets import db_username, db_password, db_name
from backend.src.consts_tpl import flask_api_secret
from backend.src.database import db
from backend.src.endpoints.account import account_routes
from backend.src.endpoints.session import session_routes

if not db_username or not db_password or not db_name:
    print('No database creds detected')
    exit()


def register_extensions(app):
    db.init_app(app)
    app.register_blueprint(account_routes)
    app.register_blueprint(session_routes)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = flask_api_secret
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@db/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.app_context().push()

    register_extensions(app)

    return app


application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
