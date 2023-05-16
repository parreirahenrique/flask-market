from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from market.models import User

class RegisterUser(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists.')
        
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('E-mail address already in use.')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password_validation = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginUser(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class UserPassword(FlaskForm):
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password_validation = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Change Password')

class DepositForm(FlaskForm):
    balance = IntegerField(label='Value to Deposit:', validators=[NumberRange(0),DataRequired()])
    submit = SubmitField(label='Deposit Amount')

class DeleteUser(FlaskForm):
    submit = SubmitField(label='Delete User')

class PurchaseItem(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItem(FlaskForm):
    submit = SubmitField(label='Sell Item')