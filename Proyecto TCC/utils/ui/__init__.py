"""
UI utilities package for TCC Data Analysis Platform
"""

from .ui_components import *
from .main_ui import *
from .error_handler import *

# Explicit imports from auth_ui to ensure they're available
from .auth_ui import (
    show_login_form,
    show_user_sidebar,
    get_current_user,
    init_sidebar,
    handle_authentication
)

__all__ = [
    'show_header',
    'show_quick_start_section',
    'should_show_main_content',
    'clear_selected_template',
    'show_login_form',
    'show_user_sidebar',
    'get_current_user',
    'init_sidebar',
    'handle_authentication',
    'create_sidebar_controls',
    'create_custom_calculations_ui',
    'display_metrics_dashboard',
    'display_custom_calculations_metrics',
    'display_export_section',
    'safe_execute',
    'display_error',
    'get_error_info',
    'clear_error_logs'
]
