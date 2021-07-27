from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///task.db"
app.config['SECRET_KEY']="3be1262fa07a7d4617123e40"
db= SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager =LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category='info'


from task import routes