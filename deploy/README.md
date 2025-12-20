# Deployment Configuration

This directory contains all deployment-related configuration files.

## 📁 Files

### Docker
- **Dockerfile** - Container image definition
- **docker-compose.yml** - Multi-container orchestration
- **.dockerignore** - Files to exclude from Docker build

### Cloud Platforms
- **render.yaml** - Render.com configuration
- **.github-ci.yml** - GitHub Actions CI/CD pipeline (move to .github/workflows/)

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and run with docker-compose
docker-compose up -d

# Access at http://localhost:8000
```

### Manual Docker Build
```bash
# Build image
docker build -t job-search-app .

# Run container
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e FLASK_ENV=production \
  -v $(pwd)/job_results:/app/job_results \
  --name job-search-app \
  job-search-app
```

### Docker Compose Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build

# Scale workers
docker-compose up --scale app=3
```

## ☁️ Cloud Platforms

### Render.com
1. Push code to GitHub
2. Connect repository to Render
3. Render auto-detects `render.yaml`
4. Click "Create Web Service"
5. Deploy automatically

**Manual Setup:**
- Go to [render.com](https://render.com)
- New → Web Service
- Connect repository
- Use `render.yaml` configuration

### Heroku
```bash
# Login
heroku login

# Create app
heroku create job-search-app

# Set environment variables
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open
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
# Build and push
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

## 🔧 Configuration

### Environment Variables

Required:
- `SECRET_KEY` - Flask secret key (generate with `openssl rand -hex 32`)
- `FLASK_ENV` - Environment (production, development, testing)

Optional:
- `PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `WORKERS` - Gunicorn workers (default: 4)

### Setting Environment Variables

**Docker:**
```bash
docker run -e SECRET_KEY="..." -e FLASK_ENV=production ...
```

**Docker Compose:**
Edit `docker-compose.yml`:
```yaml
environment:
  - SECRET_KEY=your-secret-key
  - FLASK_ENV=production
```

**Render.com:**
Add in dashboard → Environment → Environment Variables

**Heroku:**
```bash
heroku config:set SECRET_KEY="..."
```

## 🔒 Security Checklist

- [ ] Set unique `SECRET_KEY` for production
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS in production
- [ ] Enable firewall rules
- [ ] Review and restrict CORS settings
- [ ] Set up monitoring and alerts
- [ ] Configure log rotation
- [ ] Regular security updates

## 📊 Monitoring

### Health Check
```bash
curl https://your-app.com/health
```

### Docker Logs
```bash
docker logs -f job-search-app
```

### Cloud Platform Logs
- **Render**: View in dashboard → Logs
- **Heroku**: `heroku logs --tail`
- **AWS**: CloudWatch
- **GCP**: Cloud Logging
- **Azure**: App Service logs

## 🚀 CI/CD

### GitHub Actions
1. Move `.github-ci.yml` to `.github/workflows/ci.yml`
2. Configure secrets in GitHub repo settings
3. Push to trigger pipeline

Pipeline runs:
- Linting (flake8)
- Testing (pytest)
- Docker build
- Docker test
- Deploy (on merge to main)

## 🔄 Scaling

### Horizontal Scaling
**Docker Compose:**
```bash
docker-compose up --scale app=3
```

**Kubernetes:**
```bash
kubectl scale deployment job-search-app --replicas=3
```

### Vertical Scaling
Adjust worker count in start command:
```bash
gunicorn --workers 8 --bind 0.0.0.0:8000 wsgi:app
```

## 📚 Additional Resources

- [Complete Deployment Guide](../docs/DEPLOYMENT.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Main README](../README.md)

## 🆘 Troubleshooting

**Build fails:**
- Check Docker logs
- Verify all files are present
- Check `.dockerignore`

**App won't start:**
- Verify `SECRET_KEY` is set
- Check `FLASK_ENV` setting
- Review application logs

**Performance issues:**
- Increase worker count
- Scale horizontally
- Add caching layer

---

**For detailed deployment instructions, see [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)**
