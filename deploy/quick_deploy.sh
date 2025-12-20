#!/bin/bash

# Quick Deployment Script for Ubuntu/Debian VPS
# Usage: bash deploy/quick_deploy.sh

set -e

echo "🚀 Starting deployment..."
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Don't run as root. Run as regular user with sudo access."
    exit 1
fi

# Install system dependencies
echo "📦 Installing system packages..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# Install project
INSTALL_DIR="/opt/jobsearch"
echo "📁 Installing to $INSTALL_DIR..."

if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  Directory exists. Updating..."
    cd $INSTALL_DIR
    git pull || echo "Not a git repo, skipping pull"
else
    sudo mkdir -p $INSTALL_DIR
    sudo chown $USER:$USER $INSTALL_DIR
    cp -r . $INSTALL_DIR
    cd $INSTALL_DIR
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo "📚 Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production server

# Generate secret key
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Create systemd service
echo "⚙️  Setting up systemd service..."
sudo tee /etc/systemd/system/jobsearch.service > /dev/null <<EOF
[Unit]
Description=Job Search Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=$SECRET_KEY"
ExecStart=$INSTALL_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --timeout 300 wsgi:app
Restart=always
RestartSec=10
StandardOutput=append:/var/log/jobsearch.log
StandardError=append:/var/log/jobsearch-error.log

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jobsearch
sudo systemctl restart jobsearch

# Setup Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/jobsearch > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }

    location /static {
        alias /opt/jobsearch/static;
        expires 1y;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/jobsearch /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Open firewall
echo "🔥 Configuring firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp  # SSH
    sudo ufw allow 80/tcp  # HTTP
    sudo ufw allow 443/tcp # HTTPS
    sudo ufw --force enable
fi

# Get server IP
SERVER_IP=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETE!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🌐 Access your app at: http://$SERVER_IP"
echo ""
echo "📊 Useful commands:"
echo "  sudo systemctl status jobsearch   # Check status"
echo "  sudo systemctl restart jobsearch  # Restart app"
echo "  sudo journalctl -u jobsearch -f   # View logs"
echo "  make restart                      # Quick restart"
echo ""
echo "🔒 Next steps:"
echo "  1. Point your domain to this IP: $SERVER_IP"
echo "  2. Install SSL: sudo certbot --nginx -d your-domain.com"
echo "  3. Update SECRET_KEY in /etc/systemd/system/jobsearch.service"
echo ""
echo "════════════════════════════════════════════════════════"
