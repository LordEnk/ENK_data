import os

class Config:
    SECRET_KEY = 'ENK'  # secret key
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Uploads configuration (if you plan to handle file uploads)
    UPLOADS_DEFAULT_DEST = 'uploads'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/uploads/'

