# -*- coding: utf-8 -*-
from unittest import TestCase

import app as biu


class BasicBiuTestCase(TestCase):
    def create_app(self):
        return biu.create_app('testing')

    def setUp(self):
        self.app = self.create_app()
        self.test_app = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def assert_status_code(self, response, status_code):
        self.assertEquals(status_code, response.status_code)
        return response

    def assert_ok(self, response):
        return self.assert_status_code(response, 200)

    def assert_not_found(self, response):
        return self.assert_status_code(response, 404)