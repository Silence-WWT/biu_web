# -*- coding: utf-8 -*-
import time
from random import randint, seed

from flask.ext.login import UserMixin
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash, enbase64

from app import db
from config import Config

seed()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(15), nullable=False)
    nickname = db.Column(db.Unicode(10), nullable=False)
    password_hash = db.Column('password', db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created = db.Column(db.Integer, default=time.time(), nullable=False)
    mobile = db.Column(db.CHAR(11), nullable=False)
    identity = db.Column(db.String(64), nullable=False)
    golds = db.Column(db.Integer, default=0, nullable=False)
    avatar = db.Column(db.String(128), default='', nullable=False)
    signature = db.Column(db.Unicode(30), default=u'', nullable=False)
    push = db.Column(db.Boolean, default=True, nullable=False)
    disturb = db.Column(db.Boolean, default=True, nullable=False)

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
        self.salt = generate_random_salt()
        self.password_hash = generate_password_hash(password, self.salt)

    def verify_password(self, password):
        return check_password_hash(password, self.password_hash, self.salt)

    def update_identity(self, identity):
        if identity and identity != self.identity:
            self.identity = identity

    def get_user_info_dict(self):
        user_dict = {
            'user_id': self.id,
            'username': self.username,
            'mobile': self.mobile,
            'identity': self.identity,
            'golds': self.golds,
            'avatar': Config.STATIC_URL + self.avatar,
            'signature': self.signature,
            'push': self.push,
            'no_disturb': self.no_disturb
        }
        return user_dict


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
    content = db.Column(db.Unicode(140), nullable=False)
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
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    content = db.Column(db.Unicode(30), nullable=False)
    created = db.Column(db.Integer, default=time.time(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)


class PostCommentLike(db.Model):
    __tablename__ = 'post_comment_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)


class PostCommentReport(db.Model):
    __tablename__ = 'post_comment_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Unicode(30), nullable=False)