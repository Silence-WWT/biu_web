# -*- coding: utf-8 -*-
import time
from random import randint, seed
from hashlib import md5

from flask.ext.login import UserMixin

from .import db

seed()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(15), nullable=False)
    nickname = db.Column(db.Unicode(10), nullable=False)
    email = db.Column(db.String(64), default='', nullable=False)
    password_hash = db.Column('password', db.String(32), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    created = db.Column(db.Integer, nullable=False)
    mobile = db.Column(db.CHAR(11), nullable=False)
    identity = db.Column(db.String(64), nullable=False)
    money = db.Column(db.Integer, default=0, nullable=False)
    avatar = db.Column(db.String(128), default='', nullable=False)
    signature = db.Column(db.Unicode(30), default=u'', nullable=False)

    @staticmethod
    def get_random_id():
        while 1:
            random_id = randint(10000000, 99999999)
            if not User.query.get(random_id):
                return random_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = md5(password + self.salt).hexdigest()


class Fan(db.Model):
    __tablename__ = 'fans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    idol_id = db.Column(db.Integer, nullable=False)


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, default=time.time(), nullable=False)
    image = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Unicode(140), nullable=False)
    channel_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=True)


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)


class PostReport(db.Model):
    __tablename__ = 'post_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)


class PostComment(db.Model):
    __tablename__ = 'post_comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Unicode(128), nullable=False)
    created = db.Column(db.Integer, default=time.time(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    