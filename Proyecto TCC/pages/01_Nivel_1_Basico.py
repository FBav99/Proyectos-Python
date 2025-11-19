import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data, analyze_uploaded_data
from utils.learning.learning_progress import save_level_progress
from utils.learning.level_components import create_progression_summary, create_level_preview, create_data_quality_insight, create_achievement_display
from utils.learning.level_data import get_data_progression_info
from utils.ui import auth_ui
from utils.ui.icon_system import get_icon, replace_emojis
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Nivel 1: Básico - Preparación de Datos",
    page_icon=get_icon("📚", 20),
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Helper functions are now imported from utils.level_components and utils.level_data

@safe_main
def main():
    # Initialize sidebar with user info (always visible)
    current_user = init_sidebar()
    
    # Check if user is authenticated
    if not current_user:
        st.markdown(replace_emojis("🔐 Por favor inicia sesión para acceder a este nivel."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Get current user
    user = current_user
    if not user or 'id' not in user:
        st.markdown(replace_emojis("❌ Error: No se pudo obtener la información del usuario."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Verificar que el nivel anterior esté completado
    if not progress.get('nivel0', False):
        st.warning("⚠️ Primero debes completar el Nivel 0 (Introducción) antes de continuar con este nivel.")
        if st.button("Ir al Nivel 0", type="primary"):
            st.switch_page("pages/00_Nivel_0_Introduccion.py")
        return
    
    # 3. Progression Summary
    create_progression_summary(progress)
    
    # 4. Show achievement for previous level if completed
    if progress.get('nivel0', False):
        create_achievement_display('nivel0', progress)
    
    # 5. Level Preview
    create_level_preview('nivel1')
    
    # 6. Introduction Section (what the user will learn)
    st.header(replace_emojis("🎯 ¿Qué aprenderás en este nivel?"))
    st.markdown("Ahora que ya entiendes **qué son los datos** y **cómo se organizan** (como aprendiste en el Nivel 0), en este nivel aprenderás los pasos prácticos para preparar y cargar datos correctamente en herramientas de análisis. Es el primer paso técnico para trabajar con datos reales.")
    
    # Add connection to previous level
    create_info_box(
        "info-box",
        "🔗 Conectando con el Nivel 0",
        "<p>En el nivel anterior aprendiste que los datos se organizan en tablas con <strong>filas</strong> (registros) y <strong>columnas</strong> (tipos de información). Ahora vamos a ver cómo preparar esos datos para que estén listos para analizar.</p>"
    )
    
    # 7. Steps Section (clear, actionable instructions)
    st.header(replace_emojis("📋 Pasos para Preparar y Cargar Datos"))
    
    # Step 1
    create_step_card(
        step_number="1.1",
        title="Elegir el formato correcto para tus datos",
        description="<strong>¿Por qué es importante el formato?</strong> El formato correcto asegura que tus datos se carguen sin errores y sean fáciles de trabajar.",
        sections={
            replace_emojis("📁 Formatos recomendados:"): [
                "<strong>CSV (.csv)</strong> - Para datos simples, se abre en cualquier programa",
                "<strong>Excel (.xlsx)</strong> - Para datos con formato, colores y múltiples hojas",
                "<strong>JSON (.json)</strong> - Para datos estructurados complejos"
            ],
            replace_emojis("🔧 Cómo elegir el formato:"): [
                "<strong>Usa CSV si:</strong> Tienes datos simples en tabla, quieres compatibilidad máxima",
                "<strong>Usa Excel si:</strong> Tienes formato, colores, o múltiples hojas de datos",
                "<strong>Usa JSON si:</strong> Tienes datos anidados o estructuras complejas"
            ],
            "⚠️ Formatos a evitar:": [
                "<strong>PDF:</strong> No se puede analizar directamente",
                "<strong>Imágenes:</strong> Necesitan procesamiento especial",
                "<strong>Word:</strong> No está diseñado para datos tabulares"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="1.2",
        title="Preparar la estructura de datos correctamente",
        description="<strong>¿Por qué es importante la estructura?</strong> Una estructura bien organizada hace que el análisis sea más fácil y preciso.",
        sections={
            replace_emojis("📋 Reglas para organizar datos:"): [
                "<strong>Una fila = un registro:</strong> Cada fila debe representar una sola cosa (una venta, un cliente, un producto)",
                "<strong>Una columna = un tipo de información:</strong> Cada columna debe tener el mismo tipo de dato",
                "<strong>Encabezados claros:</strong> Usa nombres descriptivos para las columnas",
                "<strong>Sin filas vacías:</strong> Evita filas completamente vacías en el medio de los datos"
            ],
            replace_emojis("✅ Ejemplo de estructura correcta:"): [
                "| Fecha | Producto | Cantidad | Precio |",
                "|-------|----------|----------|--------|",
                "| 15/03 | Laptop   | 1        | 800    |",
                "| 15/03 | Mouse    | 2        | 25     |"
            ],
            replace_emojis("❌ Ejemplo de estructura incorrecta:"): [
                "| Fecha | Producto | Cantidad | Precio |",
                "|-------|----------|----------|--------|",
                "| 15/03 | Laptop   | 1        | 800    |",
                "|       |          |          |        | ← Fila vacía",
                "| 15/03 | Mouse    | 2        | 25     |"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="1.3",
        title="Cargar el archivo en la herramienta",
        description="<strong>¿Cómo cargar datos?</strong> Una vez que tienes tu archivo preparado, necesitas subirlo a la herramienta de análisis.",
        sections={
            replace_emojis("🔧 Proceso de carga paso a paso:"): [
                "<strong>1. Localiza el botón de carga:</strong> Busca 'Cargar archivo', 'Subir datos' o 'Importar'",
                "<strong>2. Selecciona tu archivo:</strong> Navega hasta donde guardaste tu archivo",
                "<strong>3. Confirma la carga:</strong> Haz clic en 'Abrir' o 'Subir'",
                "<strong>4. Espera la confirmación:</strong> La herramienta te dirá si la carga fue exitosa"
            ],
            replace_emojis("📁 Tipos de carga disponibles:"): [
                "<strong>Arrastrar y soltar:</strong> Arrastra el archivo directamente a la zona de carga",
                "<strong>Explorador de archivos:</strong> Haz clic en 'Examinar' y selecciona el archivo",
                "<strong>URL o enlace:</strong> Si tienes un enlace a los datos en internet"
            ],
            "⚠️ Problemas comunes al cargar:": [
                "<strong>Archivo muy grande:</strong> Algunas herramientas tienen límites de tamaño",
                "<strong>Formato no soportado:</strong> Verifica que el formato sea compatible",
                "<strong>Archivo corrupto:</strong> Intenta abrirlo en otro programa primero"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="1.4",
        title="Verificar que los datos se cargaron correctamente",
        description="<strong>¿Por qué verificar?</strong> Es crucial asegurarse de que todos los datos se cargaron sin errores antes de continuar con el análisis.",
        sections={
            "👀 Checklist de verificación:": [
                "<strong>¿Se ven todos los datos?</strong> Revisa que no falten números o texto",
                "<strong>¿Las fechas se ven correctas?</strong> Verifica que el formato de fechas sea el esperado",
                "<strong>¿No hay datos extraños?</strong> Busca símbolos raros, errores de tipeo, o valores imposibles",
                "<strong>¿El conteo es correcto?</strong> Confirma que el número de filas y columnas sea el esperado"
            ],
            replace_emojis("🔍 Qué buscar específicamente:"): [
                "<strong>Datos faltantes:</strong> Celdas vacías donde no debería haberlas",
                "<strong>Formato incorrecto:</strong> Números que se ven como texto, fechas mal formateadas",
                "<strong>Datos duplicados:</strong> Filas que aparecen más de una vez",
                "<strong>Valores atípicos:</strong> Números que parecen demasiado grandes o pequeños"
            ],
            replace_emojis("✅ Señales de que todo está bien:"): [
                "Los números se ven como números (alineados a la derecha)",
                "Las fechas tienen un formato consistente",
                "No hay celdas con errores (#N/A, #ERROR, etc.)",
                "El número total de registros coincide con lo esperado"
            ]
        }
    )
    
    # Step 5
    create_step_card(
        step_number="1.5",
        title="Entender la estructura de tus datos cargados",
        description="<strong>¿Por qué es importante?</strong> Conocer la estructura te ayuda a entender qué puedes hacer con los datos y cómo organizarlos para el análisis.",
        sections={
            replace_emojis("📊 Información básica a revisar:"): [
                "<strong>Número de filas:</strong> Cuántos registros tienes en total",
                "<strong>Número de columnas:</strong> Qué tipos de información tienes disponibles",
                "<strong>Tipos de datos:</strong> Qué columnas son números, texto, fechas, etc.",
                "<strong>Valores únicos:</strong> Cuántas categorías diferentes tienes en cada columna"
            ],
            replace_emojis("🔍 Cómo interpretar la información:"): [
                "<strong>Filas:</strong> Cada fila representa un evento, transacción, o registro individual",
                "<strong>Columnas:</strong> Cada columna representa una característica o medida",
                "<strong>Tipos de datos:</strong> Te dicen qué operaciones puedes hacer (sumar números, contar categorías)",
                "<strong>Valores únicos:</strong> Te muestran la diversidad de tus datos"
            ],
            replace_emojis("💡 Preguntas útiles para hacerte:"): [
                "¿Tengo suficientes datos para hacer análisis confiables?",
                "¿Qué columnas contienen la información más importante?",
                "¿Hay columnas que no necesito para mi análisis?",
                "¿Los tipos de datos son correctos para lo que quiero hacer?"
            ]
        }
    )
    
    # 5. Optional media (images, diagrams, icons)
    st.header(replace_emojis("🎥 Demostración Visual"))
    try:
        display_level_gif("nivel1", "preparacion_csv")
    except:
        st.info("📹 GIF de demostración no disponible. El proceso incluye: 1) Seleccionar archivo, 2) Hacer clic en 'Cargar', 3) Verificar la carga exitosa.")
    
    # Example section
    st.header(replace_emojis("🎯 Ejemplo Práctico"))
    
    create_info_box(
        "info-box",
        replace_emojis("📊 Vamos a practicar la preparación y carga de datos"),
        "<p>Te mostraré cómo preparar datos correctamente y qué verificar después de cargarlos.</p>"
    )
    
    # Show data quality insight for this level
    create_data_quality_insight('nivel1', 'dirty')
    
    df = create_sample_data('dirty')  # Use dirty data for Level 1
    st.subheader(replace_emojis("📁 Datos de ejemplo (Ventas de TechStore - Datos sin procesar)"))
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df.head(10), use_container_width=True)
        st.caption("Primeras 10 filas de datos")
    with col2:
        st.markdown(replace_emojis("**📊 Información básica:**"), unsafe_allow_html=True)
        st.metric("Total de registros", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Período", f"{df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')}")
    
    st.subheader(replace_emojis("🔍 Estructura de los datos"))
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(replace_emojis("**📋 Columnas disponibles:**"), unsafe_allow_html=True)
        for col in df.columns:
            st.markdown(f"- **{col}**: {df[col].dtype}")
    with col2:
        st.markdown(replace_emojis("**📚 ¿Qué significa cada tipo de dato?**"), unsafe_allow_html=True)
        
        with st.container():
            st.markdown(replace_emojis("**🔤 object:** Texto, nombres, categorías"), unsafe_allow_html=True)
            st.markdown(replace_emojis("**🔢 int64:** Números enteros"), unsafe_allow_html=True)
            st.markdown(replace_emojis("**📊 float64:** Números decimales"), unsafe_allow_html=True)
            st.markdown(replace_emojis("**📅 datetime64:** Fechas y horas"), unsafe_allow_html=True)
            st.markdown(replace_emojis("**✅ bool:** Verdadero o Falso"), unsafe_allow_html=True)
    
    # Show dirty vs clean data comparison
    st.subheader(replace_emojis("🔄 Comparación: Datos Sin Procesar vs Datos Limpios"))
    
    create_info_box(
        "info-box",
        replace_emojis("📚 ¿Por qué es importante ver ambos tipos?"),
        "<p>En el <strong>Nivel 0</strong> viste datos organizados y limpios. En la vida real, los datos raramente vienen así. En este nivel aprenderás a identificar y solucionar estos problemas para que los datos estén listos para el análisis.</p>"
    )
    
    create_info_box(
        "warning-box",
        "⚠️ Problemas en los datos sin procesar",
        "<p>Observa los problemas que pueden tener los datos reales y cómo afectan el análisis.</p>"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(replace_emojis("**📊 Datos Sin Procesar (Actual):**"))
        st.dataframe(df.head(8), use_container_width=True)
        
        # Show data quality issues
        st.markdown(replace_emojis("**🔍 Problemas identificados:**"), unsafe_allow_html=True)
        issues = []
        if df['Categoria'].isnull().any():
            issues.append(replace_emojis("❌ Valores faltantes en Categoría"))
        if df.duplicated().any():
            issues.append(replace_emojis("❌ Filas duplicadas"))
        if df['Calificacion'].max() > 5 or df['Calificacion'].min() < 1:
            issues.append(replace_emojis("❌ Calificaciones fuera del rango 1-5"))
        if df['Ventas'].max() > df['Ventas'].quantile(0.95) * 5:
            issues.append(replace_emojis("❌ Valores atípicos en Ventas"))
        
        for issue in issues:
            st.markdown(f"- {issue}")
    
    with col2:
        st.markdown("**✨ Datos Después de Limpiar:**")
        df_clean = create_sample_data('clean')
        st.dataframe(df_clean.head(8), use_container_width=True)
        
        # Show improvements
        st.markdown(replace_emojis("**✅ Mejoras aplicadas:**"), unsafe_allow_html=True)
        improvements = [
            replace_emojis("✅ Valores faltantes eliminados"),
            replace_emojis("✅ Duplicados removidos"), 
            replace_emojis("✅ Calificaciones normalizadas (1-5)"),
            replace_emojis("✅ Valores atípicos corregidos"),
            replace_emojis("✅ Formatos consistentes")
        ]
        
        for improvement in improvements:
            st.markdown(f"- {improvement}")
    
    # Show the impact
    st.markdown(replace_emojis("**📈 Impacto de la limpieza:**"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Registros originales", len(df))
        st.metric("Registros limpios", len(df_clean))
    
    with col2:
        st.metric("Datos faltantes", df.isnull().sum().sum())
        st.metric("Duplicados", df.duplicated().sum())
    
    with col3:
        st.metric("Calidad general", "75%", "25%")
        st.metric("Calidad mejorada", "95%", "20%")
    
    # Tips section
    st.header(replace_emojis("💡 Consejos Importantes"))
    
    with st.container():
        st.markdown("### ⚠️ Errores comunes al preparar datos:")
        st.markdown("- **Formato incorrecto:** Elegir un formato que no es compatible con la herramienta")
        st.markdown("- **Estructura inconsistente:** Mezclar diferentes tipos de información en una columna")
        st.markdown("- **Nombres confusos:** Usar abreviaciones o nombres poco claros en las columnas")
        st.markdown("- **Datos incompletos:** No verificar que todos los datos se cargaron correctamente")
        st.markdown("- **Archivos corruptos:** Intentar cargar archivos dañados o incompletos")
    
    with st.container():
        st.markdown(replace_emojis("### ✅ Buenas prácticas para preparar datos:"), unsafe_allow_html=True)
        st.markdown("- **Planifica antes de empezar:** Decide qué formato usar según tus necesidades")
        st.markdown("- **Organiza la estructura:** Una fila = un registro, una columna = un tipo de información")
        st.markdown("- **Usa nombres descriptivos:** Las columnas deben tener nombres claros y específicos")
        st.markdown("- **Verifica la calidad:** Siempre revisa que los datos se cargaron sin errores")
        st.markdown("- **Mantén copias de seguridad:** Guarda una copia de tus datos originales")
    
    # Practice activity
    st.header(replace_emojis("🎯 Actividad Práctica"))
    with st.container():
        st.markdown(replace_emojis("### 📝 Ejercicio para practicar la preparación de datos:"), unsafe_allow_html=True)
        st.markdown("1. **Elige un formato:** Decide si usar CSV o Excel para tu archivo")
        st.markdown("2. **Diseña la estructura:** Planifica qué columnas necesitas (ej: Fecha, Producto, Cantidad, Precio)")
        st.markdown("3. **Crea el archivo:** Abre Excel o un editor de texto y crea tu tabla")
        st.markdown("4. **Agrega datos de ejemplo:** Incluye al menos 10 registros con información realista")
        st.markdown("5. **Verifica la calidad:** Revisa que no haya errores, datos faltantes o inconsistencias")
        st.markdown("6. **Guarda correctamente:** Guarda en el formato que elegiste (.csv o .xlsx)")
    
    # Data upload and testing section
    st.header(replace_emojis("📤 Prueba lo que Aprendiste"))
    with st.container():
        st.markdown(replace_emojis("### 🚀 Sube tu propio archivo de datos"), unsafe_allow_html=True)
        st.markdown("Ahora puedes poner en práctica lo que aprendiste. Sube un archivo CSV o Excel para ver cómo se cargan y analizan los datos.")
    
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
            st.markdown(f"{get_icon("✅", 20)} Archivo cargado exitosamente: {uploaded_file.name}", unsafe_allow_html=True)
            
            # Display data overview
            st.subheader(replace_emojis("📊 Vista General de tus Datos"))
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(df_uploaded.head(10), use_container_width=True)
                st.caption(f"Primeras 10 filas de {len(df_uploaded)} registros totales")
            with col2:
                st.markdown(replace_emojis("**📊 Información básica:**"), unsafe_allow_html=True)
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
            st.subheader(replace_emojis("🔍 Estructura de tus Datos"))
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(replace_emojis("**📋 Columnas disponibles:**"), unsafe_allow_html=True)
                for col in df_uploaded.columns:
                    dtype_str = str(df_uploaded[col].dtype)
                    if 'int' in dtype_str:
                        dtype_icon = replace_emojis("🔢")
                    elif 'float' in dtype_str:
                        dtype_icon = replace_emojis("📊")
                    elif 'datetime' in dtype_str:
                        dtype_icon = replace_emojis("📅")
                    elif 'bool' in dtype_str:
                        dtype_icon = replace_emojis("✅")
                    else:
                        dtype_icon = replace_emojis("🔤")
                    
                    st.markdown(f"- {dtype_icon} **{col}**: {dtype_str}")
            
            with col2:
                st.markdown(replace_emojis("**📚 Análisis de calidad:**"), unsafe_allow_html=True)
                
                # Check for missing values and duplicates using utility function
                if analysis['total_missing'] == 0:
                    st.markdown(replace_emojis("✅ **Sin datos faltantes** - Excelente calidad"), unsafe_allow_html=True)
                else:
                    st.markdown(f"⚠️ **Datos faltantes**: {analysis['total_missing']} valores ({analysis['missing_percentage']:.1f}%)")
                
                if analysis['duplicates'] == 0:
                    st.markdown(replace_emojis("✅ **Sin filas duplicadas** - Datos únicos"), unsafe_allow_html=True)
                else:
                    st.markdown(f"⚠️ **Filas duplicadas**: {analysis['duplicates']} registros")
                
                # Data range info
                if numeric_cols:
                    numeric_sample = df_uploaded[numeric_cols].iloc[0]
                    st.markdown(f"{get_icon("🔢", 20)} **Columnas numéricas**: {', '.join(numeric_cols[:3])}{'...' if len(numeric_cols) > 3 else ''}", unsafe_allow_html=True)
                
                if text_cols:
                    text_sample = df_uploaded[text_cols].iloc[0]
                    st.markdown(f"{get_icon("🔤", 20)} **Columnas de texto**: {', '.join(text_cols[:3])}{'...' if len(text_cols) > 3 else ''}", unsafe_allow_html=True)
            
            # Data preview with more details
            st.subheader("👀 Vista Detallada de tus Datos")
            
            # Show sample data with more rows
            st.markdown(replace_emojis("**📋 Muestra de datos (primeras 15 filas):**"))
            st.dataframe(df_uploaded.head(15), use_container_width=True)
            
            # Show data info
            with st.expander(replace_emojis("🔍 Información técnica del dataset")):
                st.write("**Tipos de datos:**")
                st.write(df_uploaded.dtypes)
                
                st.write("**Estadísticas descriptivas:**")
                if numeric_cols:
                    st.write(df_uploaded[numeric_cols].describe())
                else:
                    st.info("No hay columnas numéricas para mostrar estadísticas")
                
                with st.container():
                    st.markdown(replace_emojis("#### 📊 Información General del Dataset"), unsafe_allow_html=True)
                
                # Create a nice grid layout for the info
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container():
                        st.markdown(replace_emojis("#### 🔢 Detalles Técnicos"), unsafe_allow_html=True)
                        st.markdown(f"**Memoria utilizada:** {df_uploaded.memory_usage(deep=True).sum() / 1024:.2f} KB")
                        st.markdown(f"**Rango de índice:** {df_uploaded.index[0]} a {df_uploaded.index[-1]}")
                        st.markdown(f"**Tipos de datos:** {len(df_uploaded.dtypes.unique())} diferentes")
                
                with col2:
                    with st.container():
                        st.markdown(replace_emojis("#### 📋 Resumen de Columnas"), unsafe_allow_html=True)
                        st.markdown(f"**Total de columnas:** {len(df_uploaded.columns)}")
                        st.markdown(f"**Columnas numéricas:** {len(numeric_cols)}")
                        st.markdown(f"**Columnas de texto:** {len(text_cols)}")
                        if date_cols:
                            st.markdown(f"**Columnas de fecha:** {len(date_cols)}")
                
                # Show detailed column information in a nice format
                with st.container():
                    st.markdown(replace_emojis("#### 📚 Detalle por Columna"), unsafe_allow_html=True)
                
                # Create a table-like display for column details
                col_details = []
                for col in df_uploaded.columns:
                    dtype_str = str(df_uploaded[col].dtype)
                    non_null_count = df_uploaded[col].count()
                    missing_count = df_uploaded[col].isnull().sum()
                    
                    if 'int' in dtype_str:
                        dtype_icon = replace_emojis("🔢")
                    elif 'float' in dtype_str:
                        dtype_icon = replace_emojis("📊")
                    elif 'datetime' in dtype_str:
                        dtype_icon = replace_emojis("📅")
                    elif 'bool' in dtype_str:
                        dtype_icon = replace_emojis("✅")
                    else:
                        dtype_icon = replace_emojis("🔤")
                    
                    col_details.append({
                        'columna': col,
                        'tipo': f"{dtype_icon} {dtype_str}",
                        'no_nulos': non_null_count,
                        'faltantes': missing_count
                    })
                
                # Display as a nice dataframe
                col_details_df = pd.DataFrame(col_details)
                col_details_df.columns = [replace_emojis('📋 Columna'), '🔤 Tipo', '✅ No Nulos', '⚠️ Faltantes']
                st.dataframe(col_details_df, use_container_width=True, hide_index=True)
            
            # Congratulations message
            with st.container():
                st.markdown(replace_emojis("### 🎉 ¡Excelente trabajo!"), unsafe_allow_html=True)
                st.markdown("Has cargado y analizado exitosamente tu propio archivo de datos. Esto demuestra que has dominado los conceptos básicos del Nivel 1.")
            
        except Exception as e:
            st.markdown(f"{get_icon("❌", 20)} Error al cargar el archivo: {str(e)}", unsafe_allow_html=True)
            st.markdown(replace_emojis("💡 Asegúrate de que tu archivo esté en el formato correcto y no esté corrupto."), unsafe_allow_html=True)
    
    else:
        st.markdown(replace_emojis("📁 Sube un archivo CSV o Excel para ver el análisis en acción."), unsafe_allow_html=True)
    
    # 6. Quiz Section - Must complete quiz before marking level as complete
    st.header("🧠 Quiz del Nivel")
    st.markdown("### Pon a prueba tus conocimientos")
    st.info(replace_emojis("📝 **Importante:** Debes aprobar el quiz (al menos 3 de 5 preguntas correctas) antes de poder marcar el nivel como completado."))
    
    # Check if user passed the quiz
    quiz_passed = st.session_state.get(f'quiz_nivel1_passed', False)
    
    if quiz_passed:
        st.markdown(replace_emojis("✅ ¡Has aprobado el quiz! Ahora puedes marcar el nivel como completado."), unsafe_allow_html=True)
    else:
        # Show quiz
        from core.quiz_system import create_quiz
        create_quiz('nivel1', user['username'])
        
        # Check if quiz was just completed and passed
        if st.session_state.get(f'quiz_nivel1_completed', False):
            score = st.session_state.get(f'quiz_nivel1_score', 0)
            if score >= 3:
                st.session_state[f'quiz_nivel1_passed'] = True
                st.rerun()
    
    st.divider()
    
    # 7. Navigation or next steps
    st.header(replace_emojis("✅ Verificación del Nivel"))
    
    # Only allow marking as complete if quiz is passed
    if not quiz_passed:
        st.warning("⚠️ Debes aprobar el quiz antes de poder marcar el nivel como completado.")
        nivel1_completed = False
    else:
        nivel1_completed = st.checkbox(
            "He completado todos los pasos del Nivel 1 y aprobé el quiz",
            value=st.session_state.get('nivel1_completed', False),
            key='nivel1_checkbox'
        )
    
    if nivel1_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel1', True):
            st.session_state['nivel1_completed'] = True
        else:
            st.markdown(replace_emojis("❌ Error al guardar el progreso. Intenta de nuevo."), unsafe_allow_html=True)
            return
        
        # Show achievement
        create_achievement_display('nivel1', progress)
        
        create_info_box(
            "success-box",
            replace_emojis("🎉 ¡Felicidades! Has completado el Nivel 1"),
            "<p>Ahora sabes cómo preparar y cargar datos correctamente. Estás listo para continuar con el siguiente nivel.</p>"
        )
        
        st.subheader(replace_emojis("🚀 ¿Qué sigue?"))
        st.markdown("Antes de continuar, nos gustaría conocer tu opinión sobre este nivel.")
        
        # Show next level preview
        create_level_preview('nivel2')
        
        if st.button("Completar Encuesta del Nivel", type="primary"):
            st.session_state.survey_level = 'nivel1'
            st.switch_page("pages/99_Survey_Nivel.py")
    
    # Additional resources
    create_info_box(
        "info-box",
        replace_emojis("📚 ¿Quieres saber más?"),
        "<p>Este nivel está basado en estándares de calidad de datos y mejores prácticas. Consulta la documentación para profundizar.</p>"
    )

if __name__ == "__main__":
    main()