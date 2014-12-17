# -*- coding: utf-8 -*-
import hashlib
import json
import requests

from . import time_now

android_push = None
ios_push = None


def push(message_type, target, user, comment=''):
    global android_push, ios_push
    if target.device == 0:
        if android_push is None:
            device_push = android_push = AndroidPush()
        else:
            device_push = android_push
    else:
        if ios_push is None:
            device_push = ios_push = IosPush()
        else:
            device_push = ios_push
    return device_push.push_unicast(message_type, target, user, comment)


class Push(object):
    __app_key = None
    __app_master_secret = None
    __timestamp = None
    __message_post_url = 'http://msg.umeng.com/api/send'

    __push_params = {
        'type': 'unicast',
        'payload': {
            'display_type': 'notification',
            # 'body': {
                # 'ticker': 'Hello World',
                # 'title': '你好',
                # 'text': '来自友盟推送',
                # 'after_open': 'go_app'
            # }
        }
    }

    def __get_validation_token(self):
        return hashlib.md5(self.__app_key + self.__app_master_secret + self.__timestamp).hexdigest()

    def __generate_push_message(self, message_type, user, comment):
        if message_type == 'follow':
            self.__push_params['payload']['user'] = user.get_brief_info_dict()
            return u'%s 关注了你' % user.nickname
        elif message_type == 'comment':
            self.__push_params['payload']['user'] = user.get_brief_info_dict()
            return u'%s biu了你的图片: %s' % (user.nickname, comment)
        elif message_type == 'delete_post':
            return u'你的图片包含政治不正确的信息哦'

    def __generate_push_params(self, device_token, message):
        self.__timestamp = str(int(time_now()))
        self.__push_params['timestamp'] = self.__timestamp
        self.__push_params['validation_token'] = self.__get_validation_token()
        self.__push_params['device_tokens'] = device_token
        self.__push_params['payload']['body'] = {'custom': message}

    def push_unicast(self, message_type, target, user, comment=''):
        message = self.__generate_push_message(message_type, user, comment)
        self.__generate_push_params(target.identity, message)
        resp = requests.post(self.__message_post_url, data=json.dumps(self.__push_params))
        return self.__is_push_success(resp)

    @staticmethod
    def __is_push_success(resp):
        resp = json.loads(resp.text.decode('utf8'))
        if resp['ret'] == 'SUCCESS':
            return True
        return False


class AndroidPush(Push):
    __app_key = '5481dfebfd98c5b418000768'
    __app_master_secret = 'hzwow371z3gbzplz3uvgonytmzexyxyy'


class IosPush(Push):
    __app_key = '5481e1b2fd98c5b418000a99'
    __app_master_secret = 'eurxcpfruvk7rmhir7cpelbo0lmsmsgj'

    def __generate_push_params(self, device_token, message):
        self.__timestamp = str(int(time_now()))
        self.__push_params['timestamp'] = self.__timestamp
        self.__push_params['validation_token'] = self.__get_validation_token()
        self.__push_params['device_tokens'] = device_token
        self.__push_params['payload']['aps'] = {'alert': message}