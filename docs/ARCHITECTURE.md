# Application Architecture

## Overview

The Job Search Application follows a modular, layered architecture pattern with clear separation of concerns, making it maintainable, testable, and scalable.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│                  (Browser / API Clients)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                     Web Server Layer                         │
│              (Gunicorn + Flask Application)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
┌───────▼────────┐              ┌────────▼────────┐
│  Main Routes   │              │   API Routes    │
│   (Frontend)   │              │  (REST API)     │
└───────┬────────┘              └────────┬────────┘
        │                                 │
        └────────────────┬────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Business Logic Layer                      │
│                       (Services)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ JobMatcher   │  │  Keyword     │  │  Company     │     │
│  │   Service    │  │  Expander    │  │  Scraper     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   External Services Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  JobSpy2     │  │  LinkedIn    │  │   Indeed     │     │
│  │  (Scraper)   │  │     API      │  │     API      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Layers

### 1. Application Factory (`job_search_app/app.py`)

**Responsibility**: Creates and configures the Flask application

**Key Components:**
- `create_app()`: Factory function for creating Flask instances
- Configuration loading based on environment
- Blueprint registration
- Error handler registration
- Extension initialization (CORS, logging)

**Benefits:**
- Supports multiple environments (dev, prod, test)
- Enables testing with different configurations
- Clean separation of setup logic

### 2. Configuration Layer (`job_search_app/config/`)

**Responsibility**: Manages application settings

**Files:**
- `settings.py`: Environment-specific configurations
  - `DevelopmentConfig`: Debug mode, verbose logging
  - `ProductionConfig`: Security hardening, optimized settings
  - `TestingConfig`: Test-specific settings

**Key Features:**
- Environment variable support
- Sensible defaults
- Validation of critical settings
- Path management

### 3. Routes Layer (`job_search_app/routes/`)

**Responsibility**: HTTP request handling and routing

**Blueprints:**

#### Main Blueprint (`main.py`)
- Frontend page serving
- Health check endpoint
- Static content routing

#### API Blueprint (`api.py`)
- RESTful API endpoints
- Request validation
- Response formatting
- Error handling

**Endpoints:**
- `GET /` - Main application page
- `GET /health` - Health check
- `POST /api/search` - Job search
- `GET /api/companies` - List companies
- `POST /api/companies/<name>/jobs` - Company-specific search
- `POST /api/match` - ML-powered job matching
- `POST /api/expand-keywords` - Keyword expansion
- `GET /api/download/<file>` - Download results

### 4. Services Layer (`job_search_app/services/`)

**Responsibility**: Business logic implementation

#### JobMatcher Service
```python
class JobMatcher:
    """ML-powered job matching and filtering"""
    
    def match_jobs(jobs_df, preferences):
        # Score and filter jobs based on criteria
        # Use ML algorithms for intelligent matching
```

#### KeywordExpander Service
```python
class KeywordExpander:
    """Expand search terms with related keywords"""
    
    def expand_keyword(keyword, include_related):
        # Generate synonym and related terms
        # Improve search coverage
```

#### CompanyScraper Service
```python
class CompanyScraper:
    """Company-specific job scraping"""
    
    def scrape_company_jobs(company, search_term, results_wanted):
        # Target specific company career pages
        # Return structured job data
```

### 5. Utilities Layer (`job_search_app/utils/`)

**Responsibility**: Cross-cutting concerns

#### Logger (`logger.py`)
- Structured logging
- File rotation
- Console and file outputs
- Log level management

#### Validators (`validators.py`)
- Input sanitization
- Type checking
- Range validation
- Format validation

#### Error Handlers (`errors.py`)
- Custom exception classes
- Error response formatting
- HTTP status code mapping

## Design Patterns

### 1. Application Factory Pattern
```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Initialize extensions, routes, etc.
    return app
```

**Benefits:**
- Multiple app instances
- Easy testing
- Configuration flexibility

### 2. Blueprint Pattern
```python
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/search', methods=['POST'])
def search_jobs():
    # Implementation
```

**Benefits:**
- Modular route organization
- URL prefix management
- Namespace isolation

### 3. Service Layer Pattern
```python
# Services encapsulate business logic
matcher = JobMatcher()
result = matcher.match_jobs(jobs, preferences)
```

**Benefits:**
- Reusable business logic
- Easy testing
- Separation from HTTP layer

### 4. Dependency Injection
```python
# Configuration injected at app creation
app.config.from_object(config[env])
config[env].init_app(app)
```

## Data Flow

### Job Search Flow
```
1. Client → POST /api/search
2. API Route → Validate input
3. API Route → Call scrape_jobs()
4. External Service → Scrape job sites
5. External Service → Return raw data
6. API Route → Process and format
7. API Route → Save to CSV
8. API Route → Return JSON response
9. Client → Display results
```

### Company Search Flow
```
1. Client → GET /api/companies
2. API Route → CompanyScraper.get_company_list()
3. CompanyScraper → Return company data
4. API Route → Format and group by category
5. API Route → Return JSON
6. Client → Display company list

7. Client → POST /api/companies/Google/jobs
8. API Route → Validate parameters
9. API Route → CompanyScraper.scrape_company_jobs()
10. CompanyScraper → Scrape company site
11. CompanyScraper → Return job DataFrame
12. API Route → Save results
13. API Route → Return JSON
14. Client → Display jobs
```

## Security Architecture

### Input Validation
- All inputs validated before processing
- Type checking and sanitization
- Range and format validation

### Error Handling
- Custom exception classes
- No sensitive data in error messages
- Proper HTTP status codes

### Configuration Security
- Secrets in environment variables
- Separate configs for dev/prod
- Secret key validation in production

### Session Management
- HTTP-only cookies
- Secure cookies in production
- SameSite protection

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- No in-memory session storage
- Shared file storage for job results

### Vertical Scaling
- Configurable worker processes
- Async job processing capability
- Resource-efficient scraping

### Caching Strategy (Future)
- Redis for session storage
- Cache common searches
- Rate limit with Redis

## Testing Architecture

### Unit Tests
```python
# Test individual components
def test_validate_search_params():
    params = validate_job_search_params({...})
    assert params['results_wanted'] == 15
```

### Integration Tests
```python
# Test API endpoints
def test_search_endpoint(client):
    response = client.post('/api/search', json={...})
    assert response.status_code == 200
```

### End-to-End Tests
```python
# Test complete workflows
def test_job_search_workflow():
    # Search → Match → Download
```

## Monitoring & Observability

### Logging
- Structured JSON logs
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Error tracking

### Health Checks
- `/health` endpoint
- Database connectivity check
- External service status

### Metrics (Future Integration)
- Request count and duration
- Error rates
- Job scraping success rates
- Response times

## Deployment Architecture

### Development
```
Local Machine → Python → Flask Dev Server → Port 5000
```

### Production
```
Cloud Platform → Load Balancer → Gunicorn Workers → Flask App
                                     ↓
                              Persistent Storage
```

## Future Enhancements

### Planned Improvements
1. **Database Integration**: PostgreSQL for persistent storage
2. **Caching Layer**: Redis for performance
3. **Message Queue**: Celery for async jobs
4. **API Authentication**: JWT or OAuth2
5. **Rate Limiting**: Per-user quotas
6. **WebSocket Support**: Real-time updates
7. **GraphQL API**: Alternative to REST
8. **Microservices**: Split into smaller services

### Migration Path
1. Add database models
2. Implement caching
3. Extract background jobs
4. Add authentication
5. Split into microservices

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web Framework | Flask 3.0 | HTTP handling |
| WSGI Server | Gunicorn | Production server |
| Data Processing | Pandas | Job data manipulation |
| Web Scraping | JobSpy2, BeautifulSoup | Job site scraping |
| ML/NLP | Scikit-learn | Job matching |
| Containerization | Docker | Deployment |
| CI/CD | GitHub Actions | Automation |

## Best Practices

1. **Separation of Concerns**: Each layer has a single responsibility
2. **DRY Principle**: Reusable services and utilities
3. **Configuration Management**: Environment-based configs
4. **Error Handling**: Comprehensive exception handling
5. **Logging**: Structured and contextual logging
6. **Documentation**: Code comments and docstrings
7. **Testing**: Unit and integration tests
8. **Security**: Input validation and secure defaults

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-20
