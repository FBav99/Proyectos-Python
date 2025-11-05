"""
Admin utilities for TCC Data Analysis Platform
Provides admin access control and helper functions
"""

from typing import Tuple, Optional
from utils.ui import auth_ui

# Admin users list - only these users can access admin features
ADMIN_USERS = ['fbavera']

def is_admin_user(username: str) -> bool:
    """
    Check if a username is an admin user
    
    Args:
        username: Username to check
        
    Returns:
        True if user is admin, False otherwise
    """
    return username.lower() in [admin.lower() for admin in ADMIN_USERS]

def check_admin_access() -> Tuple[bool, Optional[str]]:
    """
    Check if current authenticated user has admin access
    
    Returns:
        Tuple of (has_access, error_message)
        - has_access: True if user is admin, False otherwise
        - error_message: None if access granted, error message if denied
    """
    current_user = auth_ui.get_current_user()
    
    if not current_user:
        return False, "Authentication required. Please log in first."
    
    username = current_user.get('username', '')
    if not username:
        return False, "Could not determine username"
    
    if not is_admin_user(username):
        return False, f"Access denied. Admin privileges required. Current user: {username}"
    
    return True, None

def require_admin():
    """
    Decorator/function to require admin access for a page or function
    
    Usage in Streamlit pages:
        if not require_admin():
            st.stop()
    """
    has_access, error_message = check_admin_access()
    
    if not has_access:
        return False
    
    return True

def get_current_admin_username() -> Optional[str]:
    """
    Get current user's username if they are admin, None otherwise
    
    Returns:
        Username if user is admin, None otherwise
    """
    has_access, _ = check_admin_access()
    if not has_access:
        return None
    
    current_user = auth_ui.get_current_user()
    return current_user.get('username') if current_user else None

