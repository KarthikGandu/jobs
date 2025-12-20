#!/bin/bash

# Quick restart script for Karthik's Job Search Site

echo "🔄 Restarting application..."
echo ""

# Kill existing process on port 5001
echo "1. Stopping existing server..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
sleep 2

# Start the server
echo "2. Starting server..."
python3 app.py &

sleep 3

# Check if server is running
if curl -s http://localhost:5001/ > /dev/null; then
    echo ""
    echo "✅ Server restarted successfully!"
    echo ""
    echo "🌐 Open: http://localhost:5001"
    echo ""
else
    echo ""
    echo "❌ Server failed to start"
    echo ""
fi
