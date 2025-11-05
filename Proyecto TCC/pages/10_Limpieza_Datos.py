import streamlit as st
import pandas as pd
from utils.data import create_data_cleaning_interface, show_upload_section, show_examples_section
from utils.ui import auth_ui
init_sidebar = auth_ui.init_sidebar
from core.config import setup_page_config, apply_custom_css
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

@safe_main
def main():
    """Página de limpieza automática de datos"""
    # Configurar página
    setup_page_config()
    apply_custom_css()
    
    # Initialize sidebar with user info (always visible)
    init_sidebar()
    
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
        # Header with current file info and upload new file option
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 📊 Datos Actuales: {len(st.session_state.uploaded_data)} filas, {len(st.session_state.uploaded_data.columns)} columnas")
        with col2:
            if st.button("📁 Subir Nuevo Archivo", type="secondary", use_container_width=True):
                # Show confirmation dialog
                st.session_state.show_upload_new = True
                st.rerun()
        
        # Confirmation dialog for uploading new file
        if st.session_state.get('show_upload_new', False):
            st.warning("⚠️ ¿Estás seguro de que quieres subir un nuevo archivo? Se perderán los datos actuales y cualquier limpieza realizada.")
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("✅ Sí, Subir Nuevo", type="primary"):
                    # Clear current data and show upload section
                    st.session_state.uploaded_data = None
                    if 'global_replacements' in st.session_state:
                        del st.session_state.global_replacements
                    st.session_state.show_upload_new = False
                    st.rerun()
            with col2:
                if st.button("❌ Cancelar"):
                    st.session_state.show_upload_new = False
                    st.rerun()
        
        # Mostrar interfaz de limpieza
        cleaned_df = create_data_cleaning_interface(st.session_state.uploaded_data)
        
        # Always show comparison stats using the session state cleaner
        st.markdown("---")
        st.markdown("### 📊 Comparación de Datos")
        
        # Get the current cleaner from session state
        if 'data_cleaner' in st.session_state:
            cleaner = st.session_state.data_cleaner
            original_df = cleaner.original_df
            current_df = cleaner.cleaned_df
            # Debug info
            st.write(f"🔍 Debug: Original rows: {len(original_df)}, Current rows: {len(current_df)}")
            st.write(f"🔍 Debug: Original columns: {len(original_df.columns)}, Current columns: {len(current_df.columns)}")
        else:
            # Fallback to uploaded data if no cleaner in session state
            original_df = st.session_state.uploaded_data
            current_df = cleaned_df
            st.write("🔍 Debug: Using fallback data")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📈 Filas Originales", len(original_df))
        with col2:
            st.metric("🧹 Filas Limpiadas", len(current_df))
        with col3:
            rows_changed = len(original_df) - len(current_df)
            st.metric("📉 Filas Removidas", rows_changed)
        with col4:
            cols_changed = len(original_df.columns) - len(current_df.columns)
            st.metric("🗑️ Columnas Removidas", cols_changed)
        
        # Data preview and download section
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("👀 Ver Vista Previa de Datos Limpiados"):
                st.subheader("📊 Vista Previa de Datos Limpiados")
                st.dataframe(cleaned_df.head(20), use_container_width=True)
        
        with col2:
            # Download cleaned data using current state
            download_df = current_df if 'data_cleaner' in st.session_state else cleaned_df
            csv_data = download_df.to_csv(index=False)
            st.download_button(
                label="💾 Descargar Datos Limpiados",
                data=csv_data,
                file_name="datos_limpiados.csv",
                mime="text/csv",
                use_container_width=True
            )
    
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
