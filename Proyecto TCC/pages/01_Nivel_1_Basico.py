import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from gif_utils import display_level_gif

# Page config
st.set_page_config(
    page_title="Nivel 1: Básico - Preparación de Datos",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .level-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .step-box {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = len(dates)
    
    data = {
        'Fecha': np.random.choice(dates, n_records//2),
        'Categoria': np.random.choice(['Electronica', 'Ropa', 'Libros', 'Hogar'], n_records//2),
        'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n_records//2),
        'Ventas': np.random.normal(1000, 300, n_records//2).round(2),
        'Cantidad': np.random.poisson(5, n_records//2),
        'Calificacion': np.random.choice([1, 2, 3, 4, 5], n_records//2, p=[0.05, 0.1, 0.15, 0.4, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Ingresos'] = df['Ventas'] * df['Cantidad']
    
    return df.sort_values('Fecha').reset_index(drop=True)

def main():
    # Header
    st.markdown('<h1 class="level-header">📚 Nivel 1: Básico</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Preparación y Carga de Datos</h2>', unsafe_allow_html=True)
    
    # Progress indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(0.25)
        st.caption("Progreso: 25% - Nivel 1 de 4")
    
    st.divider()
    
    # Introduction
    st.markdown("""
    ## 🎯 Objetivo de este Nivel
    
    En este nivel aprenderás a:
    - Preparar tus archivos de datos correctamente
    - Cargar archivos en la herramienta
    - Verificar que los datos se cargaron correctamente
    - Explorar la estructura básica de tus datos
    """)
    
    # Step 1: File Preparation
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📋 Paso 1: Preparar tu Archivo de Datos")
    
    st.markdown("""
    ### ✅ Formato Recomendado
    
    Tu archivo debe tener:
    - **Formato**: CSV (.csv) o Excel (.xlsx)
    - **Encabezados**: Primera fila con nombres de columnas
    - **Datos**: Una fila por registro/transacción
    - **Columnas básicas**: Fecha, Categoría, Valor, etc.
    
    ### 📊 Ejemplo de Estructura Correcta:
    """)
    
    # Show example data
    example_data = create_sample_data()
    st.dataframe(example_data.head(10), use_container_width=True)
    
    st.markdown("""
    ### ⚠️ Errores Comunes a Evitar:
    - Archivos sin encabezados
    - Columnas mezcladas (texto y números en la misma columna)
    - Fechas en formatos inconsistentes
    - Valores vacíos sin manejar
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: File Upload Instructions
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📤 Paso 2: Cargar tu Archivo")
    
    st.markdown("""
    ### 🔧 Cómo Cargar:
    1. Ve a la barra lateral (izquierda)
    2. Busca la sección "Sube tu archivo de datos"
    3. Haz clic en "Browse files" o arrastra tu archivo
    4. Selecciona tu archivo CSV o Excel
    5. Espera a que se cargue (verás un mensaje de confirmación)
    
    ### 🎥 Demostración Visual:
    """)
    
    # Display GIF demonstration
    display_level_gif("nivel1", "preparacion_csv")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive Practice Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎯 Práctica: ¡Tu Turno!")
    
    st.markdown("""
    ### 📝 Instrucciones:
    1. Prepara un archivo CSV con datos similares al ejemplo
    2. Cárgalo usando el control de la barra lateral
    3. Verifica que se muestre correctamente en la tabla
    """)
    
    # Display GIF demonstration for file upload
    display_level_gif("nivel1", "carga_archivo")
    
    # File upload for practice
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo de práctica",
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para practicar"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Try to convert date columns
            for col in df.columns:
                if 'fecha' in col.lower() or 'date' in col.lower():
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except:
                        pass
            
            st.success(f"✅ ¡Excelente! Cargaste {len(df)} filas de datos")
            
            # Show data preview
            st.markdown("### 📊 Vista Previa de tus Datos:")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Data validation
            st.markdown("### 🔍 Verificación de Datos:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📈 Total de Filas", len(df))
                st.metric("📋 Total de Columnas", len(df.columns))
            
            with col2:
                st.metric("📅 Columnas de Fecha", len(df.select_dtypes(include=['datetime64']).columns))
                st.metric("🔢 Columnas Numéricas", len(df.select_dtypes(include=[np.number]).columns))
            
            # Show column types
            st.markdown("### 📋 Tipos de Columnas:")
            column_info = pd.DataFrame({
                'Columna': df.columns,
                'Tipo': df.dtypes.astype(str),
                'Valores Únicos': [df[col].nunique() for col in df.columns],
                'Valores Vacíos': [df[col].isnull().sum() for col in df.columns]
            })
            st.dataframe(column_info, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            st.markdown("""
            ### 💡 Consejos para solucionar:
            - Verifica que el archivo no esté corrupto
            - Asegúrate de que sea un CSV o Excel válido
            - Revisa que no haya caracteres especiales en los encabezados
            """)
    else:
        st.info("📤 Sube un archivo para comenzar la práctica")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Criteria
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("## ✅ Criterios de Éxito")
    
    st.markdown("""
    Has completado este nivel cuando:
    - ✅ Puedes preparar un archivo CSV/Excel con la estructura correcta
    - ✅ Cargas exitosamente un archivo en la herramienta
    - ✅ Ves tus datos en la tabla de vista previa
    - ✅ Entiendes los tipos de datos de tus columnas
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Dashboard Principal"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("⬅️ Volver al Inicio"):
            st.switch_page("Inicio.py")
    
    with col4:
        if st.button("➡️ Siguiente Nivel"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    # Tips section
    st.markdown("""
    ---
    ### 💡 Consejos Adicionales:
    - **Tamaño de archivo**: Para mejor rendimiento, usa archivos menores a 10MB
    - **Nombres de columnas**: Usa nombres descriptivos sin espacios (ej: "Fecha_Venta" en lugar de "Fecha de Venta")
    - **Formato de fechas**: Usa formatos consistentes como YYYY-MM-DD
    - **Valores vacíos**: Considera usar 0 o "N/A" en lugar de dejar celdas vacías
    """)

if __name__ == "__main__":
    main()
