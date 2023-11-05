from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError;
import re;


def character_check(self, field):
    exclude_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in field.data:
        if char in exclude_chars:
            raise ValidationError(f"Character {char} is not allowed.")

def is_valid_phone_number(self, phone):
    pattern = re.compile(r'^\d{4}-\d{3}-\d{4}$')
    if not pattern.match(phone.data):
        raise ValidationError(f"Phone number must be in form XXXX-XXX-XXXX")



class RegisterForm(FlaskForm):
    email = EmailField(validators=[Email()])
    firstname = StringField(validators=[character_check])
    lastname = StringField(validators=[character_check])
    phone = StringField(validators=[is_valid_phone_number])
    password = PasswordField()
    confirm_password = PasswordField()
    submit = SubmitField()
