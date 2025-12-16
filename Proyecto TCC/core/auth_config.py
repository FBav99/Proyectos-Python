# Nombre del Archivo: auth_config.py
# Descripción: Configuración y gestión de autenticación de usuarios
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# Configuracion - Cargar Configuración de Autenticación
@st.cache_data(show_spinner=False, ttl=300)
def load_auth_config():
    """Cargar configuración de autenticación desde archivo YAML con caché de corta duración"""
    config_path = 'config/config.yaml'
    
    # Configuracion - Estructura de Configuracion por Defecto
    default_config = {
        'credentials': {
            'usernames': {
                'demo_user': {
                    'email': 'demo@example.com',
                    'failed_login_attempts': 0,
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'logged_in': False,
                    'password': 'demo123'  # Seguridad - Contraseña en texto plano - será hasheada
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
    
    # Archivo - Intentar Cargar Archivo de Configuracion Existente
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
                if config:
                    return config
        except Exception:
            # Manejo de Errores - Si falla la lectura, usar configuración por defecto
            # Manejo de Errores - No exponer detalles del error al usuario
            return default_config
    
    # Archivo - Intentar Crear Archivo si No Existe
    try:
        # Archivo - Intentar crear directorio si no existe
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file, default_flow_style=False)
    except (OSError, PermissionError, IOError):
        # Manejo de Errores - En Streamlit Cloud, no podemos escribir al sistema de archivos
        # Manejo de Errores - Este es comportamiento esperado - usaremos la configuración por defecto en memoria
        pass
    
    return default_config

# Autenticacion - Inicializar Sistema de Autenticación
def init_authentication():
    """Inicializar sistema de autenticación"""
    config = load_auth_config()
    
    # Seguridad - Hashear contraseñas usando API correcta
    hashed_credentials = stauth.Hasher.hash_passwords(config['credentials'])
    
    # Inicializacion - Inicializar clase Authenticate con parámetros correctos
    authenticator = stauth.Authenticate(
        credentials=hashed_credentials,
        cookie_name=config['cookie']['name'],
        cookie_key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days'],
        auto_hash=False  # Seguridad - Deshabilitar hashing automático ya que las contraseñas están pre-hasheadas
    )
    
    return authenticator

# Progreso - Obtener Progreso del Usuario
def get_user_progress(username):
    """Obtener progreso de aprendizaje del usuario"""
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

# Progreso - Actualizar Progreso del Usuario
def update_user_progress(username, **updates):
    """Actualizar progreso de aprendizaje del usuario"""
    progress = get_user_progress(username)
    progress.update(updates)
    st.session_state.user_progress[username] = progress

# Logros - Verificar y Otorgar Logros
def check_achievement(username, achievement_type):
    """Verificar y otorgar logros"""
    progress = get_user_progress(username)
    achievements = progress.get('achievements', [])
    
    new_achievements = []
    
    # Logros - Logros de completación de niveles
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
    
    # Logros - Logros de quiz
    elif achievement_type == 'quiz_perfect':
        if 'quiz_master' not in achievements:
            new_achievements.append('quiz_master')
    
    # Logros - Logros de análisis de datos
    elif achievement_type == 'analysis_created':
        analyses_count = progress.get('data_analyses_created', 0)
        if analyses_count >= 5 and 'data_analyst' not in achievements:
            new_achievements.append('data_analyst')
    
    # Actualizacion - Actualizar logros
    if new_achievements:
        progress['achievements'].extend(new_achievements)
        update_user_progress(username, achievements=progress['achievements'])
        return new_achievements
    
    return []
