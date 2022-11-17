from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # Email, password, submit_button
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Validators will always be a list, even if there's only one item in it. Also note the parentheses!
    # DataRequired() validates there is data in the email field
    # Email() validates the email is an "actual" email (aka not something like test@@@gmail)
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

# Creating this user login form class will create the HTML needed in our forms.html