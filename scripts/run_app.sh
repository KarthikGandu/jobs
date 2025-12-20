#!/bin/bash

# Karthik's Job Search Site - Startup Script

echo "=========================================="
echo "  Karthik's Job Search Site"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip install flask flask-cors pandas
fi

# Create necessary directories
mkdir -p templates
mkdir -p static
mkdir -p job_results

# Start the Flask application
echo "Starting the web application..."
echo ""
echo "🌐 Open your browser and go to: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 app.py
