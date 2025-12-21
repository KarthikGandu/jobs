"""
Application factory for Job Search Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
import os

from .config import config
from .routes import main_bp, api_bp
from .routes.auth import auth_bp
from .utils import setup_logger
from .utils.errors import APIError
from .extensions import db, login_manager, bcrypt
from .models.user import User


def create_app(config_name='default'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration environment (development, production, testing)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(
        __name__,
        static_folder=str(Path(__file__).parent.parent / 'static'),
        template_folder=str(Path(__file__).parent.parent / 'templates')
    )
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(Path(app.root_path).parent / 'job_search.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Setup logging
    setup_logger(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Import and register resume blueprint
    from .routes.resume import resume_bp
    app.register_blueprint(resume_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    app.logger.info(f'Application initialized in {config_name} mode')
    
    return app


def register_error_handlers(app):
    """Register custom error handlers"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Resource not found',
            'status': 'error'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f'Internal server error: {str(error)}')
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors"""
        app.logger.error(f'Unexpected error: {str(error)}', exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred',
            'status': 'error'
        }), 500
