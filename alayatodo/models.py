# -*- coding: UTF-8 -*-
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import (
    hybrid_property,
    hybrid_method
)

from alayatodo import (
    db,
    bcrypt
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.Binary(60), nullable=False)

    def __init__(self, username, plaintext_password):
        self.username = username
        self.password = plaintext_password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255))
    done = db.Column(db.Boolean)

    def __init__(self, user_id, description,):
        self.user_id = user_id
        self.description = description


# from: https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
