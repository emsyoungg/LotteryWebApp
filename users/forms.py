from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError;


def character_check(form, field):
    exclude_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in field.data:
        if char in exclude_chars:
            raise ValidationError(f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    email = EmailField(validators=[Email()])
    firstname = StringField(validators=[character_check])
    lastname = StringField(validators=[character_check])
    phone = StringField()
    password = PasswordField()
    confirm_password = PasswordField()
    submit = SubmitField()
