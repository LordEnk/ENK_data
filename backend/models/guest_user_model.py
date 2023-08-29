#!/usr/bin/env python3
''''guest user model'''
from app import db
from datetime import datetime

class Guest(db.Model):
    '''guest user class'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    data = db.relationship('Data', backref='uploader', lazy=True)

    def __repr__(self):
        return f"Guest('{self.username}', '{self.email}')"
