import streamlit as st

# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.data_quality_analyzer import data_quality_page

# Import new modular components
from utils.auth_ui import handle_authentication, get_current_user
from utils.main_ui import show_header, show_quick_start_section, should_show_main_content, clear_selected_template
from utils.data_handling import show_upload_section, show_examples_section, get_current_data
from utils.learning_progress import get_level_progress, show_learning_section, show_user_profile_section
from utils.dashboard_templates import show_dashboard_selection

def main():
    """Función principal de la aplicación"""
    # Configurar página específica para Inicio
    st.set_page_config(
        page_title="Inicio - Dashboard Principal",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Handle authentication
    current_user, name = handle_authentication()
    
    if not current_user:
        return  # User is not authenticated, login form is shown
    
    # ============================================================================
    # HEADER SECTION - Welcome and User Info
    # ============================================================================
    show_header(name)
    
    # Get user progress from database (only for database users, not OAuth users)
    if 'oauth_provider' not in current_user:
        total_progress, completed_count, progress = get_level_progress(current_user['id'])
    else:
        # For OAuth users, use default values
        total_progress = 0
        completed_count = 0
        progress = {}
    
    # ============================================================================
    # QUICK START SECTION - Main Action Buttons
    # ============================================================================
    show_quick_start_section()
    
    # ============================================================================
    # UPLOAD SECTION
    # ============================================================================
    if st.session_state.get('show_upload_section', False):
        show_upload_section()
    
    # ============================================================================
    # EXAMPLES SECTION
    # ============================================================================
    if st.session_state.get('show_examples_section', False):
        show_examples_section()
    
    # ============================================================================
    # LEARNING SECTION
    # ============================================================================
    if st.session_state.get('show_learning_section', False):
        show_learning_section(total_progress, completed_count, progress)
    
    # ============================================================================
    # DATA QUALITY ANALYSIS SECTION
    # ============================================================================
    if st.session_state.get('show_data_quality', False) and 'uploaded_data' in st.session_state:
        st.divider()
        data_quality_page(st.session_state.uploaded_data)
    
    # ============================================================================
    # DASHBOARD SECTION
    # ============================================================================
    if st.session_state.get('show_dashboard', False) and st.session_state.get('data_quality_completed', False):
        st.divider()
        df = get_current_data()
        if df is not None:
            show_dashboard_selection(df, current_user['username'])
        else:
            st.error("No hay datos disponibles para el dashboard.")
    
    # ============================================================================
    # USER PROFILE SECTION (Minimal)
    # ============================================================================
    if should_show_main_content():
        # Clear selected_template when showing main page to avoid redirect loops
        clear_selected_template()
        
        show_user_profile_section(current_user['username'], total_progress, completed_count)

if __name__ == "__main__":
    main() 