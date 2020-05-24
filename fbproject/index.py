from flask import *
from datetime import datetime
from forms import RegistrationForm, LogInForm, ForgotPasswordForm, EventForm, AddStaffForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import csv

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:lucifer@123/feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = b"edkjfhiefkejbkfjb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class Event(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String())
	courses = db.Column(db.String())
	# poster = db.Column(db.BLOB())
	description = db.Column(db.Text())
	regopen = db.Column(db.DateTime())
	regclose = db.Column(db.DateTime()) 
	date = db.Column(db.DateTime())
	place = db.Column(db.String())
	status =  db.Column(db.Integer(), default = 0)
	def __str__(self):
		return self.name

class User(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	username=db.Column(db.String())
	password=db.Column(db.String())
	name = db.Column(db.String())

	def __str__(self):
		return self.username


class Registration(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	rollno=db.Column(db.Integer())
	name=db.Column(db.String())
	email=db.Column(db.String())
	coursename=db.Column(db.String())
	phno=db.Column(db.String())
	college=db.Column(db.String())
	branch=db.Column(db.String())
	section=db.Column(db.String())
	gender=db.Column(db.String())
	event = db.Column(db.Integer(), db.ForeignKey("event.id"), nullable = False)


class Feedback(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	by=db.Column(db.String())
	event=db.Column(db.Integer(),db.ForeignKey("event.id"), nullable = False)
	message= db.Column(db.String())









@app.route("/")
def home():
	all_events = Event.query.all()
	# for event in all_events:
	# 	event.poster = base64.b64encode(file_data.DATA).decode('ascii')
	return render_template("userhome.html", events = all_events)

@app.route("/register/<int:id>/",methods=['GET','POST'])
def register(id):
	form = RegistrationForm()
	event = Event.query.filter_by(id = id).first()
	if request.method=="POST":
		rollno=request.form['rollno']
		name=request.form['name']
		email=request.form['email']
		coursename=request.form['coursename']
		phno=request.form['phno']
		college=request.form['college']
		branch=request.form['branch']
		section=request.form['section']
		gender=request.form['gender']
		
		
		registration = Registration(event = event.id, rollno = rollno, coursename = coursename, gender = gender, phno = phno, college = college, branch = branch, section = section)
		db.session.add(registration)
		db.session.commit()
		return redirect("url_for('home')")
	return render_template("register.html", form= form, title = "Register", event = event)

@app.route("/about")
def about():
     return render_template("about.html")

@app.route("/admin/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
	    uname=request.form['username']
	    pwd=request.form['password']
	    return redirect(url_for("admin_home"))
	form = LogInForm()
	return render_template("login.html", form = form)

@app.route("/admin/")
def admin_home():
	return render_template("admin home.html")
@app.route("/admin/forgotpassword")
def forgotpassword():
	form = ForgotPasswordForm()
	return render_template("forgot pswd.html", form = form)



@app.route("/admin/eventcreation",methods=['GET','POST'])
def eventcreation():
	form = EventForm()
	if request.method=="POST":
		eventname=request.form['eventname']
		course=request.form['course']
		# poster=request.form['poster']
		# print(poster)
		d, m, y = list(map(int, request.form['regopen'].split("/")))
		regopen = datetime(y, m, d)
		d, m, y = list(map(int, request.form['regclose'].split("/")))
		regclose = datetime(y,m,d)
		description=request.form['description']
		place=request.form['place']
		d, m, y = list(map(int, request.form['date'].split("/")))
		date = datetime(y,m,d)
		event = Event(name = eventname, courses = course, regopen = regopen, description = description, regclose = regclose, place = place, date = date)
		db.session.add(event)
		db.session.commit()
		return redirect(url_for('eventcreation'))
	else:
		return render_template("eventcreation.html", form = form)

@app.route("/admin/view",methods=['GET','POST'])
def view():
	return render_template("view.html")

@app.route("/admin/delete",methods=['GET','POST'])
def delete():
	if request.method == "POST":
		id=request.form['delete']
		flash("Deleted Successfully")
		return redirect(url_for('view'))



@app.route("/admin/edit",methods=['GET','POST'])
def edit():
	if request.method == "POST":
		id=request.form['edit']
		
		return render_template("eventedit.html")

	return "KJUHKJHKJW"

@app.route("/admin/addstaff/")
def addstaff():
	form = AddStaffForm()
	return render_template("add staff.html", form = form)

if __name__=="__main__":
        app.run(debug=True)