# IMPORTS
import logging
from datetime import datetime

import bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from markupsafe import Markup
from flask_login import login_required, current_user

from app import db, requires_roles
from models import User
from users.forms import RegisterForm, LoginForm, PasswordForm
from flask_login import login_user, logout_user

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database
        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        date_of_birth=form.date_of_birth.data,
                        postcode=form.postcode.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # stores users username in apps session for setup_2fa to access
        session['username'] = new_user.email

        # logs user registration
        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)

        # sends user to login page
        return redirect(url_for('users.setup_2fa'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if user hasn't logged in before set to 0
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    loginForm = LoginForm()
    # checks if the form data is valid
    if loginForm.validate_on_submit():

        user = User.query.filter_by(email=loginForm.username.data).first()
        # checks login details are correct
        if not user or not user.verify_password(loginForm.password.data) or not user.verify_pin(
                loginForm.pin.data) or not user.verify_postcode(loginForm.postcode.data):
            session['authentication_attempts'] += 1
            logging.warning('SECURITY - Invalid Log In Attempt [%s, %s]', loginForm.username.data, request.remote_addr)

            # max login attempts exceeded
            if session.get('authentication_attempts') >= 3:
                flash(Markup('Number of incorrect login attempts exceeded. Please click <a href="/reset"> here </a> '
                             'to reset.'))
                return render_template('users/login.html')

            flash('Please check your login details and try again, {} login attempts remaining'.format(
                3 - session.get('authentication_attempts')))
            return render_template('users/login.html', loginForm=loginForm)
        else:
            # logs user in
            login_user(user)
            # logs the login
            logging.warning('SECURITY - User login [%s, %s, %s]', current_user.id, loginForm.username.data,
                            request.remote_addr)
            # update user details in database
            current_user.last_login = current_user.current_login
            current_user.current_login = datetime.now()
            current_user.last_ip = current_user.current_ip
            current_user.current_ip = request.remote_addr
            current_user.successful_logins = current_user.successful_logins + 1
            db.session.commit()

            if user.role == 'admin':
                return redirect(url_for('admin.admin'))
            else:
                return redirect(url_for('index'))

    return render_template('users/login.html', loginForm=loginForm)


# view user account
@users_blueprint.route('/account')
@login_required
@requires_roles('admin', 'user')
def account():
    return render_template('users/account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone,
                           date_of_birth=current_user.date_of_birth,
                           postcode=current_user.postcode)


@users_blueprint.route('/logout')
@login_required
def logout():
    # log user logout
    logging.warning('SECURITY - User log out [%s, %s, %s]', current_user.id, current_user.email,
                    request.remote_addr)
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route('/setup_2fa')
def setup_2fa():
    if 'username' not in session:
        return redirect(url_for('index'))
    # find user
    user = User.query.filter_by(email=session['username']).first()

    if not user:
        return redirect(url_for('index'))

    del session['username']
    return render_template('users/setup_2fa.html', email=user.email, uri=user.get_2fa_uri()), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


# reset login if locked out
@users_blueprint.route('/reset')
def reset():
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
def update_password():
    form = PasswordForm()

    if form.validate_on_submit():
        # checks current password
        if not current_user.verify_password(form.current_password.data):
            flash("Incorrect current password")
            return render_template('users/update_password.html', form=form)
        else:
            # checks new password isn't same as old password
            if current_user.verify_password(form.new_password.data):
                flash('New password must be different to current password')
                return render_template('users/update_password.html', form=form)
            else:
                # sets and hashes new password
                current_user.password = bcrypt.hashpw(form.new_password.data.encode('utf-8'), bcrypt.gensalt())
                db.session.commit()
                flash('Password changed successfully')

        return redirect(url_for('users.account'))

    return render_template('users/update_password.html', form=form)
