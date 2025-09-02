import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from utils.gif_utils import display_level_gif

# Page config
st.set_page_config(
    page_title="Nivel 1: Básico - Preparación de Datos",
    page_icon="📚",
    layout="wide"
)

# Custom CSS using the new boilerplate with theme-aware colors
st.markdown("""
<style>
/* ===== Global Styles ===== */
body {
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
    margin: 0;
    padding: 0;
}

/* Headings */
h1, h2, h3, h4, h5 {
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

/* Paragraphs and text */
p {
    margin-bottom: 1rem;
    color: var(--text-color);
}

/* ===== Separator Styles ===== */
.separator-thin {
    margin: 1rem 0;
    border: none;
    height: 2px;
    background: var(--text-color);
    opacity: 0.3;
    border-radius: 1px;
}

.separator-gradient {
    margin: 1rem 0;
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--text-color), transparent);
    opacity: 0.3;
    border-radius: 1px;
}

.separator-colorful {
    margin: 1rem 0;
    border: none;
    height: 3px;
    background: linear-gradient(90deg, #ff6b6b, #4facfe);
    border-radius: 2px;
}

.separator-dotted {
    margin: 1rem 0;
    border: none;
    height: 2px;
    background: repeating-linear-gradient(
        90deg,
        var(--text-color) 0px,
        var(--text-color) 4px,
        transparent 4px,
        transparent 12px
    );
    opacity: 0.3;
    border-radius: 1px;
}

/* ===== Containers ===== */
.section {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 10px;
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.2);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Cards */
.card {
    border-radius: 12px;
    padding: 1rem;
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.2);
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Lists */
ul, ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}

li {
    color: var(--text-color);
}

/* Emojis inline with text */
.emoji {
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
    h1 {
        font-size: 1.75rem;
    }
    h2 {
        font-size: 1.5rem;
    }
    .section {
        padding: 1rem;
    }
}

/* Custom progress bar styling */
.progress-container {
    background-color: rgba(128, 128, 128, 0.1);
    border: 1px solid rgba(128, 128, 128, 0.3);
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}

/* Step cards */
.step-card {
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.step-card h3,
.step-card h4,
.step-card p,
.step-card ul,
.step-card ol,
.step-card li {
    color: var(--text-color) !important;
}

.step-number {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-bottom: 1rem;
}

/* Info boxes */
.info-box {
    background-color: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.info-box h3,
.info-box p,
.info-box ul,
.info-box ol,
.info-box li {
    color: var(--text-color) !important;
}

.warning-box {
    background-color: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.warning-box h3,
.warning-box p,
.warning-box ul,
.warning-box ol,
.warning-box li {
    color: var(--text-color) !important;
}

.success-box {
    background-color: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.success-box h3,
.success-box p,
.success-box ul,
.success-box ol,
.success-box li {
    color: var(--text-color) !important;
}

/* Ensure all text in cards is readable */
.card h3,
.card p,
.card ul,
.card ol,
.card li {
    color: var(--text-color) !important;
}

/* Dark mode specific adjustments */
@media (prefers-color-scheme: dark) {
    .step-card,
    .card,
    .section {
        background-color: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .progress-container {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
    }
}

/* Light mode specific adjustments */
@media (prefers-color-scheme: light) {
    .step-card,
    .card,
    .section {
        background-color: rgba(0, 0, 0, 0.05);
        border-color: rgba(0, 0, 0, 0.2);
    }
    
    .progress-container {
        background-color: rgba(0, 0, 0, 0.1);
        border-color: rgba(0, 0, 0, 0.3);
    }
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

def create_step_card(step_number, title, description, sections=None):
    """Create a step card with proper HTML structure"""
    html_content = f"""
    <div class="step-card">
        <div class="step-number">{step_number}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    """
    
    if sections:
        for section_title, items in sections.items():
            html_content += f"<h4>{section_title}</h4>"
            if isinstance(items, list):
                html_content += "<ul>"
                for item in items:
                    html_content += f"<li>{item}</li>"
                html_content += "</ul>"
            else:
                html_content += f"<ol>"
                for i, item in enumerate(items, 1):
                    html_content += f"<li>{item}</li>"
                html_content += "</ol>"
    
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)

def create_info_box(box_type, title, content):
    """Create info boxes with different styles"""
    html_content = f"""
    <div class="{box_type}">
        <h3>{title}</h3>
        {content}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def main():
    # 1. Title (level name and description)
    st.title("📚 Nivel 1: Básico")
    st.subheader("Preparación y Carga de Datos")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress()
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/4 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Introduction Section (what the user will learn)
    st.header("🎯 ¿Qué aprenderás en este nivel?")
    st.markdown("""
    En este nivel aprenderás los pasos básicos para preparar y cargar datos en herramientas de análisis. 
    Es el primer paso fundamental para cualquier análisis de datos.
    """)
    
    # 4. Steps Section (clear, actionable instructions)
    st.header("📋 Pasos para Preparar y Cargar Datos")
    
    # Step 1
    create_step_card(
        step_number="1",
        title="Preparar tu archivo de datos",
        description="<strong>¿Por qué es importante?</strong> Los datos bien organizados son más fáciles de analizar y te dan resultados más confiables.",
        sections={
            "📁 Formatos recomendados:": [
                "<strong>CSV</strong> - Para datos simples en tablas",
                "<strong>Excel (.xlsx)</strong> - Para datos con formato y múltiples hojas"
            ],
            "✅ Consejos para organizar datos:": [
                "Cada columna debe tener un título claro",
                "Los datos deben estar en filas y columnas ordenadas",
                "Evita celdas vacías o datos mezclados"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="2",
        title="Cargar el archivo en la herramienta",
        description="<strong>¿Qué significa?</strong> Subir tu archivo de datos para que la herramienta pueda leerlo y analizarlo.",
        sections={
            "🔧 Proceso de carga:": {
                "Haz clic en 'Cargar archivo' o 'Subir datos'",
                "Selecciona tu archivo desde tu computadora",
                "Espera a que se complete la carga",
                "Verifica que los datos se cargaron correctamente"
            }
        }
    )
    
    # Step 3
    create_step_card(
        step_number="3",
        title="Verificar que los datos se cargaron correctamente",
        description="<strong>¿Por qué verificar?</strong> Es importante asegurarse de que todos los datos se cargaron sin errores.",
        sections={
            "👀 Qué revisar:": [
                "¿Se ven todos los números y texto?",
                "¿Las fechas se muestran correctamente?",
                "¿No hay datos faltantes o extraños?",
                "¿El número de filas y columnas es el esperado?"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="4",
        title="Explorar la estructura básica de los datos",
        description="<strong>¿Qué es la estructura?</strong> Es cómo están organizados tus datos: qué columnas tienes, qué tipo de información contienen, y cuántos registros hay.",
        sections={
            "📊 Información básica a revisar:": [
                "<strong>Número de filas:</strong> Cuántos registros tienes",
                "<strong>Número de columnas:</strong> Qué tipos de información tienes",
                "<strong>Tipos de datos:</strong> Números, texto, fechas",
                "<strong>Valores únicos:</strong> Qué categorías o rangos tienes"
            ]
        }
    )
    
    # 5. Optional media (images, diagrams, icons)
    st.header("🎥 Demostración Visual")
    try:
        display_level_gif("nivel1", "preparacion_csv")
    except:
        st.info("📹 GIF de demostración no disponible. El proceso incluye: 1) Seleccionar archivo, 2) Hacer clic en 'Cargar', 3) Verificar la carga exitosa.")
    
    # Example section
    st.header("🎯 Ejemplo Práctico")
    
    create_info_box(
        "info-box",
        "📊 Vamos a ver un ejemplo con datos de ventas",
        "<p>Te mostraré cómo se ven los datos cuando están bien organizados y qué información puedes obtener de ellos.</p>"
    )
    
    df = create_sample_data()
    st.subheader("📁 Datos de ejemplo (Ventas de una tienda)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df.head(10), use_container_width=True)
        st.caption("Primeras 10 filas de datos")
    with col2:
        st.markdown("**📊 Información básica:**")
        st.metric("Total de registros", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Período", f"{df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')}")
    
    st.subheader("🔍 Estructura de los datos")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**📋 Columnas disponibles:**")
        for col in df.columns:
            st.markdown(f"- **{col}**: {df[col].dtype}")
    with col2:
        st.markdown("**📚 ¿Qué significa cada tipo de dato?**")
        
        st.markdown("""
        <div class="info-box">
            <p><strong>🔤 object:</strong> Texto, nombres, categorías</p>
            <p><strong>🔢 int64:</strong> Números enteros</p>
            <p><strong>📊 float64:</strong> Números decimales</p>
            <p><strong>📅 datetime64:</strong> Fechas y horas</p>
            <p><strong>✅ bool:</strong> Verdadero o Falso</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tips section
    st.header("💡 Consejos Importantes")
    
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Errores comunes a evitar:</h3>
        <ul>
            <li><strong>Datos mezclados:</strong> No mezcles texto y números en la misma columna</li>
            <li><strong>Formato de fechas:</strong> Usa un formato consistente</li>
            <li><strong>Caracteres especiales:</strong> Evita símbolos extraños</li>
            <li><strong>Datos vacíos:</strong> Es mejor dejar celdas vacías que poner "0" o "N/A"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>✅ Buenas prácticas:</h3>
        <ul>
            <li><strong>Nombres claros:</strong> Usa nombres descriptivos</li>
            <li><strong>Consistencia:</strong> Mantén el mismo formato en toda la columna</li>
            <li><strong>Organización:</strong> Agrupa información relacionada</li>
            <li><strong>Documentación:</strong> Describe cada columna</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Practice activity
    st.header("🎯 Actividad Práctica")
    st.markdown("""
    <div class="card">
        <h3>📝 Ejercicio para practicar:</h3>
        <ol>
            <li><strong>Prepara un archivo:</strong> Crea una tabla simple en Excel con información de ventas</li>
            <li><strong>Organiza los datos:</strong> Usa columnas para: Fecha, Producto, Cantidad, Precio</li>
            <li><strong>Agrega algunos datos:</strong> Incluye al menos 10 registros</li>
            <li><strong>Guarda el archivo:</strong> Como .xlsx o .csv</li>
            <li><strong>Verifica la estructura:</strong> Asegúrate de que esté ordenado</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Data upload and testing section
    st.header("📤 Prueba lo que Aprendiste")
    st.markdown("""
    <div class="info-box">
        <h3>🚀 Sube tu propio archivo de datos</h3>
        <p>Ahora puedes poner en práctica lo que aprendiste. Sube un archivo CSV o Excel para ver cómo se cargan y analizan los datos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Selecciona tu archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Formatos soportados: CSV, Excel (.xlsx, .xls)"
    )
    
    if uploaded_file is not None:
        try:
            # Load the uploaded data
            if uploaded_file.name.endswith('.csv'):
                df_uploaded = pd.read_csv(uploaded_file)
            else:
                df_uploaded = pd.read_excel(uploaded_file)
            
            # Display success message
            st.success(f"✅ Archivo cargado exitosamente: {uploaded_file.name}")
            
            # Display data overview
            st.subheader("📊 Vista General de tus Datos")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(df_uploaded.head(10), use_container_width=True)
                st.caption(f"Primeras 10 filas de {len(df_uploaded)} registros totales")
            with col2:
                st.markdown("**📊 Información básica:**")
                st.metric("Total de registros", len(df_uploaded))
                st.metric("Columnas", len(df_uploaded.columns))
                
                # Calculate data types
                numeric_cols = df_uploaded.select_dtypes(include=[np.number]).columns.tolist()
                text_cols = df_uploaded.select_dtypes(include=['object']).columns.tolist()
                date_cols = df_uploaded.select_dtypes(include=['datetime64']).columns.tolist()
                
                st.metric("Columnas numéricas", len(numeric_cols))
                st.metric("Columnas de texto", len(text_cols))
                if date_cols:
                    st.metric("Columnas de fecha", len(date_cols))
            
            # Data structure analysis
            st.subheader("🔍 Estructura de tus Datos")
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**📋 Columnas disponibles:**")
                for col in df_uploaded.columns:
                    dtype_str = str(df_uploaded[col].dtype)
                    if 'int' in dtype_str:
                        dtype_icon = "🔢"
                    elif 'float' in dtype_str:
                        dtype_icon = "📊"
                    elif 'datetime' in dtype_str:
                        dtype_icon = "📅"
                    elif 'bool' in dtype_str:
                        dtype_icon = "✅"
                    else:
                        dtype_icon = "🔤"
                    
                    st.markdown(f"- {dtype_icon} **{col}**: {dtype_str}")
            
            with col2:
                st.markdown("**📚 Análisis de calidad:**")
                
                # Check for missing values
                missing_data = df_uploaded.isnull().sum()
                total_missing = missing_data.sum()
                missing_percentage = (total_missing / (len(df_uploaded) * len(df_uploaded.columns))) * 100
                
                if total_missing == 0:
                    st.markdown("✅ **Sin datos faltantes** - Excelente calidad")
                else:
                    st.markdown(f"⚠️ **Datos faltantes**: {total_missing} valores ({missing_percentage:.1f}%)")
                
                # Check for duplicate rows
                duplicates = df_uploaded.duplicated().sum()
                if duplicates == 0:
                    st.markdown("✅ **Sin filas duplicadas** - Datos únicos")
                else:
                    st.markdown(f"⚠️ **Filas duplicadas**: {duplicates} registros")
                
                # Data range info
                if numeric_cols:
                    numeric_sample = df_uploaded[numeric_cols].iloc[0]
                    st.markdown(f"🔢 **Columnas numéricas**: {', '.join(numeric_cols[:3])}{'...' if len(numeric_cols) > 3 else ''}")
                
                if text_cols:
                    text_sample = df_uploaded[text_cols].iloc[0]
                    st.markdown(f"🔤 **Columnas de texto**: {', '.join(text_cols[:3])}{'...' if len(text_cols) > 3 else ''}")
            
            # Data preview with more details
            st.subheader("👀 Vista Detallada de tus Datos")
            
            # Show sample data with more rows
            st.markdown("**📋 Muestra de datos (primeras 15 filas):**")
            st.dataframe(df_uploaded.head(15), use_container_width=True)
            
            # Show data info
            with st.expander("🔍 Información técnica del dataset"):
                st.write("**Tipos de datos:**")
                st.write(df_uploaded.dtypes)
                
                st.write("**Estadísticas descriptivas:**")
                if numeric_cols:
                    st.write(df_uploaded[numeric_cols].describe())
                else:
                    st.info("No hay columnas numéricas para mostrar estadísticas")
                
                st.markdown("""
                <div class="info-box">
                    <h4>📊 Información General del Dataset</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a nice grid layout for the info
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="card">
                        <h5>🔢 Detalles Técnicos</h5>
                        <p><strong>Memoria utilizada:</strong> {memory_usage}</p>
                        <p><strong>Rango de índice:</strong> {index_range}</p>
                        <p><strong>Tipos de datos:</strong> {dtype_count} diferentes</p>
                    </div>
                    """.format(
                        memory_usage=f"{df_uploaded.memory_usage(deep=True).sum() / 1024:.2f} KB",
                        index_range=f"{df_uploaded.index[0]} a {df_uploaded.index[-1]}",
                        dtype_count=len(df_uploaded.dtypes.unique())
                    ), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="card">
                        <h5>📋 Resumen de Columnas</h5>
                        <p><strong>Total de columnas:</strong> {total_cols}</p>
                        <p><strong>Columnas numéricas:</strong> {numeric_count}</p>
                        <p><strong>Columnas de texto:</strong> {text_count}</p>
                        {date_cols_info}
                    </div>
                    """.format(
                        total_cols=len(df_uploaded.columns),
                        numeric_count=len(numeric_cols),
                        text_count=len(text_cols),
                        date_cols_info=f"<p><strong>Columnas de fecha:</strong> {len(date_cols)}</p>" if date_cols else ""
                    ), unsafe_allow_html=True)
                
                # Show detailed column information in a nice format
                st.markdown("""
                <div class="card">
                    <h5>📚 Detalle por Columna</h5>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a table-like display for column details
                col_details = []
                for col in df_uploaded.columns:
                    dtype_str = str(df_uploaded[col].dtype)
                    non_null_count = df_uploaded[col].count()
                    missing_count = df_uploaded[col].isnull().sum()
                    
                    if 'int' in dtype_str:
                        dtype_icon = "🔢"
                    elif 'float' in dtype_str:
                        dtype_icon = "📊"
                    elif 'datetime' in dtype_str:
                        dtype_icon = "📅"
                    elif 'bool' in dtype_str:
                        dtype_icon = "✅"
                    else:
                        dtype_icon = "🔤"
                    
                    col_details.append({
                        'columna': col,
                        'tipo': f"{dtype_icon} {dtype_str}",
                        'no_nulos': non_null_count,
                        'faltantes': missing_count
                    })
                
                # Display as a nice dataframe
                col_details_df = pd.DataFrame(col_details)
                col_details_df.columns = ['📋 Columna', '🔤 Tipo', '✅ No Nulos', '⚠️ Faltantes']
                st.dataframe(col_details_df, use_container_width=True, hide_index=True)
            
            # Congratulations message
            st.markdown("""
            <div class="success-box">
                <h3>🎉 ¡Excelente trabajo!</h3>
                <p>Has cargado y analizado exitosamente tu propio archivo de datos. Esto demuestra que has dominado los conceptos básicos del Nivel 1.</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            st.info("💡 Asegúrate de que tu archivo esté en el formato correcto y no esté corrupto.")
    
    else:
        st.info("📁 Sube un archivo CSV o Excel para ver el análisis en acción.")
    
    # 6. Navigation or next steps
    st.header("✅ Verificación del Nivel")
    nivel1_completed = st.checkbox(
        "He completado todos los pasos del Nivel 1",
        value=st.session_state.get('nivel1_completed', False),
        key='nivel1_checkbox'
    )
    
    if nivel1_completed:
        st.session_state['nivel1_completed'] = True
        
        create_info_box(
            "success-box",
            "🎉 ¡Felicidades! Has completado el Nivel 1",
            "<p>Ahora sabes cómo preparar y cargar datos correctamente. Estás listo para continuar con el siguiente nivel.</p>"
        )
        
        st.subheader("🚀 ¿Qué sigue?")
        st.markdown("En el **Nivel 2** aprenderás a organizar y filtrar la información.")
        
        if st.button("Continuar al Nivel 2", type="primary"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    # Additional resources
    create_info_box(
        "info-box",
        "📚 ¿Quieres saber más?",
        "<p>Este nivel está basado en estándares de calidad de datos y mejores prácticas. Consulta la documentación para profundizar.</p>"
    )

if __name__ == "__main__":
    main()