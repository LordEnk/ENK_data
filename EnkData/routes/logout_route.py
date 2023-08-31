#!/usr/bin/env python3
'''Handles the user logout'''

from flask import redirect, url_for, flash
from flask_login import logout_user, login_required
from app import app  # Assuming you have created a Flask app object

# Logout route
@app.route('/logout')
@login_required  # Ensure that only authenticated users can log out
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to the home page
