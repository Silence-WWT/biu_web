# -*- coding: utf-8 -*-
import requests
from random import randint, seed
from xml.dom import minidom

from flask import current_app
from faker import Factory

from app.utils.biu_hashlib import MD5

seed()
__local_redis = current_app.config['local_redis']
__fake = Factory.create()


def redis_check(type_, content, value):
    if type_ == 'token':
        return MD5.check_md5(__local_redis.get('third_party_token:' + content), value)
    elif type_ == 'captcha':
        return value == __local_redis.get('sms_captcha:' + content)
    return False


def third_party_token(identity):
    key = 'third_party_token:' + identity
    token = __fake.password(64)
    __local_redis.set(key, token, 600)
    print(token)
    return token


def sms_captcha(mobile):
    key = 'sms_captcha:' + mobile
    captcha = str(randint(100000, 999999))
    status = __send_sms(mobile, captcha)
    if status:
        __local_redis.set(key, captcha, 600)
    return status


__MESSAGE_API_CONTENT_TEST = u'您的验证码是：%s。请不要把验证码泄露给其他人。'
__MESSAGE_API_SUCCESS = '2'


def __send_sms(number, content):
    query = {'method': 'Submit',
             'account': 'cf_biu2014',
             'password': 'BiuStriker',
             'mobile': number,
             'content': __MESSAGE_API_CONTENT_TEST % content}
    r = requests.get("http://106.ihuyi.cn/webservice/sms.php", params=query).text.encode('utf8')
    doc = minidom.parseString(r)
    status = doc.getElementsByTagName('code')[0].firstChild.nodeValue
    if status != __MESSAGE_API_SUCCESS:
        return False
    else:
        return True