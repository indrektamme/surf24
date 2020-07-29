from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, NoneOf
from flask_wtf.file import FileField, FileAllowed

class CategoryForm(FlaskForm):
    choices = []
    category1 = SelectField('Kategooria', coerce=int, choices = choices, validators=[NumberRange(min=1), Optional()])
    category2 = SelectField('Alamkategooria', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    category3 = SelectField('Alamkategooria', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    size = FloatField('Suurus', validators=[NumberRange(min=0), Optional()])
    brand = StringField('Brand', validators=[Optional()])
