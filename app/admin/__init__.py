# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.admin.contrib.sqla import ModelView

from .. import admin_app
from .. import db
from ..models import User, Post, PostComment, Channel


admin = Blueprint('biu_admin', __name__)
from .views import BiuBaseView
admin_app.add_view(BiuBaseView(User, db.session, name='user', template='admin/user.html', endpoint='admin_user'))
admin_app.add_view(BiuBaseView(Post, db.session, name='post', template='admin/post.html', endpoint='admin_post'))
admin_app.add_view(BiuBaseView(PostComment, db.session, name='comment', template='admin/comment.html',
                               endpoint='admin_comment'))
admin_app.add_view(ModelView(User, db.session, 'ModelUser', url='/admin/User'))
# admin_app.add_view(ModelView(Post, db.session, 'Post', url='/admin/post'))
# admin_app.add_view(ModelView(PostComment, db.session, 'post_comment'))
# admin_app.add_view(ModelView(Channel, db.session, 'channel', url='/admin/channel'))