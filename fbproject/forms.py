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
	course= StringField('Courses',validators = [DataRequired()], render_kw = {"placeholder" : "Example: Python, C, C++"})
	poster = FileField("Please Add Poster for the Event",validators = [DataRequired()] )
	regopen=DateField("Regopen",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	regclose=DateField("Regclose",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	description=TextAreaField("Description",validators = [DataRequired()])
	place=TextField("Place",validators = [DataRequired()])
	date=DateField("Date of Event",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	status = SelectField("Status", choices = [(0, "Not Open"), (1, "Registrations Open"), (2, "Registrations Closed")])

class ForgotPasswordForm(FlaskForm):
	email= StringField("Email", validators = [DataRequired(),Email()])
	submit = SubmitField("Forgot Password")
	
class AddStaffForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email= StringField("Email", validators = [DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    



class ChangePassword(FlaskForm):
    oldpassword=PasswordField("OldPassword",validators=[DataRequired()])
    newpassword=PasswordField("NewPassword",validators=[DataRequired()])
    confirmpassword=PasswordField("ConfirmPassword",validators=[DataRequired()])
    submit = SubmitField("ChangePassword")



# class UserForm(ModelForm):
#     class Meta:
#         model = Event
#         