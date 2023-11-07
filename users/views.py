# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, session
from app import db
from models import User
from users.forms import RegisterForm, LoginForm
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
    loginForm = LoginForm()

    if loginForm.validate_on_submit():

        user = User.query.filter_by(email=loginForm.username.data).first()

        if not user or not user.verify_password(loginForm.password.data) or not user.verify_pin(loginForm.pin.data):
            flash('Please check your login details and try again')
            return render_template('users/login.html', loginForm=loginForm)
        else:
            flash('Login successful')
            login_user(user)
            return redirect(url_for('index'))

    return render_template('users/login.html', loginForm=loginForm)


# view user account
@users_blueprint.route('/account')
def account():
    return render_template('users/account.html',
                           acc_no="PLACEHOLDER FOR USER ID",
                           email="PLACEHOLDER FOR USER EMAIL",
                           firstname="PLACEHOLDER FOR USER FIRSTNAME",
                           lastname="PLACEHOLDER FOR USER LASTNAME",
                           phone="PLACEHOLDER FOR USER PHONE",
                           date_of_birth="PLACEHOLDER FOR DOB")


@users_blueprint.route('/logout')
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