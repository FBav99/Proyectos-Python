import streamlit as st
import traceback
import sys
import os
from datetime import datetime
import logging

from utils.ui.icon_system import get_icon, replace_emojis
class SecureErrorHandler:
    """Maneja errores de forma segura ocultando información sensible"""
    
    def __init__(self):
        self.error_id_counter = 0
        self.error_log = {}
        
    def generate_error_id(self):
        """Genera un ID único para el error"""
        self.error_id_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"ERR_{timestamp}_{self.error_id_counter:04d}"
    
    def sanitize_error_message(self, error_msg):
        """Sanitiza el mensaje de error removiendo rutas sensibles"""
        if not error_msg:
            return "Error interno del sistema"
        
        # Lista de patrones a ocultar
        sensitive_patterns = [
            # Rutas del sistema
            r'C:\\Users\\.*?\\',
            r'/home/.*?/',
            r'/Users/.*?/',
            r'c:\\Users\\.*?\\',
            # Rutas del proyecto
            r'Proyecto TCC',
            r'Proyectos Python',
            r'OneDrive',
            # Extensiones de archivo comunes
            r'\.py',
            r'\.csv',
            r'\.xlsx',
            r'\.json',
            r'\.yaml',
            r'\.yml',
            # Nombres de archivos específicos
            r'Inicio\.py',
            r'main\.py',
            r'config\.py',
            r'auth_config\.py',
        ]
        
        import re
        sanitized_msg = error_msg
        
        for pattern in sensitive_patterns:
            sanitized_msg = re.sub(pattern, '[OCULTO]', sanitized_msg, flags=re.IGNORECASE)
        
        # Remover rutas absolutas
        sanitized_msg = re.sub(r'[A-Za-z]:\\[^\\]*\\', '[RUTA]\\', sanitized_msg)
        sanitized_msg = re.sub(r'/[^/]*/', '[RUTA]/', sanitized_msg)
        
        # Remover números de línea específicos
        sanitized_msg = re.sub(r'line \d+', 'línea [OCULTA]', sanitized_msg)
        sanitized_msg = re.sub(r'line \d+', 'línea [OCULTA]', sanitized_msg)
        
        return sanitized_msg
    
    def log_error(self, error, context=""):
        """Registra el error internamente para debugging"""
        error_id = self.generate_error_id()
        
        # Log completo para debugging interno
        full_error_info = {
            'error_id': error_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context
        }
        
        # Guardar en session state para debugging (solo en desarrollo)
        if 'debug_errors' not in st.session_state:
            st.session_state.debug_errors = {}
        
        st.session_state.debug_errors[error_id] = full_error_info
        
        return error_id
    
    def display_user_friendly_error(self, error, context="", show_details=False):
        """Muestra un error amigable al usuario"""
        error_id = self.log_error(error, context)
        
        # Mensaje sanitizado para el usuario
        sanitized_msg = self.sanitize_error_message(str(error))
        
        # Determinar el tipo de error y mostrar mensaje apropiado
        error_type = type(error).__name__
        
        if "FileNotFoundError" in error_type:
            user_message = replace_emojis("❌ **Error de archivo no encontrado**\n\nEl archivo solicitado no está disponible.")
        elif "PermissionError" in error_type:
            user_message = replace_emojis("❌ **Error de permisos**\n\nNo tienes permisos para acceder a este recurso.")
        elif "ValueError" in error_type:
            user_message = f"{get_icon("❌", 20)} **Error de datos**\n\n{sanitized_msg}"
        elif "KeyError" in error_type:
            user_message = replace_emojis("❌ **Error de configuración**\n\nFalta información requerida en la configuración.")
        elif "ConnectionError" in error_type:
            user_message = replace_emojis("❌ **Error de conexión**\n\nNo se pudo conectar con el servicio solicitado.")
        elif "TimeoutError" in error_type:
            user_message = replace_emojis("❌ **Error de tiempo de espera**\n\nLa operación tardó demasiado en completarse.")
        elif "MemoryError" in error_type:
            user_message = replace_emojis("❌ **Error de memoria**\n\nNo hay suficiente memoria para procesar los datos.")
        else:
            user_message = f"{get_icon("❌", 20)} **Error inesperado**\n\n{sanitized_msg}"
        
        # Mostrar error al usuario
        st.error(user_message)
        
        # Información adicional para debugging (solo en desarrollo)
        if show_details and st.session_state.get('debug_mode', False):
            with st.expander(replace_emojis("🔧 Información técnica (Solo para desarrolladores)")):
                st.code(f"Error ID: {error_id}")
                st.code(f"Tipo: {error_type}")
                st.code(f"Contexto: {context}")
                st.code(f"Timestamp: {datetime.now().isoformat()}")
        
        # Botón para reportar error
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(replace_emojis("💡 Si el problema persiste, contacta al soporte técnico."), unsafe_allow_html=True)
        with col2:
            if st.button("📋 Reportar Error", key=f"report_{error_id}"):
                self.show_error_report_form(error_id)
        
        return error_id
    
    def show_error_report_form(self, error_id):
        """Muestra un formulario para reportar errores"""
        st.markdown(replace_emojis("### 📋 Reportar Error"), unsafe_allow_html=True)
        
        with st.form(f"error_report_{error_id}"):
            user_email = st.text_input("📧 Tu email (opcional):")
            user_description = st.text_area(
                replace_emojis("📝 Describe qué estabas haciendo cuando ocurrió el error:"),
                placeholder="Ej: Estaba subiendo un archivo CSV cuando..."
            )
            include_technical = st.checkbox(replace_emojis("📊 Incluir información técnica"))
            
            if st.form_submit_button("📤 Enviar Reporte"):
                self.submit_error_report(error_id, user_email, user_description, include_technical)
    
    def submit_error_report(self, error_id, user_email, user_description, include_technical):
        """Envía el reporte de error"""
        try:
            # Aquí podrías implementar el envío real del reporte
            # Por ahora, solo mostramos un mensaje de confirmación
            
            report_data = {
                'error_id': error_id,
                'user_email': user_email,
                'user_description': user_description,
                'include_technical': include_technical,
                'timestamp': datetime.now().isoformat()
            }
            
            # Guardar en session state (en producción esto iría a una base de datos)
            if 'error_reports' not in st.session_state:
                st.session_state.error_reports = []
            
            st.session_state.error_reports.append(report_data)
            
            st.markdown(replace_emojis("✅ Reporte enviado exitosamente. Gracias por tu ayuda."), unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(replace_emojis("❌ Error al enviar el reporte. Por favor, intenta más tarde."), unsafe_allow_html=True)
    
    def safe_execute(self, func, *args, **kwargs):
        """Ejecuta una función de forma segura con manejo de errores"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.display_user_friendly_error(e, f"Función: {func.__name__}")
            return None

# Instancia global del manejador de errores
error_handler = SecureErrorHandler()

def safe_execute(func, *args, **kwargs):
    """Decorador para ejecutar funciones de forma segura"""
    return error_handler.safe_execute(func, *args, **kwargs)

def display_error(error, context="", show_details=False):
    """Función de conveniencia para mostrar errores"""
    return error_handler.display_user_friendly_error(error, context, show_details)

def get_error_info(error_id):
    """Obtiene información de un error específico (solo para debugging)"""
    return st.session_state.get('debug_errors', {}).get(error_id)

def clear_error_logs():
    """Limpia los logs de errores (útil para debugging)"""
    if 'debug_errors' in st.session_state:
        del st.session_state.debug_errors
    if 'error_reports' in st.session_state:
        del st.session_state.error_reports
