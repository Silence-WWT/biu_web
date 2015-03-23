# -*- coding: utf-8 -*-
from flask import request, render_template, current_app, redirect, flash
from flask.ext.admin import BaseView, expose
from flask.ext.login import login_user
from flask.ext.principal import identity_changed, Identity
from sqlalchemy.exc import ArgumentError

from . import admin
from ..models import Privilege
from ..permission import admin_permission
from ..utils import page_isvalid, date_from_timestamp
from forms import LoginForm


class BiuBaseView(BaseView):
    def __init__(self, model, session, template, **kwargs):
        self.model = model
        self.session = session
        self.template = template
        super(BiuBaseView, self).__init__(**kwargs)

    @expose('/')
    @admin_permission.require(http_exception=404)
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


@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        administration = Privilege.query.filter_by(username=login_form.username.data).first()
        if administration and administration.verify_password(login_form.password.data):
            login_user(administration)
            identity_changed.send(current_app._get_current_object(), identity=Identity(administration.get_id()))
            return redirect('/admin')
        flash('wrong username or password')
    return render_template('admin/login.html', login_form=login_form)