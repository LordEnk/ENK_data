#!/usr/bin/env python3
'''Authentication route to handle user logins and signups'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from models import db, User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Route for user login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        guest = Guest.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('auth.profile'))
        elif guest:
            login_user(guest)
            flash('Guest login successful', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Login unsuccessful. Please try again with the correct credentials.', 'danger')

    return render_template('login.html')

# Route for user profile (requires login)
@auth_bp.route('/profile')
@login_required
def profile():
    return 'User profile page'

# Route for user logout (requires login)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Route for user registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check if the registration form has been submitted (POST request)
    if request.method == 'POST':
        # Get the user's email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')
        # Get the username from the form
        username = request.form.get('username')
        # Check if the "is_guest" checkbox is selected
        is_guest = request.form.get('is_guest')

        # If the user has chosen to register as a guest, set the username to 'guest'
        if is_guest:
            username = 'guest'
        # If the user hasn't provided a username and hasn't chosen to register as a guest
        elif not username:
            # Display a warning flash message and redirect back to the registration page
            flash('Please enter a username or choose to register as a guest.', 'warning')
            return redirect(url_for('auth.register'))

        # Check if the email is already registered
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            # Display an error flash message and redirect back to the registration page
            flash('Email already registered. Please use another email.', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the user's password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create a new User object with the provided information
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Display a success flash message and redirect to the login page
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    # If the request method is GET (initial page load), render the registration form
    return render_template('register.html')

