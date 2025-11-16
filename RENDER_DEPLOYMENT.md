# 🚀 Deploy to Render - Step by Step Guide

Complete guide to deploy your Django Library Management System to Render.

## 📋 Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Your project code pushed to GitHub

---

## 🎯 Quick Deployment (Automatic)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Library Management System"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com/
   - Click "New +" button
   - Select "Blueprint"

2. **Connect Repository**
   - Connect your GitHub account
   - Select your repository
   - Render will detect `render.yaml` automatically

3. **Deploy**
   - Click "Apply"
   - Render will automatically:
     - Create PostgreSQL database
     - Create web service
     - Install dependencies
     - Run migrations
     - Setup demo data
     - Deploy your app

4. **Wait for Deployment**
   - First deployment takes 5-10 minutes
   - Watch the build logs

5. **Access Your App**
   - Once deployed, you'll get a URL like:
   - `https://library-management-system-xxxx.onrender.com`

---

## 🔧 Manual Deployment (Alternative)

If you prefer manual setup:

### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name:** `library-db`
   - **Database:** `library_management`
   - **User:** `library_user`
   - **Region:** Oregon (or closest to you)
   - **Plan:** Free
4. Click "Create Database"
5. Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `library-management-system`
   - **Region:** Oregon (same as database)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn myproject.wsgi:application`
   - **Plan:** Free

### Step 3: Add Environment Variables

In the web service settings, add these environment variables:

```
SECRET_KEY = [Click "Generate" to create a secure key]
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
DATABASE_URL = [Paste the Internal Database URL from Step 1]
PYTHON_VERSION = 3.13.0
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will start building and deploying
3. Monitor the logs for any errors

---

## 🔐 Environment Variables Explained

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | Auto-generated | Django secret key for security |
| `DEBUG` | `False` | Disable debug mode in production |
| `ALLOWED_HOSTS` | Your Render URL | Allowed hostnames |
| `DATABASE_URL` | PostgreSQL URL | Database connection string |
| `PYTHON_VERSION` | `3.13.0` | Python version to use |

---

## 📝 Post-Deployment Steps

### 1. Access Your Application

Visit your Render URL: `https://your-app-name.onrender.com`

### 2. Login with Demo Accounts

**Librarian:**
- Username: `librarian`
- Password: `librarian123`

**Student:**
- Username: `student1`
- Password: `student123`

### 3. Create Superuser (Optional)

If you want to create your own admin account:

1. Go to Render Dashboard
2. Select your web service
3. Click "Shell" tab
4. Run:
```bash
python manage.py createsuperuser
```

### 4. Test All Features

- ✅ Login as librarian
- ✅ Add a new book
- ✅ Login as student
- ✅ Request a book
- ✅ Check QR codes are generating
- ✅ Test search functionality

---

## 🎨 Custom Domain (Optional)

### Add Your Own Domain

1. Go to your web service settings
2. Click "Custom Domains"
3. Add your domain (e.g., `library.yourdomain.com`)
4. Update DNS records as instructed
5. Update `ALLOWED_HOSTS` environment variable:
   ```
   ALLOWED_HOSTS = your-app-name.onrender.com,library.yourdomain.com
   ```

---

## 🔄 Updating Your App

### Deploy Updates

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy!

### Manual Redeploy

1. Go to Render Dashboard
2. Select your web service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## 📊 Monitoring

### View Logs

1. Go to your web service in Render
2. Click "Logs" tab
3. Monitor real-time logs

### Check Metrics

1. Click "Metrics" tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🐛 Troubleshooting

### Build Fails

**Error:** `Permission denied: ./build.sh`
```bash
# Fix locally and push:
chmod +x build.sh
git add build.sh
git commit -m "Fix build script permissions"
git push
```

**Error:** `Module not found`
```bash
# Check requirements.txt has all dependencies
# Add missing package and push
```

### Database Connection Issues

1. Verify `DATABASE_URL` is set correctly
2. Check database is in same region as web service
3. Use **Internal Database URL** (not External)

### Static Files Not Loading

1. Check `STATIC_ROOT` is set to `staticfiles`
2. Verify `whitenoise` is in `requirements.txt`
3. Run `python manage.py collectstatic` in shell

### QR Codes Not Generating

1. Check `Pillow` is installed
2. Verify `media` directory permissions
3. Check logs for PIL/Pillow errors

### 502 Bad Gateway

- Wait a few minutes (cold start on free tier)
- Check logs for Python errors
- Verify `gunicorn` is installed

---

## 💰 Render Free Tier Limits

**Web Service:**
- 750 hours/month (enough for 1 app running 24/7)
- Spins down after 15 minutes of inactivity
- Cold start takes ~30 seconds

**PostgreSQL:**
- 1 GB storage
- 90 days retention
- Expires after 90 days (backup your data!)

**Tips:**
- Keep your app active with uptime monitoring
- Upgrade to paid plan for production use
- Backup database regularly

---

## 🔒 Security Checklist

Before going live:

- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` generated
- ✅ `ALLOWED_HOSTS` configured
- ✅ HTTPS enabled (automatic on Render)
- ✅ Database password secure
- ✅ Change default demo passwords
- ✅ Regular backups enabled

---

## 📦 Backup Your Data

### Export Database

```bash
# In Render Shell
python manage.py dumpdata > backup.json
```

### Download Backup

1. Go to Render Dashboard
2. Select your web service
3. Click "Shell"
4. Run backup command
5. Download the file

---

## 🚀 Performance Tips

### Optimize for Free Tier

1. **Keep App Warm:**
   - Use UptimeRobot or similar to ping your app every 5 minutes
   - Prevents cold starts

2. **Optimize Database:**
   - Add indexes to frequently queried fields
   - Use `select_related()` and `prefetch_related()`

3. **Cache Static Files:**
   - WhiteNoise handles this automatically
   - Compresses and caches static files

4. **Optimize Images:**
   - Compress QR codes
   - Use appropriate image formats

---

## 📞 Support

### Render Support

- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Project Issues

- Check logs in Render Dashboard
- Review Django error messages
- Test locally first

---

## 🎉 Success!

Your Django Library Management System is now live on Render!

**Your App URL:** `https://your-app-name.onrender.com`

**Next Steps:**
1. Share your app URL
2. Test all features
3. Monitor performance
4. Collect user feedback
5. Plan future enhancements

---

## 📚 Additional Resources

- [Render Django Guide](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [PostgreSQL Best Practices](https://render.com/docs/postgresql)

---

**Congratulations on deploying your Library Management System! 🎊**

Built with ❤️ using Django 5.2.8 | Deployed on Render
