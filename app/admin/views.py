# -*- coding: utf-8 -*-
from flask import request, render_template
from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy.exc import ArgumentError

from app import app
from . import admin
from ..models import User
from ..utils import page_isvalid, date_from_timestamp


class BiuBaseView(BaseView):
    def __init__(self, model, session, template, **kwargs):
        self.model = model
        self.session = session
        self.template = template
        super(BiuBaseView, self).__init__(**kwargs)

    @expose('/')
    def index(self):
        page = request.values.get('page', 1, type=int)
        sort = request.values.get('sort', '', type=str)
        desc = request.values.get('desc', 0, type=int)
        items, pagination = self.get_list(page, sort, desc)
        return self.render(
            self.template, pagination=pagination, items=items, sort=sort, desc=str(desc), get_date=date_from_timestamp)

    def get_list(self, page, sort='', desc=0, per_page=20):
        page = page_isvalid(page)
        if not sort:
            sort_key = None
        else:
            try:
                sort_key = self.model.__dict__[sort] if not desc else -self.model.__dict__[sort]
            except KeyError:
                sort_key = None
        try:
            pagination = self.model.query.order_by(sort_key).paginate(page, per_page, False)
        except ArgumentError:
            pagination = self.model.query.paginate(page, per_page, False)
        items = pagination.items
        return items, pagination


@admin.route('/user')
def admin_index():
    page = request.values.get('page', 0, type=int)
    pagination = User.query.order_by().paginate(page, 20, False)
    # user_list = pagination.items
    return render_template('admin/user.html', pagination=pagination)