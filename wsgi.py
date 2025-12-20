"""
WSGI entry point for production deployment
"""
import os
from job_search_app.app import create_app

# Determine environment
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == '__main__':
    app.run()
