.PHONY: start stop restart logs clean test

start:
	@echo "🚀 Starting Job Search App..."
	@pkill -9 -f "python run.py" 2>/dev/null || true
	@pkill -9 -f "python app.py" 2>/dev/null || true
	@sleep 2
	@python run.py > job_search_app.log 2>&1 &
	@sleep 5
	@echo "✅ App started! Visit http://localhost:5000"

stop:
	@echo "🛑 Stopping Job Search App..."
	@pkill -9 -f "python run.py" 2>/dev/null || true
	@pkill -9 -f "python app.py" 2>/dev/null || true
	@echo "✅ App stopped"

restart: stop start
	@echo "✅ App restarted successfully!"

logs:
	@tail -f job_search_app.log

clean:
	@echo "🧹 Cleaning up..."
	@pkill -9 -f "python run.py" 2>/dev/null || true
	@rm -f job_search_app.log
	@rm -f *.pyc
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

test:
	@echo "🧪 Testing API..."
	@curl -s http://localhost:5000/health || echo "❌ App not running"

status:
	@echo "📊 App Status:"
	@ps aux | grep "python run.py" | grep -v grep || echo "❌ Not running"
	@echo ""
	@curl -s http://localhost:5000/health 2>/dev/null && echo "✅ Health check passed" || echo "❌ Health check failed"
