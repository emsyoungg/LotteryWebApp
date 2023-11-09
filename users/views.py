# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, session
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
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # stores users username in apps session for setup_2fa to access
        session['username'] = new_user.email
        # sends user to login page
        return redirect(url_for('users.setup_2fa'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    loginForm = LoginForm()

    if loginForm.validate_on_submit():

        user = User.query.filter_by(email=loginForm.username.data).first()

        if not user or not user.verify_password(loginForm.password.data) or not user.verify_pin(loginForm.pin.data):
            session['authentication_attempts'] += 1

            if session.get('authentication_attempts') >= 3:
                flash(Markup('Number of incorrect login attempts exceeded. Please click <a href="/reset"> here </a> '
                             'to reset.'))
                return render_template('users/login.html')

            flash('Please check your login details and try again, {} login attempts remaining'.format(3 - session.get('authentication_attempts')))
            return render_template('users/login.html', loginForm=loginForm)
        else:
            login_user(user)
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
                           date_of_birth=current_user.date_of_birth)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route('/setup_2fa')
def setup_2fa():
    if 'username' not in session:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(email=session['username']).first()

    if not user:
        return redirect(url_for('index'))

    del session['username']
    return render_template('users/setup_2fa.html', email=user.email, uri=user.get_2fa_uri()), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

@users_blueprint.route('/reset')
def reset():
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
def update_password():
    form = PasswordForm()

    if form.validate_on_submit():
        if current_user.password == form.new_password.data:
            flash('New password must be different to current password')
            return render_template('users/update_password.html', form=form)
        else:
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully')

        return redirect(url_for('users.account'))

    return render_template('users/update_password.html', form=form)
