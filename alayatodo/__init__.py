import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import sqlite3

# configuration
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{db}'.format(db=DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
PER_PAGE = 3  # small to see pagination with default fixture
BCRYPT_LOG_ROUNDS = 12

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stdout.
        app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        app.logger.setLevel(logging.INFO)


import alayatodo.views