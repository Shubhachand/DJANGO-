# Deployment Guide

## Local Development (Current Setup)

The project is already set up for local development. Just run:

```bash
source venv/bin/activate
python manage.py runserver
```

## Production Deployment Options

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # macOS
```

2. **Create Heroku App**
```bash
heroku create your-library-app
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Update requirements.txt**
```bash
pip install gunicorn psycopg2-binary whitenoise
pip freeze > requirements.txt
```

5. **Create Procfile**
```
web: gunicorn myproject.wsgi
```

6. **Update settings.py for production**
```python
import dj_database_url

# Add to settings.py
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
STATIC_ROOT = BASE_DIR / 'staticfiles'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

7. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py setup_demo
```

### Option 2: Deploy to PythonAnywhere

1. **Upload code to PythonAnywhere**
2. **Create virtual environment**
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

3. **Configure WSGI file**
```python
import sys
import os

path = '/home/yourusername/myproject'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. **Set up static files**
```bash
python manage.py collectstatic
```

5. **Run migrations**
```bash
python manage.py migrate
python manage.py setup_demo
```

### Option 3: Deploy to DigitalOcean/AWS/VPS

1. **Install dependencies on server**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. **Clone repository**
```bash
git clone your-repo-url
cd your-repo
```

3. **Setup virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. **Configure Gunicorn**
```bash
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

5. **Setup Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }
    
    location /media/ {
        root /path/to/your/project;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Setup systemd service**
```ini
[Unit]
Description=Library Management System
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Production Settings Checklist

### Security Settings

Update `myproject/settings.py`:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Generate new secret key
SECRET_KEY = 'your-new-secret-key-here'
```

### Database Configuration

For PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'library_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

For MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_db',
        'USER': 'library_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Static Files

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# For production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files

For production, consider using cloud storage:

```python
# AWS S3 Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
```

## Environment Variables

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

Install python-decouple:
```bash
pip install python-decouple
```

Update settings.py:
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
```

## Pre-Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup production database
- [ ] Configure static files
- [ ] Setup media file storage
- [ ] Enable HTTPS
- [ ] Setup backup system
- [ ] Configure logging
- [ ] Setup monitoring
- [ ] Test all features
- [ ] Create superuser
- [ ] Load initial data

## Post-Deployment Tasks

1. **Create superuser**
```bash
python manage.py createsuperuser
```

2. **Collect static files**
```bash
python manage.py collectstatic
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Load demo data (optional)**
```bash
python manage.py setup_demo
```

5. **Test the application**
- Test login/logout
- Test book CRUD operations
- Test QR code generation
- Test fine calculation
- Test search functionality

## Monitoring & Maintenance

### Setup Logging

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Backup Database

```bash
# PostgreSQL
pg_dump library_db > backup.sql

# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

### Monitor Application

Consider using:
- Sentry for error tracking
- New Relic for performance monitoring
- Uptime Robot for uptime monitoring

## Scaling Considerations

### Database Optimization
- Add database indexes
- Use database connection pooling
- Implement caching (Redis/Memcached)

### Performance
- Enable Django caching
- Use CDN for static files
- Optimize images and QR codes
- Implement pagination for large lists

### Load Balancing
- Use multiple application servers
- Setup load balancer (Nginx/HAProxy)
- Use database replication

## Support & Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --clear
```

**Database connection errors:**
- Check database credentials
- Verify database server is running
- Check firewall settings

**QR codes not generating:**
- Ensure Pillow is installed
- Check media directory permissions
- Verify MEDIA_ROOT and MEDIA_URL settings

## Conclusion

Choose the deployment option that best fits your needs:
- **Heroku:** Easiest, good for small to medium apps
- **PythonAnywhere:** Simple, Python-focused hosting
- **VPS (DigitalOcean/AWS):** Most control, scalable

For production use, always:
- Use HTTPS
- Keep dependencies updated
- Regular backups
- Monitor application health
- Follow security best practices

Good luck with your deployment! 🚀
