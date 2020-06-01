from flask import Flask
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail,Message


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:****/feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = b"edkjfhiefkejbkfjb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USE_TLS']=True

app.config['MAIL_USERNAME'] = "*****"
app.config['MAIL_PASSWORD'] = "*****"
mail=Mail(app)






from fbproject import routes