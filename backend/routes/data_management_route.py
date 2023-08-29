#!/usr/bin/env python3
'''handles all datamanagement'''

import json
import pandas as pd
import numpy as np
import re
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from models.user_model import User
from models.dataset_model import Dataset

data_management_bp = Blueprint('data_management', __name__)

# Function to handle data entry error correction using regular expressions
def correct_data_entry_errors(df):
    # Define a list of regex patterns and their replacements
    patterns = [
        (r'pattern1', 'replacement1'),
        (r'pattern2', 'replacement2'),
        # Add more patterns as needed
    ]

    # Iterate through all columns and rows
    for column in df.columns:
        for index, value in enumerate(df[column]):
            for pattern, replacement in patterns:
                df.at[index, column] = re.sub(pattern, replacement, str(value))

    return df

# Function to handle data type conversion and date formatting
def convert_data_types_and_format_dates(df):
    # Iterate through all columns and rows
    for column in df.columns:
        for index, value in enumerate(df[column]):
            try:
                # Attempt to convert the value to a date
                date_value = pd.to_datetime(value)
                # If successful, update the cell with the formatted date
                df.at[index, column] = date_value.strftime('%Y-%m-%d')
            except ValueError:
                pass  # Handle non-date values here

            # Handle other data type conversions if needed

    return df

# Detect and handle outliers using the IQR method
def detect_and_handle_outliers(df):
    df_cleaned = df.copy()

    for column in df.columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df_cleaned = df_cleaned[(df_cleaned[column] >= lower_bound) & (df_cleaned[column] <= upper_bound)]

    return df_cleaned

# Route to display data management tasks
@data_management_bp.route('/data-management', methods=['GET', 'POST'])
@login_required
def data_management():
    # Load user-uploaded data from a CSV file (you can adjust the filename)
    try:
        df = pd.read_csv('user_data.csv')
    except FileNotFoundError:
        flash("User data file not found.", 'danger')
        return redirect(url_for('dashboard.user_dashboard'))

    # Identify and correct data entry errors
    df_corrected = identify_and_correct_errors(df)

    # Detect and handle outliers
    df_handled_outliers = detect_and_handle_outliers(df_corrected)

    # Check if outliers were detected
    outliers_detected = not df.equals(df_handled_outliers)

    # Convert the DataFrame to an HTML table for data listing
    data_table = df_handled_outliers.to_html(classes='table table-striped table-bordered')

    return render_template('data_management.html', data_table=data_table, outliers_detected=outliers_detected)

#function to processs data
def process_data(df):
    #aggregating data by column
    aggregated_data = df.groupby('category')['value'].sum().reset_index()
    #renaming columnsto a naming convention
    aggregated_data.rename(columns={'category': 'Category', 'value': 'Total'}, inplace=True)
    return aggregated_data

# Route to list datasets on the user's dashboard
@data_management_bp.route('/dashboard/datasets')
@login_required
def list_datasets():
    # Retrieve datasets uploaded by the current user
    datasets = Dataset.query.filter_by(user_id=current_user.id).all()
    return render_template('list_datasets.html', datasets=datasets)


# Route to clean and update a dataset, including data entry error correction, data type conversion, and date formatting
@data_management_bp.route('/clean-dataset/<int:dataset_id>', methods=['GET', 'POST'])
@login_required
def clean_dataset(dataset_id):
    # Retrieve the dataset by ID
    dataset = Dataset.query.get_or_404(dataset_id)

    if request.method == 'POST':
        # Serialize the data to JSON
        try:
            serialized_data = dataset.data.to_json(orient='records')
        except Exception as e:
            flash('Data cannot be serialized. Please upload data in a serializable format.', 'danger')
            return redirect(url_for('data_management.list_datasets'))

        # Convert the serialized JSON data back to a DataFrame
        cleaned_data = pd.read_json(serialized_data)

        # Handle missing values by removing rows with missing values
        cleaned_data.dropna(inplace=True)

        # Handle duplicates by removing duplicate rows
        cleaned_data.drop_duplicates(inplace=True)

        # Correct data entry errors using regular expressions
        cleaned_data = correct_data_entry_errors(cleaned_data)

        # Handle data type conversion and date formatting
        cleaned_data = convert_data_types_and_format_dates(cleaned_data)

        # Handle outliers using IQR method
        cleaned_data = detect_and_handle_outliers(cleaned_data)

        # Process the data (e.g., date formatting, naming conversion, aggregation)
        cleaned_data = process_data(cleaned_data)

        # Update the dataset's data with cleaned and processed data
        dataset.data = cleaned_data

        # Commit changes to the database
        db.session.commit()

        flash('Dataset cleaned and updated successfully.', 'success')
        return redirect(url_for('data_management.list_datasets'))
    except Exception as e:
        #handles all unexpected errors and provide error messahe
        flash('An error occured while processing the dataset: '+ str(e), 'danger')
        return redirect(url_for('data_management.list_datasets'))

    return render_template('clean_dataset.html', dataset=dataset)
