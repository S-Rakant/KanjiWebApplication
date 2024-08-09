from flask import Blueprint, request, render_template, flash, redirect, url_for
from . import login_manager
from flask_login import login_required, login_user, logout_user, current_user
from flask import session, abort
from flask_wtf.csrf import CSRFError


from .forms import RegistrationForm, LoginForm 
from .models import User

from . import db
from .myLogger import getLogger

auth = Blueprint('auth', __name__, url_prefix='/auth')
logger = getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #user_idとマッチした行を取り出す

@auth.route('/register', methods=['GET', 'POST'])
@auth.errorhandler(CSRFError)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        logger.info(f'############### UserID : {form.username.data} created account successfully ###############')
        flash('Regist your account successfully!', 'regist_success')
        return redirect(url_for('auth.login'))
    if (form.username.data != None) & (form.password.data != None) & (form.confirm_password != None):
        flash('!! Invalid user ID or password !!', 'regist_error')
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
@auth.errorhandler(CSRFError)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            logger.info(f'############### UserID : {form.username.data} Login ###############')
            session["uesr_name"] = form.username.data
            flash('Login successfully! Welcome to Kanji Quiz!', 'login_success')
            return redirect(url_for('main.index'))
        else:
            flash('!! Invalid user ID or password !!', 'login_error')
            print(f'failed Login')
    return render_template('login.html', form=form)

@auth.route('/logout')
@auth.errorhandler(CSRFError)
@login_required
def logout():
    logger.info(f'############### UserID : {current_user.username} was Loggedout ###############')
    logout_user()
    session.clear()
    flash('Logout successfully!!', 'logout_success')
    return redirect(url_for('auth.login'))