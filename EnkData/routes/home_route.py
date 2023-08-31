#!/usr/bin/env python3
'''route for home page'''

from flask import Blueprint, render_template, request, session
from flask import redirect, url_for

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Sample data for the home page sofar update later
    home_data = {
        'title': 'Welcome to ENK Data',
        'description': 'This is a system designed to clean and visualize data.',
    }
    #getting current  page from session or default to 0
    current_page = session.get('current_page', 0)
    max_page = 10 #total number of pages in the navigation subject to chnage

    return render_template('home.html', data=home_data, current_page=current_page, max_page=max_page)

@home_bp.route('/navigation/<int:page>')
def navigation (page):
    #updating current page in the session
    session['current_page'] = page
    return redirect(url_for('home.index'))

