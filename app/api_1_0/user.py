# -*- coding: utf-8 -*-
from flask import jsonify, request, render_template_string

from app import db
from app.models import User
from app.utils.image import upload_image, valid_image
from . import api
from forms import PersonalInfoForm
from api_constants import *


@api.route('/register')
def register():
    data = {'user': {}}
    username = request.values.get('username', u'', type=unicode)
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


@api.route('/personal_info_setting', methods=['GET', 'POST'])
def personal_info_setting():
    data = {}
    if request.method == 'POST':
        image = request.files.get('image')
        user_id = request.values.get('user_id', '', type=str)
        nickname = request.values.get('nickname', u'', type=unicode)
        signature = request.values.get('signature', u'', type=unicode)
        user = User.query.get(user_id)
        if user:
            user.nickname = nickname
            user.signature = signature
            if image:
                if valid_image(image.name):
                    user.avatar = upload_image(int(user_id), image)
                else:
                    data['status'] = NOT_IMAGE
                    data['message'] = NOT_IMAGE_MSG
                    return jsonify(data)
            data['status'] = SUCCESS
            data['message'] = SUCCESS_MSG
        else:
            data['status'] = USER_NOT_EXIST
            data['message'] = USER_NOT_EXIST_MSG
        return jsonify(data)
    else:
        return render_template_string(
            """
            <!DOCTYPE html>
            <html>
            <head lang="en">
              <meta charset="UTF-8">
            </head>
            <body>
              <form enctype="multipart/form-data" method="post">
                {{ form.csrf_token }}
                {{ form.image }}
                user_id:
                {{ form.user_id }}
                nickname:
                {{ form.nickname }}
                signature:
                {{ form.signature }}
                <input type="submit">
              </form>
            </body>
            </html>
            """,
            form=PersonalInfoForm()
        )