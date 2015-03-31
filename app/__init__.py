# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.principal import Principal
from config import config
from permission import config_identity


app = None
db = SQLAlchemy()
admin_app = Admin()
login_manager = LoginManager()
principal = Principal()


def create_app(config_name):
    global app
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    admin_app.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)

    config_identity(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/biu_admin')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_perfix='/')

    return app
