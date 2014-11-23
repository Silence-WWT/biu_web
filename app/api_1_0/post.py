# -*- coding: utf-8 -*-
from flask import request, jsonify

from ..models import User, Post, PostLike, PostReport, PostComment, PostCommentLike, PostCommentReport
from .import api
from app import db
from api_constants import *


@api.route('/post')
def post():
    pass


@api.route('/post_comment')
def post_comment():
    data = {'post_comment': {}}
    user_id = request.values.get('user_id', '', type=str)
    content = request.values.get('content', u'', type=unicode)
    post_id = request.values.get('post_id', '', type=str)
    x = request.values.get('x', 0.0, type=float)
    y = request.values.get('y', 0.0, type=float)
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    if not user:
        data['status'] = USER_NOT_EXIST
        data['message'] = USER_NOT_EXIST_MSG
    elif post and not post.is_deleted and content:
        comment = PostComment(
            post_id=post_id,
            user_id=user_id,
            x=x,
            y=y,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
        data['post_comment'] = comment.get_comment_info()
        comment.get_post().get_user().add_golds('comment')
        # TODO: 评论推送
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)


@api.route('/like')
def like():
    data = {}
    target_id = request.values.get('target_id', '', type=str)
    user_id = request.values.get('user_id', '', type=str)
    type_ = request.values.get('type', '', type=str)
    cancel = request.values.get('cancel', 0, type=int)
    if type_ == 'post':
        target = Post.query.get(target_id)
        target_class = PostLike
    elif type_ == 'post_comment':
        target = PostComment.query.get(target_id)
        target_class = PostCommentLike
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
        return jsonify(data)

    user = User.query.get(user_id)
    if target and user:
        target_like = target_class.is_liked(target_id, user_id)
        if not cancel and not target_like:
            target_like = target_class(target_id, user_id)
            db.session.add(target_like)
            db.session.commit()
            target_like.get_post().get_user().add_golds('like')
            # TODO: 点赞推送
        elif cancel and target_like:
            db.session.delete(target_like)
            db.session.commit()
            target_like.get_post().get_user().add_golds('like', 'minus')
        data['status'] = SUCCESS
        data['message'] = SUCCESS_MSG
    else:
        data['status'] = PARAMETER_ERROR
        data['message'] = PARAMETER_ERROR_MSG
    return jsonify(data)