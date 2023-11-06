# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


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
def forbidden_error(error):
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
