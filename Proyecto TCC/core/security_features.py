"""
Security features service for TCC Data Analysis Platform
Handles rate limiting, input sanitization, and security validations
"""

import streamlit as st
import logging
import re
import html
from datetime import datetime, timedelta
from typing import Tuple
from core.database import db_manager, ensure_database_initialized

logger = logging.getLogger(__name__)

# Ensure database is initialized when this module is imported
try:
    ensure_database_initialized()
except Exception as e:
    logger.warning(f"Could not ensure database initialization in security_features: {e}")

class SecurityFeatures:
    """Handles security features like rate limiting and input sanitization"""
    
    def __init__(self):
        self.max_attempts = 5
        self.lockout_duration = 15  # minutes
        self.rate_limit_window = 15  # minutes
    
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """Database-based rate limiting"""
        try:
            current_time = datetime.now()
            
            with db_manager.get_connection() as conn:
                # Clean old rate limit records
                conn.execute("""
                    DELETE FROM rate_limiting 
                    WHERE last_attempt < ?
                """, ((current_time - timedelta(minutes=self.rate_limit_window)).isoformat(),))
                
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
                    if attempts >= self.max_attempts:
                        # Lock for specified duration
                        lock_until = (current_time + timedelta(minutes=self.lockout_duration)).isoformat()
                        conn.execute("""
                            UPDATE rate_limiting 
                            SET locked_until = ? 
                            WHERE identifier = ?
                        """, (lock_until, identifier))
                        conn.commit()
                        return False, f"Too many attempts. Try again in {self.lockout_duration} minutes"
                
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
    
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        try:
            if not input_string:
                return ""
            
            # Convert to string if needed
            sanitized = str(input_string).strip()
            
            # HTML encode special characters
            sanitized = html.escape(sanitized)
            
            # Remove potentially dangerous characters
            dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', 'script', 'javascript']
            for char in dangerous_chars:
                sanitized = sanitized.replace(char.lower(), '')
            
            # Limit length
            return sanitized[:100] if len(sanitized) > 100 else sanitized
            
        except Exception as e:
            logger.error(f"Input sanitization error: {e}")
            return ""
    
    def sanitize_input_for_db(self, input_string: str) -> str:
        """Sanitize user input for database storage (no HTML encoding)"""
        try:
            if not input_string:
                return ""
            
            # Convert to string if needed
            sanitized = str(input_string).strip()
            
            # Remove only truly dangerous characters that could cause issues
            # Note: SQL injection is prevented by parameterized queries, not string sanitization
            # We only remove characters that could break the data format
            dangerous_chars = ['\x00', '\n', '\r', '\x1a']  # Control characters that could break SQL
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            
            # Limit length (longer for database storage)
            return sanitized[:255] if len(sanitized) > 255 else sanitized
            
        except Exception as e:
            logger.error(f"Database input sanitization error: {e}")
            return ""
    
    def sanitize_error_message(self, error: Exception) -> str:
        """Enhanced error message sanitization"""
        try:
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
                
        except Exception as e:
            logger.error(f"Error message sanitization error: {e}")
            return "An error occurred. Please try again."
    
    def validate_password_server_side(self, password: str) -> Tuple[bool, str]:
        """Server-side password validation"""
        try:
            if not password:
                return False, "Password is required"
            
            if len(password) < 8:
                return False, "Password must be at least 8 characters long"
            
            if len(password) > 128:
                return False, "Password is too long (maximum 128 characters)"
            
            # Check for common weak patterns
            weak_patterns = [
                r'^123456$',
                r'^password$',
                r'^qwerty$',
                r'^admin$',
                r'^user$',
                r'^123456789$',
                r'^12345678$',
                r'^1234567$',
                r'^1234567890$'
            ]
            
            for pattern in weak_patterns:
                if re.match(pattern, password.lower()):
                    return False, "Password is too common, please choose a stronger password"
            
            # Check for basic complexity
            has_letter = re.search(r'[a-zA-Z]', password)
            has_digit = re.search(r'\d', password)
            
            if not has_letter or not has_digit:
                return False, "Password must contain both letters and numbers"
            
            return True, "Password is valid"
            
        except Exception as e:
            logger.error(f"Password validation error: {e}")
            return False, "Password validation failed"
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        """Validate username format and security"""
        try:
            if not username:
                return False, "Username is required"
            
            if len(username) < 3:
                return False, "Username must be at least 3 characters long"
            
            if len(username) > 30:
                return False, "Username is too long (maximum 30 characters)"
            
            # Check for valid characters (alphanumeric, underscore, hyphen)
            if not re.match(r'^[a-zA-Z0-9_-]+$', username):
                return False, "Username can only contain letters, numbers, underscores, and hyphens"
            
            # Check for reserved usernames
            reserved_names = ['admin', 'root', 'system', 'guest', 'test', 'user', 'anonymous']
            if username.lower() in reserved_names:
                return False, "Username is reserved and cannot be used"
            
            return True, "Username is valid"
            
        except Exception as e:
            logger.error(f"Username validation error: {e}")
            return False, "Username validation failed"
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email format and security"""
        try:
            if not email:
                return False, "Email is required"
            
            if len(email) > 254:
                return False, "Email is too long"
            
            # Basic email format validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return False, "Invalid email format"
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'\.\.',  # Double dots
                r'@.*@',  # Multiple @ symbols
                r'\.@',   # Dot before @
                r'@\.',   # @ before dot
                r'^\.',   # Starts with dot
                r'\.$'    # Ends with dot
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, email):
                    return False, "Invalid email format"
            
            return True, "Email is valid"
            
        except Exception as e:
            logger.error(f"Email validation error: {e}")
            return False, "Email validation failed"
    
    def create_rate_limit_table(self):
        """Create rate limiting table if it doesn't exist"""
        try:
            with db_manager.get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS rate_limiting (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        identifier TEXT NOT NULL,
                        attempts INTEGER DEFAULT 1,
                        last_attempt TEXT NOT NULL,
                        locked_until TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                
                # Create index for better performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_rate_limiting_identifier 
                    ON rate_limiting(identifier)
                """)
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error creating rate limiting table: {e}")

# Global security features instance
security_features = SecurityFeatures()
