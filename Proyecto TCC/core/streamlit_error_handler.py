from utils.ui.icon_system import get_icon, replace_emojis
"""
Global error handler for Streamlit to prevent exposing file paths in tracebacks
This wraps all page functions to catch and sanitize errors before Streamlit displays them
"""

import streamlit as st
import traceback
import sys
import re
from functools import wraps
from typing import Callable, Any


def sanitize_traceback(tb_lines: list) -> list:
    """Sanitize traceback lines to remove file paths"""
    sanitized = []
    
    for line in tb_lines:
        # Remove Streamlit Cloud paths
        line = re.sub(r'/mount/src/[^/]+/', '[APP]/', line)
        line = re.sub(r'/mount/src/', '[APP]/', line)
        
        # Remove Windows paths
        line = re.sub(r'[A-Za-z]:\\[^\\]*\\', '[APP]', line)
        line = re.sub(r'C:\\Users\\[^\\]*\\', '[USER]', line)
        
        # Remove Linux/Mac paths
        line = re.sub(r'/home/[^/]+/', '[HOME]/', line)
        line = re.sub(r'/Users/[^/]+/', '[USER]/', line)
        
        # Remove project-specific paths
        line = re.sub(r'Proyecto TCC', '[PROJECT]', line)
        line = re.sub(r'Proyectos Python', '[PROJECT]', line)
        line = re.sub(r'OneDrive', '[DRIVE]', line)
        
        # Remove specific file names but keep structure
        line = re.sub(r'([^/]+)\.py', '[FILE].py', line)
        
        # Keep line numbers but make them generic
        line = re.sub(r'line \d+', 'line [N]', line)
        
        sanitized.append(line)
    
    return sanitized


def sanitize_error_message(error_msg: str) -> str:
    """Sanitize error messages to remove sensitive paths"""
    if not error_msg:
        return "An error occurred"
    
    # Limpieza - Remover Rutas de Mensajes de Error
    error_msg = re.sub(r'/mount/src/[^/]+/', '[APP]/', error_msg)
    error_msg = re.sub(r'[A-Za-z]:\\[^\\]*\\', '[PATH]', error_msg)
    error_msg = re.sub(r'/home/[^/]+/', '[HOME]/', error_msg)
    error_msg = re.sub(r'Proyecto TCC', '[PROJECT]', error_msg)
    
    return error_msg


def safe_streamlit_page(func: Callable) -> Callable:
    """
    Decorator to wrap Streamlit page functions and catch all exceptions
    This prevents Streamlit from showing full tracebacks with file paths
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Get the traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Get error type and message
            error_type = type(e).__name__
            error_message = str(e)
            
            # Sanitize error message
            sanitized_msg = sanitize_error_message(error_message)
            
            # Determine user-friendly message based on error type
            if error_type == "FileNotFoundError":
                user_msg = replace_emojis("❌ **Archivo no encontrado**\n\nEl archivo o recurso solicitado no está disponible.")
            elif error_type == "PermissionError":
                user_msg = replace_emojis("❌ **Error de permisos**\n\nNo se tienen permisos para realizar esta operación.")
            elif error_type == "OSError":
                user_msg = replace_emojis("❌ **Error del sistema**\n\nNo se pudo completar la operación solicitada.")
            elif error_type == "IOError":
                user_msg = replace_emojis("❌ **Error de entrada/salida**\n\nHubo un problema al acceder a los archivos.")
            elif error_type == "KeyError":
                user_msg = replace_emojis("❌ **Error de configuración**\n\nFalta información requerida en la configuración.")
            elif error_type == "ValueError":
                user_msg = f"{get_icon("❌", 20)} **Error de datos**\n\n{sanitized_msg}"
            elif error_type == "ConnectionError":
                user_msg = replace_emojis("❌ **Error de conexión**\n\nNo se pudo conectar con el servicio.")
            else:
                user_msg = f"{get_icon("❌", 20)} **Error inesperado**\n\nOcurrió un error al procesar tu solicitud. Por favor, intenta nuevamente."
            
            # Display user-friendly error
            st.error(user_msg)
            
            # Optionally show a generic technical message (without paths)
            # Temporarily enable debug mode for troubleshooting
            if st.session_state.get('debug_mode', False) or True:  # Temporarily always True for debugging
                with st.expander(replace_emojis("🔧 Detalles técnicos (modo debug)")):
                    st.code(f"Tipo: {error_type}\nMensaje: {sanitized_msg}\nError original: {error_message}", language=None)
                    import traceback
                    st.code(traceback.format_exc(), language='python')
            
            # Log the full error for debugging (server-side only)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {error_type}: {error_message}")
            logger.error(traceback.format_exc())
            
            # Stop execution to prevent further errors
            st.stop()
            
    return wrapper


def configure_streamlit_error_handling():
    """
    Configure Streamlit to suppress default error tracebacks
    This should be called at the start of your main page
    """
    # Configuracion - Configurar Streamlit para Mostrar Errores Minimos
    # Nota: Esto es un workaround ya que Streamlit no tiene una configuracion directa para esto
    
    # Configuracion - Sobrescribir sys.excepthook para Capturar Excepciones No Manejadas
    original_excepthook = sys.excepthook
    
    def custom_excepthook(exc_type, exc_value, exc_traceback):
        # Don't show traceback in console if running in Streamlit
        if 'streamlit' in sys.modules:
            # Just log it
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Unhandled exception: {exc_type.__name__}: {exc_value}")
            logger.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        else:
            # Show normal traceback if not in Streamlit
            original_excepthook(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = custom_excepthook


# Convenience function for wrapping main functions
def safe_main(func: Callable) -> Callable:
    """Decorator specifically for main() functions in Streamlit pages"""
    return safe_streamlit_page(func)

