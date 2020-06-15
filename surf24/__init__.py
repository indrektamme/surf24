import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "superpass"
db = SQLAlchemy(app)
login_manager = LoginManager()
from surf24.core.views import core
from surf24.users.views import users
app.register_blueprint(core)
app.register_blueprint(users)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = "users.login"
