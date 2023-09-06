from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__, template_folder='templates')

@landing_bp.route('/')
def landing():
    return render_template('landing.html')

