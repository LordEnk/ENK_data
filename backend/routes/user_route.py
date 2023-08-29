#!/usr/bin/env python3
'''show user specific data and content on user kogin'''

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import app
from models.user_model import User

#user dashboard route
@app.route('/dashboard')
@login_required  # Ensure that only authenticated users can access the dashboard
def user_dashboard():
    # Retrieve user-specific data from the database based on current_user.id
    user = User.query.filter_by(id=current_user.id).first()

    if user:
        return render_template('user_dashboard.html', user=user)
    else:

        return render_template('user_not_found.html')
