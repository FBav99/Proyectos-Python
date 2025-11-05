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
    create_dashboard_blanco_section,
    create_visualization_guide,
    create_common_scenarios,
    create_troubleshooting_section,
    create_quick_reference,
    create_learning_resources,
    create_navigation_section
)
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Ayuda - Guía de Usuario",
    page_icon="❓",
    layout="wide"
)

@safe_main
def main():
    # Load level styles for consistent appearance
    st.markdown(load_level_styles(), unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ## 🎯 Bienvenido al Panel de Análisis de Datos
    
    Esta herramienta te permite analizar tus datos de manera fácil e intuitiva. 
    Ya seas un principiante o un usuario avanzado, encontrarás funcionalidades útiles para tu análisis.
    """)
    
    # Create help sections using modular components
    create_help_header()
    create_learning_levels_section()
    create_dashboard_blanco_section()
    create_visualization_guide()
    create_common_scenarios()
    create_troubleshooting_section()
    create_quick_reference()
    create_learning_resources()
    create_navigation_section()

if __name__ == "__main__":
    main()
