from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from fbproject import db, login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Event(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String())
	courses = db.Column(db.String())
	
	description = db.Column(db.Text())
	regopen = db.Column(db.DateTime())
	regclose = db.Column(db.DateTime()) 
	date = db.Column(db.DateTime())
	place = db.Column(db.String())
	status =  db.Column(db.Integer(), default = 0)
	def __str__(self):
		return self.name

class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key = True)
	username=db.Column(db.String())
	password=db.Column(db.String())
	name = db.Column(db.String())
	email=db.Column(db.String())
	

	def __str__(self):
		return self.username
	def get_reset_token(self, expires_sec=1800):
		s=Serializer(app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s=Serializer(app.config['SECRET_KEY'])
		try:
			user_id=s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)



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
