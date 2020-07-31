from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Optional, NoneOf
from flask_wtf.file import FileField, FileAllowed

class FilterForm(FlaskForm):
    choices = []
    category1 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=1), Optional()])
    category2 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    category3 = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    size = FloatField('min suurus', validators=[NumberRange(min=0), Optional()])
    sizeMax = FloatField('max suurus', validators=[NumberRange(min=0), Optional()])
    brand = StringField('Brand', validators=[Optional()])
    price = FloatField('min hind', validators=[NumberRange(min=0), Optional()])
    priceMax = FloatField('max hind', validators=[NumberRange(min=0), Optional()])
    searchKeyword = StringField('Otsi sõna järgi', validators=[Optional()])
    submitbutton = SubmitField('Otsi')
    hidden_if_form_sent = HiddenField('', validators=[Optional()])
