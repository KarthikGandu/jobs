# Job Search Application

A professional, production-ready Flask application for intelligent job searching across multiple platforms with ML-powered matching and filtering capabilities.

## 🚀 Features

- **Multi-Platform Job Scraping**: Search across LinkedIn, Indeed, Glassdoor, Google Jobs, and ZipRecruiter
- **Company-Specific Search**: Target specific companies for job opportunities
- **ML-Powered Job Matching**: Intelligent filtering based on your preferences
- **Keyword Expansion**: Automatically expand search terms with related keywords
- **RESTful API**: Clean, well-documented API endpoints
- **Export Capabilities**: Download results as CSV files
- **Production Ready**: Configured for Docker, Kubernetes, and cloud deployment

## 📋 Requirements

- Python 3.11+
- pip or uv package manager
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd job-search-app
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.development .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**
```bash
docker build -t job-search-app .
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

## 📁 Project Structure

```
job-search-app/
├── job_search_app/           # Main application package
│   ├── __init__.py
│   ├── app.py               # Application factory
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py      # Environment-specific configs
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── main.py          # Main routes (frontend)
│   │   └── api.py           # API routes
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── job_matcher.py   # ML-powered job matching
│   │   ├── keyword_expander.py
│   │   └── company_scraper.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py        # Logging configuration
│   │   ├── validators.py    # Input validation
│   │   └── errors.py        # Custom exceptions
│   ├── static/              # Static files (CSS, JS)
│   └── templates/           # HTML templates
├── jobspy2/                 # Job scraping library
├── jobsparser/              # CLI tool
├── wsgi.py                  # Production entry point
├── run.py                   # Development entry point
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── render.yaml             # Render.com deployment config
└── .github/                # CI/CD workflows
```

## 🔧 Configuration

The application supports multiple environments:

### Development
```bash
export FLASK_ENV=development
python run.py
```

### Production
```bash
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | `development` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING) | `INFO` |
| `PORT` | Application port | `5000` |

## 📡 API Documentation

### Health Check
```bash
GET /health
```

### Search Jobs
```bash
POST /api/search
Content-Type: application/json

{
  "search_term": "Python Developer",
  "location": "San Francisco",
  "site_name": ["linkedin", "indeed"],
  "results_wanted": 20,
  "distance": 50,
  "job_type": "fulltime",
  "is_remote": false
}
```

### Company-Specific Search
```bash
POST /api/companies/{company_name}/jobs
Content-Type: application/json

{
  "search_term": "Software Engineer",
  "results_wanted": 15
}
```

### Get Available Companies
```bash
GET /api/companies
```

### Match Jobs (ML-Powered)
```bash
POST /api/match
Content-Type: application/json

{
  "jobs": [...],
  "preferences": {
    "min_salary": 100000,
    "required_skills": ["Python", "AWS"]
  }
}
```

### Expand Keywords
```bash
POST /api/expand-keywords
Content-Type: application/json

{
  "keyword": "machine learning",
  "include_related": true
}
```

### Download Results
```bash
GET /api/download/{filename}
```

## 🚢 Deployment

### Render.com
```bash
# Already configured in render.yaml
# Just connect your GitHub repository to Render
```

### Heroku
```bash
heroku create job-search-app
git push heroku main
```

### AWS/GCP/Azure
Use the provided Dockerfile for containerized deployment on any cloud platform.

### Docker Swarm/Kubernetes
Kubernetes manifests can be generated from docker-compose.yml using kompose:
```bash
kompose convert
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=job_search_app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📊 Monitoring and Logging

- **Logs**: Application logs are written to `job_search_app.log` with rotation
- **Health Endpoint**: `/health` for monitoring and health checks
- **Metrics**: Ready for Prometheus/Grafana integration

## 🔒 Security Features

- Input validation on all endpoints
- CORS configuration
- Secure session management
- SQL injection prevention
- XSS protection
- Rate limiting (configurable)
- Environment-based secrets management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation for API changes
- Use type hints where applicable
- Keep functions small and focused

## 🐛 Troubleshooting

### Common Issues

**Port already in use**
```bash
# Change port in run.py or use environment variable
export PORT=8080
python run.py
```

**Import errors**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**Scraping failures**
- Some sites may block automated requests
- Consider using proxies or rate limiting
- Check the WHY_SITES_BLOCKED.md for details

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- Original implementation by Karthik
- Professional refactoring and architecture by Rovo Dev

## 🙏 Acknowledgments

- JobSpy library for scraping functionality
- Flask framework and community
- All contributors and users

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for job seekers everywhere**
