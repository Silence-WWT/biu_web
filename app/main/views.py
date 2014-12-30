# -*- coding: utf-8 -*-
from flask import render_template

from .import main


@main.route('/share')
def share():
    return render_template('share.html')


@main.route('/download')
def download():
    return render_template('download.html')


@main.route('/')
def index():
    return render_template('index_review.html')
