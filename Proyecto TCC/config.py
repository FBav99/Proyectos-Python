import streamlit as st

# Configuración de página
def setup_page_config():
    """Configurar la página de Streamlit"""
    st.set_page_config(
        page_title="Panel de Análisis de Datos",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# CSS personalizado para mejor estilo
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

def apply_custom_css():
    """Aplicar CSS personalizado"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True) 