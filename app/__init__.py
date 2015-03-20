# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from config import config


app = None
db = SQLAlchemy()
admin = Admin()


def create_app(config_name):
    global app
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    admin.init_app(app)
    db.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/biu_admin')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_perfix='/')

    return app
