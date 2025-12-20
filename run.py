"""
Job Search Application - Main Entry Point
Run with: python run.py
"""
import os
import sys

# Check if another instance is running
def check_existing_instance():
    """Kill any existing instances before starting"""
    import subprocess
    try:
        # Get current process ID
        current_pid = os.getpid()
        
        # Find other Python processes running this app
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.split('\n')
        for line in lines:
            if 'python' in line.lower() and 'run.py' in line and str(current_pid) not in line:
                # Extract PID (second column)
                parts = line.split()
                if len(parts) > 1:
                    old_pid = parts[1]
                    print(f"⚠️  Found old instance (PID: {old_pid}), killing it...")
                    os.system(f'kill -9 {old_pid} 2>/dev/null')
    except Exception as e:
        print(f"Note: Could not check for existing instances: {e}")

# Kill any existing instances
check_existing_instance()

# Now start the app
from job_search_app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Job Search Application Starting...")
    print("="*70)
    print("📍 Local URL:    http://localhost:5000")
    print("📍 Network URL:  http://127.0.0.1:5000")
    print("="*70)
    print("Press Ctrl+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disable reloader to prevent double startup
    )
