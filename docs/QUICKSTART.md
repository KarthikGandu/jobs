# Quick Start Guide

Get the Job Search Application running in under 5 minutes!

## 🚀 Fast Track (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

### 3. Access the Application
Open your browser to: **http://localhost:5000**

That's it! 🎉

---

## 📋 Step-by-Step Guide

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

#### Option 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

#### Option 2: Docker
```bash
# Build and run with Docker Compose
docker-compose up

# Access at http://localhost:8000
```

#### Option 3: Direct Installation
```bash
# Install globally (not recommended for development)
pip install -r requirements.txt
python run.py
```

---

## 🧪 Verify Installation

### Test the Application
```bash
# Run test suite
python test_refactored_app.py

# Expected output:
# ✓ PASS - Imports
# ✓ PASS - App Creation
# ✓ PASS - Blueprints
# ✓ PASS - Routes
# ✓ PASS - Validation
# ✓ PASS - Error Handlers
# ✓ PASS - Configuration
# Results: 7/7 tests passed
```

### Check Health Endpoint
```bash
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "message": "Job Search Application is running"}
```

---

## 📡 API Examples

### 1. Search for Jobs
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Python Developer",
    "location": "San Francisco",
    "site_name": ["linkedin", "indeed"],
    "results_wanted": 10
  }'
```

### 2. Get Available Companies
```bash
curl http://localhost:5000/api/companies
```

### 3. Search Jobs at Specific Company
```bash
curl -X POST http://localhost:5000/api/companies/Google/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Software Engineer",
    "results_wanted": 15
  }'
```

### 4. Expand Keywords
```bash
curl -X POST http://localhost:5000/api/expand-keywords \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "machine learning",
    "include_related": true
  }'
```

### 5. Match Jobs with Preferences
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [...],
    "preferences": {
      "min_salary": 100000,
      "required_skills": ["Python", "AWS"]
    }
  }'
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy example environment file
cp .env.development .env

# Edit as needed
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
LOG_LEVEL=DEBUG
```

### Common Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode (development/production) | `development` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING) | `DEBUG` |
| `PORT` | Application port | `5000` |

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t job-search-app .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -v $(pwd)/job_results:/app/job_results \
  job-search-app
```

### Using Docker Compose
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build
```

---

## 📁 Project Structure

```
job-search-app/
├── job_search_app/          # Main application package
│   ├── config/              # Configuration files
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── utils/               # Utilities
│   ├── static/              # CSS, JS files
│   └── templates/           # HTML templates
├── run.py                   # Development server
├── wsgi.py                  # Production entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose setup
```

---

## 🎯 Usage Examples

### Web Interface
1. Open http://localhost:5000
2. Enter job search criteria
3. Click "Search Jobs"
4. View and filter results
5. Download as CSV

### Python API Client
```python
import requests

# Search for jobs
response = requests.post('http://localhost:5000/api/search', json={
    'search_term': 'Data Scientist',
    'location': 'New York',
    'site_name': ['linkedin'],
    'results_wanted': 20
})

jobs = response.json()['jobs']
print(f"Found {len(jobs)} jobs")
```

### JavaScript/Node.js Client
```javascript
const response = await fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    search_term: 'Frontend Developer',
    location: 'Remote',
    site_name: ['indeed', 'glassdoor'],
    results_wanted: 15
  })
});

const data = await response.json();
console.log(`Found ${data.jobs_found} jobs`);
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=8080 python run.py
```

### Import Errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Module Not Found
```bash
# Make sure you're in the project root directory
cd /path/to/job-search-app

# Run from root
python run.py
```

### Static Files Not Loading
```bash
# Check if static files exist
ls -la job_search_app/static/
ls -la job_search_app/templates/

# If missing, copy from original locations
cp -r static/* job_search_app/static/
cp -r templates/* job_search_app/templates/
```

---

## 📊 Monitoring

### View Logs
```bash
# Application logs
tail -f job_search_app.log

# Docker logs
docker-compose logs -f
```

### Health Check
```bash
# Simple health check
curl http://localhost:5000/health

# Continuous monitoring
watch -n 5 'curl -s http://localhost:5000/health'
```

---

## 🚀 Production Deployment

### Render.com (Recommended)
1. Push code to GitHub
2. Connect repository to Render
3. Render auto-detects `render.yaml`
4. Deploy automatically

### Heroku
```bash
heroku create job-search-app
git push heroku main
heroku open
```

### AWS/GCP/Azure
Use the provided `Dockerfile` for containerized deployment.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📚 Next Steps

1. **Explore the API**: Check [README_NEW.md](README_NEW.md) for full API documentation
2. **Customize**: Modify configurations in `job_search_app/config/settings.py`
3. **Extend**: Add new features in `job_search_app/services/`
4. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
5. **Contribute**: Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

## 🆘 Getting Help

- **Documentation**: Read [README_NEW.md](README_NEW.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: Open a GitHub issue
- **Community**: Join our discussions

---

## ✅ Checklist

- [ ] Python 3.11+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application running (`python run.py`)
- [ ] Health check passes (`curl http://localhost:5000/health`)
- [ ] Tests passing (`python test_refactored_app.py`)
- [ ] API endpoints working
- [ ] Ready to deploy!

---

**Happy Job Searching! 🎉**
