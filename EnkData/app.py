#!/usr/bin/env python3
'''enk_data app'''

from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_user import UserMixin
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'ENK'  # random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ENK:password@localhost/enk_data'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Set the login view to the auth.login route

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_token = db.Column(db.String(32))  # Add reset_token column
    reset_token_expiration = db.Column(db.DateTime)  # Add reset_token_expiration column

# Register the blueprints
from routes.home_route import home_bp
from routes.auth_routes import auth_bp
from routes.guest_route import guest_bp
from routes.auth_routes import reset_password_route
from routes.dashboard_route import dashboard_bp
from routes.data_management_route import data_management_bp
from routes.visualizations_route import visualizations_bp

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(guest_bp)
app.register_blueprint(reset_password_route)
app.register_blueprint(dashboard_bp)
app.register_blueprint(data_management_bp)
app.register_blueprint(visualizations_bp)

@app.route('/')
def home():
    return render_template('home.html')

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
