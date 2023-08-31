#!/bin/usr/env python3
'''handles uploading data'''

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import app
from models.user_model import User

# Data upload route
@app.route('/upload-data', methods=['GET', 'POST'])
@login_required  # Ensure that only authenticated users can upload data
def upload_data():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'data_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        data_file = request.files['data_file']

        # Check if the user has selected a file
        if data_file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        #saving the file to the user's folder with their ID as the filename
        filename = f'{current_user.id}.csv'  # You can choose a different naming scheme
        data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update the user's data_upload_status in the database
        current_user.data_upload_status = True
        db.session.commit()

        flash('File successfully uploaded', 'success')
        return redirect(url_for('dashboard'))  # Redirect to the dashboard

    return render_template('upload_data.html')
