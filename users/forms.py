from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re
from flask_wtf import RecaptchaField


# handles register form inputs
class RegisterForm(FlaskForm):

    # Validation functions
    def character_check(self, field):
        exclude_chars = "*?!'^+%&/()=}][{$#@<>"

        for char in field.data:
            if char in exclude_chars:
                raise ValidationError(f"Character {char} is not allowed.")

    def is_valid_phone_number(self, phone):
        pattern = re.compile(r'^\d{4}-\d{3}-\d{4}$')
        if not pattern.match(phone.data):
            raise ValidationError(f"Phone number must be in form XXXX-XXX-XXXX")

    def is_valid_password(self, password):
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)')
        if not pattern.match(password.data):
            raise ValidationError(
                f"Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit and 1 "
                f"special character.")

    def date_of_birth_validator(self, date_of_birth):
        pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$')
        if not pattern.match(date_of_birth.data):
            raise ValidationError(f"Invalid date, must be a valid DD/MM/YYYY")

    def postcode_validator(self, postcode):
        pattern = re.compile(r'^[A-Z\d]{2}[\dA-Z]\s[A-Z]{3}$|^[A-Z]{2}[\dA-Z]\s[A-Z]{3}$|^[A-Z]{3}[\dA-Z]\s[A-Z]{3}$')
        if not pattern.match(postcode.data):
            raise ValidationError(f"Invalid postcode, must be XY YXX, XYY YXX or XXY YXX where X is an uppercase "
                                  f"letter and Y is a digit.")

    # assigning validators
    email = EmailField(validators=[Email(), DataRequired()])
    firstname = StringField(validators=[character_check, DataRequired()])
    lastname = StringField(validators=[character_check, DataRequired()])
    phone = StringField(validators=[is_valid_phone_number, DataRequired()])
    password = PasswordField(validators=[Length(min=6, max=12), is_valid_password, DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal!')])
    date_of_birth = StringField(validators=[DataRequired(), date_of_birth_validator])
    postcode = StringField(validators=[DataRequired(), postcode_validator])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = EmailField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    pin = StringField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()


class PasswordForm(FlaskForm):

    def is_valid_password(self, new_password):
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)')
        if not pattern.match(new_password.data):
            raise ValidationError(
                f"Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit and 1 "
                f"special character.")

    current_password = PasswordField(id='password', validators=[DataRequired()])
    show_password = BooleanField('Show password', id='check')
    new_password = PasswordField(
        validators=[DataRequired(), Length(min=6, max=12, message="Must be between 6 and 12 characters in length"),
                    is_valid_password])
    confirm_new_password = PasswordField(
        validators=[DataRequired(), EqualTo('new_password', message='Both new password fields must be equal')])
    submit = SubmitField('Change Password')
