#!/usr/bin/env python3
'''handles all visualisation types'''

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

visualizations_bp = Blueprint('visualizations', __name__)

# Define recommended visualizations for different data types
RECOMMENDED_VISUALIZATIONS = {
    'numeric': ['Scatter Plot', 'Line Chart', 'Histogram', 'Box Plot'],
    'categorical': ['Bar Chart', 'Pie Chart'],
    'datetime64[ns]': ['Timeseries Line Plot'],
    'object': ['Treemap'],
}

# Function to recommend visualizations based on selected columns and data types
def recommend_visualization(selected_columns, data_types):
    recommendations = set()

    for col in selected_columns:
        data_type = data_types.get(col)
        if data_type:
            recommendations.update(RECOMMENDED_VISUALIZATIONS.get(data_type, []))

    return list(recommendations)

@visualizations_bp.route('/visualize', methods=['GET', 'POST'])
@login_required
def visualize():
    if request.method == 'POST':
        selected_columns = request.form.getlist('selected_columns')
        data_types = request.form.getlist('data_types')

        if not selected_columns or not data_types:
            flash("Please select columns and data types.", 'danger')
            return redirect(url_for('visualizations.visualize'))

        # Use the recommend_visualization function to get recommendations
        recommendations = recommend_visualization(selected_columns, data_types)

        if not recommendations:
            flash("No suitable visualizations found for the selected columns and data types.", 'danger')
            return redirect(url_for('visualizations.visualize'))

        return render_template('visualize.html', recommendations=recommendations)

    return render_template('visualize.html')

#routes for different types of visualizations

@visualizations_bp.route('/scatter_plot', methods=['GET'])
@login_required
def scatter_plot():
    # logic to generate a scatter plot based on user's data
    data = get_user_uploaded_data(current_user.id)

    if 'x_column' in request.args and 'y_column' in request.args:
        x_column = request.args['x_column']
        y_column = request.args['y_column']

        scatter_plot_img = generate_scatter_plot(data, x_column, y_column)
        return render_template('scatter_plot.html', scatter_plot_img=scatter_plot_img)

    flash("Please select columns to generate a scatter plot.", 'danger')
    return redirect(url_for('visualizations.visualize'))

def generate_scatter_plot(data, x_column, y_column):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x_column, y=y_column)
    plt.title(f'Scatter Plot: {x_column} vs {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)
    plt.tight_layout()

    #saviing the plot to image and encode it as base64 for render template
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    scatter_plot_img = base64.b64encode(img.read()).decode('utf-8')

    return scatter_plot_img

@visualizations_bp.route('/line_chart', methods=['GET'])
@login_required
def line_chart():
    #code to generate a line chart based on user's data
    data = get_user_uploaded_data(current_user.id)

    if 'x_column' in request.args and 'y_column' in request.args:
        x_column = request.args['x_column']
        y_column = request.args['y_column']

        line_chart_img = generate_line_chart(data, x_column, y_column)
        return render_template('line_chart.html', line_chart_img=line_chart_img)

    flash("Please select columns to generate a line chart.", 'danger')
    return redirect(url_for('visualizations.visualize'))

def generate_line_chart(data, x_column, y_column):
    plt.figure(figsize=(10, 5))
    plt.plot(data[x_column], data[y_column], marker='o', linestyle='-', color='b'

    # chart labels and title
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Line Chart: {y_column} vs {x_column}')

    # Converting the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    line_chart_img = base64.b64encode(img.getvalue()).decode()

    return line_chart_img

@visualizations_bp.route('/histogram', methods=['GET'])
@login_required
def histogram():
    #code to generate a histogram based on user's data
    data = get_user_uploaded_data(current_user.id)

    if 'column' in request.args:
        column = request.args['column']

        histogram_img = generate_histogram(data, column)
        return render_template('histogram.html', histogram_img=histogram_img)

    flash("Please select a column to generate a histogram.", 'danger')
    return redirect(url_for('visualizations.visualize'))

def generate_histogram(data, column):
    plt.figure(figsize=(10, 5))
    plt.hist(data[column], bins=10, color='skyblue', edgecolor='black')

    #chart labels and title
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'Histogram: {column}')

    # Converting the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    histogram_img = base64.b64encode(img.getvalue()).decode()

    return histogram_img

@visualizations_bp.route('/box_plot', methods=['GET'])
@login_required
def box_plot():
    # Code to get user's data
    data = get_user_uploaded_data(current_user.id)

    if 'column' in request.args:
        column = request.args['column']

        box_plot_img = generate_box_plot(data, column)
        return render_template('box_plot.html', box_plot_img=box_plot_img)

    flash("Please select a column to generate a box plot.", 'danger')
    return redirect(url_for('visualizations.visualize'))

def generate_box_plot(data, column):
    plt.figure(figsize=(10, 5))
    plt.boxplot(data[column], vert=False)

    #chart labels and title
    plt.xlabel(column)
    plt.title(f'Box Plot: {column}')

    # Converting the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    box_plot_img = base64.b64encode(img.getvalue()).decode()

    return box_plot_img

# Route for generating a bar chart
@visualizations_bp.route('/bar_chart', methods=['GET'])
@login_required
def bar_chart():
    # Code to get user's data (replace this with your method)
    data = get_user_uploaded_data(current_user.id)

    if 'x_column' in request.args and 'y_column' in request.args:
        x_column = request.args['x_column']
        y_column = request.args['y_column']

        bar_chart_img = generate_bar_chart(data, x_column, y_column)
        return render_template('bar_chart.html', bar_chart_img=bar_chart_img)

    flash("Please select columns to generate a bar chart.", 'danger')
    return redirect(url_for('visualizations.visualize'))

# Function to generate a bar chart
def generate_bar_chart(data, x_column, y_column):
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_column], data[y_column])

    # Chart labels and title
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Bar Chart: {x_column} vs. {y_column}')

    # Rotating x-axis labels
    plt.xticks(rotation=45)

    # Converting the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    bar_chart_img = base64.b64encode(img.getvalue()).decode()

    return bar_chart_img

# Route for generating a pie chart
@visualizations_bp.route('/pie_chart', methods=['GET'])
@login_required
def pie_chart():
    # Code to get user's data
    data = get_user_uploaded_data(current_user.id)

    if 'category_column' in request.args and 'value_column' in request.args:
        category_column = request.args['category_column']
        value_column = request.args['value_column']

        pie_chart_img = generate_pie_chart(data, category_column, value_column)
        return render_template('pie_chart.html', pie_chart_img=pie_chart_img)

    flash("Please select columns to generate a pie chart.", 'danger')
    return redirect(url_for('visualizations.visualize'))

# Function to generate a pie chart
def generate_pie_chart(data, category_column, value_column):
    plt.figure(figsize=(8, 8))
    plt.pie(data[value_column], labels=data[category_column], autopct='%1.1f%%', startangle=140)

    #chart title
    plt.title(f'Pie Chart: {category_column} Distribution')

    # Converting the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    pie_chart_img = base64.b64encode(img.getvalue()).decode()

    return pie_chart_img

# Route for generating a time series line plot
@visualizations_bp.route('/timeseries_line_plot', methods=['GET'])
@login_required
def timeseries_line_plot():
    # Code to get user's data
    data = get_user_uploaded_data(current_user.id)

    if 'x_column' in request.args and 'y_column' in request.args:
        x_column = request.args['x_column']
        y_column = request.args['y_column']

        timeseries_line_plot_img = generate_timeseries_line_plot(data, x_column, y_column)
        return render_template('timeseries_line_plot.html', timeseries_line_plot_img=timeseries_line_plot_img)

    flash("Please select columns to generate a time series line plot.", 'danger')
    return redirect(url_for('visualizations.visualize'))

# Function to generate a time series line plot
def generate_timeseries_line_plot(data, x_column, y_column):
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_column], data[y_column], marker='o', linestyle='-')

    #chart title and labels
    plt.title(f'Time Series Line Plot: {x_column} vs. {y_column}')
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45)

    # Convertng the chart to an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 to embed in HTML
    timeserieslineplot_img = base64.b64encode(img.getvalue()).decode()

    return timeserieslineplot_img

# Route for generating a treemap
@visualizations_bp.route('/treemap', methods=['GET'])
@login_required
def treemap():
    # Code to get user's data
    data = get_user_uploaded_data(current_user.id)

    if 'labels_column' in request.args and 'values_column' in request.args:
        labels_column = request.args['labels_column']
        values_column = request.args['values_column']

        treemap_html = generate_treemap(data, labels_column, values_column)
        return render_template('treemap.html', treemap_html=treemap_html)

    flash("Please select columns to generate a treemap.", 'danger')
    return redirect(url_for('visualizations.visualize'))

# Function to generate a treemap
def generate_treemap(data, labels_column, values_column):
    import plotly.express as px

    fig = px.treemap(data, path=[labels_column], values=values_column)

    # Encode the plot as HTML
    treemap_html = fig.to_html(full_html=False)

    return treemap_html

