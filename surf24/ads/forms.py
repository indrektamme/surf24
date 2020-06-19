from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional(), NumberRange()])
    submit = SubmitField('Post')

class PicForm(FlaskForm):
    picture1 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture4 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    picture5 = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
