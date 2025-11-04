import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

def load_auth_config():
    """Load authentication configuration from YAML file"""
    config_path = 'config/config.yaml'
    
    # Default config structure as per official GitHub documentation
    default_config = {
        'credentials': {
            'usernames': {
                'demo_user': {
                    'email': 'demo@example.com',
                    'failed_login_attempts': 0,
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'logged_in': False,
                    'password': 'demo123'  # Plain text password - will be hashed
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'some_signature_key',
            'name': 'some_cookie_name'
        },
        'pre-authorized': {
            'emails': []
        }
    }
    
    # Try to load existing config file
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
                if config:
                    return config
        except Exception as e:
            # If reading fails, use default config
            st.warning(f"⚠️ No se pudo leer el archivo de configuración: {str(e)}. Usando configuración por defecto.")
            return default_config
    
    # If file doesn't exist, try to create it (will fail on Streamlit Cloud, but that's OK)
    try:
        # Try to create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file, default_flow_style=False)
    except (OSError, PermissionError, IOError):
        # On Streamlit Cloud, we can't write to the file system
        # This is expected behavior - we'll use the default config in memory
        pass
    
    return default_config

def init_authentication():
    """Initialize authentication system"""
    config = load_auth_config()
    
    # Hash passwords using the correct API
    hashed_credentials = stauth.Hasher.hash_passwords(config['credentials'])
    
    # Initialize the Authenticate class with the correct parameters
    authenticator = stauth.Authenticate(
        credentials=hashed_credentials,
        cookie_name=config['cookie']['name'],
        cookie_key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days'],
        auto_hash=False  # Disable automatic hashing since passwords are pre-hashed
    )
    
    return authenticator

def get_user_progress(username):
    """Get user's learning progress"""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {}
    
    if username not in st.session_state.user_progress:
        st.session_state.user_progress[username] = {
            'nivel1_completed': False,
            'nivel2_completed': False,
            'nivel3_completed': False,
            'nivel4_completed': False,
            'achievements': [],
            'quiz_scores': {},
            'total_time_spent': 0,
            'data_analyses_created': 0
        }
    
    return st.session_state.user_progress[username]

def update_user_progress(username, **updates):
    """Update user's learning progress"""
    progress = get_user_progress(username)
    progress.update(updates)
    st.session_state.user_progress[username] = progress

def check_achievement(username, achievement_type):
    """Check and award achievements"""
    progress = get_user_progress(username)
    achievements = progress.get('achievements', [])
    
    new_achievements = []
    
    # Level completion achievements
    if achievement_type == 'level_completion':
        completed_levels = sum([
            progress.get('nivel1_completed', False),
            progress.get('nivel2_completed', False),
            progress.get('nivel3_completed', False),
            progress.get('nivel4_completed', False)
        ])
        
        if completed_levels == 1 and 'first_level' not in achievements:
            new_achievements.append('first_level')
        elif completed_levels == 4 and 'all_levels' not in achievements:
            new_achievements.append('all_levels')
    
    # Quiz achievements
    elif achievement_type == 'quiz_perfect':
        if 'quiz_master' not in achievements:
            new_achievements.append('quiz_master')
    
    # Data analysis achievements
    elif achievement_type == 'analysis_created':
        analyses_count = progress.get('data_analyses_created', 0)
        if analyses_count >= 5 and 'data_analyst' not in achievements:
            new_achievements.append('data_analyst')
    
    # Update achievements
    if new_achievements:
        progress['achievements'].extend(new_achievements)
        update_user_progress(username, achievements=progress['achievements'])
        return new_achievements
    
    return []
