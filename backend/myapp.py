#!/usr/bin/env python3
'''enk_data app'''

from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

#import blueprints from routes
from routes.auth_route import reset_password_route
from routes.home_route import home_bp
from routes.auth_route import auth_bp
from routes.guest_route import guest_bp
from routes.dashboard_route import dashboard_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ENK'  #random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ENK:password@localhost/enk_data'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Set the login view to the auth.login route

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_token = db.Column(db.String(32))  # Add reset_token column
    reset_token_expiration = db.Column(db.DateTime)  # Add reset_token_expiration column

# Initialize Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register the blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(guest_bp)
app.register_blueprint(reset_password_route.auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)
