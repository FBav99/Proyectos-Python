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
from utils.ui.onboarding import show_onboarding_tour, check_onboarding_status
from core.database import DatabaseManager

logger = logging.getLogger(__name__)

# Configuracion - Configurar Manejo de Errores
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


# UI - Mostrar Banner de Nivel Actual
def show_current_level_banner(progress):
    """Show a banner indicating the user's current learning level"""
    # Determinar el nivel actual
    level_order = ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']
    current_level = None
    current_level_name = None
    current_level_subtitle = None
    learning_content = None
    
    for level in level_order:
        if not progress.get(level, False):
            current_level = level
            break
    
    # Si todos los niveles están completados
    if current_level is None:
        current_level = 'completed'
        current_level_name = 'Todos los Niveles Completados'
        current_level_subtitle = '¡Felicidades! Visita la Conclusión para ver tu resumen y próximos pasos'
        learning_content = None
        level_icon = '🏆'
        level_color = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    else:
        # Mapeo de niveles a nombres, subtítulos y contenido de aprendizaje
        level_info = {
            'nivel0': (
                'Nivel 0', 
                'Introducción', 
                '🧭', 
                'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'entender qué son los datos, sus tipos principales y cómo se organizan en tablas'
            ),
            'nivel1': (
                'Nivel 1', 
                'Básico', 
                '📚', 
                'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'cargar y preparar datos, verificar su calidad y limpiarlos para el análisis'
            ),
            'nivel2': (
                'Nivel 2', 
                'Filtros', 
                '🔍', 
                'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'filtrar datos por condiciones específicas, rangos de fechas y combinar múltiples filtros'
            ),
            'nivel3': (
                'Nivel 3', 
                'Métricas', 
                '📊', 
                'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                'calcular métricas y KPIs, interpretar resultados y comparar datos para tomar decisiones'
            ),
            'nivel4': (
                'Nivel 4', 
                'Avanzado', 
                '🚀', 
                'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                'analizar tendencias, crear visualizaciones interactivas y construir dashboards profesionales'
            )
        }
        
        current_level_name, current_level_subtitle, level_icon, level_color, learning_content = level_info.get(
            current_level, 
            ('Nivel Actual', 'Continuar aprendiendo', '🎓', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'continuar tu aprendizaje')
        )
    
    # Mostrar el banner
    if learning_content:
        banner_html = f"""
        <div style="background: {level_color}; padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <div style="font-size: 2.5rem;">{get_icon(level_icon, 40)}</div>
                <div style="text-align: center; flex: 1; min-width: 200px;">
                    <h3 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 600;">Tu Nivel Actual: {current_level_name}</h3>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.95;">{current_level_subtitle}</p>
                    <p style="color: white; margin: 0.8rem 0 0 0; font-size: 0.95rem; opacity: 0.9; font-style: italic;">Actualmente, estás aprendiendo a {learning_content}</p>
                </div>
            </div>
        </div>
        """
    else:
        banner_html = f"""
        <div style="background: {level_color}; padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <div style="font-size: 2.5rem;">{get_icon(level_icon, 40)}</div>
                <div style="text-align: center; flex: 1; min-width: 200px;">
                    <h3 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 600;">Tu Nivel Actual: {current_level_name}</h3>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.95;">{current_level_subtitle}</p>
                </div>
            </div>
        </div>
        """
    
    st.markdown(banner_html, unsafe_allow_html=True)
    
    # Si todos los niveles están completados, mostrar botón para conclusión
    if current_level == 'completed':
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎓 Ver Conclusión y Próximos Pasos", type="primary", use_container_width=True, key="banner_conclusion_button"):
                st.switch_page("pages/05_Conclusion.py")


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
    # SECCIÓN ONBOARDING - Tour guiado para nuevos usuarios
    # ============================================================================
    if 'oauth_provider' not in current_user:
        # Cache DatabaseManager instance per session to avoid recreating connections
        if '_db_manager' not in st.session_state:
            st.session_state._db_manager = DatabaseManager()
        db_manager = st.session_state._db_manager
        user_id = current_user['id']
        
        # Check if user needs onboarding (first time or not completed)
        # This is now cached to reduce database queries
        onboarding_completed = check_onboarding_status(user_id, db_manager)
        
        # Show onboarding if:
        # 1. User hasn't completed it in DB, OR
        # 2. User just registered (registration_welcome exists), OR
        # 3. User manually requests it (session state)
        should_show_onboarding = (
            not onboarding_completed or 
            welcome_data is not None or
            st.session_state.get('show_onboarding', False)
        )
        
        if should_show_onboarding:
            onboarding_active = show_onboarding_tour(user_id, db_manager)
            
            # If onboarding is active, don't show other content
            if onboarding_active:
                st.stop()  # Stop rendering rest of page
    
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
    # SECCIÓN BANNER NIVEL ACTUAL - Mostrar nivel actual del usuario
    # ============================================================================
    # Solo mostrar el banner si el usuario tiene progreso (no es OAuth o tiene ID)
    if 'oauth_provider' not in current_user:
        show_current_level_banner(progress)
    
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