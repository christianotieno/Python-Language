from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from blog.users.utils import SavePicture, SendResetEmail

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        HashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=HashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            NextPage = request.args.get('next')
            return redirect(NextPage) if NextPage else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            PictureFile = SavePicture(form.picture.data)
            current_user.ImageFile = PictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    ImageFile = url_for(
        'static', filename='ProfilePics/' + current_user.ImageFile)
    return render_template('account.html', title='Account',
                           ImageFile=ImageFile, form=form)


@users.route("/user/<string:username>")
def UserPosts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.DatePosted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('UserPosts.html', posts=posts, user=user)


@users.route("/ResetPassword", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        SendResetEmail(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('ResetRequest.html', title='Reset Password', form=form)


@users.route("/ResetPassword/<token>", methods=['GET', 'POST'])
def ResetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_ResetToken(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.ResetRequest'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        HashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = HashedPassword
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('ResetToken.html', title='Reset Password', form=form)