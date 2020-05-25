from flask import Flask


from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:lucifer@123/feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = b"edkjfhiefkejbkfjb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


from fbproject import routes