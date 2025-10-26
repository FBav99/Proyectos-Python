"""
Nombre del Archivo: Inicio.py
Descripción: Página principal de la aplicación con autenticación y dashboard
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

import streamlit as st

# Imports de módulos core
from core.config import apply_custom_css
from core.data_quality_analyzer import data_quality_page

# Imports de módulos utils
from utils.dashboard import show_dashboard_selection
from utils.data import (create_data_cleaning_interface, get_current_data,
                        show_examples_section, show_upload_section)
from utils.learning.learning_progress import (get_level_progress,
                                               show_learning_section,
                                               show_user_profile_section)
from utils.ui import (clear_selected_template, get_current_user,
                      handle_authentication, should_show_main_content,
                      show_header, show_quick_start_section)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Función principal de la aplicación - Punto de entrada principal"""
    
    # Configurar página para Inicio
    st.set_page_config(
        page_title="Inicio - Dashboard Principal",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Autenticación del usuario
    current_user, name = handle_authentication()
    
    if not current_user:
        return  # Usuario no autenticado, formulario de login mostrado
    
    # ============================================================================
    # SECCIÓN HEADER - Bienvenida e información del usuario
    # ============================================================================
    show_header(name)
    
    # Obtener progreso del usuario desde la base de datos (solo para usuarios DB, no OAuth)
    if 'oauth_provider' not in current_user:
        total_progress, completed_count, progress = get_level_progress(current_user['id'])
    else:
        # Para usuarios OAuth, usar valores por defecto
        total_progress = 0
        completed_count = 0
        progress = {}
    
    # ============================================================================
    # SECCIÓN QUICK START - Botones de acción principal
    # ============================================================================
    show_quick_start_section()
    
    # ============================================================================
    # SECCIÓN UPLOAD - Cargar archivos
    # ============================================================================
    if st.session_state.get('show_upload_section', False):
        show_upload_section()
    
    # ============================================================================
    # SECCIÓN EXAMPLES - Ejemplos de datos
    # ============================================================================
    if st.session_state.get('show_examples_section', False):
        show_examples_section()
    
    # ============================================================================
    # SECCIÓN LEARNING - Aprendizaje y niveles
    # ============================================================================
    if st.session_state.get('show_learning_section', False):
        show_learning_section(total_progress, completed_count, progress)
    
    # ============================================================================
    # SECCIÓN DATA QUALITY - Análisis de calidad de datos
    # ============================================================================
    if st.session_state.get('show_data_quality', False) and 'uploaded_data' in st.session_state:
        st.divider()
        data_quality_page(st.session_state.uploaded_data)
    
    # ============================================================================
    # SECCIÓN DATA CLEANING - Limpieza de datos
    # ============================================================================
    if st.session_state.get('show_data_cleaning', False) and 'uploaded_data' in st.session_state:
        st.divider()
        create_data_cleaning_interface(st.session_state.uploaded_data)
    
    # ============================================================================
    # SECCIÓN DASHBOARD - Visualización de datos
    # ============================================================================
    if st.session_state.get('show_dashboard', False) and st.session_state.get('data_quality_completed', False):
        st.divider()
        df = get_current_data()
        if df is not None:
            show_dashboard_selection(df, current_user['username'])
        else:
            st.error("No hay datos disponibles para el dashboard.")
    
    # ============================================================================
    # SECCIÓN USER PROFILE - Perfil del usuario (mínima)
    # ============================================================================
    if should_show_main_content():
        # Limpiar selected_template al mostrar página principal para evitar loops de redirección
        clear_selected_template()
        
        show_user_profile_section(current_user['username'], total_progress, completed_count, current_user['id'])

if __name__ == "__main__":
    main() 