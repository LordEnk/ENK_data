#!/usr/bin/env python3
'''the flask application'''

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import mysql.connector


app = Flask(__name__)
app.config['SECRETE_KEY'] = 'ENK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ENK:password@localhost/enk_data'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=true, nullable=False)
    password = db.Column(db.String(60), nullable-False)

#flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#route for login
@app.route('login', methods-['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login unsuccesful. pleasecheck your credentials.', 'dnager')

    return render_template('login.html')

#route for profile after logingin
@app.route('/profile')
@login_required
def profile():
    return 'User profile'

if __name__ == '__main__':
    app.run(debug=True)
