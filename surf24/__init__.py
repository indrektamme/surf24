import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_babel import Babel
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
babel = Babel(app)
app.config['SECRET_KEY'] = "superpass"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
from surf24.core.views import core
from surf24.users.views import users
from surf24.users.views import google_blueprint
from surf24.ads.views import ads
from surf24.categories.views import categories
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(ads)
app.register_blueprint(categories)


Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = "users.login"
