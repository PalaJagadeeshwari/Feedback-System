from flask_wtf  import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email
from fbproject.models import User, Event
	
class EventForm(FlaskForm):
	name = StringField("Eventname", validators = [DataRequired()])
	courses= StringField('Courses',validators = [DataRequired()], render_kw = {"placeholder" : "Example: Python, C, C++"})
	regopen=DateField("Regopen",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	regclose=DateField("Regclose",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	description=TextAreaField("Description",validators = [DataRequired()],render_kw = { 'cols' :80, 'rows' : 10})
	place=TextField("Place",validators = [DataRequired()])
	date=DateField("Date of Event",validators = [DataRequired()], render_kw = {"placeholder" : "dd/mm/yyyy"})
	status = SelectField("Status", choices = [(0, "Not Open"), (1, "Registrations Open"), (2, "Registrations Closed"), (3, "Event Completed")])


class RegistrationForm(FlaskForm):
	# choices = Event.query.filter_by(id = self.id).first().course.split()
	rollno = StringField("Roll No.", validators=[DataRequired()])
	name = StringField("Name", validators = [DataRequired(), Length(min=3, max=50)])
	email = StringField("Email", validators = [DataRequired(), Email()])
	coursename = SelectMultipleField("Coursename", validators = [DataRequired()])
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

class FeedbackForm(FlaskForm):
	by= StringField("Roll No.: ", validators = [DataRequired()], render_kw = {"placeholder" : "Enter your Roll No."})
	email  = StringField("Email: ", validators = [DataRequired(), Email()], render_kw = {"placeholder" : "Enter your Email"})
	msg = TextAreaField("Feedback: ", validators = [DataRequired()], render_kw = {"placeholder" : "Enter your Feedback Message...", 'cols' :80, 'rows' : 10})



class LogInForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired()])
	password = PasswordField("Password", validators = [DataRequired()])
	remember = BooleanField("Remember me")
	login = SubmitField("Log In")

	
	




class RequestResetForm(FlaskForm):
	email= StringField("Email", validators = [DataRequired(),Email()])
	submit = SubmitField("request reset Password")


	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('that email is taken please take a diff one')
		if user is None:
			raise ValidationError('there is no account with that email.you must register first')

class ResetPasswordForm(FlaskForm):	
    password=PasswordField("NewPassword",validators=[DataRequired()])
    confirmpassword=PasswordField("ConfirmPassword",validators=[DataRequired()])
    submit = SubmitField("Reset Password")



	
class AddStaffForm(FlaskForm):
    username=StringField("Username", validators = [DataRequired()])
    name = StringField("Name", validators = [DataRequired()])
    email= StringField("Email", validators = [DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    



class ChangePasswordForm(FlaskForm):
    oldpassword=PasswordField("OldPassword",validators=[DataRequired()])
    newpassword=PasswordField("NewPassword",validators=[DataRequired()])
    confirmpassword=PasswordField("ConfirmPassword",validators=[DataRequired()])
    submit = SubmitField("Change Password")


