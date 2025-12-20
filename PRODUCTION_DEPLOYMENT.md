# Production Deployment Guide

## 🚀 Options for Continuous Production Deployment

### Option 1: Simple VPS Deployment (Recommended for Getting Started)

#### A. Using systemd (Linux Service)

**Best for:** DigitalOcean, AWS EC2, Linode, etc.

1. **Create systemd service file:**

```bash
sudo nano /etc/systemd/system/jobsearch.service
```

Add this content:

```ini
[Unit]
Description=Job Search Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/your/jobs
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable and start the service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable jobsearch
sudo systemctl start jobsearch
sudo systemctl status jobsearch
```

3. **Useful commands:**

```bash
sudo systemctl restart jobsearch  # Restart
sudo systemctl stop jobsearch     # Stop
sudo systemctl status jobsearch   # Check status
sudo journalctl -u jobsearch -f   # View logs
```

---

### Option 2: Docker Deployment

**Best for:** Portable, consistent environments

1. **Build Docker image:**

```bash
docker build -t job-search-app .
```

2. **Run with Docker Compose:**

```bash
docker-compose up -d
```

3. **Auto-restart on boot:**

Docker containers automatically restart with `restart: always` in docker-compose.yml

---

### Option 3: Cloud Platform Deployment (Free Tier Available)

#### A. **Render.com** (Easiest, Free Tier)

1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically on push
4. **Free tier includes:**
   - Auto-sleep after 15 min inactivity
   - Wakes up on request
   - Good for demos/personal use

#### B. **Railway.app** (Simple, $5/month)

1. Connect GitHub
2. One-click deploy
3. Always running
4. Automatic HTTPS

#### C. **Heroku** (Classic, Free tier removed)

Now requires paid plan ($7/month minimum)

#### D. **AWS EC2 / DigitalOcean** ($5-10/month)

Full control, run 24/7

---

### Option 4: Using Supervisor (Process Manager)

**Best for:** Multiple apps on one server

1. **Install Supervisor:**

```bash
sudo apt-get install supervisor
```

2. **Create config:**

```bash
sudo nano /etc/supervisor/conf.d/jobsearch.conf
```

Add:

```ini
[program:jobsearch]
command=/path/to/venv/bin/python run.py
directory=/path/to/jobs
user=your-username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/jobsearch.log
```

3. **Start:**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start jobsearch
sudo supervisorctl status
```

---

## 🔧 Production Configuration Changes

### 1. Update `run.py` for production:

```python
if __name__ == '__main__':
    import os
    
    # Use environment variable to determine mode
    env = os.getenv('FLASK_ENV', 'production')
    
    app = create_app(env)
    
    # Production settings
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=False,  # Never True in production
        use_reloader=False
    )
```

### 2. Set environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY="your-secure-random-secret-key-here"
export PORT=5000
```

### 3. Use Gunicorn (Production WSGI Server):

**Install:**
```bash
pip install gunicorn
```

**Run:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

For systemd, update `ExecStart`:
```ini
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 4. Add Nginx as Reverse Proxy:

**Install:**
```bash
sudo apt-get install nginx
```

**Configure** (`/etc/nginx/sites-available/jobsearch`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/jobs/static;
    }
}
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/jobsearch /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🌐 Quick Deployment Scripts

### A. Deploy to VPS (Ubuntu/Debian)

```bash
#!/bin/bash
# deploy.sh - Run this on your VPS

# Update system
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx supervisor

# Clone/pull your code
cd /opt
git clone YOUR_REPO_URL jobsearch
cd jobsearch

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo cp deploy/jobsearch.service /etc/systemd/system/
sudo systemctl enable jobsearch
sudo systemctl start jobsearch

echo "✅ Deployed! App running at http://your-ip:5000"
```

### B. Auto-deploy on git push

Create systemd path unit (`/etc/systemd/system/jobsearch-deploy.path`):

```ini
[Path]
PathChanged=/opt/jobsearch

[Install]
WantedBy=multi-user.target
```

Create service (`/etc/systemd/system/jobsearch-deploy.service`):

```ini
[Unit]
Description=Auto-deploy jobsearch on changes

[Service]
Type=oneshot
ExecStart=/opt/jobsearch/scripts/deploy.sh
```

---

## 📊 Monitoring & Logs

### View logs in production:

**Systemd:**
```bash
sudo journalctl -u jobsearch -f
```

**Supervisor:**
```bash
sudo tail -f /var/log/jobsearch.log
```

**Docker:**
```bash
docker logs -f job-search-app
```

### Health check endpoint:

Your app already has: `http://your-domain.com/health`

Use for monitoring services like:
- UptimeRobot
- Pingdom
- StatusCake

---

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` to random value
- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (Let's Encrypt free)
- [ ] Set up firewall (UFW)
- [ ] Regular backups
- [ ] Rate limiting (Flask-Limiter)
- [ ] Keep dependencies updated

---

## 💰 Cost Comparison

| Provider | Price | Features |
|----------|-------|----------|
| **Render** | Free | Auto-sleep, good for demos |
| **Railway** | $5/mo | Always on, easy |
| **DigitalOcean** | $6/mo | Full control, 1GB RAM |
| **AWS EC2** | $8/mo | Scalable, complex |
| **Linode** | $5/mo | Simple, reliable |

---

## 🚀 Recommended Setup for Production

**For personal/small use:**
1. DigitalOcean Droplet ($6/month)
2. Systemd service
3. Nginx reverse proxy
4. Let's Encrypt SSL
5. Gunicorn (4 workers)

**For scaling:**
1. Docker containers
2. Load balancer
3. Multiple workers
4. Redis for caching
5. PostgreSQL database

---

## 📝 Next Steps

Choose your deployment method:
1. **Quick & Easy:** Render.com (5 minutes)
2. **Full Control:** VPS + systemd (30 minutes)
3. **Container:** Docker deployment (20 minutes)

Need help with any of these? Let me know!
