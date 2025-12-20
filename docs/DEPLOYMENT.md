# Deployment Guide

This guide covers various deployment options for the Job Search Application.

## Table of Contents
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Environment Variables](#environment-variables)
- [Monitoring](#monitoring)

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Git

### Fastest Way to Run

```bash
# Clone and setup
git clone <repo-url>
cd job-search-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run development server
python run.py
```

Visit `http://localhost:5000`

## Local Development

### Using Python Virtual Environment

1. **Setup**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

2. **Configure environment**
```bash
cp .env.development .env
# Edit .env as needed
```

3. **Run development server**
```bash
python run.py
```

### Using Docker

```bash
docker-compose up
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t job-search-app:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e FLASK_ENV=production \
  -v $(pwd)/job_results:/app/job_results \
  --name job-search-app \
  job-search-app:latest
```

### Docker Compose (Recommended)

```yaml
# docker-compose.yml already configured
docker-compose up -d
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Cloud Platforms

### Render.com (Recommended for Easy Deployment)

1. **Connect GitHub repository** to Render
2. **Configuration** is already in `render.yaml`
3. **Deploy** automatically on push

**Manual Steps:**
- Go to [render.com](https://render.com)
- New > Web Service
- Connect your repository
- Render will detect `render.yaml` automatically

### Heroku

```bash
# Login
heroku login

# Create app
heroku create job-search-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 job-search-app

# Create environment
eb create job-search-env

# Deploy
eb deploy

# Open
eb open
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT-ID/job-search-app

# Deploy
gcloud run deploy job-search-app \
  --image gcr.io/PROJECT-ID/job-search-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

```bash
# Create resource group
az group create --name job-search-rg --location eastus

# Create app service plan
az appservice plan create \
  --name job-search-plan \
  --resource-group job-search-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group job-search-rg \
  --plan job-search-plan \
  --name job-search-app \
  --runtime "PYTHON|3.11"

# Deploy
az webapp up --name job-search-app
```

### DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create App from GitHub
3. Select repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --bind 0.0.0.0:8080 --workers 4 wsgi:app`
   - Environment: Add `SECRET_KEY` and `FLASK_ENV=production`

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | Use `openssl rand -hex 32` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `WORKERS` | Gunicorn workers | `4` |

### Setting Environment Variables

**Linux/Mac:**
```bash
export SECRET_KEY="your-secret-key"
export FLASK_ENV=production
```

**Windows:**
```cmd
set SECRET_KEY=your-secret-key
set FLASK_ENV=production
```

**Docker:**
```bash
docker run -e SECRET_KEY="..." -e FLASK_ENV=production ...
```

**Cloud Platforms:**
Each platform has its own method (environment variables section in dashboard)

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure proper `LOG_LEVEL`
- [ ] Set up SSL/HTTPS
- [ ] Configure firewall rules
- [ ] Set up monitoring/alerts
- [ ] Configure backup for job results
- [ ] Test health endpoint
- [ ] Review security headers
- [ ] Enable rate limiting

## Monitoring

### Health Endpoint
```bash
curl https://your-app.com/health
```

### Logs

**Local:**
```bash
tail -f job_search_app.log
```

**Docker:**
```bash
docker logs -f job-search-app
```

**Heroku:**
```bash
heroku logs --tail
```

### Metrics

The application is ready for:
- Prometheus metrics
- Application Performance Monitoring (APM)
- Error tracking (Sentry, Rollbar)

## Scaling

### Horizontal Scaling

**Docker Swarm:**
```bash
docker service create \
  --name job-search-app \
  --replicas 3 \
  --publish 8000:8000 \
  job-search-app:latest
```

**Kubernetes:**
```bash
kubectl scale deployment job-search-app --replicas=3
```

### Vertical Scaling

Adjust worker count in Gunicorn:
```bash
gunicorn --workers 8 --bind 0.0.0.0:8000 wsgi:app
```

## Troubleshooting

### Port Issues
```bash
# Check if port is in use
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# View logs
docker logs job-search-app

# Shell into container
docker exec -it job-search-app /bin/bash

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Performance Issues
- Increase Gunicorn workers
- Add caching layer (Redis)
- Use CDN for static files
- Optimize database queries

## Security Recommendations

1. **Use HTTPS** in production
2. **Rotate SECRET_KEY** regularly
3. **Keep dependencies updated**
4. **Use environment-specific configs**
5. **Implement rate limiting**
6. **Add authentication** if needed
7. **Regular security audits**

## Backup and Recovery

### Backup Job Results
```bash
# Local backup
tar -czf backup-$(date +%Y%m%d).tar.gz job_results/

# Cloud backup (AWS S3)
aws s3 sync job_results/ s3://your-bucket/backups/
```

### Recovery
```bash
# Restore from backup
tar -xzf backup-YYYYMMDD.tar.gz
```

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test health endpoint
4. Review platform-specific documentation
5. Open GitHub issue if needed

---

**Last Updated:** 2025-12-20
