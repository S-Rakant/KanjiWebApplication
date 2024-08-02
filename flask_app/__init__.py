from flask import Flask, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import current_app
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

import os
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes = 150)
# csrf = CSRFProtect(app) #csrf_tokenがsession毎に自動で生成される

load_dotenv()

def create_app():
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

    db.init_app(app)

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