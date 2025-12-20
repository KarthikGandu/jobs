#!/bin/bash

echo "🛑 Stopping Job Search App..."
pkill -9 -f "python run.py"
pkill -9 -f "python app.py"
pkill -9 -f "flask run"
pkill -9 -f "job_search_app"
sleep 1
echo "✅ App stopped"
