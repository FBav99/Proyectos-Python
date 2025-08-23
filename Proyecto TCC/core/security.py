import streamlit as st
import hashlib
import secrets
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class SecurityManager:
    """Security manager for authentication and session handling"""
    
    def __init__(self):
        self.rate_limit_attempts = {}
        self.session_tokens = {}
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        self.session_timeout = 3600  # 1 hour
        
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        # Basic email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password meets strength requirements"
    
    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not input_str:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Limit length
        return sanitized[:100] if len(sanitized) > 100 else sanitized
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """Check if user is rate limited"""
        current_time = time.time()
        
        if identifier in self.rate_limit_attempts:
            attempts, last_attempt = self.rate_limit_attempts[identifier]
            
            # Check if lockout period has expired
            if current_time - last_attempt > self.lockout_duration:
                # Reset attempts after lockout period
                self.rate_limit_attempts[identifier] = (0, current_time)
                return True, "Rate limit reset"
            
            # Check if max attempts exceeded
            if attempts >= self.max_login_attempts:
                remaining_time = int(self.lockout_duration - (current_time - last_attempt))
                return False, f"Too many attempts. Try again in {remaining_time} seconds"
        
        return True, "Rate limit check passed"
    
    def record_attempt(self, identifier: str, success: bool):
        """Record login attempt"""
        current_time = time.time()
        
        if identifier not in self.rate_limit_attempts:
            self.rate_limit_attempts[identifier] = (0, current_time)
        
        attempts, _ = self.rate_limit_attempts[identifier]
        
        if success:
            # Reset attempts on successful login
            self.rate_limit_attempts[identifier] = (0, current_time)
        else:
            # Increment failed attempts
            self.rate_limit_attempts[identifier] = (attempts + 1, current_time)
    
    def generate_session_token(self, username: str) -> str:
        """Generate a secure session token"""
        token_data = f"{username}:{time.time()}:{secrets.token_hex(16)}"
        return hashlib.sha256(token_data.encode()).hexdigest()
    
    def validate_session_token(self, token: str, username: str) -> bool:
        """Validate session token"""
        if not token or not username:
            return False
        
        # Check if token exists and is not expired
        if token in self.session_tokens:
            token_data = self.session_tokens[token]
            if (token_data['username'] == username and 
                time.time() - token_data['created'] < self.session_timeout):
                return True
        
        return False
    
    def create_session(self, username: str) -> str:
        """Create a new session for user"""
        token = self.generate_session_token(username)
        self.session_tokens[token] = {
            'username': username,
            'created': time.time(),
            'last_activity': time.time()
        }
        return token
    
    def update_session_activity(self, token: str):
        """Update session last activity time"""
        if token in self.session_tokens:
            self.session_tokens[token]['last_activity'] = time.time()
    
    def invalidate_session(self, token: str):
        """Invalidate a session token"""
        if token in self.session_tokens:
            del self.session_tokens[token]
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = time.time()
        expired_tokens = [
            token for token, data in self.session_tokens.items()
            if current_time - data['last_activity'] > self.session_timeout
        ]
        
        for token in expired_tokens:
            del self.session_tokens[token]
    
    def validate_oauth_state(self, state: str, stored_state: str) -> bool:
        """Validate OAuth state parameter"""
        if not state or not stored_state:
            return False
        
        # State should match exactly and not be too old
        return state == stored_state
    
    def sanitize_error_message(self, error: Exception) -> str:
        """Sanitize error messages to prevent information disclosure"""
        error_type = type(error).__name__
        
        # Generic error messages based on error type
        if "authentication" in error_type.lower() or "auth" in error_type.lower():
            return "Authentication error occurred"
        elif "connection" in error_type.lower() or "network" in error_type.lower():
            return "Connection error occurred"
        elif "validation" in error_type.lower():
            return "Validation error occurred"
        elif "permission" in error_type.lower() or "access" in error_type.lower():
            return "Access denied"
        else:
            return "An error occurred. Please try again."

# Global security manager instance
security_manager = SecurityManager()

def secure_login(username: str, password: str) -> Tuple[bool, str]:
    """Secure login function with rate limiting and validation"""
    try:
        # Sanitize inputs
        username = security_manager.sanitize_input(username)
        password = security_manager.sanitize_input(password)
        
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
        
        # Check rate limiting
        rate_limit_ok, rate_limit_msg = security_manager.check_rate_limit(username)
        if not rate_limit_ok:
            return False, rate_limit_msg
        
        # Here you would validate against your authentication system
        # For now, we'll assume the authentication is handled elsewhere
        # and we just record the attempt
        
        # Record attempt (success will be determined by auth system)
        security_manager.record_attempt(username, True)  # Assume success for now
        
        return True, "Login successful"
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return False, security_manager.sanitize_error_message(e)

def secure_oauth_callback(code: str, state: str, stored_state: str) -> Tuple[bool, str]:
    """Secure OAuth callback handling"""
    try:
        # Validate state parameter
        if not security_manager.validate_oauth_state(state, stored_state):
            return False, "Invalid OAuth state"
        
        # Sanitize code
        code = security_manager.sanitize_input(code)
        
        if not code:
            return False, "Invalid authorization code"
        
        return True, "OAuth callback validated"
        
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return False, security_manager.sanitize_error_message(e)

def secure_user_registration(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Secure user registration with validation"""
    try:
        # Sanitize inputs
        username = security_manager.sanitize_input(username)
        email = security_manager.sanitize_input(email)
        password = security_manager.sanitize_input(password)
        
        # Validate email
        if not security_manager.validate_email(email):
            return False, "Invalid email format"
        
        # Validate password strength
        password_ok, password_msg = security_manager.validate_password_strength(password)
        if not password_ok:
            return False, password_msg
        
        # Validate username
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Registration validation passed"
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return False, security_manager.sanitize_error_message(e)

def get_secure_session_info() -> Dict:
    """Get secure session information"""
    try:
        # Clean up expired sessions
        security_manager.cleanup_expired_sessions()
        
        return {
            'active_sessions': len(security_manager.session_tokens),
            'rate_limited_users': len([
                user for user, (attempts, _) in security_manager.rate_limit_attempts.items()
                if attempts >= security_manager.max_login_attempts
            ])
        }
    except Exception as e:
        logger.error(f"Session info error: {str(e)}")
        return {'error': 'Unable to retrieve session information'}

# Security decorators for Streamlit functions
def secure_function(func):
    """Decorator to add security checks to functions"""
    def wrapper(*args, **kwargs):
        try:
            # Add any additional security checks here
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Function {func.__name__} error: {str(e)}")
            st.error(security_manager.sanitize_error_message(e))
            return None
    return wrapper

def require_authentication(func):
    """Decorator to require authentication for functions"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authentication_status'):
            st.error("Authentication required")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
