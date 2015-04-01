# -*- coding: utf-8 -*-
from flask import json
from faker import Factory

from app.api_1_0.api_constants import *
from tests import BasicBiuTestCase


class BiuApiTestCase(BasicBiuTestCase):
    PREFIX = '/api/v1.0/'
    fake = Factory.create()

    def assert_dict_recur(self, expect, actual):
        for key in actual:
            if isinstance(actual[key], dict) and key in expect:
                self.assert_dict_recur(expect[key], actual[key])
            elif key in expect:
                self.assertIs(not expect[key], not actual[key])

    def assert_api(self, response, expect):
        self.assert_ok_json(response)
        data = json.loads(response.data)
        self.assert_dict_recur(expect, data)
        return response

    def test_register_token(self):
        url = self.PREFIX + 'register_token'
        query = {'identity': ''}
        expect = {
            'status': PARAMETER_ERROR,
            'message': True,
            'token': False
        }
        response = self.test_app.get(url, data=query)
        self.assert_api(response, expect)

        query['identity'] = self.fake.password(32)
        response = self.test_app.get(url, data=query)
        expect['status'] = SUCCESS
        expect['token'] = True
        self.assert_api(response, expect)


    def test_get_posts(self):
        url = self.PREFIX + 'get_posts'
        response = self.test_app.get(url)
        self.assert_ok_json(response)

    def test_get_channels(self):
        url = self.PREFIX + 'get_channels'
        response = self.test_app.get(url)
        self.assert_ok_json(response)