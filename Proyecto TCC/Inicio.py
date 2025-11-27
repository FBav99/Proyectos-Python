from utils.ui.icon_system import get_icon, replace_emojis
# Nombre del Archivo: Inicio.py
# Descripción: Página principal de la aplicación con autenticación y dashboard
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import logging
import streamlit as st

# Imports de módulos core
from core.config import apply_custom_css
from core.data_loader import load_sample_data
from core.data_quality_analyzer import analyze_data_quality, data_quality_page
from core.database import init_database, check_database_exists

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
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling
from data.sample_datasets import get_sample_datasets

logger = logging.getLogger(__name__)

# Configure error handling
configure_streamlit_error_handling()


# Cache - Precalentar Recursos
def warm_initial_caches():
    """Preload heavy resources once per session to avoid cloud cold-start delays."""
    if st.session_state.get("_warm_start_complete"):
        return
    try:
        sample_df = load_sample_data()
        analyze_data_quality(sample_df)
        get_sample_datasets()
    except Exception as exc:  # pragma: no cover - defensive logging for cloud traces
        logger.debug("Cache warm-up skipped: %s", exc)
    st.session_state["_warm_start_complete"] = True


# ============================================================================
# MAIN FUNCTION
# ============================================================================

# Principal - Punto de Entrada
@safe_main
def main():
    """Función principal de la aplicación - Punto de entrada principal"""
    
    # Inicializar base de datos si no existe (necesario para despliegue en Streamlit Cloud)
    if not check_database_exists():
        init_database()
    
    # Configurar página para Inicio
    st.set_page_config(
        page_title="Inicio - Dashboard Principal",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    warm_initial_caches()
    
    # Autenticación del usuario
    current_user, name = handle_authentication()
    
    if not current_user:
        return  # Usuario no autenticado, formulario de login mostrado

    welcome_data = st.session_state.pop('registration_welcome', None)
    if welcome_data:
        welcome_name = current_user.get('first_name') or welcome_data.get('first_name') or current_user.get('username', '')
        st.markdown(f"{get_icon("🎉", 20)} ¡Bienvenido, {welcome_name}! Tu cuenta se creó correctamente.", unsafe_allow_html=True)
    
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
    # SECCIÓN ENCUESTA INICIAL - Botón prominente para encuesta (solo para pruebas)
    # ============================================================================
    # Solo mostrar si el usuario no ha completado la encuesta inicial
    if 'oauth_provider' not in current_user:
        from core.survey_system import survey_system
        user_id = current_user['id']
        if not survey_system.has_completed_survey(user_id, 'initial'):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); padding: 2rem; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border: 3px solid #fff;">
                <h2 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.6rem;">{get_icon("📋", 24)} Encuesta Inicial - Período de Pruebas</h2>
                <p style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.1rem; opacity: 0.95;">Ayúdanos a mejorar la plataforma completando nuestra encuesta inicial</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📝 Completar Encuesta Inicial", type="primary", use_container_width=True, key="initial_survey_banner"):
                    st.switch_page("pages/99_Survey_Inicial.py")
            
            st.markdown("---")
    
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
        
        # Para usuarios de base de datos usamos su ID real; para OAuth no hay ID en la BD
        user_id_for_profile = current_user.get('id') if 'oauth_provider' not in current_user else None
        show_user_profile_section(current_user['username'], total_progress, completed_count, user_id_for_profile)

if __name__ == "__main__":
    main() 