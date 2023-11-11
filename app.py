# IMPORTS
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_qrcode import QRcode
import logging


# EVENT LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return 'SECURITY' in record.getMessage()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('lottery.log', 'a')
file_handler.setLevel(logging.WARNING)

file_handler.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# load .env
load_dotenv()

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# initialise database
db = SQLAlchemy(app)

qrcode = QRcode(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                logging.warning('SECURITY - Unauthorised Access Attempts [%s, %s, %s, %s]', current_user.id,
                                current_user.email, current_user.role, request.remote_addr)
                return render_template('errors/403.html')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint

#
# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)

# FLASK LOGIN MANAGER
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from models import User


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# ERROR HANDLING
# # Bad Request
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


# # Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403


# # Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# # Internal Server Error
@app.errorhandler(500)
def not_found_error(error):
    return render_template('errors/500.html'), 500


# # Service Unavailable
@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('errors/503.html'), 503


if __name__ == "__main__":
    app.run()
