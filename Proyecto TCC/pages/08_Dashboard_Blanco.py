import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.auth_service import get_current_user, require_auth
from utils.analysis import (
    calculate_metrics, 
    calculate_growth_metrics, 
    calculate_performance_insights,
    create_time_series_chart, 
    create_category_analysis, 
    create_regional_analysis,
    create_correlation_matrix,
    create_custom_calculation_charts,
    apply_custom_calculations,
    apply_all_filters
)
from utils.ui import (
    create_sidebar_controls,
    create_custom_calculations_ui,
    display_metrics_dashboard,
    display_custom_calculations_metrics,
    display_export_section,
    display_error, 
    safe_execute
)

# Import new dashboard modules
from utils.dashboard import configure_component, render_dashboard, create_dashboard_sidebar, show_dashboard_info
from utils.ui import auth_ui
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

@safe_main
def main():
    """Dashboard en Blanco - Construcción Manual"""
    # Configurar página
    st.set_page_config(
        page_title="Dashboard en Blanco - Construcción Manual",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Initialize sidebar with user info (always visible)
    current_user = init_sidebar()
    if not current_user:
        st.error("Por favor inicia sesión para acceder a esta página.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Volver al Inicio", use_container_width=True):
                st.switch_page("Inicio.py")
        with col2:
            if st.button("🔐 Iniciar Sesión", use_container_width=True):
                st.switch_page("Inicio.py")
        st.stop()
    
    username = current_user['username']
    name = f"{current_user['first_name']} {current_user['last_name']}"
    
    # Header
    st.markdown(f'<h1 class="main-header">🎨 Dashboard en Blanco</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.1rem;">Construye tu dashboard personalizado, <strong>{name}</strong></p>', unsafe_allow_html=True)
    
    # Get data
    df = None
    if 'cleaned_data' in st.session_state:
        df = st.session_state.cleaned_data
    elif 'sample_data' in st.session_state:
        df = st.session_state.sample_data
    else:
        st.error("❌ No hay datos disponibles. Por favor, sube datos o usa un dataset de ejemplo desde la página de inicio.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Volver al Inicio", type="primary"):
                st.switch_page("Inicio.py")
        with col2:
            if st.button("📤 Subir Datos", type="primary"):
                st.switch_page("Inicio.py")
        st.stop()
    
    # Initialize dashboard components in session state
    if 'dashboard_components' not in st.session_state:
        st.session_state.dashboard_components = []
    
    # Create sidebar
    create_dashboard_sidebar(df)
    
    # Main content area
    st.markdown("---")
    
    # Component configuration section
    if st.session_state.get('editing_component') is not None:
        editing_id = st.session_state.editing_component
        component = next((c for c in st.session_state.dashboard_components if c['id'] == editing_id), None)
        
        if component:
            st.markdown(f"### ⚙️ Configurando: {component['title']}")
            configure_component(component, df)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Guardar Configuración", type="primary", use_container_width=True):
                    st.session_state.editing_component = None
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.session_state.editing_component = None
                    st.rerun()
            
            st.markdown("---")
        else:
            st.session_state.editing_component = None
    
    # Dashboard info
    show_dashboard_info(df)
    
    # Render dashboard
    render_dashboard(df)
    
    # Footer navigation
    st.markdown("---")
    st.markdown("### 🧭 Navegación Rápida")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("📊 Ver Métricas", use_container_width=True):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col3:
        if st.button("🚀 Nivel Avanzado", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col4:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

if __name__ == "__main__":
    main()
