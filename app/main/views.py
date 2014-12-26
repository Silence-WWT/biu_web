# -*- coding: utf-8 -*-
from flask import render_template

from .import main


@main.route('/share')
def share():
    return render_template('share.html')
