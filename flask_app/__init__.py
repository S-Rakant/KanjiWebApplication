from flask import Flask, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import current_app
from flask_wtf.csrf import CSRFProtect
from .local_config import LocalConfig
from .config import Config

import os
from datetime import timedelta


app = Flask(__name__)
app.config.from_object(LocalConfig)

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context(): #アプリケーションコンテキスト
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .func import func as func_blueprint
    app.register_blueprint(func_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint)

    return app