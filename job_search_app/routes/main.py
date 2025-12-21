"""
Main routes - serves frontend pages
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page - redirect based on auth status"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/splash')
@login_required
def splash():
    """Splash screen after login"""
    return render_template('splash.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main application dashboard"""
    return render_template('dashboard.html')


@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Job Search Application is running'}, 200
