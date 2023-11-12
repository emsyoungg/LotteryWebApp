from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class DrawForm(FlaskForm):

    def is_valid_number(self, number):
        if not (0 < number < 61):
            raise ValidationError(f"Number must be between 1 and 60.")

    number1 = IntegerField(id='no1', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    number2 = IntegerField(id='no2', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    number3 = IntegerField(id='no3', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    number4 = IntegerField(id='no4', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    number5 = IntegerField(id='no5', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    number6 = IntegerField(id='no6', validators=[DataRequired("There must be 6 entries"), is_valid_number])
    submit = SubmitField("Submit Draw")
