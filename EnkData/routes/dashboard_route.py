#!/usr/bin/env python3
'''route to the dashboard for registered users'''

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.user_model import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def user_dashboard():
    user = User.query.filter_by(id=current_user.id).first()  # Retrieve the logged-in user
    username = user.username
    email = user.email

    return render_template('user_dashboard.html', username=username, email=email)

