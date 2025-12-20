# Migration Guide: From Old to New Structure

This guide helps you migrate from the old `app.py` to the new professional structure.

## What Changed?

### Old Structure
```
├── app.py                    # Everything in one file (361 lines)
├── company_scraper.py
├── job_matcher.py
├── keyword_expander.py
├── static/
├── templates/
└── requirements.txt
```

### New Structure
```
├── job_search_app/           # Organized application package
│   ├── __init__.py
│   ├── app.py               # Application factory
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── routes/              # Separated routes
│   │   ├── __init__.py
│   │   ├── main.py          # Frontend routes
│   │   └── api.py           # API routes
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── job_matcher.py
│   │   ├── keyword_expander.py
│   │   └── company_scraper.py
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── errors.py
│   ├── static/              # Static files
│   └── templates/           # HTML templates
├── wsgi.py                  # Production entry point
├── run.py                   # Development entry point
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose
└── requirements.txt         # Updated dependencies
```

## Benefits of New Structure

✅ **Separation of Concerns**: Routes, logic, config are separate  
✅ **Environment Management**: Dev/prod configs built-in  
✅ **Error Handling**: Professional error responses  
✅ **Input Validation**: All inputs validated  
✅ **Logging**: Structured logging with rotation  
✅ **Testing**: Easy to test individual components  
✅ **Deployment**: Docker, CI/CD ready  
✅ **Scalability**: Clean architecture for growth  

## Migration Steps

### Step 1: Keep Old Files (Backup)
```bash
# Backup old structure
mkdir backup_old_structure
cp app.py company_scraper.py job_matcher.py keyword_expander.py backup_old_structure/
```

### Step 2: Understand the New Structure

#### Old Way (app.py)
```python
# Everything in one file
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_jobs():
    # Implementation here
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

#### New Way (Organized)
```python
# Application Factory (job_search_app/app.py)
from flask import Flask
from .config import config
from .routes import main_bp, api_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app

# Routes (job_search_app/routes/main.py)
from flask import Blueprint, render_template
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# API Routes (job_search_app/routes/api.py)
from flask import Blueprint, request, jsonify
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/search', methods=['POST'])
def search_jobs():
    # Implementation here
    pass

# Entry Point (run.py)
from job_search_app.app import create_app
app = create_app('development')

if __name__ == '__main__':
    app.run()
```

### Step 3: Update Import Statements

#### Old Imports
```python
from job_matcher import JobMatcher
from keyword_expander import KeywordExpander
from company_scraper import CompanyScraper
```

#### New Imports
```python
from job_search_app.services import JobMatcher, KeywordExpander, CompanyScraper
```

### Step 4: Run Migration Script

The services (job_matcher, keyword_expander, company_scraper) have been automatically copied to the new structure. They work as-is!

### Step 5: Update How You Run the App

#### Old Way
```bash
python app.py
# or
gunicorn app:app
```

#### New Way
```bash
# Development
python run.py

# Production
gunicorn wsgi:app
```

### Step 6: Update Environment Variables

#### Old Way
```python
# Hardcoded in app.py
app.secret_key = 'some-secret-key'
app.debug = True
```

#### New Way
```bash
# .env file
FLASK_ENV=development
SECRET_KEY=your-secret-key
LOG_LEVEL=DEBUG
```

## API Compatibility

### ✅ All Endpoints Remain the Same!

The API endpoints haven't changed, so existing clients work without modification:

```bash
# These still work exactly the same
POST /api/search
GET /api/companies
POST /api/companies/<name>/jobs
POST /api/match
POST /api/expand-keywords
GET /api/download/<filename>
```

## Configuration Changes

### Old Configuration (Hardcoded)
```python
# In app.py
app = Flask(__name__)
CORS(app)
OUTPUT_DIR = Path("job_results")
```

### New Configuration (Flexible)
```python
# job_search_app/config/settings.py
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
```

## Testing Migration

### 1. Test Old App Still Works
```bash
python app.py  # Old way
curl http://localhost:5000/health
```

### 2. Test New App Works
```bash
python run.py  # New way
curl http://localhost:5000/health
```

### 3. Compare Responses
Both should return identical results!

## Gradual Migration Strategy

If you want to migrate gradually:

### Option 1: Keep Both Running
```bash
# Old app on port 5000
python app.py

# New app on port 5001
PORT=5001 python run.py
```

### Option 2: Test New App First
```bash
# Run tests
python test_refactored_app.py

# If all pass, switch over
mv app.py app.py.old
python run.py
```

## Common Issues & Solutions

### Issue: Import Errors
```python
# Error: cannot import name 'JobMatcher'
```
**Solution**: Make sure you're importing from the new location:
```python
from job_search_app.services import JobMatcher
```

### Issue: Templates Not Found
```python
# Error: TemplateNotFound: index.html
```
**Solution**: Ensure templates are in `job_search_app/templates/`:
```bash
cp templates/* job_search_app/templates/
```

### Issue: Static Files 404
```python
# Error: 404 on /static/style.css
```
**Solution**: Copy static files:
```bash
cp static/* job_search_app/static/
```

### Issue: Port Already in Use
```bash
# Error: Address already in use
```
**Solution**: Kill old process or use different port:
```bash
pkill -f "python app.py"
# or
PORT=5001 python run.py
```

## Deployment Updates

### Old Render Config
```yaml
buildCommand: "pip install -r requirements.txt"
startCommand: "gunicorn app:app"
```

### New Render Config
```yaml
buildCommand: "pip install -r requirements.txt"
startCommand: "gunicorn wsgi:app"
```

## Rollback Plan

If you need to rollback:

```bash
# 1. Stop new app
pkill -f "python run.py"

# 2. Restore old files
cp backup_old_structure/* .

# 3. Start old app
python app.py
```

## Feature Comparison

| Feature | Old Structure | New Structure |
|---------|--------------|---------------|
| Job Search | ✅ | ✅ |
| Company Scraping | ✅ | ✅ |
| Job Matching | ✅ | ✅ |
| Keyword Expansion | ✅ | ✅ |
| CSV Export | ✅ | ✅ |
| Error Handling | Basic | ✅ Professional |
| Input Validation | Partial | ✅ Comprehensive |
| Logging | Basic | ✅ Structured |
| Configuration | Hardcoded | ✅ Environment-based |
| Testing | Manual | ✅ Automated |
| Docker Support | ❌ | ✅ Full support |
| CI/CD | ❌ | ✅ GitHub Actions |
| Documentation | Minimal | ✅ Complete |

## Next Steps After Migration

1. ✅ Test all endpoints
2. ✅ Update deployment configurations
3. ✅ Run automated tests
4. ✅ Update documentation
5. ✅ Deploy to production
6. ✅ Monitor logs and errors
7. ✅ Archive old code

## Questions?

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- See [README_NEW.md](README_NEW.md) for full documentation

---

**The migration is complete! Your app is now production-ready! 🚀**
