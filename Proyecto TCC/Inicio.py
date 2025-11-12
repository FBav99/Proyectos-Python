"""
Nombre del Archivo: Inicio.py
Descripción: Página principal de la aplicación con autenticación y dashboard
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

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

HERO_BANNER_HTML = """
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.75rem; border-radius: 18px; margin: 1.5rem 0 2rem; box-shadow: 0 20px 35px rgba(15,23,42,0.18); border: 1px solid rgba(255,255,255,0.2);">
    <h2 style="color: #e2e8f0; margin-bottom: 0.8rem; text-align: center; font-size: 1.6rem;">🌟 Bienvenido al piloto de la Plataforma TCC</h2>
    <p style="color: rgba(226,232,240,0.95); font-size: 1rem; margin-bottom: 1rem; text-align: center;">
        Estás probando una versión en preparación de nuestra guía interactiva para analizar datos desde cero: carga tus propios archivos,
        evalúa la calidad, aplica limpiezas guiadas y diseña dashboards personalizados siguiendo niveles paso a paso.
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 1rem;">
        <div style="background: rgba(15, 118, 110, 0.2); border-radius: 12px; padding: 1rem; border: 1px solid rgba(16,185,129,0.35);">
            <h4 style="color: #bbf7d0; margin: 0 0 0.3rem 0;">Aprendizaje guiado</h4>
            <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem;">Recorre niveles prácticos que explican cada paso con ejemplos claros y sin tecnicismos innecesarios.</p>
        </div>
        <div style="background: rgba(59, 130, 246, 0.18); border-radius: 12px; padding: 1rem; border: 1px solid rgba(96,165,250,0.35);">
            <h4 style="color: #bfdbfe; margin: 0 0 0.3rem 0;">Procesamiento de datos</h4>
            <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem;">Sube tus archivos CSV o Excel, revisa la calidad y aplica limpiezas guiadas antes de visualizar.</p>
        </div>
        <div style="background: rgba(129, 140, 248, 0.18); border-radius: 12px; padding: 1rem; border: 1px solid rgba(165,180,252,0.35);">
            <h4 style="color: #c7d2fe; margin: 0 0 0.3rem 0;">Dashboards a medida</h4>
            <p style="color: #e2e8f0; margin: 0; font-size: 0.9rem;">Combina componentes visuales, guarda tus configuraciones y exporta resultados para compartirlos.</p>
        </div>
    </div>
    <p style="color: rgba(226,232,240,0.85); font-size: 0.9rem; margin-top: 1.4rem; text-align: center;">
        Tu feedback es clave en esta etapa piloto: completa la encuesta inicial y cuéntanos qué te resulta útil o qué mejorarías.
    </p>
</div>
"""

# Configure error handling
configure_streamlit_error_handling()


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
    
    # ============================================================================
    # SECCIÓN HEADER - Bienvenida e información del usuario
    # ============================================================================
    show_header(name)
    
    # Resumen contextual durante la fase de pruebas
    st.markdown(HERO_BANNER_HTML, unsafe_allow_html=True)
    
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
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); padding: 2rem; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border: 3px solid #fff;">
                <h2 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.6rem;">📋 Encuesta Inicial - Período de Pruebas</h2>
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
        
        show_user_profile_section(current_user['username'], total_progress, completed_count, current_user['id'])

if __name__ == "__main__":
    main() 