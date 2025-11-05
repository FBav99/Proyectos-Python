"""
Nombre del Archivo: auth_service.py
Descripción: Servicio de autenticación - Registro, login, gestión de sesiones y contraseñas
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

# Imports estándar
import logging
import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import bcrypt
import streamlit as st

# Imports locales
from core.database import db_manager, ensure_database_initialized
from core.progress_tracker import progress_tracker
from core.security import security_manager
from core.security_features import security_features

logger = logging.getLogger(__name__)

# Ensure database is initialized when this module is imported
try:
    ensure_database_initialized()
except Exception as e:
    logger.warning(f"Could not ensure database initialization in auth_service: {e}")

# ============================================================================
# AUTH SERVICE CLASS
# ============================================================================

class AuthService:
    """
    Maneja la autenticación de usuarios y gestión de sesiones.
    
    Esta clase proporciona funcionalidad completa para registro de usuarios,
    autenticación, gestión de sesiones y operaciones relacionadas con contraseñas.
    """
    
    def __init__(self):
        """Inicializa el servicio de autenticación con configuración por defecto"""
        self.session_timeout = 3600  # 1 hora en segundos
    
    # ============================================================================
    # USER REGISTRATION AND AUTHENTICATION
    # ============================================================================
    
    def register_user(self, username: str, email: str, password: str, 
                     first_name: str, last_name: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario único
            email: Email del usuario
            password: Contraseña del usuario
            first_name: Nombre del usuario
            last_name: Apellido del usuario
        
        Returns:
            Tupla con (éxito, mensaje)
        """
        try:
            # Validar entradas
            if not username or not email or not password:
                return False, "All fields are required"
            
            # Server-side validation using security features
            username_valid, username_msg = security_features.validate_username(username)
            if not username_valid:
                return False, username_msg
            
            email_valid, email_msg = security_features.validate_email(email)
            if not email_valid:
                return False, email_msg
            
            password_valid, password_msg = security_features.validate_password_server_side(password)
            if not password_valid:
                return False, password_msg
            
            # Server-side input sanitization for database storage (no HTML encoding)
            # HTML encoding is for display, not database storage
            username = security_features.sanitize_input_for_db(username)
            email = security_features.sanitize_input_for_db(email)
            first_name = security_features.sanitize_input_for_db(first_name)
            last_name = security_features.sanitize_input_for_db(last_name)
            
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
                
                # Create user progress record in the same transaction to avoid nested connections
                try:
                    conn.execute("""
                        INSERT INTO user_progress (user_id, last_updated)
                        VALUES (?, ?)
                    """, (user_id, datetime.now().isoformat()))
                except Exception as e:
                    logger.error(f"Error creating user progress: {e}")
                    # Don't fail registration if progress creation fails
                
                conn.commit()
            
            # Log activity
            self.log_activity(user_id, 'registration', {
                'username': username,
                'email': email
            })
            
            return True, "User registered successfully"
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, security_features.sanitize_error_message(e)
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate user login"""
        try:
            # Check rate limiting first
            rate_limit_ok, rate_limit_msg = security_features.check_rate_limit(username)
            if not rate_limit_ok:
                return False, rate_limit_msg, None
            
            # Sanitize inputs for database (no HTML encoding)
            username = security_features.sanitize_input_for_db(username)
            
            # Get user from database
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM users 
                    WHERE username = ? AND is_active = 1
                """, (username,))
                user = cursor.fetchone()
            
            if not user:
                # Record failed attempt
                security_features.record_attempt(username, False)
                return False, "Invalid username or password", None
            
            # Check if account is locked
            if user['locked_until']:
                locked_until = datetime.fromisoformat(user['locked_until'])
                if locked_until > datetime.now():
                    remaining_time = int((locked_until - datetime.now()).total_seconds())
                    return False, f"Account is locked. Try again in {remaining_time} seconds", None
                else:
                    # Unlock account
                    self.unlock_account(user['id'])
            
            # Verify password
            if not self.verify_password(password, user['password_hash']):
                # Increment failed attempts
                self.increment_failed_attempts(user['id'])
                # Record failed attempt
                security_features.record_attempt(username, False)
                return False, "Invalid username or password", None
            
            # Reset failed attempts on successful login
            self.reset_failed_attempts(user['id'])
            # Record successful attempt
            security_features.record_attempt(username, True)
            
            # Update last login
            self.update_last_login(user['id'])
            
            # Create session
            session_token = self.create_session(user['id'])
            
            # Prepare user data
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_active': user['is_active']
            }
            
            return True, "Login successful", {
                'user': user_data,
                'session_token': session_token
            }
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False, security_features.sanitize_error_message(e), None
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        try:
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
    
    def unlock_account(self, user_id: int):
        """Unlock a locked account"""
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
            # This could be extended to log to a separate user_activity table
            logger.info(f"User activity - User {user_id}: {activity_type} - {details}")
        except Exception as e:
            logger.error(f"Error logging user activity: {e}")

    def forgot_password(self, username: str) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
        """
        Generate a new random password for a user (password recovery).
        
        Args:
            username: Username of the account to recover
            
        Returns:
            Tuple of (success, username, email, new_password)
            Returns (False, None, None, None) if user not found
        """
        try:
            # Sanitize input for database (no HTML encoding)
            username = security_features.sanitize_input_for_db(username)
            
            # Find user by username
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, username, email, first_name, last_name, is_active
                    FROM users 
                    WHERE username = ? AND is_active = 1
                """, (username,))
                user = cursor.fetchone()
            
            if not user:
                return False, None, None, None
            
            # Generate a secure random password
            # Using a mix of letters, numbers, and special characters
            alphabet = string.ascii_letters + string.digits + "!@#$%"
            new_password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            # Hash the new password
            password_hash = self.hash_password(new_password)
            
            # Update password in database and reset failed attempts
            with db_manager.get_connection() as conn:
                conn.execute("""
                    UPDATE users 
                    SET password_hash = ?, 
                        failed_login_attempts = 0,
                        locked_until = NULL
                    WHERE id = ?
                """, (password_hash, user['id']))
                conn.commit()
            
            # Log activity
            self.log_activity(user['id'], 'password_reset', {
                'username': username,
                'reset_type': 'forgot_password'
            })
            
            return True, user['username'], user['email'], new_password
            
        except Exception as e:
            logger.error(f"Password recovery error: {e}")
            return False, None, None, None

    def update_email(self, user_id: int, new_email: str) -> Tuple[bool, str]:
        """
        Update user email address
        
        Args:
            user_id: ID of the user
            new_email: New email address
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate email format
            email_valid, email_msg = security_features.validate_email(new_email)
            if not email_valid:
                return False, email_msg
            
            # Sanitize email
            new_email = security_features.sanitize_input_for_db(new_email)
            
            # Check if email is already taken by another user
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id FROM users WHERE email = ? AND id != ?
                """, (new_email, user_id))
                if cursor.fetchone():
                    return False, "Este email ya está en uso por otra cuenta"
                
                # Update email
                conn.execute("""
                    UPDATE users SET email = ? WHERE id = ?
                """, (new_email, user_id))
                conn.commit()
            
            # Log activity
            self.log_activity(user_id, 'email_update', {
                'new_email': new_email
            })
            
            return True, "Email actualizado exitosamente"
            
        except Exception as e:
            logger.error(f"Email update error: {e}")
            return False, security_features.sanitize_error_message(e)
    
    def verify_session(self, session_token: str) -> Tuple[bool, Optional[Dict]]:
        """Verify if a session is valid and return user data"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT us.*, u.username, u.email, u.first_name, u.last_name, u.is_active
                    FROM user_sessions us
                    JOIN users u ON us.user_id = u.id
                    WHERE us.session_token = ? AND us.expires_at > ? AND u.is_active = 1
                """, (session_token, datetime.now().isoformat()))
                
                session_data = cursor.fetchone()
                
                if not session_data:
                    return False, None
                
                # Update session activity
                self.update_session_activity(session_token)
                
                # Prepare user data
                user_data = {
                    'id': session_data['user_id'],
                    'username': session_data['username'],
                    'email': session_data['email'],
                    'first_name': session_data['first_name'],
                    'last_name': session_data['last_name'],
                    'is_active': session_data['is_active']
                }
                
                return True, user_data
                
        except Exception as e:
            logger.error(f"Session verification error: {e}")
            return False, None

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
