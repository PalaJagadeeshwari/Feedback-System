from flask import *
from flask_mysqldb import MySQL
from forms import EventRegistration, LogInForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


import os
import csv

app = Flask(__name__)


app.secret_key = b"dnt tell" # 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'feedback'

db = SQLAlchemy(app)

class Event(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String())
	courses = db.Column(db.String())
	# poster = db.Column(db.Image())
	description = db.Column(db.Text())
	regopen = db.Column(db.DateTime())
	regclose = db.Column(db.DateTime()) 
	date = db.Column(db.DateTime()) 


class User(db.Model)
     username=db.Column(db.String())
     password=db.column(db.String())


class Registration(db.Model)
     rollno=db.Column(db.Integer())
     name=db.Column(db.String())
     email=db.column(db.String())
     eventname=db.Column(db.String())
     coursename=db.Column(db.String())
     phno=db.Column(db.String())
     college=db.Column(db.String())
     branch=db.Column(db.String())
     section=db.Column(db.())
     gender=db.Column(db.())
























all_events = [
	{
		"name" : "Event 1",
		"desc" : "asdfgfrdsfdjbuivybekrbvkbz",
		"status" : "Open"
	},
	{
		"name" : "Event 2",
		"desc" : "asdfgfrdsfdjbuivybekrbvkbz",
		"status" : "Open"
	},
	{
		"name" : "Event 3",
		"desc" : "asdfgfrdsfdjbuivybekrbvkbz",
		"status" : "Open"
	}
]







@app.route("/")
def home():
	# all_events = Event.query.all()
	return render_template("userhome.html", events = all_events)
@app.route("/register",methods=['GET','POST'])
def register():
	form = EventRegistration()
	return render_template("register.html", form= form, title = "Register")

@app.route("/about")
def about():
     return render_template("about.html")

@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
	    uname=request.form['uname']
	    pwd=request.form['pwd']
	form = LogInForm()
	return render_template("login.html", form = form)

@app.route("/admin/eventcreation",methods=['GET','POST'])
def eventcreation():
    if request.method=="POST":
        eventname=request.form['eventname']
        courses=request.form.getlist('courses')
        courses=','.join(courses)
        mycur=myconn.cursor()
        mycur.execute("""insert into event(eventname,courses)values(%s,%s)""",(eventname,courses))
        myconn.commit()
        flash("Registered successfully")

        return redirect(url_for('eventcreation'))
    else:

        return render_template("eventcreation.html")

@app.route("/view",methods=['GET','POST'])
def view():
	
	cur=myconn.cursor()
	cur.execute("select * from event")
	data=cur.fetchall()
	return render_template("view.html",data=data)

@app.route("/delete",methods=['GET','POST'])
def delete():
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from event where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('view'))



@app.route("/edit",methods=['GET','POST'])
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