#!/bin/bash

echo "🔄 Restarting Job Search Application..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill old processes
echo "1. Killing old Flask processes..."
pkill -9 -f "python run.py" 2>/dev/null
sleep 1

# Verify they're gone
RUNNING=$(ps aux | grep "python.*run.py" | grep -v grep)
if [ -z "$RUNNING" ]; then
    echo "   ✓ All old processes killed"
else
    echo "   ⚠️  Some processes still running:"
    echo "$RUNNING"
fi

echo ""
echo "2. Starting Flask app..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the app
python run.py
