# 🚀 Supabase Setup Guide - Persistent Database Backup

This guide shows you how to set up Supabase as a persistent database option for your Streamlit app. This is useful if you need to demonstrate data persistence during your presentation.

---

## 📋 Why Supabase?

- ✅ **Free tier** - Perfect for school projects (500 MB storage, generous limits)
- ✅ **PostgreSQL database** - Industry-standard, reliable
- ✅ **Easy setup** - Get started in minutes
- ✅ **Persistent storage** - Data survives app restarts
- ✅ **No credit card required** for free tier

---

## 🔧 Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email
4. Verify your email if needed

---

## 📦 Step 2: Create a New Project

1. Click "New Project"
2. Fill in the details:
   - **Project Name**: `tcc-data-platform` (or your choice)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free
3. Click "Create new project"
4. Wait 2-3 minutes for project setup

---

## 🔑 Step 3: Get Your Connection String

1. In your Supabase project dashboard (https://supabase.com/dashboard):
   - Click on your project name or go directly to your project
   - You should see your project URL like: `https://xxxxx.supabase.co`

2. Navigate to **Settings**:
   - Look for the gear icon (⚙️) in the left sidebar
   - Click on **Settings**

3. Go to **Database** section:
   - In the Settings page, click on **Database** in the left menu
   - Or scroll down to find the Database section

4. Find **Connection string**:
   - Scroll down to the **Connection string** section
   - You'll see different tabs: **URI**, **JDBC**, **Golang**, etc.
   - Click on the **URI** tab

5. Copy the connection string:
   - It will look like this:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
   Or the direct connection:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
   
   **Important**: 
   - Replace `[YOUR-PASSWORD]` with the database password you created when setting up the project
   - If you forgot the password, you'll need to reset it (see troubleshooting below)

6. **For your project URL** (`https://pscxqbieyoimkpkspmsa.supabase.co`):
   - Your project reference is: `pscxqbieyoimkpkspmsa`
   - Your connection string will be:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.pscxqbieyoimkpkspmsa.supabase.co:5432/postgres
   ```
   - Replace `[YOUR-PASSWORD]` with your actual database password

---

## 📝 Step 4: Add to Streamlit Cloud Secrets

1. In Streamlit Cloud, go to your app settings
2. Open **Secrets** editor
3. Add your Supabase connection:

```toml
# Database Configuration
[database]
# Use "sqlite" for local/ephemeral or "supabase" for persistent
db_type = "sqlite"

# Supabase Connection (only needed if db_type = "supabase")
[supabase]
connection_string = "postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
```

**Security Note**: The password is in the connection string - this is secure in Streamlit Cloud's encrypted secrets.

---

## 🔄 Step 5: Update Your Code

Your code has been updated to automatically use Supabase if configured. The database manager will:
- Use **SQLite** by default (current setup)
- Automatically switch to **Supabase** if `db_type = "supabase"` in secrets

---

## ✅ Step 6: Test the Connection

1. Deploy your app with Supabase secrets
2. First user registration will create tables automatically
3. Data will now persist across app restarts!

---

## 🔀 Switching Between Databases

### Use SQLite (Default - Ephemeral)
```toml
[database]
db_type = "sqlite"
```

### Use Supabase (Persistent)
```toml
[database]
db_type = "supabase"

[supabase]
connection_string = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
```

---

## 📊 Supabase Free Tier Limits

- **Database Size**: 500 MB
- **Database Egress**: 2 GB/month
- **API Requests**: 50,000/month
- **Auth Users**: 50,000

**For a school project, this is more than enough!**

---

## 🛠️ Troubleshooting

### Can't Find Connection String?
1. Make sure you're logged into https://supabase.com/dashboard
2. Click on your project (should show your project URL)
3. Click **Settings** (⚙️ icon in sidebar) → **Database**
4. Scroll to **Connection string** section
5. If you still don't see it, try:
   - **Project Settings** → **Database** → **Connection string**

### Forgot Database Password?
1. Go to **Settings** → **Database**
2. Look for **Database password** section
3. Click **Reset database password** (if available)
4. Or check your project setup email/notes for the password

### Connection Error
- **Check password**: Make sure the password in the connection string matches your database password
- **Check network**: Ensure your Supabase project is active (free tier pauses after 1 week of inactivity)
- **Check URL format**: Use the format: `postgresql://postgres:PASSWORD@db.PROJECT-REF.supabase.co:5432/postgres`

### Using Pooler Connection (Recommended for Production)
Supabase also provides a connection pooler. For your project, you can use:
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```
But for simplicity, the direct connection works fine:
```
postgresql://postgres:[PASSWORD]@db.pscxqbieyoimkpkspmsa.supabase.co:5432/postgres
```

### Tables Not Created
- The first user registration should create tables automatically
- Check Supabase dashboard → Table Editor to see if tables exist

### Migration from SQLite
- If you have existing SQLite data, you can export it and import to Supabase
- For school projects, fresh start is usually fine

---

## 🎯 Quick Reference

**Supabase Dashboard**: https://supabase.com/dashboard

**Connection String Format**:
```
postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres
```

**Streamlit Secrets Format**:
```toml
[database]
db_type = "supabase"

[supabase]
connection_string = "your-connection-string-here"
```

---

## 💡 Presentation Tips

When asked about data persistence, you can say:

> "By default, we use SQLite for quick local development. However, for production deployments requiring persistent storage, we've integrated Supabase PostgreSQL, which provides:
> - Persistent data storage across sessions
> - Industry-standard PostgreSQL database
> - Free tier suitable for small to medium projects
> - Easy scalability when needed"

The code automatically switches between databases based on configuration - no code changes needed!

---

## ✅ Setup Checklist

- [ ] Created Supabase account
- [ ] Created new project
- [ ] Saved database password securely
- [ ] Copied connection string
- [ ] Added secrets to Streamlit Cloud
- [ ] Tested app deployment
- [ ] Verified tables are created
- [ ] Tested data persistence (register user, restart app, user still exists)

---

**🎉 You're all set!** Your app now has persistent database backup option ready to go!

