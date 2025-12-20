"""
Application configuration settings
Supports multiple environments: development, production, testing
"""
import os
from pathlib import Path
from datetime import timedelta


class Config:
    """Base configuration"""
    
    # Application
    APP_NAME = "Job Search Application"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    OUTPUT_DIR = BASE_DIR / "job_results"
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATE_DIR = BASE_DIR / "templates"
    
    # Job Search Settings
    DEFAULT_RESULTS_WANTED = 15
    DEFAULT_DISTANCE = 50
    MAX_RESULTS = 100
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = timedelta(hours=1)
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'job_search_app.log'
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Session
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with this config"""
        # Create necessary directories
        cls.OUTPUT_DIR.mkdir(exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    RATE_LIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        
        # Override with environment variables
        secret_key = os.environ.get('SECRET_KEY')
        if secret_key:
            app.config['SECRET_KEY'] = secret_key
        
        # Validate critical settings
        if not app.config.get('SECRET_KEY') or app.config['SECRET_KEY'] == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production!")


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    RATE_LIMIT_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
