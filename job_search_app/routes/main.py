"""
Main routes - serves frontend pages
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')


@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Job Search Application is running'}, 200
