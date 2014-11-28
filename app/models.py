# -*- coding: utf-8 -*-
from random import randint, seed

from flask import current_app
from flask.ext.login import UserMixin
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash

from app import db
from utils.time_now import time_now

seed()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Unicode(10), nullable=False)
    password_hash = db.Column('password', db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
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
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'mobile': self.mobile,
            'identity': self.identity,
            'golds': self.golds,
            'avatar': current_app.config['STATIC_URL'] + self.avatar,
            'signature': self.signature,
            'push': self.push,
            'disturb': self.disturb
        }

    def get_brief_info_dict(self):
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'avatar': current_app.config['STATIC_URL'] + self.avatar,
        }

    def add_golds(self, parameter, method='add', reword=0):
        if parameter == 'post':
            golds = current_app.config['GOLDS_POST']
        elif parameter == 'comment':
            golds = current_app.config['GOLDS_COMMENT']
        elif parameter == 'like':
            golds = current_app.config['GOLDS_LIKE']
        elif parameter == 'reword':
            golds = reword
        else:
            return False
        if method == 'minus' and not reword:
            golds = -golds
        if golds >= 0 or self.golds >= -golds:
            self.golds += golds
            return True
        else:
            return False

    def get_fans(self, following, page, per_page):
        if following:
            return Fan.query.filter_by(user_id=self.id, is_deleted=False).order_by(-Fan.created). \
                paginate(page, per_page, False).items
        else:
            return Fan.query.filter_by(idol_id=self.id, is_deleted=False).order_by(-Fan.created). \
                paginate(page, per_page, False).items


class Fan(db.Model):
    __tablename__ = 'fans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    idol_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_user_or_idol(self, following):
        if following:
            return User.query.get(self.idol_id)
        else:
            return User.query.get(self.user_id)


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    image = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Unicode(140), nullable=False)
    channel_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=True)

    def get_user(self):
        return User.query.get(self.user_id)

    def get_post(self):
        return self

    def report_delete(self):
        reports_count = PostReport.query.filter_by(post_id=self.id).count()
        if self.is_deleted:
            return False
        elif not self.is_deleted and reports_count >= 10:
            self.is_deleted = True
        return self.is_deleted

    def get_post_info_dict(self):
        return {
            'user': self.get_user().get_brief_info_dict(),
            'post_id': self.id,
            'content': self.content,
            'created': self.created,
            'channel_id': self.channel_id,
            'image': current_app.config['STATIC_URL'] + self.image
        }


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    @staticmethod
    def is_liked(post_id, user_id):
        return PostLike.query.filter_by(post_id=post_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class PostReport(db.Model):
    __tablename__ = 'post_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    @staticmethod
    def is_reported(post_id, user_id):
        return PostReport.query.filter_by(post_id=post_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class PostComment(db.Model):
    __tablename__ = 'post_comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    content = db.Column(db.Unicode(30), nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_comment_info(self):
        comment_dict = {
            'post_id': self.post_id,
            'created': self.created,
            'content': self.content,
            'x': self.x,
            'y': self.y,
            'user': User.query.get(self.user_id).get_brief_info_dict()
        }
        return comment_dict

    def get_post(self):
        return Post.query.get(self.post_id)

    def report_delete(self):
        reports_count = PostCommentReport.query.filter_by(post_comment_id=self.id).count()
        if self.is_deleted:
            return False
        elif not self.is_deleted and reports_count >= 10:
            self.is_deleted = True
        return self.is_deleted


class PostCommentLike(db.Model):
    __tablename__ = 'post_comment_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_comment_id, user_id):
        self.post_comment_id = post_comment_id
        self.user_id = user_id

    @staticmethod
    def is_liked(post_comment_id, user_id):
        return PostCommentLike.query.filter_by(post_comment_id=post_comment_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class PostCommentReport(db.Model):
    __tablename__ = 'post_comment_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_comment_id, user_id):
        self.post_comment_id = post_comment_id
        self.user_id = user_id

    @staticmethod
    def is_reported(post_comment_id, user_id):
        return PostCommentReport.query.filter_by(post_comment_id=post_comment_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Unicode(30), nullable=False)

    @staticmethod
    def generate():
        db.session.add(Channel(channel=u'热门'))
        db.session.add(Channel(channel=u'关注'))
        db.session.add(Channel(channel=u'涨姿势'))
        db.session.add(Channel(channel=u'随手拍'))
        db.session.add(Channel(channel=u'那么问题来了'))
        db.session.add(Channel(channel=u'全明星阵容'))
        db.session.commit()


def generate_helper_data():
    Channel.generate()


def generate_fake_data(user_count=1000):
    User.generate_fake(user_count)