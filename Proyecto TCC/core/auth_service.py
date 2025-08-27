"""
Authentication service for TCC Data Analysis Platform
Handles user registration, login, session management, and password operations
"""

import streamlit as st
import bcrypt
import secrets
import hashlib
import json
import logging
import re
import html
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from core.database import db_manager
from core.security import security_manager

logger = logging.getLogger(__name__)

class AuthService:
    """Handles user authentication and session management"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour in seconds
    
    def register_user(self, username: str, email: str, password: str, 
                     first_name: str, last_name: str) -> Tuple[bool, str]:
        """Register a new user"""
        try:
            # Validate inputs
            if not username or not email or not password:
                return False, "All fields are required"
            
            # Server-side password validation
            password_valid, password_msg = self.validate_password_server_side(password)
            if not password_valid:
                return False, password_msg
            
            # Server-side input sanitization
            username = self.sanitize_input(username)
            email = self.sanitize_input(email)
            first_name = self.sanitize_input(first_name)
            last_name = self.sanitize_input(last_name)
            
            # Check if user already exists
            if self.user_exists(username, email):
                return False, "Username or email already exists"
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Create user
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (username, email, password_hash, first_name, last_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, email, password_hash, first_name, last_name))
                
                user_id = cursor.lastrowid
                
                # Create user progress record
                conn.execute("""
                    INSERT INTO user_progress (user_id)
                    VALUES (?)
                """, (user_id,))
                
                conn.commit()
            
            # Log activity
            self.log_activity(user_id, 'registration', {
                'username': username,
                'email': email
            })
            
            return True, "User registered successfully"
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, self.sanitize_error_message(e)
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate user login"""
        try:
            # Check rate limiting first
            rate_limit_ok, rate_limit_msg = self.check_rate_limit(username)
            if not rate_limit_ok:
                return False, rate_limit_msg, None
            
            # Sanitize inputs
            username = self.sanitize_input(username)
            
            # Get user from database
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM users 
                    WHERE username = ? AND is_active = 1
                """, (username,))
                user = cursor.fetchone()
            
            if not user:
                # Record failed attempt
                self.record_attempt(username, False)
                return False, "Invalid username or password", None
            
            # Check if account is locked
            if user['locked_until'] and datetime.fromisoformat(user['locked_until']) > datetime.now():
                return False, "Account is temporarily locked", None
            
            # Verify password
            if not self.verify_password(password, user['password_hash']):
                # Record failed attempt
                self.record_attempt(username, False)
                # Increment failed attempts
                self.increment_failed_attempts(user['id'])
                return False, "Invalid username or password", None
            
            # Record successful attempt
            self.record_attempt(username, True)
            # Reset failed attempts on successful login
            self.reset_failed_attempts(user['id'])
            
            # Update last login
            self.update_last_login(user['id'])
            
            # Create session
            session_token = self.create_session(user['id'])
            
            # Convert user to dict
            user_dict = dict(user)
            
            # Log activity
            self.log_activity(user['id'], 'login', {
                'username': username,
                'session_token': session_token[:10] + '...'  # Log partial token
            })
            
            return True, "Login successful", {
                'user': user_dict,
                'session_token': session_token
            }
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False, self.sanitize_error_message(e), None
    
    def verify_session(self, session_token: str) -> Tuple[bool, Optional[Dict]]:
        """Verify session token and return user data"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT u.*, s.expires_at 
                    FROM users u
                    JOIN user_sessions s ON u.id = s.user_id
                    WHERE s.session_token = ? AND u.is_active = 1
                """, (session_token,))
                result = cursor.fetchone()
            
            if not result:
                return False, None
            
            # Check if session is expired
            expires_at = datetime.fromisoformat(result['expires_at'])
            if expires_at < datetime.now():
                self.invalidate_session(session_token)
                return False, None
            
            # Update session activity
            self.update_session_activity(session_token)
            
            # Return user data (without sensitive fields)
            user_data = dict(result)
            user_data.pop('password_hash', None)
            user_data.pop('reset_token', None)
            user_data.pop('verification_token', None)
            
            return True, user_data
            
        except Exception as e:
            logger.error(f"Session verification error: {e}")
            return False, None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user by invalidating session"""
        try:
            # Get user ID from session
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT user_id FROM user_sessions 
                    WHERE session_token = ?
                """, (session_token,))
                result = cursor.fetchone()
            
            if result:
                # Log activity
                self.log_activity(result['user_id'], 'logout', {
                    'session_token': session_token[:10] + '...'
                })
            
            # Invalidate session
            self.invalidate_session(session_token)
            return True
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def user_exists(self, username: str, email: str) -> bool:
        """Check if user exists by username or email"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id FROM users 
                    WHERE username = ? OR email = ?
                """, (username, email))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"User exists check error: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def create_session(self, user_id: int) -> str:
        """Create a new session for user"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
        
        with db_manager.get_connection() as conn:
            conn.execute("""
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            """, (user_id, session_token, expires_at.isoformat()))
            conn.commit()
        
        return session_token
    
    def invalidate_session(self, session_token: str):
        """Invalidate a session"""
        with db_manager.get_connection() as conn:
            conn.execute("""
                DELETE FROM user_sessions WHERE session_token = ?
            """, (session_token,))
            conn.commit()
    
    def update_session_activity(self, session_token: str):
        """Update session last activity time"""
        with db_manager.get_connection() as conn:
            conn.execute("""
                UPDATE user_sessions 
                SET last_activity = ? 
                WHERE session_token = ?
            """, (datetime.now().isoformat(), session_token))
            conn.commit()
    
    def increment_failed_attempts(self, user_id: int):
        """Increment failed login attempts"""
        with db_manager.get_connection() as conn:
            conn.execute("""
                UPDATE users 
                SET failed_login_attempts = failed_login_attempts + 1
                WHERE id = ?
            """, (user_id,))
            
            # Lock account after 5 failed attempts
            conn.execute("""
                UPDATE users 
                SET locked_until = ?
                WHERE id = ? AND failed_login_attempts >= 5
            """, ((datetime.now() + timedelta(minutes=15)).isoformat(), user_id))
            
            conn.commit()
    
    def reset_failed_attempts(self, user_id: int):
        """Reset failed login attempts"""
        with db_manager.get_connection() as conn:
            conn.execute("""
                UPDATE users 
                SET failed_login_attempts = 0, locked_until = NULL
                WHERE id = ?
            """, (user_id,))
            conn.commit()
    
    def update_last_login(self, user_id: int):
        """Update user's last login time"""
        with db_manager.get_connection() as conn:
            conn.execute("""
                UPDATE users 
                SET last_login = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), user_id))
            conn.commit()
    
    def log_activity(self, user_id: int, activity_type: str, details: Dict[str, Any]):
        """Log user activity"""
        try:
            with db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO user_activity_log (user_id, activity_type, activity_details)
                    VALUES (?, ?, ?)
                """, (user_id, activity_type, json.dumps(details)))
                conn.commit()
        except Exception as e:
            logger.error(f"Activity logging error: {e}")
    
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Get user's learning progress"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM user_progress WHERE user_id = ?
                """, (user_id,))
                progress = cursor.fetchone()
                
                if progress:
                    return dict(progress)
                else:
                    # Create progress record if it doesn't exist
                    conn.execute("""
                        INSERT INTO user_progress (user_id)
                        VALUES (?)
                    """, (user_id,))
                    conn.commit()
                    
                    return {
                        'user_id': user_id,
                        'nivel1_completed': False,
                        'nivel2_completed': False,
                        'nivel3_completed': False,
                        'nivel4_completed': False,
                        'total_time_spent': 0,
                        'data_analyses_created': 0
                    }
        except Exception as e:
            logger.error(f"Get user progress error: {e}")
            return {}
    
    def update_user_progress(self, user_id: int, **updates) -> bool:
        """Update user's learning progress"""
        try:
            if not updates:
                return True
            
            # Build update query
            set_clauses = []
            values = []
            for key, value in updates.items():
                set_clauses.append(f"{key} = ?")
                values.append(value)
            
            values.append(datetime.now().isoformat())  # last_updated
            values.append(user_id)  # WHERE clause
            
            with db_manager.get_connection() as conn:
                conn.execute(f"""
                    UPDATE user_progress 
                    SET {', '.join(set_clauses)}, last_updated = ?
                    WHERE user_id = ?
                """, values)
                conn.commit()
            
            return True
        except Exception as e:
            logger.error(f"Update user progress error: {e}")
            return False
    
    # ============================================================================
    # SECURITY METHODS
    # ============================================================================
    
    def validate_password_server_side(self, password: str) -> Tuple[bool, str]:
        """Server-side password validation"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        return True, "Password valid"
    
    def sanitize_input(self, input_str: str) -> str:
        """Enhanced input sanitization"""
        if not input_str:
            return ""
        
        # HTML escape to prevent XSS
        sanitized = html.escape(input_str)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', 'script', 'javascript']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char.lower(), '')
        
        # Limit length
        return sanitized[:100] if len(sanitized) > 100 else sanitized
    
    def sanitize_error_message(self, error: Exception) -> str:
        """Enhanced error message sanitization"""
        error_type = type(error).__name__
        
        # Log full error for debugging
        logger.error(f"Error occurred: {str(error)}")
        
        # Return generic messages based on error type
        if "authentication" in error_type.lower() or "auth" in error_type.lower():
            return "Authentication failed"
        elif "database" in error_type.lower() or "sql" in error_type.lower():
            return "System error occurred"
        elif "validation" in error_type.lower():
            return "Validation error occurred"
        elif "connection" in error_type.lower() or "network" in error_type.lower():
            return "Connection error occurred"
        elif "permission" in error_type.lower() or "access" in error_type.lower():
            return "Access denied"
        else:
            return "An error occurred. Please try again."
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """Database-based rate limiting"""
        try:
            current_time = datetime.now()
            
            with db_manager.get_connection() as conn:
                # Clean old rate limit records (older than 15 minutes)
                conn.execute("""
                    DELETE FROM rate_limiting 
                    WHERE last_attempt < ?
                """, ((current_time - timedelta(minutes=15)).isoformat(),))
                
                # Check current rate limit
                cursor = conn.execute("""
                    SELECT attempts, last_attempt, locked_until 
                    FROM rate_limiting 
                    WHERE identifier = ?
                """, (identifier,))
                
                result = cursor.fetchone()
                
                if result:
                    attempts, last_attempt, locked_until = result
                    
                    # Check if still locked
                    if locked_until and datetime.fromisoformat(locked_until) > current_time:
                        remaining_time = int((datetime.fromisoformat(locked_until) - current_time).total_seconds())
                        return False, f"Too many attempts. Try again in {remaining_time} seconds"
                    
                    # Check if max attempts exceeded
                    if attempts >= 5:
                        # Lock for 15 minutes
                        lock_until = (current_time + timedelta(minutes=15)).isoformat()
                        conn.execute("""
                            UPDATE rate_limiting 
                            SET locked_until = ? 
                            WHERE identifier = ?
                        """, (lock_until, identifier))
                        conn.commit()
                        return False, "Too many attempts. Try again in 15 minutes"
                
                conn.commit()
                return True, "Rate limit check passed"
                
        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            return True, "Rate limit check passed"  # Fail open for now
    
    def record_attempt(self, identifier: str, success: bool):
        """Record login attempt in database"""
        try:
            current_time = datetime.now()
            
            with db_manager.get_connection() as conn:
                if success:
                    # Reset attempts on successful login
                    conn.execute("""
                        DELETE FROM rate_limiting WHERE identifier = ?
                    """, (identifier,))
                else:
                    # Check if record exists
                    cursor = conn.execute("""
                        SELECT attempts FROM rate_limiting WHERE identifier = ?
                    """, (identifier,))
                    
                    result = cursor.fetchone()
                    
                    if result:
                        attempts = result[0] + 1
                        conn.execute("""
                            UPDATE rate_limiting 
                            SET attempts = ?, last_attempt = ?
                            WHERE identifier = ?
                        """, (attempts, current_time.isoformat(), identifier))
                    else:
                        conn.execute("""
                            INSERT INTO rate_limiting (identifier, attempts, last_attempt)
                            VALUES (?, 1, ?)
                        """, (identifier, current_time.isoformat()))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Record attempt error: {e}")

# Global auth service instance
auth_service = AuthService()

# Streamlit session state integration
def init_auth_session():
    """Initialize authentication in Streamlit session state"""
    if 'auth_initialized' not in st.session_state:
        st.session_state.auth_initialized = True
        st.session_state.user = None
        st.session_state.authenticated = False

def login_user(username: str, password: str) -> Tuple[bool, str]:
    """Login user and store in session state"""
    init_auth_session()
    
    success, message, data = auth_service.authenticate_user(username, password)
    
    if success and data:
        st.session_state.user = data['user']
        st.session_state.authenticated = True
        st.session_state.session_token = data['session_token']
        return True, message
    else:
        return False, message

def logout_user():
    """Logout user and clear session state"""
    init_auth_session()
    
    if 'session_token' in st.session_state:
        auth_service.logout_user(st.session_state.session_token)
    
    st.session_state.user = None
    st.session_state.authenticated = False
    st.session_state.session_token = None

def get_current_user() -> Optional[Dict]:
    """Get current authenticated user"""
    init_auth_session()
    
    if not st.session_state.authenticated:
        return None
    
    # Verify session is still valid
    if 'session_token' in st.session_state:
        valid, user_data = auth_service.verify_session(st.session_state.session_token)
        if valid:
            st.session_state.user = user_data
            return user_data
        else:
            # Session expired, logout
            logout_user()
            return None
    
    return st.session_state.user

def require_auth():
    """Decorator to require authentication for pages"""
    user = get_current_user()
    if not user:
        st.error("Please log in to access this page")
        st.stop()
    return user
