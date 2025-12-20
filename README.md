# Job Search Application

A professional, production-ready Flask application for intelligent job searching across multiple platforms with ML-powered matching and filtering capabilities.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Access at http://localhost:5000
```

## ✨ Features

- 🔍 **Multi-Platform Search** - LinkedIn, Indeed, Glassdoor, Google Jobs, ZipRecruiter
- 🏢 **Company-Specific Search** - Target specific companies
- 🤖 **ML-Powered Matching** - Intelligent job filtering
- 📊 **Keyword Expansion** - Auto-expand search terms
- 📥 **CSV Export** - Download results
- 🔒 **Secure** - Input validation, error handling
- 🐳 **Docker Ready** - Containerized deployment
- 📚 **Well Documented** - Comprehensive guides

## 📁 Project Structure

```
job-search-app/
├── job_search_app/        # Main application package
│   ├── config/           # Configuration management
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   ├── static/           # Frontend assets
│   └── templates/        # HTML templates
├── docs/                 # Documentation
├── deploy/               # Deployment configs
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── archive/              # Old files (reference)
```

## 📖 Documentation

- 📘 **[Start Here](docs/START_HERE_NEW.md)** - Main entry point
- ⚡ **[Quick Start](docs/QUICKSTART.md)** - 5-minute setup
- 🏗️ **[Architecture](docs/ARCHITECTURE.md)** - Technical details
- 🚀 **[Deployment](docs/DEPLOYMENT.md)** - Deploy anywhere
- 🔄 **[Migration Guide](docs/MIGRATION_GUIDE.md)** - From old structure
- 📊 **[Summary](docs/REFACTORING_SUMMARY.md)** - What changed

## 🛠️ Tech Stack

- **Framework**: Flask 3.0
- **Server**: Gunicorn
- **Data**: Pandas
- **Scraping**: JobSpy2, BeautifulSoup
- **ML**: Scikit-learn
- **Container**: Docker

## 🧪 Testing

```bash
# Run test suite
python tests/test_application.py

# Expected: 7/7 tests passed ✅
```

## 🐳 Docker

```bash
# Build and run
docker-compose -f deploy/docker-compose.yml up

# Access at http://localhost:8000
```

## 🚢 Deployment

### Render.com
```bash
# Already configured in deploy/render.yaml
# Just connect your GitHub repository
```

### Heroku
```bash
heroku create job-search-app
git push heroku main
```

### Docker Anywhere
```bash
docker build -f deploy/Dockerfile -t job-search-app .
docker run -p 8000:8000 job-search-app
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage |
| `/health` | GET | Health check |
| `/api/search` | POST | Search jobs |
| `/api/companies` | GET | List companies |
| `/api/companies/<name>/jobs` | POST | Company-specific search |
| `/api/match` | POST | ML-powered matching |
| `/api/expand-keywords` | POST | Keyword expansion |
| `/api/download/<file>` | GET | Download CSV |

## 🔧 Configuration

```bash
# Create environment file
cp .env.example .env

# Edit configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key
LOG_LEVEL=DEBUG
```

## 📊 Example Usage

### Search for Jobs
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Python Developer",
    "location": "San Francisco",
    "site_name": ["linkedin", "indeed"],
    "results_wanted": 20
  }'
```

### Get Companies
```bash
curl http://localhost:5000/api/companies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

See [CONTRIBUTING.md](archive/CONTRIBUTING.md) for details.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 👥 Authors

- **Original**: Karthik
- **Professional Refactoring**: Rovo Dev

## 🙏 Acknowledgments

- JobSpy library for scraping
- Flask framework and community
- All contributors

## 📞 Support

- **Documentation**: See [docs/](docs/) folder
- **Issues**: Open a GitHub issue
- **Health Check**: `curl http://localhost:5000/health`

## ⭐ Star Us!

If you find this project useful, please star it on GitHub!

---

**Made with ❤️ for job seekers everywhere**
