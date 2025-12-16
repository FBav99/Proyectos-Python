# Nombre del Archivo: security_features.py
# Descripción: Servicio de características de seguridad para la plataforma de análisis de datos TCC - Maneja rate limiting, sanitización de entrada y validaciones de seguridad
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import logging
import re
import html
from datetime import datetime, timedelta
from typing import Tuple
from core.database import db_manager, ensure_database_initialized

logger = logging.getLogger(__name__)

# Inicializacion - Asegurar Inicializacion de Base de Datos al Importar Modulo
try:
    ensure_database_initialized()
except Exception as e:
    logger.warning(f"Could not ensure database initialization in security_features: {e}")

# Clase - Características de Seguridad
class SecurityFeatures:
    """Maneja características de seguridad como rate limiting y sanitización de entrada"""
    
    def __init__(self):
        self.max_attempts = 5
        self.lockout_duration = 15  # Configuracion - minutos
        self.rate_limit_window = 15  # Configuracion - minutos
    
    # Validacion - Verificar Rate Limit
    def check_rate_limit(self, identifier: str) -> Tuple[bool, str]:
        """Rate limiting basado en base de datos"""
        try:
            current_time = datetime.now()
            
            with db_manager.get_connection() as conn:
                # Limpieza - Limpiar Registros Antiguos de Rate Limiting
                conn.execute("""
                    DELETE FROM rate_limiting 
                    WHERE last_attempt < ?
                """, ((current_time - timedelta(minutes=self.rate_limit_window)).isoformat(),))
                
                # Validacion - Verificar Rate Limit Actual
                cursor = conn.execute("""
                    SELECT attempts, last_attempt, locked_until 
                    FROM rate_limiting 
                    WHERE identifier = ?
                """, (identifier,))
                
                result = cursor.fetchone()
                
                if result:
                    attempts, last_attempt, locked_until = result
                    
                    # Validacion - Verificar si Aun Esta Bloqueado
                    if locked_until and datetime.fromisoformat(locked_until) > current_time:
                        remaining_time = int((datetime.fromisoformat(locked_until) - current_time).total_seconds())
                        return False, f"Too many attempts. Try again in {remaining_time} seconds"
                    
                    # Validacion - Verificar si Maximo de Intentos Excedido
                    if attempts >= self.max_attempts:
                        # Seguridad - Bloquear por Duracion Especificada
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
    
    # Registro - Registrar Intento
    def record_attempt(self, identifier: str, success: bool):
        """Registrar intento de login en la base de datos"""
        try:
            current_time = datetime.now()
            
            with db_manager.get_connection() as conn:
                if success:
                    # Seguridad - Reiniciar Intentos en Login Exitoso
                    conn.execute("""
                        DELETE FROM rate_limiting WHERE identifier = ?
                    """, (identifier,))
                else:
                    # Consulta - Verificar si Registro Existe
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
    
    # Seguridad - Sanitizar Entrada
    def sanitize_input(self, input_string: str) -> str:
        """Sanitizar entrada del usuario para prevenir ataques XSS e inyección"""
        try:
            if not input_string:
                return ""
            
            # Conversion - Convertir a string si es necesario
            sanitized = str(input_string).strip()
            
            # Seguridad - Codificar Caracteres Especiales en HTML
            sanitized = html.escape(sanitized)
            
            # Seguridad - Remover Caracteres Potencialmente Peligrosos
            dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}', 'script', 'javascript']
            for char in dangerous_chars:
                sanitized = sanitized.replace(char.lower(), '')
            
            # Validacion - Limitar Longitud
            return sanitized[:100] if len(sanitized) > 100 else sanitized
            
        except Exception as e:
            logger.error(f"Input sanitization error: {e}")
            return ""
    
    # Seguridad - Sanitizar Entrada para Base de Datos
    def sanitize_input_for_db(self, input_string: str) -> str:
        """Sanitizar entrada del usuario para almacenamiento en base de datos (sin codificación HTML)"""
        try:
            if not input_string:
                return ""
            
            # Conversion - Convertir a String si es Necesario
            sanitized = str(input_string).strip()
            
            # Seguridad - Remover Solo Caracteres Realmente Peligrosos
            # Nota: La inyeccion SQL se previene con consultas parametrizadas, no con sanitizacion de strings
            # Solo removemos caracteres que podrian romper el formato de datos
            dangerous_chars = ['\x00', '\n', '\r', '\x1a']  # Control characters that could break SQL
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            
            # Validacion - Limitar Longitud (mas larga para almacenamiento en BD)
            return sanitized[:255] if len(sanitized) > 255 else sanitized
            
        except Exception as e:
            logger.error(f"Database input sanitization error: {e}")
            return ""
    
    # Seguridad - Sanitizar Mensaje de Error
    def sanitize_error_message(self, error: Exception) -> str:
        """Sanitización mejorada de mensajes de error"""
        try:
            error_type = type(error).__name__
            
            # Logging - Registrar Error Completo para Debugging
            logger.error(f"Error occurred: {str(error)}")
            
            # Mensaje - Retornar Mensajes Genericos por Tipo de Error
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
    
    # Validacion - Validar Contraseña en Servidor
    def validate_password_server_side(self, password: str) -> Tuple[bool, str]:
        """Validación de contraseña en el servidor"""
        try:
            if not password:
                return False, "Password is required"
            
            if len(password) < 8:
                return False, "Password must be at least 8 characters long"
            
            if len(password) > 128:
                return False, "Password is too long (maximum 128 characters)"
            
            # Validacion - Verificar Patrones Debiles Comunes
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
            
            # Validacion - Verificar Complejidad Basica
            has_letter = re.search(r'[a-zA-Z]', password)
            has_digit = re.search(r'\d', password)
            
            if not has_letter or not has_digit:
                return False, "Password must contain both letters and numbers"
            
            return True, "Password is valid"
            
        except Exception as e:
            logger.error(f"Password validation error: {e}")
            return False, "Password validation failed"
    
    # Validacion - Validar Nombre de Usuario
    def validate_username(self, username: str) -> Tuple[bool, str]:
        """Validar formato y seguridad del nombre de usuario"""
        try:
            if not username:
                return False, "Username is required"
            
            if len(username) < 3:
                return False, "Username must be at least 3 characters long"
            
            if len(username) > 30:
                return False, "Username is too long (maximum 30 characters)"
            
            # Validacion - Verificar Caracteres Validos
            if not re.match(r'^[a-zA-Z0-9_-]+$', username):
                return False, "Username can only contain letters, numbers, underscores, and hyphens"
            
            # Validacion - Verificar Usuarios Reservados
            reserved_names = ['admin', 'root', 'system', 'guest', 'test', 'user', 'anonymous']
            if username.lower() in reserved_names:
                return False, "Username is reserved and cannot be used"
            
            return True, "Username is valid"
            
        except Exception as e:
            logger.error(f"Username validation error: {e}")
            return False, "Username validation failed"
    
    # Validacion - Validar Email
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validar formato y seguridad del email"""
        try:
            if not email:
                return False, "Email is required"
            
            if len(email) > 254:
                return False, "Email is too long"
            
            # Validacion - Validar Formato Basico de Email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return False, "Invalid email format"
            
            # Validacion - Verificar Patrones Sospechosos
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
    
    # Base de Datos - Crear Tabla de Rate Limiting
    def create_rate_limit_table(self):
        """Crear tabla de rate limiting si no existe"""
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
                
                # Base de Datos - Crear Indice para Mejor Rendimiento
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_rate_limiting_identifier 
                    ON rate_limiting(identifier)
                """)
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error creating rate limiting table: {e}")

# Instancia - Instancia Global de Security Features
security_features = SecurityFeatures()
