from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, NoneOf
from flask_wtf.file import FileField, FileAllowed

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional(), NumberRange()])
    submitbutton = SubmitField('Edasi')

class PicForm(FlaskForm):
    picture = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])

class CategoryForm(FlaskForm):
    choices = []
    category1 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=1), Optional()])
    category2 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    category3 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    size = FloatField('Suurus', validators=[NumberRange(min=0), Optional()])
    brand = StringField('Brand', validators=[Optional()])
