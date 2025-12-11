import streamlit as st
import pandas as pd
import csv
import io
from data.sample_datasets import get_sample_datasets
from .data_cleaner import create_data_cleaning_interface

from utils.ui.icon_system import get_icon, replace_emojis

# Archivo - Obtener Nombres de Hojas Excel
def get_excel_sheet_names(uploaded_file):
    """Obtener lista de nombres de hojas de un archivo Excel"""
    try:
        # Archivo - Determinar motor según extensión del archivo
        file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
        
        if file_extension == 'xlsx':
            engine = 'openpyxl'
        elif file_extension == 'xls':
            # Archivo - Para archivos .xls antiguos, intentar con xlrd
            # Nota: xlrd 2.0+ no soporta .xls, solo .xlsx
            engine = 'xlrd'
        else:
            engine = None  # Dejar que pandas lo detecte automáticamente
        
        excel_file = pd.ExcelFile(uploaded_file, engine=engine)
        return excel_file.sheet_names
    except Exception as e:
        error_msg = str(e)
        # Error - Verificar si es error relacionado con .xls y xlrd
        if '.xls' in uploaded_file.name.lower() and 'xlrd' in error_msg.lower():
            st.error(f"Error al leer el archivo Excel: {error_msg}")
            st.warning("⚠️ **Nota importante:** Los archivos .xls (formato antiguo de Excel) tienen soporte limitado. "
                      "Se recomienda convertir el archivo a formato .xlsx para mejor compatibilidad.")
        else:
            st.error(f"Error al leer el archivo Excel: {error_msg}")
        return []

# Archivo - Cargar Excel con Seleccion de Hoja
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
        # Datos - Obtener lista de hojas
        sheet_names = get_excel_sheet_names(uploaded_file)
        
        if not sheet_names:
            st.error("No se pudieron leer las hojas del archivo Excel.")
            return None
        
        # Archivo - Determinar motor según extensión del archivo
        file_extension = uploaded_file.name.lower().split('.')[-1] if uploaded_file.name else ''
        
        if file_extension == 'xlsx':
            engine = 'openpyxl'
        elif file_extension == 'xls':
            engine = 'xlrd'
        else:
            engine = None  # Dejar que pandas lo detecte automáticamente
        
        # UI - Si hay múltiples hojas, mostrar selector
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
            # Archivo - Solo una hoja, cargar directamente
            df = pd.read_excel(uploaded_file, sheet_name=sheet_names[0], engine=engine)
        
        return df
    except Exception as e:
        error_msg = str(e)
        # Error - Verificar si es error relacionado con .xls y xlrd
        if '.xls' in uploaded_file.name.lower() and ('xlrd' in error_msg.lower() or 'xls' in error_msg.lower()):
            st.error(f"Error al cargar el archivo Excel: {error_msg}")
            st.warning("⚠️ **Nota importante:** Los archivos .xls (formato antiguo de Excel) tienen soporte limitado. "
                      "Se recomienda convertir el archivo a formato .xlsx para mejor compatibilidad. "
                      "Puedes abrir el archivo en Excel y guardarlo como .xlsx.")
        else:
            st.error(f"Error al cargar el archivo Excel: {error_msg}")
        return None

# Archivo - Detectar Delimitador CSV
def detect_csv_delimiter(uploaded_file, sample_size=1024):
    """
    Detectar automáticamente el delimitador de un archivo CSV.
    
    Args:
        uploaded_file: Archivo subido por el usuario
        sample_size: Tamaño de la muestra en bytes para analizar
    
    Returns:
        Delimitador detectado (str) o None si no se puede detectar
    """
    try:
        # Archivo - Guardar posición actual
        current_pos = uploaded_file.tell()
        
        # Archivo - Leer muestra del archivo
        uploaded_file.seek(0)
        sample_bytes = uploaded_file.read(sample_size)
        
        # Archivo - Intentar decodificar con diferentes codificaciones
        sample = None
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                sample = sample_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if sample is None:
            uploaded_file.seek(current_pos)
            return None
        
        # Archivo - Resetear posición del archivo
        uploaded_file.seek(0)
        
        # Datos - Usar csv.Sniffer para detectar delimitador
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample, delimiters=',;\t|').delimiter
        return delimiter
    except Exception as e:
        # Error - Si falla la detección, intentar resetear y retornar None
        try:
            uploaded_file.seek(0)
        except:
            pass
        return None

# Archivo - Cargar CSV con Seleccion de Delimitador
def load_csv_with_delimiter_selection(uploaded_file, key_prefix="csv_delimiter"):
    """
    Cargar archivo CSV con soporte para selección de delimitador.
    Detecta automáticamente el delimitador y permite cambiarlo si es necesario.
    
    Args:
        uploaded_file: Archivo subido por el usuario
        key_prefix: Prefijo para la clave única del selector de delimitador
    
    Returns:
        DataFrame con los datos del CSV
    """
    try:
        # Datos - Delimitadores comunes disponibles
        delimiter_options = {
            'Coma (,)': ',',
            'Punto y coma (;)': ';',
            'Tabulador (\\t)': '\t',
            'Pipe (|)': '|',
            'Espacio': ' '
        }
        
        # Archivo - Detectar delimitador automáticamente
        detected_delimiter = detect_csv_delimiter(uploaded_file)
        
        # UI - Mostrar información sobre delimitador detectado
        if detected_delimiter:
            # Datos - Encontrar nombre del delimitador detectado
            detected_name = None
            for name, delim in delimiter_options.items():
                if delim == detected_delimiter:
                    detected_name = name
                    break
            
            if detected_name:
                st.info(f"🔍 Delimitador detectado automáticamente: **{detected_name}** (`{repr(detected_delimiter)}`)")
            else:
                st.info(f"🔍 Delimitador detectado automáticamente: `{repr(detected_delimiter)}`")
        else:
            st.warning("⚠️ No se pudo detectar automáticamente el delimitador. Por favor, selecciona uno manualmente.")
        
        # UI - Mostrar selector de delimitador
        delimiter_labels = list(delimiter_options.keys())
        
        # Datos - Si se detectó delimitador, usarlo como valor por defecto
        default_index = 0
        if detected_delimiter:
            for i, (name, delim) in enumerate(delimiter_options.items()):
                if delim == detected_delimiter:
                    default_index = i
                    break
        
        selected_delimiter_label = st.selectbox(
            "Selecciona el delimitador:",
            delimiter_labels,
            index=default_index,
            key=f"{key_prefix}_{uploaded_file.name}",
            help="Si el delimitador detectado no es correcto, puedes seleccionar otro de la lista."
        )
        
        selected_delimiter = delimiter_options[selected_delimiter_label]
        
        # Archivo - Cargar CSV con delimitador seleccionado
        uploaded_file.seek(0)  # Asegurar que el archivo esté al inicio
        
        # Archivo - Intentar cargar con diferentes codificaciones
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        encoding_used = None
        
        for encoding in encodings:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, delimiter=selected_delimiter, encoding=encoding)
                encoding_used = encoding
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        
        if df is None:
            raise Exception("No se pudo cargar el archivo CSV. Verifica la codificación y el delimitador.")
        
        if detected_delimiter and selected_delimiter != detected_delimiter:
            st.success(f"✅ Archivo CSV cargado con delimitador: **{selected_delimiter_label}**")
        elif detected_delimiter:
            st.success(f"✅ Archivo CSV cargado exitosamente (usando delimitador detectado)")
        else:
            st.success(f"✅ Archivo CSV cargado con delimitador: **{selected_delimiter_label}**")
        
        return df
    except Exception as e:
        error_msg = str(e)
        st.error(f"Error al cargar el archivo CSV: {error_msg}")
        st.warning("💡 **Sugerencia:** Verifica que el delimitador seleccionado sea correcto. Puedes intentar con otro delimitador de la lista.")
        return None

# UI - Mostrar Seccion de Carga de Archivos
def show_upload_section():
    """Show the file upload section"""
    st.markdown("---")
    st.markdown(replace_emojis("### 📤 Subir tus Propios Datos"), unsafe_allow_html=True)
    
    # UI - Mostrar Info de Datos Actuales si Existen
    if 'uploaded_data' in st.session_state and st.session_state.uploaded_data is not None:
        st.markdown(f"{get_icon("📊", 20)} Datos actuales: {len(st.session_state.uploaded_data)} filas, {len(st.session_state.uploaded_data.columns)} columnas", unsafe_allow_html=True)
        if st.button("⬅️ Volver a Datos Actuales", type="secondary"):
            st.rerun()
        st.markdown("---")
    
    # UI - st.file_uploader no renderiza HTML, usar emoji directamente
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para comenzar tu análisis"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = load_csv_with_delimiter_selection(uploaded_file, key_prefix="upload_section")
                if df is None:
                    return
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
    
    # UI - Mostrar Boton de Volver
    if st.button("⬅️ Volver", key="back_from_upload"):
        st.session_state.show_upload_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

# UI - Mostrar Seccion de Datasets de Ejemplo
def show_examples_section():
    """Show the sample datasets section"""
    st.markdown("---")
    st.markdown(replace_emojis("### 📊 Datasets de Ejemplo"), unsafe_allow_html=True)
    st.markdown("Elige un dataset para practicar:")
    
    sample_datasets = get_sample_datasets()
    
    # UI - Mostrar Datasets de Ejemplo en Grid
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
    
    # UI - Mostrar Boton de Volver
    if st.button("⬅️ Volver", key="back_from_examples"):
        st.session_state.show_examples_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

# Consulta - Obtener Datos Actuales
def get_current_data():
    """Get the current data from session state"""
    if 'cleaned_data' in st.session_state:
        return st.session_state.cleaned_data
    elif 'sample_data' in st.session_state:
        return st.session_state.sample_data
    else:
        return None
