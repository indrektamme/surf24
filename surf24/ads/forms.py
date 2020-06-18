from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    price = FloatField('Price', validators=[NumberRange()])
    submit = SubmitField('Post')
