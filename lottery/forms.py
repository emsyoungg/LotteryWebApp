from flask import flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange


class DrawForm(FlaskForm):
    def validate(self):
        standard_validators = FlaskForm.validate(self)
        if standard_validators:
            numbers = [self.number1.data, self.number2.data, self.number3.data, self.number4.data, self.number5.data, self.number6.data]
            if len(set(numbers))==6:
                return True
            else:
                self.number1.errors.append('Numbers must be unique.')
        return False

    number1 = IntegerField(id='no1', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    number2 = IntegerField(id='no2', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    number3 = IntegerField(id='no3', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    number4 = IntegerField(id='no4', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    number5 = IntegerField(id='no5', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    number6 = IntegerField(id='no6', validators=[DataRequired("There must be 6 entries"), NumberRange(min=1, max=60, message="Number must be between 1 and 60.")])
    submit = SubmitField("Submit Draw")
