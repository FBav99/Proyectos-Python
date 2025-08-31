import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.gif_utils import display_level_gif

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
    .completion-checkbox {
        background: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_level_progress():
    """Get current progress across all levels"""
    progress = {
        'nivel1': st.session_state.get('nivel1_completed', False),
        'nivel2': st.session_state.get('nivel2_completed', False),
        'nivel3': st.session_state.get('nivel3_completed', False),
        'nivel4': st.session_state.get('nivel4_completed', False)
    }
    
    completed_count = sum(progress.values())
    total_progress = (completed_count / 4) * 100
    
    return total_progress, completed_count, progress

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
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso: {total_progress:.0f}% - {completed_count} de 4 niveles completados")
        
        # Show completion status for each level
        st.markdown("**Estado de Niveles:**")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            status = "✅" if progress['nivel1'] else "⏳"
            st.markdown(f"{status} Nivel 1")
        with col_b:
            status = "✅" if progress['nivel2'] else "⏳"
            st.markdown(f"{status} Nivel 2")
        with col_c:
            status = "✅" if progress['nivel3'] else "⏳"
            st.markdown(f"{status} Nivel 3")
        with col_d:
            status = "✅" if progress['nivel4'] else "⏳"
            st.markdown(f"{status} Nivel 4")
    
    # Level Completion Checkbox - At the top
    st.markdown('<div class="completion-checkbox">', unsafe_allow_html=True)
    st.markdown("## 🎯 Marcar Nivel como Completado")
    
    # Check if this is the first time completing the level
    was_completed = st.session_state.get('nivel1_completed', False)
    
    if st.checkbox("✅ Click aquí para marcar este nivel como Completado", 
                  value=was_completed,
                  key='nivel1_completion_checkbox'):
        # Only show balloons if this is the first time completing
        if not was_completed:
            st.balloons()
            st.success("🎉 ¡Felicidades! Has completado el Nivel 1. ¡Continúa con el siguiente nivel!")
        st.session_state['nivel1_completed'] = True
    else:
        st.session_state['nivel1_completed'] = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Official Sources Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🏛️ Fuentes Oficiales")
    
    st.markdown("""
    ### 📚 Respaldos Oficiales para este Nivel:
    
    **Estándares de Calidad de Datos:**
    - **DAMA International (DMBOK)**: [Estándar internacional de gestión de datos](https://www.dama.org/cpages/body-of-knowledge)
    
    **Formatos de Datos Estándar:**
    - **RFC 4180 (CSV)**: [Formato estándar para archivos CSV](https://tools.ietf.org/html/rfc4180)
    
    **Mejores Prácticas:**
    - **Google Data Studio**: [Mejores prácticas de preparación](https://support.google.com/datastudio/answer/6283323)
    
    **Validación de Datos:**
    - **Data Quality Assessment Framework (DQAF)**: [Verificación de calidad](https://www.imf.org/external/pubs/ft/dqrs/dqrs01.pdf)
    
    ### 📖 Certificaciones Relacionadas:
    - **DAMA CDMP Foundation**: [Certificación en gestión de datos](https://www.dama.org/cpages/cdmp)
    - **Google Data Analytics Professional Certificate**: [Certificación de Google](https://www.coursera.org/professional-certificates/google-data-analytics)
    
    ### 🔗 Recursos Adicionales:
    - **DataCamp Data Cleaning**: [Curso de limpieza de datos](https://www.datacamp.com/courses/data-cleaning-with-python)
    - **OpenRefine**: [Herramienta de limpieza gratuita](https://openrefine.org/)
    - **Pandas Documentation**: [Documentación oficial](https://pandas.pydata.org/docs/)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Dashboard Principal", key="nivel1_dashboard"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("⬅️ Volver al Inicio", key="nivel1_volver"):
            st.switch_page("Inicio.py")
    
    with col4:
        if st.button("➡️ Siguiente Nivel", key="nivel1_siguiente"):
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
