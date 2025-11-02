# 🚀 Streamlit Cloud Deployment Guide

This guide will walk you through deploying your TCC project to Streamlit Cloud.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Your project in a GitHub repository
- ✅ A Streamlit Cloud account (free tier available)
- ✅ OAuth credentials (if you want to use Google/Microsoft login)

---

## 🔧 Step 1: Project Configuration Files

### ✅ What's Already Set Up

Your project already has:
- ✅ `requirements.txt` - All dependencies listed
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.streamlit/secrets.toml.example` - Example secrets file
- ✅ `.gitignore` - Properly configured (secrets excluded)
- ✅ Entry point: `Inicio.py`

### ⚠️ What Needs Configuration

#### 1. **Database Initialization**

The database (`tcc_database.db`) needs to be initialized on first run. You have two options:

**Option A: Automatic Initialization (Recommended)**

Add this to your `Inicio.py` at the beginning of the `main()` function:

```python
from core.database import init_database, check_database_exists

def main():
    """Función principal de la aplicación - Punto de entrada principal"""
    
    # Initialize database if it doesn't exist
    if not check_database_exists():
        init_database()
    
    # ... rest of your code
```

**Option B: Manual Initialization Script**

Create a one-time initialization that runs before the app starts (not recommended for Streamlit Cloud).

---

## 🔐 Step 2: Configure Secrets in Streamlit Cloud

### What You Need to Set Up

Your app uses OAuth (Google/Microsoft), so you'll need to configure secrets in Streamlit Cloud.

### How to Set Secrets in Streamlit Cloud:

1. **Go to your Streamlit Cloud Dashboard**
   - Navigate to: https://share.streamlit.io/
   - Select your app

2. **Open Secrets Management**
   - Click on "⚙️ Settings" (or "Manage app" → "⚙️ Settings")
   - Scroll down to "Secrets" section
   - Click "Edit secrets" or "Open secrets editor"

3. **Add Your Secrets**

Add the following secrets in TOML format:

```toml
# OAuth Configuration
oauth_configured = true

# Google OAuth (if using)
[google_oauth]
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
redirect_uri = "https://your-app-name.streamlit.app/oauth_callback"

# Microsoft OAuth (if using)
[microsoft_oauth]
client_id = "your-microsoft-client-id"
client_secret = "your-microsoft-client-secret"
redirect_uri = "https://your-app-name.streamlit.app/oauth_callback"
```

### 📝 Important Notes:

1. **Update Redirect URIs in OAuth Providers:**
   - **Google Cloud Console**: Add your Streamlit Cloud URL to authorized redirect URIs
   - **Microsoft Azure Portal**: Add your Streamlit Cloud URL to redirect URIs
   - Format: `https://your-app-name.streamlit.app/oauth_callback`

2. **If You Don't Use OAuth:**
   ```toml
   oauth_configured = false
   ```
   You can leave the OAuth sections empty or omit them.

---

## 📦 Step 3: Deploy to Streamlit Cloud

### Method 1: Deploy from GitHub (Recommended)

1. **Push Your Code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your GitHub repository
   - Select branch: `main` (or your default branch)
   - Main file path: `Inicio.py`

3. **Configure App Settings**
   - App URL: Choose your desired subdomain
   - Python version: 3.11 (or latest supported)
   - Advanced settings: Usually not needed

4. **Deploy**
   - Click "Deploy!"
   - Wait for the build to complete

### Method 2: Deploy via Streamlit CLI (Alternative)

```bash
streamlit deploy
```

---

## 🔍 Step 4: Post-Deployment Checklist

### ✅ Verify Everything Works:

1. **Database Initialization**
   - First user registration should create the database automatically
   - Check that tables are created on first run

2. **Authentication**
   - Test local username/password login
   - Test registration of new users
   - Test OAuth (if configured)

3. **Features**
   - Test file upload
   - Test data analysis features
   - Test learning levels
   - Test dashboard generation

---

## ⚠️ Common Issues and Solutions

### Issue 1: Database Not Initialized

**Error:** `sqlite3.OperationalError: no such table: users`

**Solution:** Add database initialization check in `Inicio.py`:

```python
from core.database import init_database, check_database_exists

def main():
    # Initialize database if needed
    if not check_database_exists():
        init_database()
    # ... rest of code
```

### Issue 2: OAuth Not Working

**Error:** OAuth redirect fails or shows errors

**Solutions:**
1. Verify redirect URI matches exactly in OAuth provider settings
2. Check that secrets are correctly set in Streamlit Cloud
3. Ensure `oauth_configured = true` in secrets
4. Format: `https://your-app-name.streamlit.app/oauth_callback` (note: no trailing slash)

### Issue 3: Missing Dependencies

**Error:** Import errors or missing modules

**Solution:** 
- Verify all packages are in `requirements.txt`
- Check that Python version is compatible
- Review deployment logs for specific errors

### Issue 4: File Upload Issues

**Solution:** 
- Streamlit Cloud has file size limits (usually 200MB per file)
- Consider using Streamlit Cloud's file system limitations
- For larger files, consider cloud storage solutions

---

## 🔒 Security Best Practices

### ✅ Already Implemented:

- ✅ Secrets file excluded from Git (`.gitignore`)
- ✅ Error details hidden (`config.toml`)
- ✅ Rate limiting for login attempts
- ✅ Secure password hashing (bcrypt)
- ✅ Session management with timeouts

### 📝 Additional Recommendations:

1. **Review Secrets Regularly**
   - Rotate OAuth credentials periodically
   - Remove unused secrets

2. **Monitor Usage**
   - Check Streamlit Cloud analytics
   - Monitor for suspicious activity

3. **Backup Database** (if needed)
   - Streamlit Cloud uses ephemeral storage
   - Consider database backups if user data is critical
   - SQLite databases reset on app restart in free tier

---

## 📊 Streamlit Cloud Limitations (Free Tier)

- **App sleeps after 7 days of inactivity**
- **50GB bandwidth per month**
- **SQLite databases are ephemeral** (reset on restart)
- **File upload size limit: ~200MB**
- **No persistent storage** between deployments

### 💡 Solutions for Persistent Storage:

1. **Use Supabase (Recommended for School Projects)**
   - Free tier with 500MB storage
   - See `SUPABASE_SETUP_GUIDE.md` for detailed instructions
   - Just add secrets and your app automatically uses PostgreSQL
   
2. **Other Options:**
   - Use Streamlit Cloud Secrets for configuration
   - Use External Database (PostgreSQL, MySQL) for production
   - Use Cloud Storage (AWS S3, Google Cloud Storage) for files

---

## 🎯 Quick Reference

### Required Secrets Format:

```toml
# OAuth Configuration (optional)
oauth_configured = true/false

[google_oauth]
client_id = "..."
client_secret = "..."
redirect_uri = "https://your-app.streamlit.app/oauth_callback"

[microsoft_oauth]
client_id = "..."
client_secret = "..."
redirect_uri = "https://your-app.streamlit.app/oauth_callback"

# Database Configuration (optional - for persistent storage with Supabase)
[database]
db_type = "sqlite"  # or "supabase" for persistent storage

[supabase]
connection_string = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
```

### Database Initialization:

Add to `Inicio.py` main function:
```python
from core.database import init_database, check_database_exists

if not check_database_exists():
    init_database()
```

---

## 📞 Need Help?

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Forums**: https://discuss.streamlit.io/
- **Your Project Docs**: Check `docs/` folder for detailed guides

---

## ✅ Deployment Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` up to date
- [ ] Database initialization added to `Inicio.py`
- [ ] OAuth redirect URIs updated in provider settings
- [ ] Secrets configured in Streamlit Cloud
- [ ] App deployed successfully
- [ ] Tested user registration
- [ ] Tested user login
- [ ] Tested OAuth (if applicable)
- [ ] Tested core features
- [ ] Verified error handling

---

**🎉 Ready to Deploy!**

Once all steps are complete, your app should be live on Streamlit Cloud!

