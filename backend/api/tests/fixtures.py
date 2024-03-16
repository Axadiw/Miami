import base64
import os

import pytest
from alembic.command import upgrade
from alembic.config import Config

from api.app import prepare_app
from api.database import db
from api.tests.test_session import get_test_user_token


@pytest.fixture
def app():
    app = prepare_app()
    src_path = os.path.join(os.path.dirname(__file__), '../..')
    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 0
    db_file = os.path.join(os.path.dirname(__file__), "../test.db")
    if os.path.exists(db_file):
        os.unlink(db_file)
    in_memory_db_url = "sqlite:///" + db_file
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = in_memory_db_url
    db.init_app(app)
    db.drop_all()
    with app.app_context():
        alembic_cfg = Config(os.path.join(src_path, 'shared', "alembic.ini"))
        alembic_cfg.set_main_option('script_location', os.path.join(src_path, 'shared', "migrations"))
        alembic_cfg.set_main_option('sqlalchemy.url', in_memory_db_url)
        upgrade(alembic_cfg, revision='head')
    return app


@pytest.fixture
def user1_token(client):
    return get_test_user_token(client)


@pytest.fixture
def user2_token(client):
    client.post("/register", json={"username": "other_user", 'password': 'pass1', 'email': 'email2@gmail.com'})
    user_credentials = base64.b64encode(b"other_user:pass1").decode()
    response = client.post("/login", headers={"Authorization": "Basic {}".format(user_credentials)})
    return response.json['token']
