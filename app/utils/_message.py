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
    _app_key = None
    _app_master_secret = None
    _timestamp = None
    _message_post_url = 'http://msg.umeng.com/api/send'

    _push_params = {
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

    def _get_validation_token(self):
        return hashlib.md5(self._app_key + self._app_master_secret + self._timestamp).hexdigest()

    def _generate_push_message(self, message_type, user, comment):
        if message_type == 'follow':
            self._push_params['payload']['user'] = user.get_brief_info_dict()
            return u'%s 关注了你' % user.nickname
        elif message_type == 'comment':
            self._push_params['payload']['user'] = user.get_brief_info_dict()
            return u'%s biu了你的图片: %s' % (user.nickname, comment)
        elif message_type == 'delete_post':
            return u'你的图片包含政治不正确的信息哦'

    def _generate_push_params(self, device_token, message):
        self._timestamp = str(int(time_now()))
        self._push_params['appkey'] = self._app_key
        self._push_params['timestamp'] = self._timestamp
        self._push_params['validation_token'] = self._get_validation_token()
        self._push_params['device_tokens'] = 'AhCrzhfKzPtP3xM8XUXLvRSeRw2Tox472FOHG6fothDo'
        self._push_params['payload']['body'] = {'custom': message}

    def push_unicast(self, message_type, target, user, comment=''):
        message = self._generate_push_message(message_type, user, comment)
        self._generate_push_params(target.identity, message)
        resp = requests.post(self._message_post_url, data=json.dumps(self._push_params))
        print(self._push_params)
        return self._is_push_success(resp)

    @staticmethod
    def _is_push_success(resp):
        resp = json.loads(resp.text.decode('utf8'))
        print(resp)
        if resp['ret'] == 'SUCCESS':
            return True
        return False


class AndroidPush(Push):
    _app_key = '5481dfebfd98c5b418000768'
    _app_master_secret = 'hzwow371z3gbzplz3uvgonytmzexyxyy'


class IosPush(Push):
    _app_key = '5481e1b2fd98c5b418000a99'
    _app_master_secret = 'eurxcpfruvk7rmhir7cpelbo0lmsmsgj'

    def _generate_push_params(self, device_token, message):
        print(self._app_key, self._app_master_secret)
        self._timestamp = str(int(time_now()))
        self._push_params['appkey'] = self._app_key
        self._push_params['timestamp'] = self._timestamp
        self._push_params['validation_token'] = self._get_validation_token()
        self._push_params['device_tokens'] = '2ec6db4cdedb923d9ae19cc2a489157f292d900d8306a4e3c0fc8a69d56935a3'
        self._push_params['payload']['aps'] = {'alert': message}