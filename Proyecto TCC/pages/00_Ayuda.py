"""
Help page for TCC Data Analysis Platform
Main help interface with learning guides and user assistance
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.learning import (
    load_level_styles,
    create_help_header,
    create_learning_levels_section,
    create_platform_functions_section,
    create_general_concepts_section,
    create_best_practices_section,
    create_external_tools_section,
    create_decision_guide_section,
    create_dashboard_blanco_section,
    create_visualization_guide,
    create_common_scenarios,
    create_troubleshooting_section,
    create_quick_reference,
    create_learning_resources,
    create_navigation_section
)
from utils.ui import auth_ui
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Ayuda - Guía de Usuario",
    page_icon="❓",
    layout="wide"
)

# Principal - Pagina de Ayuda
@safe_main
def main():
    # UI - Inicializar Sidebar con Info de Usuario
    init_sidebar()
    
    # UI - Cargar Estilos de Nivel para Apariencia Consistente
    st.markdown(load_level_styles(), unsafe_allow_html=True)
    
    # UI - Crear Secciones de Ayuda usando Componentes Modulares
    create_help_header()
    
    # Secciones principales con índice navegable
    create_learning_levels_section()
    create_platform_functions_section()
    create_general_concepts_section()
    create_best_practices_section()
    create_external_tools_section()
    create_decision_guide_section()
    create_dashboard_blanco_section()
    create_visualization_guide()
    create_common_scenarios()
    create_troubleshooting_section()
    create_quick_reference()
    create_learning_resources()
    create_navigation_section()

if __name__ == "__main__":
    main()
