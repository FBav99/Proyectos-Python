"""
Nombre del Archivo: database.py
Descripción: Utilidades de base de datos SQLite/PostgreSQL - Conexiones, migraciones y operaciones básicas
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

# Imports estándar
import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import bcrypt

# Try to import PostgreSQL support (optional - for Supabase)
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

# =============================================================================
# PostgreSQL wrappers to emulate SQLite-style convenience methods
# =============================================================================
class PostgresConnectionWrapper:
    """Wrapper that mimics sqlite3 connection API for psycopg2 connections."""

    def __init__(self, connection):
        self._connection = connection

    def _adapt_query(self, query, params):
        adapted_query = query.replace("?", "%s") if "?" in query else query
        adapted_params = self._adapt_params(params)
        return adapted_query, adapted_params

    def _adapt_params(self, params):
        if params is None:
            return None
        if isinstance(params, dict):
            return params
        return tuple(params)

    def cursor(self):
        raw_cursor = self._connection.cursor(cursor_factory=RealDictCursor)
        return PostgresCursorWrapper(raw_cursor, self)

    def execute(self, query, params=None):
        cursor = self.cursor()
        cursor.execute(query, params)
        return cursor

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        return self._connection.close()

    def __getattr__(self, item):
        return getattr(self._connection, item)


class PostgresCursorWrapper:
    """Adapter for psycopg2 cursor to provide sqlite-style interface (lastrowid, dict rows)."""

    def __init__(self, cursor, connection_wrapper):
        self._cursor = cursor
        self._connection_wrapper = connection_wrapper
        self._lastrowid = None

    def _update_lastrowid(self, adapted_query):
        query = adapted_query.lstrip().upper()
        if not query.startswith("INSERT"):
            self._lastrowid = None
            return

        try:
            temp_cursor = self._connection_wrapper._connection.cursor()
            try:
                temp_cursor.execute("SELECT LASTVAL()")
                result = temp_cursor.fetchone()
                self._lastrowid = result[0] if result else None
            finally:
                temp_cursor.close()
        except Exception:
            self._lastrowid = None

    def execute(self, query, params=None):
        adapted_query, adapted_params = self._connection_wrapper._adapt_query(query, params)
        if adapted_params is None:
            self._cursor.execute(adapted_query)
        else:
            self._cursor.execute(adapted_query, adapted_params)
        self._update_lastrowid(adapted_query)
        return self

    def executemany(self, query, seq_of_params):
        adapted_query, _ = self._connection_wrapper._adapt_query(query, None)
        if seq_of_params is None:
            self._cursor.executemany(adapted_query, None)
            self._lastrowid = None
            return self

        adapted_params_list = [
            self._connection_wrapper._adapt_params(params) for params in seq_of_params
        ]
        self._cursor.executemany(adapted_query, adapted_params_list)
        self._lastrowid = None
        return self

    @property
    def lastrowid(self):
        return self._lastrowid

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        return self._cursor.close()

    def __iter__(self):
        return iter(self._cursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattr__(self, item):
        return getattr(self._cursor, item)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de base de datos
DB_PATH = 'tcc_database.db'
MIGRATIONS_DIR = 'migrations'

# Detectar tipo de base de datos desde secrets (Streamlit Cloud)
def get_db_type():
    """Detecta el tipo de base de datos desde secrets"""
    try:
        import streamlit as st
        db_type = st.secrets.get("database", {}).get("db_type", "sqlite")
        return db_type.lower()
    except:
        return "sqlite"  # Default a SQLite

def get_supabase_connection_string():
    """Obtiene el connection string de Supabase desde secrets"""
    try:
        import streamlit as st
        return st.secrets.get("supabase", {}).get("connection_string", "")
    except:
        return ""

# ============================================================================
# DATABASE MANAGER CLASS
# ============================================================================

class DatabaseManager:
    """
    Administra conexiones de base de datos y operaciones.
    
    Esta clase gestiona todas las operaciones de base de datos incluyendo
    conexiones, creación de tablas, y operaciones CRUD básicas.
    """
    
    def __init__(self, db_path: str = DB_PATH):
        """Inicializa el gestor de base de datos con la ruta especificada"""
        self.db_path = db_path
        self.db_type = get_db_type()
        self.connection_string = get_supabase_connection_string() if self.db_type == "supabase" else None
        self.ensure_migrations_dir()
        
        # Verificar disponibilidad de PostgreSQL si se requiere
        if self.db_type == "supabase" and not POSTGRES_AVAILABLE:
            logger.warning("Supabase configurado pero psycopg2 no está instalado. Usando SQLite.")
            logger.warning("Instala con: pip install psycopg2-binary")
            self.db_type = "sqlite"
    
    def ensure_migrations_dir(self):
        """Asegura que el directorio de migraciones existe"""
        if not os.path.exists(MIGRATIONS_DIR):
            os.makedirs(MIGRATIONS_DIR)
            logger.info(f"Created migrations directory: {MIGRATIONS_DIR}")
    
    def _execute_sql(self, conn, sql):
        """Helper method to execute SQL for both SQLite and PostgreSQL"""
        if self.db_type == "supabase":
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor
        else:
            return conn.execute(sql)
    
    def get_boolean_literal(self, value: bool) -> str:
        """Return boolean literal suitable for current database backend"""
        if self.db_type == "supabase":
            return "TRUE" if value else "FALSE"
        return "1" if value else "0"
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper configuration (SQLite or PostgreSQL)"""
        if self.db_type == "supabase" and POSTGRES_AVAILABLE and self.connection_string:
            # PostgreSQL/Supabase connection
            raw_conn = None
            try:
                raw_conn = psycopg2.connect(self.connection_string)
                raw_conn.autocommit = False  # Use transactions
                conn = PostgresConnectionWrapper(raw_conn)
                yield conn
            except Exception as e:
                logger.error(f"PostgreSQL connection error: {e}")
                if raw_conn:
                    raw_conn.rollback()
                raise
            finally:
                if raw_conn:
                    raw_conn.close()
        else:
            # SQLite connection (default)
            # Add timeout to handle concurrent access (5 seconds)
            conn = sqlite3.connect(self.db_path, timeout=5.0)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            # Enable WAL mode for better concurrent access
            conn.execute("PRAGMA journal_mode = WAL")
            
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
        self.create_survey_responses_table()
        
        # File upload tables (needed for data analysis)
        self.create_uploaded_files_table()
        self.create_file_analysis_sessions_table()
        self.create_dashboards_table()
        self.create_dashboard_components_table()
        self.create_user_activity_log_table()
        
        # Optional tables (can be enabled later if needed)
        # self.create_user_activity_log_table()
        
        # Create indexes
        self.create_indexes()
        
        logger.info("Database initialization completed with essential tables and file uploads")
    
    def create_users_table(self):
        """Create users table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # SQL syntax differs slightly between SQLite and PostgreSQL
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE,
                        failed_login_attempts INTEGER DEFAULT 0,
                        locked_until TIMESTAMP,
                        email_verified BOOLEAN DEFAULT FALSE,
                        verification_token VARCHAR(255),
                        reset_token VARCHAR(255),
                        reset_token_expires TIMESTAMP
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id SERIAL PRIMARY KEY,
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
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_progress (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        nivel0_completed BOOLEAN DEFAULT FALSE,
                        nivel1_completed BOOLEAN DEFAULT FALSE,
                        nivel2_completed BOOLEAN DEFAULT FALSE,
                        nivel3_completed BOOLEAN DEFAULT FALSE,
                        nivel4_completed BOOLEAN DEFAULT FALSE,
                        total_time_spent INTEGER DEFAULT 0,
                        data_analyses_created INTEGER DEFAULT 0,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        nivel0_completed BOOLEAN DEFAULT 0,
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_attempts (
                        id SERIAL PRIMARY KEY,
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
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_answers (
                        id SERIAL PRIMARY KEY,
                        quiz_attempt_id INTEGER NOT NULL,
                        question_text TEXT NOT NULL,
                        selected_answer TEXT NOT NULL,
                        correct_answer TEXT NOT NULL,
                        is_correct BOOLEAN NOT NULL,
                        explanation TEXT,
                        FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS achievements (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        achievement_type VARCHAR(50) NOT NULL,
                        achievement_title VARCHAR(100) NOT NULL,
                        achievement_description TEXT,
                        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS uploaded_files (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        filename VARCHAR(255) NOT NULL,
                        original_filename VARCHAR(255) NOT NULL,
                        file_size INTEGER NOT NULL,
                        file_type VARCHAR(50) NOT NULL,
                        file_path VARCHAR(500) NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_analysis_sessions (
                        id SERIAL PRIMARY KEY,
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
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dashboards (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        dashboard_name VARCHAR(100) NOT NULL,
                        dashboard_config TEXT NOT NULL,
                        is_public BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS dashboard_components (
                        id SERIAL PRIMARY KEY,
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
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_activity_log (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        activity_type VARCHAR(50) NOT NULL,
                        activity_details TEXT,
                        ip_address VARCHAR(45),
                        user_agent TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_metrics (
                        id SERIAL PRIMARY KEY,
                        metric_name VARCHAR(100) NOT NULL,
                        metric_value DECIMAL(10,2) NOT NULL,
                        metric_unit VARCHAR(20),
                        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        additional_data TEXT
                    )
                """)
            else:
                cursor.execute("""
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
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rate_limiting (
                        id SERIAL PRIMARY KEY,
                        identifier VARCHAR(100) NOT NULL,
                        attempts INTEGER DEFAULT 0,
                        last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        locked_until TIMESTAMP
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rate_limiting (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifier VARCHAR(100) NOT NULL,
                        attempts INTEGER DEFAULT 0,
                        last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        locked_until TIMESTAMP
                    )
                """)
            conn.commit()
    
    def create_survey_responses_table(self):
        """Create survey responses table for all survey types"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS survey_responses (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        survey_type VARCHAR(50) NOT NULL,
                        level VARCHAR(20),
                        responses TEXT NOT NULL,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        UNIQUE(user_id, survey_type, level)
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS survey_responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        survey_type VARCHAR(50) NOT NULL,
                        level VARCHAR(20),
                        responses TEXT NOT NULL,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        UNIQUE(user_id, survey_type, level)
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
            
            # Survey indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_survey_user_type ON survey_responses(user_id, survey_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_survey_completed ON survey_responses(completed_at)")
            
            conn.commit()
    
    def check_database_exists(self) -> bool:
        """Check if database exists (SQLite file or PostgreSQL connection)"""
        if self.db_type == "supabase":
            # For PostgreSQL, check if we can connect and if tables exist
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'users'
                        )
                    """)
                    return cursor.fetchone()[0]
            except:
                return False
        else:
            # SQLite - check if file exists AND if tables are created
            if not os.path.exists(self.db_path):
                return False
            
            # Also verify that essential tables exist
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    # Check for essential tables
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name='users'
                    """)
                    if not cursor.fetchone():
                        return False  # Database file exists but tables not created
                    return True
            except:
                # If we can't connect, database might be corrupted or locked
                return False
    
    def ensure_database_initialized(self):
        """Ensure database is initialized - creates it if it doesn't exist or is incomplete"""
        if not self.check_database_exists():
            logger.info("Database not found or incomplete, initializing...")
            try:
                self.init_database()
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing database: {e}")
                raise
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        if not self.check_database_exists():
            return {"exists": False}
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if self.db_type == "supabase":
                # PostgreSQL query
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                
                return {
                    "exists": True,
                    "db_type": "PostgreSQL/Supabase",
                    "tables": tables,
                    "user_count": user_count,
                    "file_size_bytes": 0,  # Not applicable for PostgreSQL
                    "file_size_mb": 0
                }
            else:
                # SQLite query
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row['name'] for row in cursor.fetchall()]
                
                cursor.execute("SELECT COUNT(*) as count FROM users")
                user_count = cursor.fetchone()['count']
                
                file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    "exists": True,
                    "db_type": "SQLite",
                    "tables": tables,
                    "user_count": user_count,
                    "file_size_bytes": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 2)
                }

# Global database manager instance
db_manager = DatabaseManager()

# Auto-initialize database on module import (for Streamlit Cloud)
# This ensures the database is always ready when any module imports this
# Using a module-level flag to prevent multiple initializations
_db_initialized = False

def _auto_init_database():
    """Auto-initialize database when module is imported"""
    global _db_initialized
    if _db_initialized:
        return
    
    try:
        if not db_manager.check_database_exists():
            logger.info("Auto-initializing database on module import...")
            db_manager.init_database()
            logger.info("Database auto-initialized successfully")
        _db_initialized = True
    except Exception as e:
        # Don't fail on import if there's an error - let it fail later when actually used
        logger.warning(f"Could not auto-initialize database on import: {e}")
        # Still mark as attempted to avoid repeated tries
        _db_initialized = True

# Run auto-initialization (only once)
_auto_init_database()

def get_db_connection():
    """Get database connection (for backward compatibility)"""
    return db_manager.get_connection()

def init_database():
    """Initialize database (for backward compatibility)"""
    return db_manager.init_database()

def check_database_exists():
    """Check if database exists (for backward compatibility)"""
    return db_manager.check_database_exists()

def ensure_database_initialized():
    """Ensure database is initialized - creates it if it doesn't exist or is incomplete"""
    return db_manager.ensure_database_initialized()

def get_database_info():
    """Get database info (for backward compatibility)"""
    return db_manager.get_database_info()
