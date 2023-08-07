import os
from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
from get_docker_secret import get_docker_secret


db_username = get_docker_secret('MIAMI_POSTGRES_USER') or os.getenv('MIAMI_POSTGRES_USER')
db_password = get_docker_secret('MIAMI_POSTGRES_PASSWORD') or os.getenv('MIAMI_POSTGRES_PASSWORD')
db_name = get_docker_secret('MIAMI_POSTGRES_DB') or os.getenv('MIAMI_POSTGRES_DB')

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
