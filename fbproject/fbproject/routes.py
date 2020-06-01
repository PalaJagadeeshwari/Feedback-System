import os
import csv
from datetime import datetime
from fbproject.forms import(RegistrationForm, LogInForm, RequestResetForm,
	EventForm, AddStaffForm, FeedbackForm, ChangePasswordForm,ResetPasswordForm)
from flask import render_template, url_for, redirect, flash, request
from fbproject import app,db,bcrypt,mail
from fbproject.models import (Event, Registration, Feedback, User)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail,Message





@app.route("/")
def home():
	all_events = Event.query.filter_by(status = 1).all()
	return render_template("userhome.html", events = all_events)

@app.route("/futureevents")
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
	form.coursename.choices = [(i, i) for i in event.courses.split(",")]
	if request.method=="POST":
		rollno=request.form['rollno']
		name=request.form['name']
		email=request.form['email']
		# coursename=request.form.coursename.data
		coursename = form.coursename.data
		coursename = ",".join(coursename)
		phno=request.form['phno']
		college=request.form['college']
		branch=request.form['branch']
		section=request.form['section']
		gender=request.form['gender']
		registration = Registration(event = event.id, rollno = rollno, coursename = coursename, gender = gender, phno = phno, college = college, branch = branch, section = section)		
		db.session.add(registration)
		db.session.commit()
		return redirect(url_for('home'))
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


@app.route("/admin/")
@login_required
def admin_home():
	return render_template("admin/admin home.html")

@app.route("/admin/viewfeedback")
def viewfeedback():
	feedbacks_list = Feedback.query.all()
	return render_template("events/view feedback.html", feedbacks = feedbacks_list)

@app.route("/admin/viewregistration/")
def viewregistration():
	registrations = Registration.query.all()
	return render_template("events/view registrations.html", registrations = registrations)
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

@app.route("/admin/<int:id>/delete",methods=['GET','POST'])
def delete(id):
	Event.query.filter_by(id = id).delete()
	db.session.commit()
	flash("Deleted Successfully")
	return redirect(url_for('view'))

@app.route("/admin/<int:id>/edit",methods=['GET','POST'])
def edit(id):
	event = Event.query.filter_by(id = id).first()
	form = EventForm(obj = event)
	if request.method == "POST":
	    event.name=request.form['name']
	    event.courses=request.form['courses']
	    y, m, d = list(map(int, request.form['regopen'].split("-")))
	    event.regopen = datetime(y, m, d)
	    y, m, d= list(map(int, request.form['regclose'].split("-")))
	    event.regclose = datetime(y,m,d)
	    y,m,d = list(map(int, request.form['date'].split("-")))
	    event.date = datetime(y,m,d)
	    event.description=request.form['description']
	    event.place=request.form['place']
	    event.status=request.form['status']
	    db.session.commit()
	    flash("Edited")
	    return redirect(url_for("admin_home"))
	return render_template("events/eventedit.html", form = form)

@app.route("/admin/addstaff/",methods=['GET','POST'])
def addstaff():
	form = AddStaffForm()
	if request.method=="POST":
		username=request.form['username']
		name=request.form['name']
		email=request.form['email']
		password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
		u=User(name=name, username = username,email=email,password=password)
		db.session.add(u)
		db.session.commit()
	return render_template("admin/add staff.html", form = form)

@app.route("/admin/viewstaff/")
def viewstaff():
	staff = User.query.all()
	return render_template("admin/viewstaff.html", staff = staff)

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender="noreply@demo.com",recipients=[user.email])
    a = url_for("reset_token", token=token, _external=True)
    msg.body=f'''To Reset Your Password ,visit the following link:
    {a}
    If u did not make this request simply ignore this mail and no chnage swill be made'''
    mail.send(msg)


@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('reset_request'))
	form = RequestResetForm()
	if request.method == "POST":
		print(form.email.data)
		user = User.query.filter_by(email = form.email.data).first()
		if user is None:
			flash("No Such User Exists")
		send_reset_email(user)
		flash('An email has sent with an instructions to reset your password','info')
		return render_template('admin/reset_request.html',form=form)
	return render_template("admin/reset_request.html", form = form)
 	

@app.route("/reset_password/<token>",methods=['GET', 'POST'])
def reset_token(token):
	form=ResetPasswordForm()
	if current_user.is_authenticated:
 		return render_template('adminhome.html')

	user = User.verify_reset_token(token)
	if user is None:
		flash("invalid or expired token",'warning')
		return redirect(url_for('reset_request'))
	if form.validate_on_submit():
	    hashed_password=bcrypt.generate_password_hash( form.password.data).decode(utf-8)
	    user.password=hashed_password
	    db.session.commit()	
	    flash('your password has been updated now you are able to login')
	    return redirect(url_for('login'))
	
	return render_template('admin/reset_token.html',title='Reset Password',form=form)

		