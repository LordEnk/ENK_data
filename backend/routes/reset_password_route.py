#!/usr/bin/env python3
'''password reset'''
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if the token is valid and hasn't expired
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiration < datetime.utcnow():
        flash('Invalid or expired reset token.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password == confirm_password:
            # Reset the user's password and clear the reset token
            user.password = generate_password_hash(new_password)
            user.reset_token = None
            user.reset_token_expiration = None #clear the token expiration
            db.session.commit()

            flash('Password reset successful. You can now log in with your new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'danger')

    return render_template('reset_password.html', token=token)
