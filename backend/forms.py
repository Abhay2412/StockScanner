from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
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

class AddFormExchange(FlaskForm):    
    name = StringField('Name', 
    validators=[DataRequired(), Length(min = 2, max = 25)])
    
    location = StringField('Location', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    number_of_tickers = IntegerField('Number of Tickers', 
    validators=[DataRequired()])

    submit = SubmitField('Add Exchange')

class DeleteFormExchange(FlaskForm):    
    name = StringField('Name', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    submit = SubmitField('Delete Exchange')

class UpdateFormExchange(FlaskForm):    
    name = StringField('Name', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    location = StringField('Location', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    number_of_tickers = IntegerField('Number of Tickers', 
    validators=[DataRequired()])

    submit = SubmitField('Update Exchange')

class AddFormBusiness(FlaskForm):    
    business_id = StringField('Business ID', 
    validators=[DataRequired(), Length(min = 2, max = 4)])
    
    address = StringField('Address', 
    validators=[DataRequired(), Length(min = 2, max = 45)])

    founding_date = StringField('Founding Date', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    business_name = StringField('Business Name', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    submit = SubmitField('Add Business')

class DeleteFormBusiness(FlaskForm):    
    business_id = StringField('Business ID', 
    validators=[DataRequired(), Length(min = 2, max = 4)])

    submit = SubmitField('Delete Business')

class UpdateFormBusiness(FlaskForm):    
    business_id = StringField('Business ID', 
    validators=[DataRequired(), Length(min = 2, max = 4)])
    
    address = StringField('Address', 
    validators=[DataRequired(), Length(min = 2, max = 45)])

    founding_date = StringField('Founding Date', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    business_name = StringField('Business Name', 
    validators=[DataRequired(), Length(min = 2, max = 25)])

    submit = SubmitField('Update Business')