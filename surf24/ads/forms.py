from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    price = FloatField('Price', validators=[NumberRange()])
    submit = SubmitField('Post')

class PicForm(FlaskForm):
    picture = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
