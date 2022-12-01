from flask import render_template, flash, redirect, url_for
from app import app, login
from app.app_account import account_bp
from .models import *
from .forms import RegisterForm, LoginForm, ChangePwdForm

from app.app_demo import demolinks # 导航栏链接

@login.user_loader
def load_user():
    return

@account_bp.route('/', methods=['GET','POST'])
@account_bp.route('/index', methods=['GET','POST'])
def index():
    return redirect(url_for('account.login'))

@account_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    user_id = form.user_id.data
    password = form.password.data
    if form.submit.data:
        if user_id != "test12345" or password != "test12345":
            flash("账号或密码错误！")
        else:
            flash("登录成功！")
            return redirect(url_for('account.panel'))

    return render_template(
        "index.html",
        title = '登录',
        form = form
    )

@account_bp.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.submit.data:
        pwd1 = form.password1.data
        pwd2 = form.password2.data
        if pwd1 != pwd2:
            flash('两次密码不一致！')
        else:
            flash('注册成功！')
            return redirect(url_for('account.login'))
    return render_template(
        "signup.html",
        title = '注册',
        form = form
    )

@account_bp.route('/changepwd', methods=['GET','POST'])
def changepwd():
    form = ChangePwdForm()
    if form.submit.data:
        flash("密码修改成功！")
        return redirect(url_for('account.panel'))
    return render_template(
        "changepwd.html",
        title = '修改密码',
        form = form
    )

@account_bp.route('/panel', methods=['GET','POST'])
def panel():
    return render_template(
        "panel.html",
        title = '控制面板',
        demolinks = demolinks,
    )
