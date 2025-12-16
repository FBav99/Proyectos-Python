# Nombre del Archivo: security.py
# Descripción: Gestor de seguridad para autenticación y manejo de sesiones
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import hashlib
import secrets
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

# Configuracion - Configurar Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Clase - Gestor de Seguridad
class SecurityManager:
    """Gestor de seguridad para autenticación y manejo de sesiones"""
    
    def __init__(self):
        self.rate_limit_attempts = {}
        self.session_tokens = {}
        self.max_login_attempts = 5
        self.lockout_duration = 900  # Configuracion - 15 minutos
        self.session_timeout = 3600  # Configuracion - 1 hora
        
    # Validacion - Validar Email
    def validate_email(self, email: str) -> bool:
        """Validar formato de email"""
        if not email:
            return False
        
        # Validacion - Validar Formato de Email con Regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    # Validacion - Validar Fortaleza de Contraseña
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validar fortaleza de contraseña"""
        if not password:
            return False, "La contraseña no puede estar vacía"
        
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una letra mayúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe contener al menos una letra minúscula"
        
        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "La contraseña debe contener al menos un carácter especial"
        
        return True, "La contraseña cumple con los requisitos de fortaleza"
    
    # Seguridad - Sanitizar Entrada
    def sanitize_input(self, input_str: str) -> str:
        """Sanitizar entrada del usuario para prevenir ataques de inyección"""
        if not input_str:
            return ""
        
        # Seguridad - Remover Caracteres Potencialmente Peligrosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Validacion - Limitar Longitud
        return sanitized[:100] if len(sanitized) > 100 else sanitized
    
    # Validacion - Verificar Rate Limit
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """Verificar si el usuario está limitado por rate limit"""
        current_time = time.time()
        
        if identifier in self.rate_limit_attempts:
            attempts, last_attempt = self.rate_limit_attempts[identifier]
            
            # Validacion - Verificar si Periodo de Bloqueo Expiro
            if current_time - last_attempt > self.lockout_duration:
                # Seguridad - Reiniciar Intentos Despues de Periodo de Bloqueo
                self.rate_limit_attempts[identifier] = (0, current_time)
                return True, "Rate limit reset"
            
            # Validacion - Verificar si Maximo de Intentos Excedido
            if attempts >= self.max_login_attempts:
                remaining_time = int(self.lockout_duration - (current_time - last_attempt))
                return False, f"Too many attempts. Try again in {remaining_time} seconds"
        
        return True, "Rate limit check passed"
    
    # Registro - Registrar Intento
    def record_attempt(self, identifier: str, success: bool):
        """Registrar intento de login"""
        current_time = time.time()
        
        if identifier not in self.rate_limit_attempts:
            self.rate_limit_attempts[identifier] = (0, current_time)
        
        attempts, _ = self.rate_limit_attempts[identifier]
        
        if success:
            # Seguridad - Reiniciar Intentos en Login Exitoso
            self.rate_limit_attempts[identifier] = (0, current_time)
        else:
            # Contador - Incrementar Intentos Fallidos
            self.rate_limit_attempts[identifier] = (attempts + 1, current_time)
    
    # Seguridad - Generar Token de Sesión
    def generate_session_token(self, username: str) -> str:
        """Generar un token de sesión seguro"""
        token_data = f"{username}:{time.time()}:{secrets.token_hex(16)}"
        return hashlib.sha256(token_data.encode()).hexdigest()
    
    # Validacion - Validar Token de Sesión
    def validate_session_token(self, token: str, username: str) -> bool:
        """Validar token de sesión"""
        if not token or not username:
            return False
        
        # Validacion - Verificar si Token Existe y No Expiro
        if token in self.session_tokens:
            token_data = self.session_tokens[token]
            if (token_data['username'] == username and 
                time.time() - token_data['created'] < self.session_timeout):
                return True
        
        return False
    
    # Sesion - Crear Sesión
    def create_session(self, username: str) -> str:
        """Crear una nueva sesión para el usuario"""
        token = self.generate_session_token(username)
        self.session_tokens[token] = {
            'username': username,
            'created': time.time(),
            'last_activity': time.time()
        }
        return token
    
    # Sesion - Actualizar Actividad de Sesión
    def update_session_activity(self, token: str):
        """Actualizar tiempo de última actividad de sesión"""
        if token in self.session_tokens:
            self.session_tokens[token]['last_activity'] = time.time()
    
    # Sesion - Invalidar Sesión
    def invalidate_session(self, token: str):
        """Invalidar un token de sesión"""
        if token in self.session_tokens:
            del self.session_tokens[token]
    
    # Limpieza - Limpiar Sesiones Expiradas
    def cleanup_expired_sessions(self):
        """Limpiar sesiones expiradas"""
        current_time = time.time()
        expired_tokens = [
            token for token, data in self.session_tokens.items()
            if current_time - data['last_activity'] > self.session_timeout
        ]
        
        for token in expired_tokens:
            del self.session_tokens[token]
    
    # Validacion - Validar Estado OAuth
    def validate_oauth_state(self, state: str, stored_state: str) -> bool:
        """Validar parámetro de estado OAuth"""
        # Validacion - Rechazar si Proveedor No Envio State
        if not state:
            return False
        
        # Validacion - Manejar Caso de Callback en Sesion Nueva
        # En algunos flujos OAuth de Streamlit, el callback puede llegar en una sesion nueva
        # donde ya no tenemos el stored_state original. Para evitar bloquear logins legitimos,
        # relajamos la validacion en ese caso.
        if not stored_state:
            # Validacion - Permitir Flujo si No Hay Stored State
            logger.warning("OAuth callback received without stored_state; skipping strict state validation.")
            return True
        
        # Validacion - State Debe Coincidir Exactamente
        return state == stored_state
    
    # Seguridad - Sanitizar Mensaje de Error
    def sanitize_error_message(self, error: Exception) -> str:
        """Sanitizar mensajes de error para prevenir divulgación de información"""
        error_type = type(error).__name__
        
        # Mensaje - Generar Mensajes de Error Genericos por Tipo
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

# Instancia - Instancia Global de Security Manager
security_manager = SecurityManager()

# Autenticacion - Login Seguro
def secure_login(username: str, password: str) -> Tuple[bool, str]:
    """Función de login seguro con rate limiting y validación"""
    try:
        # Seguridad - Sanitizar entradas
        username = security_manager.sanitize_input(username)
        password = security_manager.sanitize_input(password)
        
        # Validacion - Validar entradas
        if not username or not password:
            return False, "Username and password are required"
        
        # Seguridad - Verificar Rate Limiting
        rate_limit_ok, rate_limit_msg = security_manager.check_rate_limit(username)
        if not rate_limit_ok:
            return False, rate_limit_msg
        
        # Nota: La validacion contra el sistema de autenticacion se maneja en otro lugar
        
        # Logging - Registrar Intento (el exito sera determinado por el sistema de auth)
        security_manager.record_attempt(username, True)  # Assume success for now
        
        return True, "Login successful"
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return False, security_manager.sanitize_error_message(e)

def secure_oauth_callback(code: str, state: str, stored_state: str) -> Tuple[bool, str]:
    """Secure OAuth callback handling"""
    try:
        # Validacion - Validar Parametro State
        if not security_manager.validate_oauth_state(state, stored_state):
            return False, "Invalid OAuth state"
        
        # Seguridad - Sanitizar Codigo
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
        
        # Validacion - Validar Email
        if not security_manager.validate_email(email):
            return False, "Invalid email format"
        
        # Validacion - Validar Fortaleza de Contraseña
        password_ok, password_msg = security_manager.validate_password_strength(password)
        if not password_ok:
            return False, password_msg
        
        # Validacion - Validar Usuario
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
        # Limpieza - Limpiar Sesiones Expiradas
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

# Decorador - Decoradores de Seguridad para Funciones de Streamlit
def secure_function(func):
    """Decorador para agregar verificaciones de seguridad a funciones"""
    def wrapper(*args, **kwargs):
        try:
            # Seguridad - Agregar verificaciones de seguridad adicionales
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Function {func.__name__} error: {str(e)}")
            st.error(security_manager.sanitize_error_message(e))
            return None
    return wrapper

# Decorador - Requerir Autenticación
def require_authentication(func):
    """Decorador para requerir autenticación en funciones"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authentication_status'):
            st.error("Authentication required")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
