# -*- coding: utf-8 -*-
from flask import request, jsonify, current_app

from ..models import User, Fan, Post, PostLike, PostReport, PostShare, PostComment, PostCommentLike, PostCommentReport,\
    Channel, Society, Message, MessageType
from . import api
from app import db
from app.utils import upload_image, page_isvalid
from api_constants import *


@api.route('/post')
def post():
    data = {'post': {}}
    image_str = request.values.get('image_str', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    content = request.values.get('content', u'', type=unicode)
    channel_id = request.values.get('channel_id', '', type=str)
    user = User.query.get(user_id)
    channel = Channel.query.get(channel_id)
    image_path = upload_image(user.id, image_str)
    if user and image_path and channel:
        post_ = Post(
            user_id=user_id,
            image=image_path,
            content=content,
            channel_id=channel_id
        )
        db.session.add(post_)
        db.session.commit()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
        data['post'] = post_.get_post_info_dict()
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/post_comment')
def post_comment():
    data = {'post_comment': {}}
    user_id = request.values.get('user_id', '', type=str)
    content = request.values.get('content', u'', type=unicode)
    post_id = request.values.get('post_id', '', type=str)
    x = request.values.get('x', 0.0, type=float)
    y = request.values.get('y', 0.0, type=float)
    user = User.query.get(user_id)
    post_ = Post.query.get(post_id)
    if not user:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    elif post_ and not post_.is_deleted:
        comment_message_type = MessageType.query.filter_by(type='comment').first()
        #  TODO: comment_message_type Factory
        comment = PostComment(
            post_id=post_id,
            user_id=user_id,
            x=x,
            y=y,
            content=content
        )
        db.session.add(comment)
        author = comment.get_post().get_user()
        author.add_golds('comment')
        #  TODO: 弹幕推送
        print author.id, user.id
        if author.id != user.id:
            print author.id, user.id, 'comment push'
            message = Message(comment_message_type, author, user, comment)
            db.session.add(message)
            db.session.commit()
        data['post_comment'] = comment.get_comment_info()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/get_channels')
def get_channels():
    channels = Channel.query.all()
    data = {
        'channels': [channel.get_channel() for channel in channels],
        'status': SUCCESS,
        'message': SUCCESS_MSG
    }
    return jsonify(data)


@api.route('/get_posts')
def get_posts():
    data = {'posts': []}
    channel_id = request.values.get('channel_id', current_app.config['HOT_CHANNEL_ID'], type=int)
    page = request.values.get('page', 1, type=int)
    user_id = request.values.get('user_id', '', type=str)
    identity = request.values.get('identity', '', type=str)
    page = page_isvalid(page)
    if channel_id > 0:
        posts = Post.query.filter_by(channel_id=channel_id, is_deleted=False).\
            order_by(-Post.created).\
            paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
    elif channel_id == current_app.config['LATEST_CHANNEL_ID']:
        posts = Post.query.filter_by(is_deleted=False).\
            order_by(-Post.created).\
            paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
    elif channel_id == current_app.config['HOT_CHANNEL_ID']:
        posts = Post.query.filter_by(is_deleted=False).\
            order_by(-Post.created).\
            order_by(-Post.likes_count).\
            paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
        # TODO: hot posts
    else:
        user = User.query.get(user_id)
        if user:
            followings_id = [following.idol_id for following in Fan.query.filter_by(user_id=user_id, is_deleted=False)]
            posts = Post.query.filter(Post.user_id.in_(followings_id), Post.is_deleted is not False).\
                order_by(Post.created).\
                paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
        else:
            data['status'] = USER_NOT_EXIST
            data['message'] = USER_NOT_EXIST_MSG
            return jsonify(data)
    for post_ in posts:
        post_dict = post_.get_post_info_dict(user_id, identity)
        post_dict['comments'] = post_.get_comments_dict(current_app.config['FIRST_PAGE'],
                                                        current_app.config['COMMENTS_PER_PAGE'])
        data['posts'].append(post_dict)
    data['status'] = SUCCESS
    data['message'] = SUCCESS_MSG
    return jsonify(data)


@api.route('/post_detail')
def post_detail():
    data = {'post': {}}
    post_id = request.values.get('post_id', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    identity = request.values.get('identity', '', type=str)
    comment_id = request.values.get('comment_id', '', type=str)
    post_ = Post.query.get(post_id)
    if post_ and (user_id or identity):
        data['post'] = post_.get_post_info_dict(user_id, identity)
        data['post']['comments'] = post_.get_comments_dict(1, 10, comment_id)
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    elif not post_:
        data['status'] = POST_NOT_EXIST
        data['message'] = POST_NOT_EXIST_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/get_post_comments')
def get_post_comments():
    data = {}
    post_id = request.values.get('post_id', '', type=str)
    page = request.values.get('page', 1, type=int)
    post_ = Post.query.get(post_id)
    if post_:
        data['comments'] = post_.get_comments_dict(page, current_app.config['COMMENTS_PER_PAGE'])
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = POST_NOT_EXIST
        data['message'] = POST_NOT_EXIST_MSG
    return jsonify(data)


@api.route('/like')
def like():
    data = {}
    target_id = request.values.get('target_id', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    type_ = request.values.get('type', '', type=str)
    cancel = request.values.get('cancel', 0, type=int)
    identity = request.values.get('identity', '', type=str)
    user = User.query.get(user_id)

    if not (user or identity):
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)
    elif type_ == 'post' and (user or identity):
        target = Post.query.get(target_id)
        target_class = PostLike
    elif type_ == 'post_comment' and (user or identity):
        target = PostComment.query.get(target_id)
        target_class = PostCommentLike
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)

    if target and (user or identity):
        target_like = target_class.get_like(target_id, user_id, identity)
        if not cancel and not target_like:
            target_like = target_class(target_id, user_id, identity)
            db.session.add(target_like)
            db.session.commit()
            target_like.get_post().get_user().add_golds('like')
            if isinstance(target_like, PostLike):
                target_like.get_post().add_likes_count()
            if user:
                pass
                # TODO: 点赞推送
        elif cancel and target_like:
            if isinstance(target_like, PostLike):
                target_like.get_post().minus_likes_count()
            db.session.delete(target_like)
            db.session.commit()
            target_like.get_post().get_user().add_golds('like', 'minus')
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/share')
def share():
    data = {}
    post_id = request.values.get('post_id')
    user_id = request.values.get('user_id', '', type=str)
    identity = request.values.get('identity', '', type=str)
    society_id = request.values.get('society_id', '', type=str)
    society = Society.query.get(society_id)
    post_ = Post.query.get(post_id)
    if post_ and society and (user_id or identity):
        post_share_ = PostShare(post_id, society_id, user_id, identity)
        db.session.add(post_share_)
        db.session.commit()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/report')
def report():
    data = {}
    target_id = request.values.get('target_id', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    type_ = request.values.get('type', '', type=str)
    if type_ == 'post':
        target = Post.query.get(target_id)
        target_class = PostReport
    elif type_ == 'post_comment':
        target = PostComment.query.get(target_id)
        target_class = PostCommentReport
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)

    user = User.query.get(user_id)
    if target and user:
        target_report = target_class.is_reported(target_id, user_id)
        if not target_report:
            target_report = target_class(target_id, user_id)
            db.session.add(target_report)
            db.session.commit()
            # if target.report_delete() and isinstance(target, Post):
                # delete_message_type = MessageType.query.filter_by(type='delete_post').first()
                #  TODO: delete_message_type Factory
                # author = target.get_user()
                # message = Message(delete_message_type, author, None, is_read=True)
                # db.session.aad(message)
                # db.session.commit()
                # TODO: 举报删除推送
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/delete')
def delete():
    data = {}
    post_id = request.values.get('post_id', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    user = User.query.get(user_id)
    post_ = Post.query.get(post_id)
    if user and post_ and user.id == post_.user_id:
        if not post_.is_deleted:
            post_.is_deleted = True
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/post/share')
def post_share():
    data = {}
    post_id = request.values.get('post', '', type=str)
    post_ = Post.query.filter_by(id=post_id, is_deleted=False).limit(1).first()
    if post_:
        data['post'] = post_.get_share_dict()
        data['post']['comments'] = post_.get_comments_dict(1, 10)
        data['status'] = SUCCESS
    else:
        data['status'] = POST_NOT_EXIST
    return jsonify(data)


@api.route('/up_reword')
def up_reword():
    data = {}
    user_id = request.values.get('user_id', '', type=str)
    up_id = request.values.get('up_id', '', type=str)
    golds = request.values.get('golds', 0, type=int)
    user = User.query.get(user_id)
    up = User.query.get(up_id)
    if user and up and user != up and golds:
        if user.add_golds('reword', 'minus', golds):
            up.add_golds('reword', 'add', golds)
            data['status'] = SUCCESS
            data['message'] = SUCCESS_MSG
        else:
            data['status'] = USER_GOLDS_NOT_ENOUGH
            data['message'] = USER_GOLDS_NOT_ENOUGH_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/test_generate_image_path', methods=['GET', 'POST'])
def generate_image_path():
    image = request.files.get('image')
    from random import randint
    with open('images.txt', 'a') as f:
        path = upload_image(randint(1, 1001), image)
        f.write(path + '\n')
    return 'ok'