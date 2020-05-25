import os
import csv

from datetime import datetime
from fbproject.forms import (RegistrationForm, LogInForm, ForgotPasswordForm,
	EventForm, AddStaffForm, FeedbackForm, ChangePasswordForm)

from flask import render_template, url_for, redirect, flash, request
from fbproject import app, db, bcrypt
from fbproject.models import Event, Registration, Feedback, User

from flask_login import login_user, current_user, logout_user

@app.route("/")
def home():
	all_events = Event.query.filter_by(status = 1).all()
	return render_template("userhome.html", events = all_events)

@app.route("/futureevennts")
def future_events():
	events = Event.query.filter_by(status = 0).all()
	return render_template('future events.html', events = events)



@app.route("/pastevents/")
def past_events():
	events = Event.query.filter_by(status = 2)
	completed_events = Event.query.filter_by(status = 3).all()
	return render_template('past events.html', events = events, completed_events = completed_events)

@app.route("/<int:id>/submitfeedback/", methods = ['GET', 'POST'])
def submit_feedback(id):
	form = FeedbackForm()
	if request.method == "POST":
		email = request.form['email']
		by = request.form['by']
		msg = request.form['msg']
		event = id
		feedback = Feedback(email = email, by = by, event = event, msg = msg)
		db.session.add(feedback)
		db.session.commit()
		return redirect(url_for("home"))
	event = Event.query.filter_by(id = id).first()
	return render_template("feedback page.html", form = form, event = event)


@app.route("/about")
def about():
     return render_template("about.html")

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
	return render_template("register.html", form= form, event = event)




@app.route("/admin/login",methods=['GET','POST'])
def login():
	form = LogInForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			return redirect(url_for("admin_home"))
		else:
			flash("Invalid username or password")
	return render_template("admin/login.html", form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/admin/forgotpassword")
def forgotpassword():
	form = ForgotPasswordForm()
	return render_template("admin/forgot pswd.html", form = form)

@app.route("/admin/")
def admin_home():
	return render_template("admin/admin home.html")

@app.route("/admin/changepassword", methods=["GET", "POST"])
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.get(current_user.id)
		if user and bcrypt.check_password_hash(user.password, form.oldpassword.data):
			if form.newpassword.data == form.confirmpassword.data:
				new_password = bcrypt.generate_password_hash(form.newpassword.data)
				user.password = new_password.decode('utf-8')
				db.session.commit()
				flash("Passsword Changed Successfully")
				return redirect(url_for("admin_home"))
			else:
				flash("Password Mismatch")
		else:
			flash("Wrong Current Password")
	return render_template("admin/change pwd.html", form = form)

@app.route("/admin/eventcreation",methods=['GET','POST'])
def eventcreation():
	form = EventForm()
	if request.method=="POST":
		eventname=request.form['name']
		course=request.form['courses']
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
		status = request.form['status']
		print(status)
		event = Event(name = eventname, courses = course, regopen = regopen, description = description, regclose = regclose, place = place, date = date, status = status)
		db.session.add(event)
		db.session.commit()
		return redirect(url_for('eventcreation'))
	else:
		return render_template("events/eventcreation.html", form = form)

@app.route("/admin/view",methods=['GET','POST'])
def view():
	events = Event.query.all()
	return render_template("events/view.html", events = events)

@app.route("/admin/delete",methods=['GET','POST'])
def delete():
	if request.method == "POST":
		id=request.form['delete']
		flash("Deleted Successfully")
		return redirect(url_for('view'))

@app.route("/admin/<int:id>/edit",methods=['GET','POST'])
def edit(id):
	event = Event.query.filter_by(id = id).first()
	form = EventForm(obj = event)
	if request.method == "POST":
		id=request.form['edit']
		flash("Edited")
		return redirect(url_for("admin_home"))
	return render_template("events/eventedit.html", form = form)

@app.route("/admin/addstaff/")
def addstaff():
	form = AddStaffForm()
	return render_template("admin/add staff.html", form = form)
