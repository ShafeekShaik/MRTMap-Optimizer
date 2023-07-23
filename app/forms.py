from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PathForm(FlaskForm):
    startpoint = StringField('Start Point', validators=[DataRequired()])
    endpoint = StringField('End Point', validators=[DataRequired()])
    submit = SubmitField('Find My Way')
