from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, URLField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, URL
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PathForm(FlaskForm):
    startpoint = StringField('Start Point', validators=[DataRequired()])
    endpoint = StringField('End Point', validators=[DataRequired()])
    submit = SubmitField('Find My Way')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class Addstudent(FlaskForm):
    s_name = StringField('Student Name')
    s_id = StringField('Student ID')
    class_code = StringField('Class Code')
    submit = SubmitField('Add')
