# -*- coding: utf-8 -*-
from tests import BasicBiuTestCase


class BiuTestCase(BasicBiuTestCase):
    def test_biu_admin_login(self):
        response = self.test_app.post('/biu_admin/login', data={'username': 'silence', 'password': '123456'},
                                      follow_redirects=True)
        self.assert_ok(response)
        for url in ['user', 'post', 'comment']:
            response = self.test_app.get('/admin/admin_' + url, follow_redirects=True)
            self.assert_ok(response)

    def test_admin_index(self):
        response = self.test_app.get('/admin', follow_redirects=True)
        self.assert_ok(response)

    def test_get_posts(self):
        response = self.test_app.get('/api/v1.0/get_posts')
        self.assert_ok(response)

    def test_admin_user(self):
        response = self.test_app.get('/admin/admin_user', follow_redirects=True)
        self.assert_not_found(response)