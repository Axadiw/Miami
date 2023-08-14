import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend.src.consts_secrets import db_username, db_password, db_name

if not db_username or not db_password or not db_name:
    print('No database creds detected')
    exit()

app = Flask(__name__)

app.config['SECRET_KEY'] = '1cc52f74f7f3bbbca31c1e1368230358'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@db/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

app.app_context().push()
