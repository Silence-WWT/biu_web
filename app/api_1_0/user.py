# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app
from sqlalchemy import func, desc

from app import db
from app.models import User, Fan, ThirdPartyUser, Society, Post, Message, MessageType
from app.utils import sex_isvalid, upload_image, get_image_from_url, sms_captcha, redis_check, third_party_token
from . import api
from api_constants import *


@api.route('/register_token')
def register_token():
    identity = request.values.get('identity', '', type=str)
    data = {
        'token': third_party_token(identity),
        'status': SUCCESS,
        'message': SUCCESS_MSG
    }
    return jsonify(data)


# @api.route('/confirm_mobile')
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
    email = request.values.get('email', '', type=str)
    token = request.values.get('token', '', type=str)
    device = request.values.get('device', 0, type=int)
    user = User.query.filter_by(email=email).limit(1).first()
    if user:
        data['status'] = EMAIL_EXIST
        data['message'] = EMAIL_EXIST_MSG
    elif not redis_check('token', identity, token):
        data['status'] = TOKEN_INCORRECT
        data['message'] = TOKEN_INCORRECT_MSG
    elif email and password and identity:
        user = User(
            id=User.get_random_id(),
            password=password,
            email=email,
            identity=identity,
            device=device
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
    email = request.values.get('email', '', type=str)
    password = request.values.get('password', '', type=str)
    identity = request.values.get('identity', '', type=str)
    device = request.values.get('device', 0, type=int)
    user = User.query.filter_by(email=email).limit(1).first()
    if user and user.verify_password(password):
        user.update_identity_device(identity, device)
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
    device = request.values.get('device', 0, type=int)
    society_id = request.values.get('society_id', 0, type=int)
    society_user_id = request.values.get('society_user_id', '', type=str)
    token = request.values.get('token', '', type=str)
    nickname = request.values.get('nickname', u'', type=unicode)
    sex = request.values.get('sex', current_app.config['SEX_UNKNOWN'], type=int)
    avatar = request.values.get('avatar', '', type=str)
    society = Society.query.get(society_id)
    if not redis_check('token', identity, token):
        data['status'] = TOKEN_INCORRECT
        data['message'] = TOKEN_INCORRECT_MSG
    elif society and society_user_id:
        third_party_user = ThirdPartyUser.query.filter_by(society_id=society_id, society_user_id=society_user_id). \
            limit(1).first()
        if not third_party_user:
            user_id = User.get_random_id()
            user = User(
                id=user_id,
                identity=identity,
                nickname=nickname,
                password='',
                email='',
                sex=sex,
                avatar=get_image_from_url(user_id, avatar),
                device=device
            )
            db.session.add(user)
            third_party_user = ThirdPartyUser(
                user_id=user.id,
                society_user_id=society_user_id,
                society_id=society_id
            )
            db.session.add(third_party_user)
            db.session.commit()
        else:
            user = third_party_user.get_user()
            user.update_identity_device(identity, device)
        data['user'] = user.get_self_info_dict()
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
    identity = request.values.get('identity', '', type=str)
    target = User.query.get(target_id)
    if target:
        data['profile'] = target.get_profile_dict(page, user_id, identity)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/profile_posts')
def profile_posts():
    data = {'posts': []}
    user_id = request.values.get('user_id', '', type=str)
    target_id = request.values.get('target_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    identity = request.values.get('identity', '', type=str)
    target = User.query.get(target_id)
    if target:
        post_dicts = target.get_self_posts(page, user_id, identity)
        for post_dict in post_dicts:
            post_ = Post.query.get(post_dict['post_id'])
            post_dict['comments'] = post_.get_comments_dict(current_app.config['FIRST_PAGE'],
                                                            current_app.config['COMMENTS_PER_PAGE'])
            data['posts'].append(post_dict)
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
        user.sex = sex
        data['user'] = user.get_personal_info_dict()
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
            follow_message_type = MessageType.query.filter_by(type='follow').first()
            # TODO: follow_message_type Factory
            fan = Fan(user_id=user_id, idol_id=idol_id)
            db.session.add(fan)
            message = Message(follow_message_type, idol, user)
            db.session.add(message)
            db.session.commit()
        elif fan and fan.is_deleted and not cancel:
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
        if following:
            follow_dict['is_followed'] = Fan.is_follow(follow_.idol_id, user_id)
            follow_dict['is_following'] = Fan.is_follow(user_id, follow_.idol_id)
        else:
            follow_dict['is_followed'] = Fan.is_follow(follow_.user_id, user_id)
            follow_dict['is_following'] = Fan.is_follow(user_id, follow_.user_id)
        data['follows'].append(follow_dict)
    data['status'] = SUCCESS
    data['message'] = SUCCESS_MSG
    return jsonify(data)


@api.route('/message_list')
def message_list():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    user = User.query.get(user_id)
    page = request.values.get('page', 1, type=int)
    if user:
        data['messages'] = user.get_message_list(page)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/message_read')
def message_read():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    message_id = request.values.get('message_id', '', type=str)
    user = User.query.get(user_id)
    message = Message.query.get(message_id)
    if user and message and user.id == message.user_id:
        if not message.is_read:
            message.is_read = True
        data['status'] = SUCCESS
        data['messages'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/active_users')
def active_users():
    data = {
        'status': SUCCESS,
        'message': SUCCESS_MSG,
        'users': []
    }
    posts = db.session.query(Post.user_id, func.count('*').label('posts_count')).group_by(Post.user_id). \
        order_by(desc('posts_count')).limit(12)
    jiecao_sister = User.query.get('69331659')  # 节操姐
    user_list = [Post.query.get(post[0]).get_user() for post in posts]
    if jiecao_sister and jiecao_sister not in user_list:
        user_list.insert(0, jiecao_sister)
        user_list = user_list[:12]
    for user in user_list:
        data['users'].append(user.get_brief_info_dict())
    data['users'] = data['users'][:12]
    return jsonify(data)