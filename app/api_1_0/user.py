# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app

from app import db
from app.models import User, Fan, ThirdPartyUser
from app.utils.image import upload_image, get_image_from_url
from app.utils.sex import sex_isvalid
from app.utils.verification import sms_captcha, redis_check, third_party_token
from . import api
from api_constants import *


@api.route('/third_party_token')
def get_third_party_token():
    identity = request.values.get('identity', '', type=str)
    data = {
        'token': third_party_token(identity),
        'status': SUCCESS,
        'message': SUCCESS_MSG
    }
    return jsonify(data)


@api.route('/confirm_mobile')
def confirm_mobile():
    data = {}
    mobile = request.values.get('mobile', '', type=str)
    status = sms_captcha(mobile)
    if status:
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = MESSAGE_CONFIRM_FAIL
        data['message'] = MESSAGE_CONFIRM_FAIL_MSG
    return jsonify(data)


@api.route('/register')
def register():
    data = {'user': {}}
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    mobile = request.values.get('mobile', '', type=str)
    captcha = request.values.get('captcha', '', type=str)
    user = User.query.filter_by(mobile=mobile).limit(1).first()
    if user:
        data['status'] = MOBILE_EXIST
        data['message'] = MOBILE_EXIST_MSG
    elif not redis_check('captcha', mobile, captcha):
        data['status'] = CAPTCHA_INCORRECT
        data['message'] = CAPTCHA_INCORRECT_MSG
    elif mobile and password and identity:
        user = User(
            id=User.get_random_id(),
            password=password,
            mobile=mobile,
            identity=identity,
        )
        db.session.add(user)
        db.session.commit()
        data['user'] = user.get_self_info_dict()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/login')
def login():
    data = {'user': {}}
    mobile = request.values.get('mobile', '', type=str)
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    user = User.query.filter_by(mobile=mobile).limit(1).first()
    if user and user.verify_password(password):
        user.update_identity(identity)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
        data['user'] = user.get_self_info_dict()
    else:
        data['status'] = LOGIN_FAIL
        data['message'] = LOGIN_FAIL_MSG
    return jsonify(data)


@api.route('/third_party_login')
def third_party_login():
    data = {'user': {}}
    identity = request.values.get('identity', '', type=str)
    source = request.values.get('source', 0, type=int)
    source_user_id = request.values.get('source_user_id', '', type=str)
    token = request.values.get('token', '', type=str)
    nickname = request.values.get('nickname', u'', type=unicode)
    sex = request.values.get('sex', current_app.config['SEX_UNKNOWN'], type=int)
    avatar = request.values.get('avatar', '', type=str)
    if not redis_check('token', identity, token):
        data['status'] = TOKEN_INCORRECT
        data['message'] = TOKEN_INCORRECT_MSG
    elif source and source_user_id:
        third_party_user = ThirdPartyUser.query.filter_by(source=source, source_user_id=source_user_id).limit(1).first()
        if not third_party_user:
            user_id = User.get_random_id()
            user = User(
                id=user_id,
                identity=identity,
                nickname=nickname,
                password='',
                mobile='',
                sex=sex,
                avatar=get_image_from_url(user_id, avatar)
            )
            db.session.add(user)
            third_party_user = ThirdPartyUser(
                user_id=user.id,
                source_user_id=source_user_id,
                source=source
            )
            db.session.add(third_party_user)
            db.session.commit()
        data['user'] = third_party_user.get_user().get_self_info_dict()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/profile')
def profile():
    data = {'profile': {}}
    user_id = request.values.get('user_id', '', type=str)
    target_id = request.values.get('target_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    user = User.query.get(user_id)
    target = User.query.get(target_id)
    if user and target:
        data['profile'] = target.get_profile_dict(page, user_id)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
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


@api.route('/personal_info_setting')
def personal_info_setting():
    data = {}
    image_str = request.values.get('image_str', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    nickname = request.values.get('nickname', u'', type=unicode)
    signature = request.values.get('signature', u'', type=unicode)
    sex = request.values.get('sex', current_app.config['SEX_UNKNOWN'], type=int)
    user = User.query.get(user_id)
    if user and sex_isvalid(sex):
        if image_str:
            avatar_path = upload_image(user.id, image_str)
            if avatar_path:
                user.avatar = avatar_path
            else:
                data['status'] = NOT_IMAGE
                data['message'] = NOT_IMAGE_MSG
                return jsonify(data)
        user.nickname = nickname
        user.signature = signature
        user.sex = sex
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/follow')
def follow():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    idol_id = request.values.get('idol_id', '', type=str)
    cancel = request.values.get('cancel', 0, type=int)
    user = User.query.get(user_id)
    idol = User.query.get(idol_id)
    if user and idol:
        fan = Fan.query.filter_by(user_id=user_id, idol_id=idol_id).limit(1).first()
        if not fan and not cancel:
            fan = Fan(user_id=user_id, idol_id=idol_id)
            db.session.add(fan)
            db.session.commit()
            # TODO: 关注推送
        elif fan.is_deleted and not cancel:
            fan.is_deleted = False
        elif fan and cancel:
            fan.is_deleted = True
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/follow_list')
def follow_list():
    data = {'follows': []}
    user_id = request.values.get('user_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    following = request.values.get('following', 1, type=int)
    target_id = request.values.get('target_id', '', type=str)
    user = User.query.get(user_id)
    target = User.query.get(target_id)
    if target:
        follows = target.get_fans(following, page, current_app.config['FOLLOW_LIST_PER_PAGE'])
    elif user:
        follows = user.get_fans(following, page, current_app.config['FOLLOW_LIST_PER_PAGE'])
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)
    for follow_ in follows:
        follow_dict = follow_.get_user_or_idol(following).get_brief_info_dict()
        follow_dict['is_followed'] = Fan.is_followed(target_id, user_id)
        follow_dict['is_following'] = Fan.is_following(user_id, target_id)
        data['follows'].append(follow_dict)
    data['status'] = SUCCESS
    data['message'] = SUCCESS_MSG
    return jsonify(data)