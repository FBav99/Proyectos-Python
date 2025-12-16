# Nombre del Archivo: streamlit_error_handler.py
# Descripción: Manejador global de errores para Streamlit que previene exponer rutas de archivos en tracebacks
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

from utils.ui.icon_system import get_icon, replace_emojis

import streamlit as st
import traceback
import sys
import re
from functools import wraps
from typing import Callable, Any


# Limpieza - Sanitizar Traceback
def sanitize_traceback(tb_lines: list) -> list:
    """Sanitiza las líneas del traceback para remover rutas de archivos"""
    sanitized = []
    
    for line in tb_lines:
        # Limpieza - Remover rutas de Streamlit Cloud
        line = re.sub(r'/mount/src/[^/]+/', '[APP]/', line)
        line = re.sub(r'/mount/src/', '[APP]/', line)
        
        # Limpieza - Remover rutas de Windows
        line = re.sub(r'[A-Za-z]:\\[^\\]*\\', '[APP]', line)
        line = re.sub(r'C:\\Users\\[^\\]*\\', '[USER]', line)
        
        # Limpieza - Remover rutas de Linux/Mac
        line = re.sub(r'/home/[^/]+/', '[HOME]/', line)
        line = re.sub(r'/Users/[^/]+/', '[USER]/', line)
        
        # Limpieza - Remover rutas específicas del proyecto
        line = re.sub(r'Proyecto TCC', '[PROJECT]', line)
        line = re.sub(r'Proyectos Python', '[PROJECT]', line)
        line = re.sub(r'OneDrive', '[DRIVE]', line)
        
        # Limpieza - Remover nombres de archivos específicos pero mantener estructura
        line = re.sub(r'([^/]+)\.py', '[FILE].py', line)
        
        # Limpieza - Mantener números de línea pero hacerlos genéricos
        line = re.sub(r'line \d+', 'line [N]', line)
        
        sanitized.append(line)
    
    return sanitized


# Limpieza - Sanitizar Mensaje de Error
def sanitize_error_message(error_msg: str) -> str:
    """Sanitiza mensajes de error para remover rutas sensibles"""
    if not error_msg:
        return "Ocurrió un error"
    
    # Limpieza - Remover rutas de mensajes de error
    error_msg = re.sub(r'/mount/src/[^/]+/', '[APP]/', error_msg)
    error_msg = re.sub(r'[A-Za-z]:\\[^\\]*\\', '[PATH]', error_msg)
    error_msg = re.sub(r'/home/[^/]+/', '[HOME]/', error_msg)
    error_msg = re.sub(r'Proyecto TCC', '[PROJECT]', error_msg)
    
    return error_msg


# Decorador - Wrapper Seguro para Páginas de Streamlit
def safe_streamlit_page(func: Callable) -> Callable:
    """
    Decorador para envolver funciones de página de Streamlit y capturar todas las excepciones
    Esto previene que Streamlit muestre tracebacks completos con rutas de archivos
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Manejo de Errores - Obtener el traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Manejo de Errores - Obtener tipo y mensaje de error
            error_type = type(e).__name__
            error_message = str(e)
            
            # Limpieza - Sanitizar mensaje de error
            sanitized_msg = sanitize_error_message(error_message)
            
            # UI - Determinar mensaje amigable para el usuario basado en el tipo de error
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
            
            # UI - Mostrar error amigable para el usuario
            st.error(user_msg)
            
            # Debug - Opcionalmente mostrar mensaje técnico genérico (sin rutas)
            # Debug - Temporalmente habilitar modo debug para troubleshooting
            if st.session_state.get('debug_mode', False) or True:  # Debug - Temporalmente siempre True para debugging
                with st.expander(replace_emojis("🔧 Detalles técnicos (modo debug)")):
                    st.code(f"Tipo: {error_type}\nMensaje: {sanitized_msg}\nError original: {error_message}", language=None)
                    import traceback
                    st.code(traceback.format_exc(), language='python')
            
            # Logging - Registrar el error completo para debugging (solo servidor)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {error_type}: {error_message}")
            logger.error(traceback.format_exc())
            
            # Control de Flujo - Detener ejecución para prevenir más errores
            st.stop()
            
    return wrapper


# Configuracion - Configurar Manejo de Errores de Streamlit
def configure_streamlit_error_handling():
    """
    Configura Streamlit para suprimir tracebacks de error por defecto
    Esto debe ser llamado al inicio de tu página principal
    """
    # Configuracion - Configurar Streamlit para mostrar errores mínimos
    # Nota: Esto es un workaround ya que Streamlit no tiene una configuración directa para esto
    
    # Configuracion - Sobrescribir sys.excepthook para capturar excepciones no manejadas
    original_excepthook = sys.excepthook
    
    def custom_excepthook(exc_type, exc_value, exc_traceback):
        # Logging - No mostrar traceback en consola si se ejecuta en Streamlit
        if 'streamlit' in sys.modules:
            # Logging - Solo registrarlo
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Unhandled exception: {exc_type.__name__}: {exc_value}")
            logger.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        else:
            # Debug - Mostrar traceback normal si no está en Streamlit
            original_excepthook(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = custom_excepthook


# Decorador - Función Conveniente para Envolver Funciones Main
def safe_main(func: Callable) -> Callable:
    """Decorador específicamente para funciones main() en páginas de Streamlit"""
    return safe_streamlit_page(func)

