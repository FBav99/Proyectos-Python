from utils.ui.icon_system import get_icon, replace_emojis
"""
Nombre del Archivo: config.py
Descripción: Configuración general de la aplicación Streamlit
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Configuracion - Configurar Pagina
def setup_page_config():
    """Configura la página principal de Streamlit con título, icono y layout"""
    st.set_page_config(
        page_title="Dashboard Principal",
        page_icon=get_icon("📊", 20),
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ============================================================================
# CUSTOM STYLES
# ============================================================================

# Estilo - CSS Personalizado para Mejorar Estilo Visual
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #28a745;
        margin: 1rem 0;
    }
</style>
"""

# Estilo - Aplicar CSS Personalizado
def apply_custom_css():
    """
    Aplica los estilos CSS personalizados a la aplicación.
    
    Esta función debe ser llamada después de st.set_page_config() para
    aplicar los estilos personalizados definidos en CUSTOM_CSS.
    """
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True) 