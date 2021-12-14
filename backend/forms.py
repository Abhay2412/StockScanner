from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min = 2, max = 25)])
    
    email = StringField('Email', 
    validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
    validators=[DataRequired(), Length(min = 8, max = 20)])

    confirm_password = PasswordField('Confirm Password', 
    validators=[DataRequired(), Length(min = 8, max = 20), EqualTo('password')])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):    
    username = StringField('Username', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    password = PasswordField('Password', 
    validators=[DataRequired(), Length(min = 8, max = 20)])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')


class DeleteFormUser(FlaskForm):    
    username = StringField('Username', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    submit = SubmitField('Delete User')

class UpdateFormUser(FlaskForm):    
    username = StringField('Username', 
    validators=[DataRequired(), Length(min = 2, max = 25)])
    
    password = PasswordField('Password', 
    validators=[DataRequired(), Length(min = 8, max = 20)])

    submit = SubmitField('Update User')