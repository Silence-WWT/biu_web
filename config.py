# -*- coding: utf-8 -*-
import os
import redis
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: add a random string as the default SECRET_KEY.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    DEBUG = True
    IMAGE_DIR = '/home/silence/Python/Biu/images/'
    STATIC_URL = 'http://127.0.0.1:5000/images/'
    GOLDS_POST = 5
    GOLDS_COMMENT = 1
    GOLDS_LIKE = 2
    FIRST_PAGE = 1
    FOLLOW_LIST_PER_PAGE = 10
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10
    HOME_PAGE_POSTS_PER_PAGE = 9
    FOLLOWING_CHANNEL_ID = -1
    LATEST_CHANNEL_ID = -2
    HOT_CHANNEL_ID = -3
    SEX_FEMALE = 0
    SEX_MALE = 1
    SEX_UNKNOWN = 2


class DevelopmentConfig(Config):
    DEBUG = True
    CDN_DEBUG = False
    IMAGE_DIR = os.path.join(basedir, 'images')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://dev:devpassword@localhost/biu?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://test:testpassword@localhost/biu_test?charset=utf8'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://dbuser:usER_2014@node1.db/znx?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
