# QuickDesk Configuration Guide

This comprehensive guide will help you configure QuickDesk for production use with all the enhanced features.

## 🔐 Environment Configuration (.env file)

### Required Configuration

Create or update your `.env` file with the following settings:

```env
# Security Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production-min-32-chars
DATABASE_URL=sqlite:///quickdesk.db

# Email Configuration (Required for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Optional: Advanced Features
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Video Call Configuration (Optional)
DAILY_API_KEY=your-daily-api-key
JITSI_DOMAIN=meet.jit.si

# Performance Settings
WTF_CSRF_TIME_LIMIT=3600
PERMANENT_SESSION_LIFETIME=86400
```

## 🔑 Generating a Secure SECRET_KEY

### Method 1: Using Python
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Method 2: Using OpenSSL
```bash
openssl rand -base64 32
```

### Method 3: Using Online Generator
Visit: https://djecrety.ir/ (Django Secret Key Generator works for Flask too)

**Important:** 
- Use a unique key for each environment (development, staging, production)
- Never commit your SECRET_KEY to version control
- The key should be at least 32 characters long
- Store it securely (use environment variables in production)

## 📧 Email Configuration

### Gmail Setup (Recommended for Development)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `MAIL_PASSWORD`

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
```

### Outlook/Hotmail Setup

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

### Custom SMTP Server

```env
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=your-password
```

### SendGrid Setup (Production Recommended)

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

### Mailgun Setup

```env
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-password
```

## 🗄️ Database Configuration

### SQLite (Default - Development)
```env
DATABASE_URL=sqlite:///quickdesk.db
```

### PostgreSQL (Production Recommended)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/quickdesk
```

### MySQL
```env
DATABASE_URL=mysql://username:password@localhost:3306/quickdesk
```

## 🚀 Production Deployment Configuration

### Environment Variables for Production

```env
# Security
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
WTF_CSRF_ENABLED=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/quickdesk_prod

# Email (Use a service like SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key

# File Storage
UPLOAD_FOLDER=/var/www/quickdesk/uploads
MAX_CONTENT_LENGTH=52428800

# Performance
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/quickdesk/app.log
```

## 🎥 Video Call Configuration

### Daily.co Integration (Recommended)

1. Sign up at https://daily.co
2. Get your API key from the dashboard
3. Add to your `.env`:

```env
DAILY_API_KEY=your-daily-api-key
VIDEO_CALL_PROVIDER=daily
```

### Jitsi Meet Integration (Free)

```env
JITSI_DOMAIN=meet.jit.si
VIDEO_CALL_PROVIDER=jitsi
```

### Custom Jitsi Server

```env
JITSI_DOMAIN=your-jitsi-domain.com
VIDEO_CALL_PROVIDER=jitsi
```

## 📊 Performance Optimization

### Redis Configuration (Optional but Recommended)

Install Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# Download from https://redis.io/download
```

Configure in `.env`:
```env
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Celery for Background Tasks

Install Celery:
```bash
pip install celery redis
```

Start Celery worker:
```bash
celery -A app.celery worker --loglevel=info
```

## 🔒 Security Configuration

### HTTPS Configuration (Production)

```env
FORCE_HTTPS=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### CSRF Protection

```env
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
```

### Rate Limiting

```env
RATELIMIT_STORAGE_URL=redis://localhost:6379/1
RATELIMIT_DEFAULT=100 per hour
```

## 📁 File Upload Configuration

### Local Storage (Default)

```env
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx,txt,zip
```

### AWS S3 Storage (Production)

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=your-bucket-name
AWS_S3_REGION=us-east-1
UPLOAD_PROVIDER=s3
```

## 🌐 CDN Configuration (Optional)

### CloudFlare

```env
CDN_DOMAIN=your-domain.cloudflare.com
USE_CDN=True
```

### AWS CloudFront

```env
CDN_DOMAIN=your-distribution.cloudfront.net
USE_CDN=True
```

## 📱 Progressive Web App (PWA) Configuration

```env
PWA_ENABLED=True
PWA_NAME=QuickDesk
PWA_SHORT_NAME=QuickDesk
PWA_DESCRIPTION=Professional Help Desk System
PWA_THEME_COLOR=#6366f1
PWA_BACKGROUND_COLOR=#ffffff
```

## 🔧 Advanced Configuration

### Logging Configuration

```env
LOG_LEVEL=INFO
LOG_FILE=/var/log/quickdesk/app.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

### Session Configuration

```env
PERMANENT_SESSION_LIFETIME=86400  # 24 hours
SESSION_COOKIE_NAME=quickdesk_session
```

### Internationalization

```env
LANGUAGES=en,es,fr,de
DEFAULT_LANGUAGE=en
BABEL_DEFAULT_LOCALE=en
BABEL_DEFAULT_TIMEZONE=UTC
```

## 🧪 Testing Configuration

Create a separate `.env.test` file:

```env
SECRET_KEY=test-secret-key
DATABASE_URL=sqlite:///test.db
TESTING=True
WTF_CSRF_ENABLED=False
MAIL_SUPPRESS_SEND=True
```

## 🐳 Docker Configuration

### docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/quickdesk
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=quickdesk
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

## 🔍 Troubleshooting

### Common Issues

1. **Email not sending:**
   - Check SMTP settings
   - Verify app password for Gmail
   - Check firewall settings

2. **File upload errors:**
   - Ensure upload directory exists and is writable
   - Check MAX_CONTENT_LENGTH setting
   - Verify file permissions

3. **Database connection errors:**
   - Verify DATABASE_URL format
   - Check database server is running
   - Ensure database exists

4. **Secret key errors:**
   - Generate a new SECRET_KEY
   - Ensure it's at least 32 characters
   - Don't use spaces or special characters

### Environment Validation

Run this script to validate your configuration:

```python
import os
from urllib.parse import urlparse

def validate_config():
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required variables: {missing_vars}")
        return False
    
    # Validate SECRET_KEY
    secret_key = os.getenv('SECRET_KEY')
    if len(secret_key) < 32:
        print("SECRET_KEY should be at least 32 characters long")
        return False
    
    # Validate DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    try:
        parsed = urlparse(db_url)
        if not parsed.scheme:
            print("Invalid DATABASE_URL format")
            return False
    except:
        print("Invalid DATABASE_URL")
        return False
    
    print("Configuration validation passed!")
    return True

if __name__ == '__main__':
    validate_config()
```

## 📞 Support

If you encounter issues with configuration:

1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Test email configuration with a simple test
4. Ensure all required services (database, Redis) are running
5. Check file permissions for upload directories

For additional help, refer to the main README.md or create an issue in the project repository.
