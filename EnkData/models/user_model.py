#!/usr/bin/env python3
'''user model'''

from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    data = db.relationship('Data', backref='uploader', lazy=True)

    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#data model for storing uploasded data
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String(100), nullable=False) #formats of uploaded data
    content = db.Column(db.Text, nullable=False) #actual data contents
    #linking data to user who uploaded it using foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column (db.DateTime, default=datetime.utcnow, nullable=False)
