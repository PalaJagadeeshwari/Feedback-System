from fbproject import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Event.query.get(id = int(user_id))

class Event(db.Model, UserMixin):
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
	email = db.Column(db.String())
	event=db.Column(db.Integer(),db.ForeignKey("event.id"), nullable = False)
	msg= db.Column(db.String())
