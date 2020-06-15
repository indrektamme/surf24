from surf24 import db, login_manager
from flask_login import UserMixin
from enum import Enum
from datetime import datetime

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
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String(30), unique=True, index=True)
    phone = db.Column(db.String(15), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    oauth = db.Column(db.Enum(oauth))
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile_image.png')
    adverts = db.relationship('Advert', backref='author', lazy=True)

class Advert(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    price = db.Column()
    condition = db.Column(db.Enum(condition))
    location = db.Column(db.String(20))
    hide = db.Column(db.Boolean, default=False, nullable=False)
    images = db.relationship('Image', backref='picture', lazy=True)

class Image(db.Model):
    adverts = db.relationship(Advert)
    id = db.Column(db.Integer, primary_key=True, index=True)
    advert_id = db.Column(db.Integer, db.ForeignKey('adverts.id'), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20))
    order = db.Column(db.Integer)
