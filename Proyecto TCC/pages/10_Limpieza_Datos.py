import streamlit as st
import pandas as pd
from utils.data import create_data_cleaning_interface, show_upload_section, show_examples_section
from core.config import setup_page_config, apply_custom_css

def main():
    """Página de limpieza automática de datos"""
    # Configurar página
    setup_page_config()
    apply_custom_css()
    
    # Título principal
    st.markdown('<h1 class="main-header">🧹 Limpieza Automática de Datos</h1>', unsafe_allow_html=True)
    
    # Descripción
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.5rem;">🧽 Limpieza Automática de Datos</h2>
        <p style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.1rem;">
            Limpia y prepara tus datos automáticamente antes del análisis
        </p>
        <div style="color: rgba(255,255,255,0.9); text-align: center; font-size: 0.9rem;">
            <p><strong>Funcionalidades incluidas:</strong></p>
            <p>🧹 Limpieza de espacios • 📝 Normalización de texto • 🔄 Reemplazo de valores</p>
            <p>📞 Estandarización de teléfonos • 📧 Estandarización de emails • ❌ Manejo de valores faltantes</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar si hay datos cargados
    if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
        # Mostrar interfaz de limpieza
        cleaned_df = create_data_cleaning_interface(st.session_state.uploaded_data)
        
        # Mostrar vista previa de datos limpiados
        if st.button("👀 Ver Vista Previa de Datos Limpiados"):
            st.subheader("📊 Vista Previa de Datos Limpiados")
            st.dataframe(cleaned_df.head(20), use_container_width=True)
            
            # Estadísticas comparativas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Filas Originales", len(st.session_state.uploaded_data))
            with col2:
                st.metric("Filas Limpiadas", len(cleaned_df))
            with col3:
                st.metric("Cambios", len(st.session_state.uploaded_data) - len(cleaned_df))
    
    else:
        # Mostrar opciones para cargar datos
        st.markdown("### 📤 Cargar Datos para Limpiar")
        
        # Tabs para diferentes opciones de carga
        tab1, tab2 = st.tabs(["📁 Subir Archivo", "📊 Datasets de Ejemplo"])
        
        with tab1:
            show_upload_section()
        
        with tab2:
            show_examples_section()
    
    # Navegación
    st.markdown("---")
    st.markdown("### 🧭 Navegación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Dashboard Principal", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("📚 Nivel 1: Básico", use_container_width=True):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col3:
        if st.button("🔍 Nivel 2: Filtros", use_container_width=True):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col4:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

if __name__ == "__main__":
    main()
