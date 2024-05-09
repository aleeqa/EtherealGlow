from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    text = TextAreaField('Feedback', validators=[DataRequired()])
    product_name = TextAreaField('Skincare Product', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')