"""
Database utilities for TCC Data Analysis Platform
Handles SQLite database connections, migrations, and basic operations
"""

import sqlite3
import os
import json
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import bcrypt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = 'tcc_database.db'
MIGRATIONS_DIR = 'migrations'

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.ensure_migrations_dir()
    
    def ensure_migrations_dir(self):
        """Ensure migrations directory exists"""
        if not os.path.exists(MIGRATIONS_DIR):
            os.makedirs(MIGRATIONS_DIR)
            logger.info(f"Created migrations directory: {MIGRATIONS_DIR}")
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper configuration"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with essential tables including file uploads"""
        logger.info("Initializing database with essential tables...")
        
        # Create essential tables
        self.create_users_table()
        self.create_user_sessions_table()
        self.create_user_progress_table()
        self.create_quiz_attempts_table()
        self.create_quiz_answers_table()
        self.create_rate_limiting_table()
        
        # File upload tables (needed for data analysis)
        self.create_uploaded_files_table()
        self.create_file_analysis_sessions_table()
        
        # Optional tables (can be enabled later if needed)
        # self.create_user_activity_log_table()
        
        # Create indexes
        self.create_indexes()
        
        logger.info("Database initialization completed with essential tables and file uploads")
    
    def create_users_table(self):
        """Create users table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    failed_login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    email_verified BOOLEAN DEFAULT 0,
                    verification_token VARCHAR(255),
                    reset_token VARCHAR(255),
                    reset_token_expires TIMESTAMP
                )
            """)
            conn.commit()
    
    def create_user_sessions_table(self):
        """Create user sessions table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_user_progress_table(self):
        """Create user progress table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    nivel1_completed BOOLEAN DEFAULT 0,
                    nivel2_completed BOOLEAN DEFAULT 0,
                    nivel3_completed BOOLEAN DEFAULT 0,
                    nivel4_completed BOOLEAN DEFAULT 0,
                    total_time_spent INTEGER DEFAULT 0,
                    data_analyses_created INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_quiz_attempts_table(self):
        """Create quiz attempts table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    level VARCHAR(20) NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    percentage DECIMAL(5,2) NOT NULL,
                    passed BOOLEAN NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    time_taken INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_quiz_answers_table(self):
        """Create quiz answers table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quiz_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_attempt_id INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    selected_answer TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL,
                    explanation TEXT,
                    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_achievements_table(self):
        """Create achievements table (optional - for future gamification)"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_type VARCHAR(50) NOT NULL,
                    achievement_title VARCHAR(100) NOT NULL,
                    achievement_description TEXT,
                    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_uploaded_files_table(self):
        """Create uploaded files table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    original_filename VARCHAR(255) NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_type VARCHAR(50) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_file_analysis_sessions_table(self):
        """Create file analysis sessions table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_analysis_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    file_id INTEGER NOT NULL,
                    session_name VARCHAR(100),
                    filters_applied TEXT,
                    metrics_calculated TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration_minutes INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_dashboards_table(self):
        """Create dashboards table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dashboards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    dashboard_name VARCHAR(100) NOT NULL,
                    dashboard_config TEXT NOT NULL,
                    is_public BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_dashboard_components_table(self):
        """Create dashboard components table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dashboard_components (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dashboard_id INTEGER NOT NULL,
                    component_type VARCHAR(50) NOT NULL,
                    component_config TEXT NOT NULL,
                    position_x INTEGER,
                    position_y INTEGER,
                    width INTEGER,
                    height INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dashboard_id) REFERENCES dashboards(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_user_activity_log_table(self):
        """Create user activity log table (optional - for security auditing)"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type VARCHAR(50) NOT NULL,
                    activity_details TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    
    def create_system_metrics_table(self):
        """Create system metrics table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name VARCHAR(100) NOT NULL,
                    metric_value DECIMAL(10,2) NOT NULL,
                    metric_unit VARCHAR(20),
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    additional_data TEXT
                )
            """)
            conn.commit()
    
    def create_rate_limiting_table(self):
        """Create rate limiting table"""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rate_limiting (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifier VARCHAR(100) NOT NULL,
                    attempts INTEGER DEFAULT 0,
                    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    locked_until TIMESTAMP
                )
            """)
            conn.commit()
    
    def create_indexes(self):
        """Create database indexes for performance"""
        with self.get_connection() as conn:
            # User authentication indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token)")
            
            # Session management indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)")
            
            # Progress tracking indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_progress_user_id ON user_progress(user_id)")
            
            # Quiz indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_level ON quiz_attempts(user_id, level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_quiz_attempts_completed ON quiz_attempts(completed_at)")
            
            # File management indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_files_user_id ON uploaded_files(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_files_uploaded_at ON uploaded_files(uploaded_at)")
            
            # Dashboard indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_dashboards_user_id ON dashboards(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_dashboards_public ON dashboards(is_public)")
            
            # Activity tracking indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_user_type ON user_activity_log(user_id, activity_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_created ON user_activity_log(created_at)")
            
            # Rate limiting indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rate_limiting_identifier ON rate_limiting(identifier)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rate_limiting_last_attempt ON rate_limiting(last_attempt)")
            
            conn.commit()
    
    def check_database_exists(self) -> bool:
        """Check if database file exists"""
        return os.path.exists(self.db_path)
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        if not self.check_database_exists():
            return {"exists": False}
        
        with self.get_connection() as conn:
            # Get table count
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row['name'] for row in cursor.fetchall()]
            
            # Get user count
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            # Get file size
            file_size = os.path.getsize(self.db_path)
            
            return {
                "exists": True,
                "tables": tables,
                "user_count": user_count,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }

# Global database manager instance
db_manager = DatabaseManager()

def get_db_connection():
    """Get database connection (for backward compatibility)"""
    return db_manager.get_connection()

def init_database():
    """Initialize database (for backward compatibility)"""
    return db_manager.init_database()

def check_database_exists():
    """Check if database exists (for backward compatibility)"""
    return db_manager.check_database_exists()

def get_database_info():
    """Get database info (for backward compatibility)"""
    return db_manager.get_database_info()
