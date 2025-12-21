"""
Authentication routes - Login, Signup, Logout
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from job_search_app.extensions import db
from job_search_app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        full_name = data.get('full_name', '').strip()
        
        # Validation
        errors = []
        
        if not email or '@' not in email:
            errors.append('Valid email is required')
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        if not full_name:
            errors.append('Full name is required')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        
        if errors:
            if request.is_json:
                return jsonify({'status': 'error', 'errors': errors}), 400
            for error in errors:
                flash(error, 'error')
            return render_template('auth/signup.html')
        
        # Create new user
        user = User(
            email=email,
            username=username,
            full_name=full_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log user in
        login_user(user)
        user.update_last_login()
        
        if request.is_json:
            return jsonify({
                'status': 'success',
                'message': 'Account created successfully',
                'redirect': url_for('main.splash')
            })
        
        flash('Account created successfully! Welcome!', 'success')
        return redirect(url_for('main.splash'))
    
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email_or_username = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        remember = data.get('remember', False)
        
        # Find user by email or username
        user = User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()
        
        if not user or not user.check_password(password):
            error = 'Invalid email/username or password'
            if request.is_json:
                return jsonify({'status': 'error', 'error': error}), 401
            flash(error, 'error')
            return render_template('auth/login.html')
        
        # Log user in
        login_user(user, remember=remember)
        user.update_last_login()
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.splash')
        
        if request.is_json:
            return jsonify({
                'status': 'success',
                'message': 'Logged in successfully',
                'redirect': next_page
            })
        
        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/check')
def check_auth():
    """Check if user is authenticated (for AJAX)"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        })
    return jsonify({'authenticated': False}), 401
