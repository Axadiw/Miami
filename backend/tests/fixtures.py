import os

import pytest
from alembic.command import upgrade
from alembic.config import Config

from app import prepare_app
from database import db


@pytest.fixture
def app():
    app = prepare_app()
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
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
        alembic_cfg = Config(os.path.join(src_path, "../alembic.ini"))
        alembic_cfg.set_main_option('script_location', os.path.join(src_path, "../migrations"))
        alembic_cfg.set_main_option('sqlalchemy.url', in_memory_db_url)
        upgrade(alembic_cfg, revision='head')
    return app
