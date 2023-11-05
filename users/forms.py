from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
import re


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
        raise ValidationError(f"Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit and 1 "
                              f"special character.")


def date_of_birth_validator(self, date_of_birth):
    pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$')
    if not pattern.match(date_of_birth):
        raise ValidationError(f"Invalid date, must be DD/MM/YYYY")


class RegisterForm(FlaskForm):
    email = EmailField(validators=[Email(), DataRequired()])
    firstname = StringField(validators=[character_check, DataRequired()])
    lastname = StringField(validators=[character_check, DataRequired()])
    phone = StringField(validators=[is_valid_phone_number, DataRequired()])
    password = PasswordField(validators=[Length(min=6, max=12), is_valid_password, DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password', message='Both password fields '
                                                                                             'must be equal!')])
    date_of_birth = StringField(validators=[DataRequired(), date_of_birth_validator])

    submit = SubmitField()
