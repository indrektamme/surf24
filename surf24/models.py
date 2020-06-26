from surf24 import db, login_manager
from flask_login import UserMixin
from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class oauth(Enum):
    NONE=0
    GOOGLE=1
    TWITTER=2
    FACEBOOK=3
    INSTAGRAM=4

class condition(Enum):
    NONE=0
    OLD=1
    USED=2
    NEW=3

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(30), unique=True, index=True)
    phone = db.Column(db.String(15), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    oauth = db.Column(db.Enum(oauth))
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile_image.png')
    adverts = db.relationship('Advert', backref='author', lazy=True)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"UserName: {self.username}"

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Advert(db.Model):
    __tablename__ = 'adverts'
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Numeric(10,2))
    condition = db.Column(db.Enum(condition))
    location = db.Column(db.String(20))
    hide = db.Column(db.Boolean, default=False, nullable=False)
    images = db.relationship('Picture', backref='picture', lazy=True)
    categories = db.relationship('AdvertCategory', backref='category', lazy=True)

class Picture(db.Model):
    __tablename__ = 'images'
    adverts = db.relationship(Advert)
    id = db.Column(db.Integer, primary_key=True, index=True)
    advert_id = db.Column(db.Integer, db.ForeignKey('adverts.id'), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20))
    order = db.Column(db.Integer)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20))
    parent = db.Column(db.Integer)
    order = db.Column(db.Integer)

class AdvertCategory():
    __tablename__ = 'advert_category'
    adverts = db.relationship(Advert)
    id = db.Column(db.Integer, primary_key=True, index=True)
    advert_id = db.Column(db.Integer, db.ForeignKey('adverts.id'), nullable=False)
