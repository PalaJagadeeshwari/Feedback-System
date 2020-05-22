from flask_wtf  import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email




class RegistrationForm(FlaskForm):
	rollno = StringField("Roll No.", validators=[DataRequired()])
	name = StringField("Name", validators = [DataRequired(), Length(min=3, max=50)])
	email = StringField("Email", validators = [DataRequired(), Email()])
	eventname=StringField("Eventname", validators = [DataRequired()])
	coursename = StringField("Coursename", validators = [DataRequired()])
	phno=IntegerField("Phno",validators=[DataRequired()])
	colleges = ["AEC -- Aditya Engineering College", "ACET -- Aditya College of Engineering and Technology", "AAA -- Sai Aditya Engineering College" ]
	college = SelectField("College: ", choices = colleges)
	branches = ["CSE-computer science and engg","ECE-Electrical and computer engg","IT-information technology"]
	branch = SelectField("Branch:",choices=branches)
	sections=["Section - A","Section - B","Section - C"]
	section=RadioField("Section:",choices=sections)
	gen=["Male","Female","Others"]
	gender=RadioField("gender:",choices=gen)
	submit = SubmitField("Register")


class LogInForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired()])
	password = PasswordField("Password", validators = [DataRequired()])
	login = SubmitField("Log In")



class EventForm(FlaskForm):
	eventname = StringField("Eventname", validators = [DataRequired()])
	courses=["Python","Machine learning","Deep learning","Meansatck","Internet of Things"]
	courses= BooleanField("Courses",choices=courses)
	submit = SubmitField("EventForm")

class ForgotPasswordForm(FlaskForm):
	email= StringField("Email", validators = [DataRequired(),Email()])
	submit = SubmitField("Forgot Password")
	
class Staffhome(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email= StringField("Email", validators = [DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Staffhome")



class ChangePassword(FlaskForm):
    oldpassword=PasswordField("OldPassword",validators=[DataRequired()])
    newpassword=PasswordField("NewPassword",validators=[DataRequired()])
    confirmpassword=PasswordField("ConfirmPassword",validators=[DataRequired()])
    submit = SubmitField("ChangePassword")



# class UserForm(ModelForm):
#     class Meta:
#         model = Event
#         