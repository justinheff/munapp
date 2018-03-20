
## TODO: right now if more than 1 validator fails both messages print in a weird list


from string import punctuation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


## Test used in RegistrationForm that checks password for a special character
def SpecialChar(form, field):
    if len(set(punctuation).intersection(field.data)) < 1:
        ## TODO: Find a better error message
        raise ValidationError('Field must contain atleast 1 special character!')

## Create child of FLaskForm that defines a template for the registration form.
## Using flask_wtf gives us extra functionality when it comes to security and
## validation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])#, Length(min=8), SpecialChar])
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TopicForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    body = StringField('Body',validators=[DataRequired()])
    submit = SubmitField('Submit')
	
class CommentForm(FlaskForm):
    comment = StringField('Comment',validators=[DataRequired()])
    submit = SubmitField('Submit')
