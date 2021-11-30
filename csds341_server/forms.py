from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,InputRequired
from models import User

# login form, used in login page
class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

# registration form, used to get registration information
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = PasswordField('First Name', validators=[DataRequired()])
    last_name = PasswordField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Register')
    # make sure email is not empty or duplicate
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# form used to get answer (what user has submitted)
class AnswerForm(FlaskForm):
    answer = TextAreaField('answer', validators=[DataRequired()])
    submit = SubmitField('Save')

# form used to get qustion information submitted by administrator
class QuestionForm( FlaskForm ):
    Tag = StringField('Tag', validators=[DataRequired()])
    Mark = IntegerField('Mark', validators=[DataRequired()])
    Que = TextAreaField('Question', validators=[DataRequired()])
    Stand_answer = TextAreaField('Stand_answer')
    submit = SubmitField('Submit')
