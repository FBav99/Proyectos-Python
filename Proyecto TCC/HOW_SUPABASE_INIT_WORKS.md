# 🔧 How Database Auto-Initialization Works in Supabase

## 📋 Current Status

You have Supabase configured, but you're still using SQLite because:

```toml
[database]
db_type = "sqlite"  # ❌ This makes it use SQLite
```

## ✅ Fix: Change to Supabase

In your **Streamlit Cloud Secrets**, change:

```toml
[database]
db_type = "supabase"  # ✅ Change this from "sqlite" to "supabase"
```

## 🔄 How Auto-Initialization Works

### Step 1: App Starts
When your Streamlit app starts, it imports `core.database`, which automatically:

1. **Detects database type** from secrets:
   ```python
   db_type = st.secrets.get("database", {}).get("db_type", "sqlite")
   ```

2. **Creates DatabaseManager** with the correct connection:
   - If `db_type = "supabase"` → Uses PostgreSQL connection
   - If `db_type = "sqlite"` → Uses SQLite file

### Step 2: Auto-Initialization Check
The code automatically runs `_auto_init_database()` which:

1. **Checks if database exists**:
   ```python
   if not db_manager.check_database_exists():
   ```

2. **For Supabase**: Checks if `users` table exists
   ```python
   # In check_database_exists() for Supabase:
   cursor.execute("""
       SELECT EXISTS (
           SELECT FROM information_schema.tables 
           WHERE table_schema = 'public' 
           AND table_name = 'users'
       )
   """)
   ```

3. **If tables don't exist**: Calls `init_database()`

### Step 3: Table Creation
`init_database()` creates all tables using `CREATE TABLE IF NOT EXISTS`:

```python
def init_database(self):
    """Initialize database with essential tables"""
    self.create_users_table()
    self.create_user_sessions_table()
    self.create_user_progress_table()
    self.create_quiz_attempts_table()
    self.create_quiz_answers_table()
    self.create_rate_limiting_table()
    self.create_survey_responses_table()
    self.create_dashboards_table()
    self.create_indexes()
```

### Step 4: PostgreSQL-Specific SQL
Each `create_*_table()` method uses different SQL for PostgreSQL vs SQLite:

**For Supabase (PostgreSQL):**
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    ...
)
```

**For SQLite:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    ...
)
```

## 🎯 What Happens When You Change to Supabase

1. **First App Restart After Change**:
   - Code detects `db_type = "supabase"`
   - Connects to your Supabase PostgreSQL database
   - Checks if tables exist (they won't, it's a new database)
   - Automatically creates all tables
   - Your app is ready! ✅

2. **Subsequent Restarts**:
   - Code connects to Supabase
   - Tables already exist (from first run)
   - Skips table creation
   - All your data is still there! 🎉

## 📝 Complete Secrets Configuration

After changing to Supabase, your secrets should look like:

```toml
# Database Configuration
[database]
db_type = "supabase"  # ✅ Changed from "sqlite"

# Supabase Connection
[supabase]
connection_string = "postgresql://postgres:Totote905!@db.pscxqbieyoimkpkspmsa.supabase.co:5432/postgres"
```

## ✅ Verification Steps

1. **Change `db_type` to `"supabase"`** in Streamlit Cloud Secrets
2. **Save secrets** (app will automatically restart)
3. **Check logs** in Streamlit Cloud → Manage app → Logs
4. Look for:
   ```
   Auto-initializing database on module import...
   Database auto-initialized successfully
   ```
5. **Test**: Register a new user
6. **Restart app** (or wait for container restart)
7. **Login again** → User should still exist! ✅

## 🔍 Troubleshooting

### "Table already exists" error
- This is normal if tables were already created
- The code uses `CREATE TABLE IF NOT EXISTS`, so it's safe
- You can ignore this message

### "Cannot connect to Supabase"
- Check connection string format
- Verify password is correct (no extra spaces)
- Ensure `psycopg2-binary` is in `requirements.txt`

### Still using SQLite?
- Verify secrets are saved correctly
- Check `db_type = "supabase"` (not "sqlite")
- Restart app after changing secrets

## 📊 Tables Created Automatically

1. `users` - User accounts and authentication
2. `user_sessions` - Active sessions
3. `user_progress` - Learning progress tracking
4. `quiz_attempts` - Quiz results
5. `quiz_answers` - Detailed quiz answers
6. `rate_limiting` - Security rate limiting
7. `uploaded_files` - File uploads
8. `file_analysis_sessions` - Analysis history

All created automatically on first run! 🚀

