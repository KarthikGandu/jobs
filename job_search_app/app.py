"""
Application factory for Job Search Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path

from .config import config
from .routes import main_bp, api_bp
from .utils import setup_logger
from .utils.errors import APIError


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
    
    # Initialize extensions
    CORS(app)
    
    # Setup logging
    setup_logger(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
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
