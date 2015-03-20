# -*- coding: utf-8 -*-
import time
import datetime

from flask import current_app


def time_now():
    return time.time() + 28800


def sex_isvalid(sex):
    return current_app.config['SEX_FEMALE'] <= sex <= current_app.config['SEX_UNKNOWN']


def page_isvalid(page):
    return page if page > 0 else 1


def date_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%F %T')