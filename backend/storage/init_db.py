#!/usr/bin/env python3
'''creates tables in the database'''

from app import db
from models.user_model import User

def create_tables():
    '''creates all the tables defined in models'''
    db.create_all()
    print('Database tables created successfully')

if __name__ == "__main__":
    create_tables()
