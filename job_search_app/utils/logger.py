"""
Logging configuration for the application
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(app):
    """
    Configure application logging with both file and console handlers
    
    Args:
        app: Flask application instance
    """
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    if not app.testing:
        log_file = Path(app.config['LOG_FILE'])
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    
    # Add console handler
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Suppress overly verbose loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    app.logger.info(f'{app.config["APP_NAME"]} logger initialized')
