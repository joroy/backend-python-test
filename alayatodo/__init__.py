import logging
import sys
import subprocess
import os

from flask import (
    Flask,
    session,
    request,
    redirect,
    url_for
)

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


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


def add_default_users():
    from alayatodo.models import User
    for user, password in [('user{}'.format(i),
                            'user{}'.format(i)) for i in range(1, 4)]:
        new_user = User(user, password)
        db.session.add(new_user)
    db.session.commit()


def init_db():
    print("AlayaTodo: Initializing database")
    _run_sql('resources/database.sql')
    _run_sql('resources/fixtures.sql')
    add_default_users()
    print("AlayaTodo: Database initialized.")


def run_migrations():
    print("AlayaTodo: Running migrations")
    _run_sql('resources/1to2.sql')


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    if 'logged_in' not in session and request.endpoint not in ['login', 'login_POST']:
        return redirect(url_for('login'))


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stdout.
        app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        app.logger.setLevel(logging.INFO)


import alayatodo.views  # noqa