# Nombre del Archivo: 00_Ayuda.py
# Descripción: Página de ayuda para la plataforma de análisis de datos TCC - Interfaz principal de ayuda con guías de aprendizaje y asistencia al usuario
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import sys
import os

# Configuracion - Agregar la raíz del proyecto al path de Python
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

# Configuracion - Configurar manejo de errores
configure_streamlit_error_handling()

# Configuracion - Configurar página
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
    
    # UI - Crear secciones de ayuda usando componentes modulares
    create_help_header()
    
    # UI - Secciones principales con índice navegable
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
