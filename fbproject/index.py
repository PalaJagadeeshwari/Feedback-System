from flask import *
from forms import RegistrationForm, LogInForm, ForgotPasswordForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import csv

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:lucifer@123/feedback"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = b"edkjfhiefkejbkfjb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class Event(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String())
	courses = db.Column(db.String())
	# poster = db.Column(db.Image())
	description = db.Column(db.Text())
	regopen = db.Column(db.DateTime())
	regclose = db.Column(db.DateTime()) 
	date = db.Column(db.DateTime()) 
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



@app.route("/")
def home():
	all_events = Event.query.all()
	return render_template("userhome.html", events = all_events)

@app.route("/register/<int:id>/",methods=['GET','POST'])
def register(id):
	form = RegistrationForm()
	event = Event.query.filter_by(id = id).first()
	return render_template("register.html", form= form, title = "Register", event = event)

@app.route("/about")
def about():
     return render_template("about.html")

@app.route("/admin/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
	    uname=request.form['uname']
	    pwd=request.form['pwd']
	form = LogInForm()
	return render_template("login.html", form = form)

@app.route("/admin/forgotpassword")
def forgotpassword():
	form = ForgotPasswordForm()
	return render_template("forgot pswd.html", form = form)



@app.route("/admin/eventcreation",methods=['GET','POST'])
def eventcreation():
    if request.method=="POST":
        eventname=request.form['eventname']
        courses=request.form.getlist('courses')
        courses=','.join(courses)
        flash("Registered successfully")

        return redirect(url_for('eventcreation'))
    else:

        return render_template("eventcreation.html")

@app.route("/admin/view",methods=['GET','POST'])
def view():
	return render_template("view.html",data=data)

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
		cur=myconn.cursor()
		cur.execute("select * from event where sno=%s"%(id))
		data=cur.fetchall()
		courses=data[0][-1].split(',')
		return render_template("eventedit.html",data=data,courses= courses)

	return "KJUHKJHKJW"



if __name__=="__main__":
        app.run(debug=True)