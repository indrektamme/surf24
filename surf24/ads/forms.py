from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional, NoneOf
from flask_wtf.file import FileField, FileAllowed

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional(), NumberRange()])
    submitbutton = SubmitField('Post')

class PicForm(FlaskForm):
    picture1 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture4 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture5 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])

class CategoryForm1(FlaskForm):
    choices = []
    category = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=1)])

class CategoryForm2(FlaskForm):
    choices = []
    category = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=1)])

class CategoryForm3(FlaskForm):
    choices = []
    category = SelectField('valikud', coerce=int, choices = choices, validators=[NumberRange(min=1)])
