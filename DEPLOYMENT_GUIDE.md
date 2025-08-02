# QuickDesk Production Deployment Guide

This guide covers deploying QuickDesk Enhanced Edition to production environments with all advanced features enabled.

## 🚀 Quick Production Setup

### Prerequisites
- Python 3.10+
- PostgreSQL or MySQL (recommended for production)
- Redis (for caching and background tasks)
- Nginx (for reverse proxy)
- SSL certificate (Let's Encrypt recommended)

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server

# Install Node.js (for PWA features)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE quickdesk_prod;
CREATE USER quickdesk WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE quickdesk_prod TO quickdesk;
\q
```

### 3. Application Deployment

```bash
# Create application directory
sudo mkdir -p /var/www/quickdesk
sudo chown $USER:$USER /var/www/quickdesk
cd /var/www/quickdesk

# Clone or upload your QuickDesk files
# (Upload your enhanced QuickDesk files here)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Create production environment file
cat > .env << EOF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
DATABASE_URL=postgresql://quickdesk:your_secure_password@localhost:5432/quickdesk_prod
FLASK_ENV=production

# Email configuration (update with your SMTP settings)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key

# File uploads
UPLOAD_FOLDER=/var/www/quickdesk/uploads
MAX_CONTENT_LENGTH=52428800

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# Performance
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF

# Create uploads directory
mkdir -p uploads
chmod 755 uploads

# Initialize database
python migrate_database.py
```

### 4. Gunicorn Configuration

Create `/var/www/quickdesk/gunicorn.conf.py`:

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
user = "www-data"
group = "www-data"
tmp_upload_dir = None
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}
```

### 5. Systemd Service

Create `/etc/systemd/system/quickdesk.service`:

```ini
[Unit]
Description=QuickDesk Help Desk System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/quickdesk
Environment=PATH=/var/www/quickdesk/venv/bin
ExecStart=/var/www/quickdesk/venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 6. Celery Service (for background tasks)

Create `/etc/systemd/system/quickdesk-celery.service`:

```ini
[Unit]
Description=QuickDesk Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/quickdesk
Environment=PATH=/var/www/quickdesk/venv/bin
ExecStart=/var/www/quickdesk/venv/bin/celery -A app.celery worker --detach --loglevel=info
ExecStop=/var/www/quickdesk/venv/bin/celery -A app.celery control shutdown
ExecReload=/var/www/quickdesk/venv/bin/celery -A app.celery control reload
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 7. Nginx Configuration

Create `/etc/nginx/sites-available/quickdesk`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # File upload size
    client_max_body_size 50M;

    # Static files
    location /static {
        alias /var/www/quickdesk/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Uploaded files
    location /uploads {
        alias /var/www/quickdesk/uploads;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }

    # WebSocket support for real-time features
    location /socket.io {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 8. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### 9. Start Services

```bash
# Set permissions
sudo chown -R www-data:www-data /var/www/quickdesk
sudo chmod -R 755 /var/www/quickdesk

# Enable and start services
sudo systemctl enable quickdesk
sudo systemctl enable quickdesk-celery
sudo systemctl start quickdesk
sudo systemctl start quickdesk-celery

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/quickdesk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Check service status
sudo systemctl status quickdesk
sudo systemctl status quickdesk-celery
sudo systemctl status nginx
```

## 🐳 Docker Deployment

### Docker Compose Setup

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://quickdesk:${DB_PASSWORD}@db:5432/quickdesk_prod
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - MAIL_SERVER=${MAIL_SERVER}
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.quickdesk.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.quickdesk.tls.certresolver=letsencrypt"

  celery:
    build: .
    restart: unless-stopped
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://quickdesk:${DB_PASSWORD}@db:5432/quickdesk_prod
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    restart: unless-stopped
    environment:
      - POSTGRES_DB=quickdesk_prod
      - POSTGRES_USER=quickdesk
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  redis:
    image: redis:6-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  traefik:
    image: traefik:v2.5
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@your-domain.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./acme.json:/acme.json

volumes:
  postgres_data:
  redis_data:
```

### Deploy with Docker

```bash
# Create environment file
cat > .env << EOF
SECRET_KEY=$(openssl rand -base64 32)
DB_PASSWORD=$(openssl rand -base64 32)
MAIL_SERVER=smtp.sendgrid.net
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
EOF

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker-compose -f docker-compose.prod.yml exec web python migrate_database.py
```

## 📊 Monitoring and Maintenance

### Log Management

```bash
# Create log rotation
sudo tee /etc/logrotate.d/quickdesk << EOF
/var/www/quickdesk/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload quickdesk
    endscript
}
EOF
```

### Database Backup

```bash
# Create backup script
sudo tee /usr/local/bin/backup-quickdesk.sh << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/quickdesk"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h localhost -U quickdesk quickdesk_prod | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Files backup
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C /var/www/quickdesk uploads

# Keep only last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

sudo chmod +x /usr/local/bin/backup-quickdesk.sh

# Add to crontab (daily backup at 2 AM)
echo "0 2 * * * /usr/local/bin/backup-quickdesk.sh" | sudo crontab -
```

### Health Monitoring

Create `/var/www/quickdesk/health_check.py`:

```python
#!/usr/bin/env python3
import requests
import sys
import os

def health_check():
    try:
        response = requests.get('https://your-domain.com/health', timeout=10)
        if response.status_code == 200:
            print("✅ QuickDesk is healthy")
            return 0
        else:
            print(f"❌ QuickDesk returned status {response.status_code}")
            return 1
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(health_check())
```

## 🔧 Performance Optimization

### Database Optimization

```sql
-- Add indexes for better performance
CREATE INDEX idx_tickets_status ON ticket(status);
CREATE INDEX idx_tickets_created_at ON ticket(created_at);
CREATE INDEX idx_tickets_user_id ON ticket(user_id);
CREATE INDEX idx_tickets_assigned_to ON ticket(assigned_to);
CREATE INDEX idx_comments_ticket_id ON comment(ticket_id);
CREATE INDEX idx_activities_ticket_id ON ticket_activity(ticket_id);
```

### Redis Configuration

Add to `/etc/redis/redis.conf`:

```
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

## 🚨 Security Checklist

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall (UFW)
- [ ] Set up fail2ban for SSH protection
- [ ] Regular security updates
- [ ] Database access restrictions
- [ ] File upload restrictions
- [ ] CSRF protection enabled
- [ ] Security headers configured

## 📞 Support

For deployment issues:
1. Check service logs: `sudo journalctl -u quickdesk -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Check application logs: `tail -f /var/www/quickdesk/logs/app.log`
4. Verify database connectivity
5. Test email configuration

Your QuickDesk Enhanced Edition is now ready for production! 🎉
