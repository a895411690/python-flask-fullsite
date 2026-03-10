from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='首页')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/user')
@login_required
def user():
    return render_template('user.html', title='个人中心', user=current_user)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('无管理员权限')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin.html', title='管理后台', users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
