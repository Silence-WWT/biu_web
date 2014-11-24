# -*- coding: utf-8 -*-
from flask import jsonify, request

from app import db
from app.models import User
from . import api
from api_constants import *


@api.route('/register')
def register():
    data = {'user': {}}
    username = request.values.get('username', '', type=str)
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    mobile = request.values.get('mobile', '', type=str)
    user = User.query.filter_by(username=username).limit(1).first()
    if user:
        data['status'] = USERNAME_EXIST
        data['message'] = USERNAME_EXIST_MSG
    elif username and password and identity:
        user_id = User.get_random_id()
        user = User(
            id=user_id,
            username=username,
            nickname='',
            password=password,
            mobile=mobile,
            identity=identity,
        )
        db.session.add(user)
        db.session.commit()
        data['user'] = user.get_user_info_dict()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


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
        data['message'] = SUCCESS_MSG
        data['user'] = user.get_user_info_dict()
    else:
        data['status'] = LOGIN_FAIL
        data['message'] = LOGIN_FAIL_MSG
    return jsonify(data)


@api.route('/push_setting')
def push_setting():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    push = request.values.get('push', SETTING_IS_NOT_VALID, type=int)
    disturb = request.values.get('disturb', SETTING_IS_NOT_VALID, type=int)
    user = User.query.get(user_id)
    print(push, disturb)
    if not user:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    else:
        if push > SETTING_IS_NOT_VALID:
            user.push = push
        if disturb > SETTING_IS_NOT_VALID:
            user.disturb = disturb
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    return jsonify(data)