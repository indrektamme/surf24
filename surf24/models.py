from surf24 import db
from flask_login import UserMixin
from enum import Enum

class oauth(Enum):
    NONE
    GOOGLE
    TWITTER
    FACEBOOK
    INSTAGRAM

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    oauth = db.Column(db.Enum(oauth))
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile_image.png')

class Advert(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id), nullable=False)
    date
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    price =
    condition =
    location =

class Image(db.Model):
    adverts = db.relationship(Advert)
    id = db.Column(db.Integer, primary_key=True, index=True)
    advert_id = db.Column(db.Integer, db.ForeignKey(adverts.id), nullable=False)
    image = db.Column(db.String(20), nullable=False)
