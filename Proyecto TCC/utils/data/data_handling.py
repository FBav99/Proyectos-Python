import streamlit as st
import pandas as pd
from data.sample_datasets import get_sample_datasets
from .data_cleaner import create_data_cleaning_interface

from utils.ui.icon_system import get_icon, replace_emojis

def get_excel_sheet_names(uploaded_file):
    """Obtener lista de nombres de hojas de un archivo Excel"""
    try:
        # Determinar el motor según la extensión del archivo
        file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
        
        if file_extension == 'xlsx':
            engine = 'openpyxl'
        elif file_extension == 'xls':
            # Para archivos .xls antiguos, intentar con xlrd
            # Nota: xlrd 2.0+ no soporta .xls, solo .xlsx
            engine = 'xlrd'
        else:
            engine = None  # Dejar que pandas lo detecte automáticamente
        
        excel_file = pd.ExcelFile(uploaded_file, engine=engine)
        return excel_file.sheet_names
    except Exception as e:
        error_msg = str(e)
        # Verificar si es un error relacionado con .xls y xlrd
        if '.xls' in uploaded_file.name.lower() and 'xlrd' in error_msg.lower():
            st.error(f"Error al leer el archivo Excel: {error_msg}")
            st.warning("⚠️ **Nota importante:** Los archivos .xls (formato antiguo de Excel) tienen soporte limitado. "
                      "Se recomienda convertir el archivo a formato .xlsx para mejor compatibilidad.")
        else:
            st.error(f"Error al leer el archivo Excel: {error_msg}")
        return []

def load_excel_with_sheet_selection(uploaded_file, key_prefix="excel_sheet"):
    """
    Cargar archivo Excel con soporte para selección de hoja cuando hay múltiples hojas.
    
    Args:
        uploaded_file: Archivo subido por el usuario
        key_prefix: Prefijo para la clave única del selector de hoja
    
    Returns:
        DataFrame con los datos de la hoja seleccionada
    """
    try:
        # Obtener lista de hojas
        sheet_names = get_excel_sheet_names(uploaded_file)
        
        if not sheet_names:
            st.error("No se pudieron leer las hojas del archivo Excel.")
            return None
        
        # Determinar el motor según la extensión del archivo
        file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
        
        if file_extension == 'xlsx':
            engine = 'openpyxl'
        elif file_extension == 'xls':
            engine = 'xlrd'
        else:
            engine = None  # Dejar que pandas lo detecte automáticamente
        
        # Si hay múltiples hojas, mostrar selector
        if len(sheet_names) > 1:
            st.info(f"📑 Este archivo Excel contiene {len(sheet_names)} hojas. Selecciona la hoja que deseas cargar:")
            selected_sheet = st.selectbox(
                "Selecciona la hoja:",
                sheet_names,
                key=f"{key_prefix}_{uploaded_file.name}",
                help="Por defecto se carga la primera hoja, pero puedes seleccionar cualquier otra."
            )
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, engine=engine)
            st.success(f"✅ Hoja '{selected_sheet}' cargada exitosamente")
        else:
            # Solo una hoja, cargar directamente
            df = pd.read_excel(uploaded_file, sheet_name=sheet_names[0], engine=engine)
        
        return df
    except Exception as e:
        error_msg = str(e)
        # Verificar si es un error relacionado con .xls y xlrd
        if '.xls' in uploaded_file.name.lower() and ('xlrd' in error_msg.lower() or 'xls' in error_msg.lower()):
            st.error(f"Error al cargar el archivo Excel: {error_msg}")
            st.warning("⚠️ **Nota importante:** Los archivos .xls (formato antiguo de Excel) tienen soporte limitado. "
                      "Se recomienda convertir el archivo a formato .xlsx para mejor compatibilidad. "
                      "Puedes abrir el archivo en Excel y guardarlo como .xlsx.")
        else:
            st.error(f"Error al cargar el archivo Excel: {error_msg}")
        return None
def show_upload_section():
    """Show the file upload section"""
    st.markdown("---")
    st.markdown(replace_emojis("### 📤 Subir tus Propios Datos"), unsafe_allow_html=True)
    
    # Show current data info if exists
    if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
        st.markdown(f"{get_icon("📊", 20)} Datos actuales: {len(st.session_state.uploaded_data)} filas, {len(st.session_state.uploaded_data.columns)} columnas", unsafe_allow_html=True)
        if st.button("⬅️ Volver a Datos Actuales", type="secondary"):
            st.rerun()
        st.markdown("---")
    
    uploaded_file = st.file_uploader(
        replace_emojis("📁 Sube tu archivo de datos"),
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para comenzar tu análisis"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = load_excel_with_sheet_selection(uploaded_file, key_prefix="upload_section")
                if df is None:
                    return
            
            st.markdown(f"{get_icon("✅", 20)} Archivo cargado exitosamente: {uploaded_file.name}", unsafe_allow_html=True)
            st.markdown(f"{get_icon("📊", 20)} {len(df)} filas, {len(df.columns)} columnas", unsafe_allow_html=True)
            
            # Show data preview
            with st.expander("👀 Vista previa de datos"):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Action buttons for loaded data
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🧹 Analizar Calidad de Datos", type="primary", use_container_width=True):
                    st.session_state.uploaded_data = df
                    st.session_state.current_data_name = uploaded_file.name
                    st.session_state.current_data_type = "uploaded_file"
                    st.session_state.show_data_quality = True
                    st.rerun()
            
            with col2:
                if st.button("🧽 Limpieza Automática", use_container_width=True):
                    st.session_state.uploaded_data = df
                    st.session_state.current_data_name = uploaded_file.name
                    st.session_state.current_data_type = "uploaded_file"
                    st.session_state.show_data_cleaning = True
                    st.rerun()
            
            with col3:
                if st.button("🚀 Ir Directo al Dashboard", use_container_width=True):
                    st.session_state.cleaned_data = df
                    st.session_state.current_data_name = uploaded_file.name
                    st.session_state.current_data_type = "uploaded_file"
                    st.session_state.data_quality_completed = True
                    st.session_state.show_dashboard = True
                    st.rerun()
                    
        except Exception as e:
            st.markdown(f"{get_icon("❌", 20)} Error al cargar el archivo: {str(e)}", unsafe_allow_html=True)
    
    # Back button
    if st.button("⬅️ Volver", key="back_from_upload"):
        st.session_state.show_upload_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

def show_examples_section():
    """Show the sample datasets section"""
    st.markdown("---")
    st.markdown(replace_emojis("### 📊 Datasets de Ejemplo"), unsafe_allow_html=True)
    st.markdown("Elige un dataset para practicar:")
    
    sample_datasets = get_sample_datasets()
    
    # Display sample datasets in a clean grid
    cols = st.columns(2)
    for i, (name, info) in enumerate(sample_datasets.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #007bff; margin-bottom: 0.5rem;">📊 {name}</h4>
                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Dificultad:</strong> {info['difficulty']}</p>
                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📥 Usar {name}", key=f"sample_{name}", use_container_width=True):
                    dataset_df = info['data']
                    # Set as sample_data for dashboard compatibility
                    st.session_state.sample_data = dataset_df
                    # Also set as uploaded_data for data cleaning page compatibility
                    st.session_state.uploaded_data = dataset_df
                    # Store dataset name and type
                    st.session_state.current_data_name = name
                    st.session_state.current_data_type = "sample_dataset"
                    st.session_state.data_quality_completed = True
                    st.session_state.show_dashboard = True
                    st.success(f"¡Dataset {name} cargado exitosamente!")
                    st.rerun()
    
    # Back button
    if st.button("⬅️ Volver", key="back_from_examples"):
        st.session_state.show_examples_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

def get_current_data():
    """Get the current data from session state"""
    if 'cleaned_data' in st.session_state:
        return st.session_state.cleaned_data
    elif 'sample_data' in st.session_state:
        return st.session_state.sample_data
    else:
        return None
