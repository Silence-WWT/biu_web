# -*- coding: utf-8 -*-
from flask import jsonify, request

from app.models import User
from . import api
from api_constants import *


@api.route('/login')
def login():
    data = {'user': {}}
    username = request.values.get('username', '', type=str)
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    user = User.query.filter_by(username=username).limit(1).first() \
        or User.query.filter_by(mobile=username).limit(1).first()
    if user and user.verify_password(password):
        user.update_identity(identity)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MESSAGE
        data['user'] = {
            'user_id': user.id,
            'username': user.username,
            'mobile': user.mobile,
            'identity': user.identity,
            'golds': user.golds,
            'avatar': STATIC_URL + user.avatar,
            'signature': user.signature,
            'push': user.push,
            'no_disturb': user.no_disturb
        }
    else:
        data['status'] = LOGIN_FAIL
        data['message'] = LOGIN_FAIL_MESSAGE
    return jsonify(data)