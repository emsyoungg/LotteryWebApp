from datetime import datetime

import pyotp
import rsa

from app import db, app
from flask_login import UserMixin

from cryptography.fernet import Fernet
import bcrypt
import pickle


# encryption function
def encrypt(data, draw_key):
    return Fernet(draw_key).encrypt(bytes(data, 'utf-8'))


# decryption function
def decrypt(data, draw_key):
    return Fernet(draw_key).decrypt(data).decode('utf-8')


class User(db.Model, UserMixin):

    # functions for verifying login details
    def verify_postcode(self, postcode):
        return self.postcode == postcode

    def verify_pin(self, pin):
        return pyotp.TOTP(self.pin_key).verify(pin)

    def get_2fa_uri(self):
        return str(pyotp.totp.TOTP(self.pin_key).provisioning_uri(
            name=self.email,
            issuer_name='CSC2031 Lottery Web App')
        )

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    ## create users table in database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    pin_key = db.Column(db.String(32), nullable=False, default=pyotp.random_base32())
    registered_on = db.Column(db.DateTime, nullable=False)
    current_login = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    # SYMMETRIC ENCRYPTION
    # draw_key = db.Column(db.BLOB, nullable=False, default=Fernet.generate_key())

    # asymmetric encryption
    public_key = db.Column(db.LargeBinary, nullable=False)
    private_key = db.Column(db.LargeBinary, nullable=False)

    current_ip = db.Column(db.String(100), nullable=True)
    last_ip = db.Column(db.String(100), nullable=True)
    successful_logins = db.Column(db.Integer, nullable=False)

    # Define the relationship to Draw
    draws = db.relationship('Draw')

    def __init__(self, email, firstname, lastname, phone, password, date_of_birth, postcode, role):
        self.date_of_birth = date_of_birth
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.postcode = postcode
        self.role = role
        self.registered_on = datetime.now()
        self.current_login = None
        self.last_login = None
        # advanced tasks
        self.current_ip = None
        self.last_ip = None
        self.successful_logins = 0
        # asymmetric encryption
        publicKey, privateKey = rsa.newkeys(512)
        self.public_key = pickle.dumps(publicKey)
        self.private_key = pickle.dumps(privateKey)


class Draw(db.Model):

    ## VIEW_DRAW FOR SYMMETRIC ENCRYPTION
    # def view_draw(self, draw_key):
    #    self.numbers = decrypt(self.numbers, draw_key)

    ## ASYMMETRIC DECRYPTION view_draw
    def view_draw(self, private_key):
        decrypted_numbers = rsa.decrypt(self.numbers, pickle.loads(private_key)).decode()
        self.numbers = decrypted_numbers

    __tablename__ = 'draws'

    id = db.Column(db.Integer, primary_key=True)

    # ID of user who submitted draw
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    # 6 draw numbers submitted
    numbers = db.Column(db.String(100), nullable=False)

    # Draw has already been played (can only play draw once)
    been_played = db.Column(db.BOOLEAN, nullable=False, default=False)

    # Draw matches with master draw created by admin (True = draw is a winner)
    matches_master = db.Column(db.BOOLEAN, nullable=False, default=False)

    # True = draw is master draw created by admin. User draws are matched to master draw
    master_draw = db.Column(db.BOOLEAN, nullable=False)

    # Lottery round that draw is used
    lottery_round = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user_id, numbers, master_draw, lottery_round,
                 public_key):  # would be draw_key for symmetric encryption
        self.user_id = user_id
        ## SYMMETRIC ENCRYPTION
        # self.numbers = encrypt(numbers, draw_key)
        ## ASYMMETRIC ENCRYPTION
        self.numbers = rsa.encrypt(numbers.encode(), pickle.loads(public_key))
        self.been_played = False
        self.matches_master = False
        self.master_draw = master_draw
        self.lottery_round = lottery_round


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     firstname='Alice',
                     lastname='Jones',
                     phone='0191-123-4567',
                     date_of_birth='01/01/2001',
                     postcode='DN2 7NY',
                     role='admin')

        db.session.add(admin)
        db.session.commit()
