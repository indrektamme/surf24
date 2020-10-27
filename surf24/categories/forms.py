from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional, NoneOf
from flask_wtf.file import FileField, FileAllowed

class CategoryForm(FlaskForm):
    choices = []
    category1 = SelectField('Kategooria', coerce=int, choices = choices, validators=[NumberRange(min=1), Optional()])
    category2 = SelectField('Alamkategooria', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    category3 = SelectField('Alamkategooria', coerce=int, choices = choices, validators=[NumberRange(min=0), Optional()])
    size = FloatField('Suurus', validators=[NumberRange(min=0), Optional()])
    brand = StringField('Brand', validators=[Optional()])

class EditCategoryForm(FlaskForm):
    en = StringField('Category name', validators=[Optional()])
    parent = IntegerField('Parent ID', validators=[NumberRange(min=0), Optional()])
    order = IntegerField('Order', validators=[NumberRange(min=0), Optional()])
    et = StringField('Estonian', validators=[Optional()])
    ru = StringField('Estonian', validators=[Optional()])
    es = StringField('Estonian', validators=[Optional()])
    submitbutton = SubmitField('Save')
