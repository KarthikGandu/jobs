"""
Development server entry point
"""
import os
from job_search_app.app import create_app

# Create app in development mode
app = create_app('development')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*70}")
    print(f"🚀 Job Search Application Starting...")
    print(f"{'='*70}")
    print(f"📍 Local URL:    http://localhost:{port}")
    print(f"📍 Network URL:  http://127.0.0.1:{port}")
    print(f"{'='*70}")
    print(f"Press Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
