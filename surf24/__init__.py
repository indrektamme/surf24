import os
from flask import Flask, session, g, request, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_babel import Babel
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, gettext, ngettext, lazy_gettext


app = Flask(__name__)
app.config.from_pyfile('mysettings.cfg')
#app.config.from_object(Config)
babel = Babel(app)
#app.config.update(SECRET_KEY=os.urandom(24))
app.config['BABEL_DEFAULT_LOCALE'] = "de"
app.config['SECRET_KEY'] = "superpass"
app.config['SESSION_TYPE'] = 'filesystem'
#app.secret_key = os.urandom(24)

app.config.from_object(__name__)

babel = Babel(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SESSION_TYPE = 'filesystem'
Session(app)

# @babel.localeselector
# def get_locale():
#     # if a user is logged in, use the locale from the user settings
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.locale
#     # otherwise try to guess the language from the user accept
#     # header the browser transmits.  We support de/fr/en in this
#     # example.  The best match wins.
#     return request.accept_languages.best_match(['de', 'fr', 'en', 'ee'])


@babel.localeselector
def get_locale():
    #return 'de'
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
        print("siin")
    print(g.lang_code)
    return g.lang_code

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@app.route('/')
def home():
    g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return redirect(url_for('multilingual.index'))


login_manager = LoginManager()
from surf24.core.views import core
from surf24.users.views import users
from surf24.users.views import google_blueprint
from surf24.ads.views import ads
from surf24.categories.views import categories
from surf24.multilingual import multilingual
app.register_blueprint(multilingual)
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(ads)
app.register_blueprint(categories)

Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = "users.login"
