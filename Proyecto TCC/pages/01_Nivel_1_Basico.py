import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data, analyze_uploaded_data
from utils.learning.learning_progress import save_level_progress

# Page config
st.set_page_config(
    page_title="Nivel 1: Básico - Preparación de Datos",
    page_icon="📚",
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Helper functions are now imported from utils.level_components and utils.level_data

def main():
    # Check if user is authenticated
    if 'user' not in st.session_state or not st.session_state.get('authenticated'):
        st.error("🔐 Por favor inicia sesión para acceder a este nivel.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Get current user
    user = st.session_state.get('user')
    if not user or 'id' not in user:
        st.error("❌ Error: No se pudo obtener la información del usuario.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Title (level name and description)
    st.title("📚 Nivel 1: Básico")
    st.subheader("Preparación y Carga de Datos")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
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
                
                # Calculate data types using utility function
                analysis = analyze_uploaded_data(df_uploaded)
                numeric_cols = analysis['numeric_cols']
                text_cols = analysis['text_cols']
                date_cols = analysis['date_cols']
                
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
                
                # Check for missing values and duplicates using utility function
                if analysis['total_missing'] == 0:
                    st.markdown("✅ **Sin datos faltantes** - Excelente calidad")
                else:
                    st.markdown(f"⚠️ **Datos faltantes**: {analysis['total_missing']} valores ({analysis['missing_percentage']:.1f}%)")
                
                if analysis['duplicates'] == 0:
                    st.markdown("✅ **Sin filas duplicadas** - Datos únicos")
                else:
                    st.markdown(f"⚠️ **Filas duplicadas**: {analysis['duplicates']} registros")
                
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
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel1', True):
            st.session_state['nivel1_completed'] = True
        else:
            st.error("❌ Error al guardar el progreso. Intenta de nuevo.")
            return
        
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