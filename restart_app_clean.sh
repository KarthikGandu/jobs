#!/bin/bash

echo "=========================================="
echo "🔄 Restarting Job Search App (Clean)"
echo "=========================================="
echo ""

# Kill all existing Python processes running the app
echo "1. Killing old sessions..."
pkill -9 -f "python run.py" 2>/dev/null
pkill -9 -f "python app.py" 2>/dev/null
pkill -9 -f "flask run" 2>/dev/null
pkill -9 -f "job_search_app" 2>/dev/null

# Wait to ensure processes are terminated
sleep 2

# Check if any processes are still running
RUNNING=$(ps aux | grep -E "python.*run.py|python.*app.py" | grep -v grep | wc -l)
if [ $RUNNING -gt 0 ]; then
    echo "   ⚠️  Warning: Some processes still running. Force killing..."
    ps aux | grep -E "python.*run.py|python.*app.py" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "   ✓ All old sessions killed"
echo ""

# Start the new app
echo "2. Starting new app session..."
python run.py > job_search_app.log 2>&1 &
APP_PID=$!

echo "   ✓ App started with PID: $APP_PID"
echo ""

# Wait for app to start
echo "3. Waiting for app to initialize..."
sleep 5

# Check if app is running
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "   ✓ App is running successfully!"
    echo ""
    echo "=========================================="
    echo "✅ App Ready!"
    echo "=========================================="
    echo "📍 URL: http://localhost:5000"
    echo "📋 PID: $APP_PID"
    echo "📄 Logs: tail -f job_search_app.log"
    echo "=========================================="
else
    echo "   ✗ App failed to start. Check logs:"
    echo "   tail -20 job_search_app.log"
fi
