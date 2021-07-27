from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired, ValidationError
from task.models import User


class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user= User.query.filter_by(username=username_to_check.data).first()
        if user :
            raise ValidationError("this username already exists")


    def validate_email(self,email_to_check):
        user= User.query.filter_by(email=email_to_check.data).first()
        if user :
            raise ValidationError("this email already exists")
    

    username=StringField(label="Username",validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label="Email",validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password' , validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password1')])
    submit=SubmitField(label='Submit')


class LoginForm(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired()])
    password=PasswordField(label='Password',validators =[DataRequired()])
    submit=SubmitField(label='Submit')


class TaskForm(FlaskForm):
    taskname=StringField(label="Username",validators=[DataRequired()])
    schedule_date=StringField(label="Username",validators=[DataRequired()])
    submit=SubmitField(label='Submit')