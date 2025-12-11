from utils.ui.icon_system import get_icon, replace_emojis
"""
Help content components for TCC Data Analysis Platform
Handles help sections, learning guides, and content organization
"""

import streamlit as st
from .level_styles import load_level_styles
from .level_components import create_step_card, create_info_box

def load_help_styles():
    """Load help-specific styles"""
    return load_level_styles()

def create_table_of_contents():
    """Create a navigable table of contents for the help page"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">📑 Índice de Contenidos</h2>
        <div style="color: white; display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem;">
            <div><strong>1.</strong> <a href="#niveles-aprendizaje" style="color: white; text-decoration: underline;">Niveles de Aprendizaje</a></div>
            <div><strong>2.</strong> <a href="#funciones-plataforma" style="color: white; text-decoration: underline;">Funciones de la Plataforma</a></div>
            <div><strong>3.</strong> <a href="#conceptos-generales" style="color: white; text-decoration: underline;">Conceptos Generales</a></div>
            <div><strong>4.</strong> <a href="#buenas-practicas" style="color: white; text-decoration: underline;">Buenas Prácticas</a></div>
            <div><strong>5.</strong> <a href="#herramientas-externas" style="color: white; text-decoration: underline;">Otras Herramientas</a></div>
            <div><strong>6.</strong> <a href="#guia-decision" style="color: white; text-decoration: underline;">Guía de Decisión</a></div>
            <div><strong>7.</strong> <a href="#visualizaciones" style="color: white; text-decoration: underline;">Guía de Visualizaciones</a></div>
            <div><strong>8.</strong> <a href="#casos-uso" style="color: white; text-decoration: underline;">Casos de Uso</a></div>
            <div><strong>9.</strong> <a href="#solucion-problemas" style="color: white; text-decoration: underline;">Solución de Problemas</a></div>
            <div><strong>10.</strong> <a href="#recursos-aprendizaje" style="color: white; text-decoration: underline;">Recursos de Aprendizaje</a></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_help_header():
    """Create the main help header"""
    st.markdown(f'<h1 class="main-header">{get_icon("❓", 28)} Centro de Ayuda y Documentación</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #f0f2f6; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>Bienvenido a la guía completa de la Plataforma de Análisis de Datos TCC</strong></p>
        <p>Esta guía te ayudará a entender todas las funcionalidades disponibles, conceptos fundamentales de análisis de datos, 
        buenas prácticas, y cómo elegir la herramienta correcta para cada tarea. Úsala como referencia cuando lo necesites.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create table of contents
    create_table_of_contents()
    st.divider()

def create_learning_levels_section():
    """Create the learning levels overview section"""
    st.markdown('<div id="niveles-aprendizaje"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 📚 1. Niveles de Aprendizaje"), unsafe_allow_html=True)
    
    st.markdown("""
    La plataforma incluye **5 niveles progresivos** diseñados para guiarte desde conceptos básicos hasta análisis avanzados.
    Cada nivel se construye sobre el anterior, creando una experiencia de aprendizaje estructurada.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_step_card(
            step_number="0",
            title=replace_emojis("🌟 Nivel 0: Introducción"),
            description="**Duración:** 15-20 minutos\n\n"
                       "**Objetivo:** Entender qué son los datos y sus tipos fundamentales\n\n"
                       "**Contenido:**\n"
                       "- ¿Qué son los datos?\n"
                       "- Tipos de datos (numéricos, texto, fechas, booleanos)\n"
                       "- Estructura de datos (filas y columnas)\n"
                       "- ¿Qué es el análisis de datos?\n\n"
                       "**Resultado:** Comprensión básica de conceptos fundamentales"
        )
        
        create_step_card(
            step_number="1",
            title=replace_emojis("📚 Nivel 1: Básico - Preparación"),
            description="**Duración:** 20-30 minutos\n\n"
                       "**Objetivo:** Aprender a preparar y cargar datos correctamente\n\n"
                       "**Contenido:**\n"
                       "- Formatos de archivos (CSV, Excel)\n"
                       "- Carga de datos con selección de hojas/delimitadores\n"
                       "- Verificación de calidad de datos\n"
                       "- Estructura correcta de datos\n\n"
                       "**Resultado:** Datos preparados y listos para análisis"
        )
        
        create_step_card(
            step_number="2",
            title=replace_emojis("🔍 Nivel 2: Filtros"), 
            description="**Duración:** 20-25 minutos\n\n"
                       "**Objetivo:** Aprender a filtrar y segmentar datos\n\n"
                       "**Contenido:**\n"
                       "- Filtros básicos y avanzados\n"
                       "- Filtros por texto, números, fechas\n"
                       "- Filtros combinados (AND, OR)\n"
                       "- Segmentación de datos\n\n"
                       "**Resultado:** Capacidad de encontrar información específica en los datos"
        )
    
    with col2:
        create_step_card(
            step_number="3",
            title=replace_emojis("📊 Nivel 3: Métricas"),
            description="**Duración:** 25-30 minutos\n\n"
                       "**Objetivo:** Calcular e interpretar KPIs importantes\n\n"
                       "**Contenido:**\n"
                       "- ¿Qué son los KPIs?\n"
                       "- Métricas básicas (suma, promedio, conteo)\n"
                       "- Métricas avanzadas (mediana, desviación estándar)\n"
                       "- Interpretación de resultados\n"
                       "- Quiz de comprensión (requiere 80%)\n\n"
                       "**Resultado:** Capacidad de calcular e interpretar métricas clave"
        )
        
        create_step_card(
            step_number="4",
            title=replace_emojis("🚀 Nivel 4: Avanzado"),
            description="**Duración:** 30-40 minutos\n\n"
                       "**Objetivo:** Crear visualizaciones profesionales y análisis avanzados\n\n"
                       "**Contenido:**\n"
                       "- Cálculos personalizados\n"
                       "- Visualizaciones interactivas (Plotly)\n"
                       "- Gráficos de barras, líneas, circulares\n"
                       "- Análisis de correlaciones\n"
                       "- Quiz final (requiere 80%)\n\n"
                       "**Resultado:** Capacidad de crear análisis completos y visualizaciones profesionales"
        )
    
    create_info_box(
        "info-box",
        replace_emojis("💡 Consejo de Progresión"),
        "**Orden recomendado:** Completa los niveles en secuencia (0→1→2→3→4). "
        "Cada nivel desbloquea el siguiente. Si ya tienes experiencia, puedes avanzar más rápido, "
        "pero te recomendamos al menos revisar cada nivel para asegurar que no te pierdas conceptos importantes."
    )
    
    st.markdown("---")

def create_platform_functions_section():
    """Create comprehensive section describing all platform functions"""
    st.markdown('<div id="funciones-plataforma"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 🛠️ 2. Funciones de la Plataforma"), unsafe_allow_html=True)
    
    st.markdown("""
    La plataforma ofrece múltiples herramientas especializadas para diferentes necesidades de análisis de datos.
    """)
    
    # Dashboard en Blanco
    st.markdown(replace_emojis("### 🎨 Dashboard en Blanco"), unsafe_allow_html=True)
    st.markdown("""
    **Herramienta de construcción de dashboards personalizados desde cero.**
    
    **Características principales:**
    - **Componentes disponibles:**
      - 📈 Métricas (KPIs): Suma, promedio, conteo, máximo, mínimo, mediana
      - 📊 Gráficos de Líneas: Para mostrar tendencias temporales
      - 📋 Gráficos de Barras: Para comparar categorías
      - 🥧 Gráficos Circulares: Para mostrar proporciones
      - 📈 Gráficos de Área: Para mostrar acumulados
      - 🔄 Gráficos de Dispersión: Para relaciones entre variables
      - 📊 Histogramas: Para distribuciones
      - 📦 Box Plots: Para identificar outliers
      - 🎻 Gráficos de Violín: Para distribuciones detalladas
      - 🔗 Matrices de Correlación: Para relaciones entre múltiples variables
      - 📋 Tablas de Datos: Para visualización detallada
    
    - **Funcionalidades:**
      - Filtros globales interactivos
      - Configuración personalizada de cada componente
      - Guardado y carga de dashboards
      - Exportación de datos y visualizaciones
      - Plantillas predefinidas (Ejecutiva, Rendimiento, Operativa)
    
    - **Cuándo usar:**
      - Necesitas crear visualizaciones específicas para tu negocio
      - Las plantillas predefinidas no cubren tus necesidades
      - Quieres experimentar con diferentes tipos de análisis
      - Necesitas un dashboard completamente personalizado
    """)
    
    # Limpieza de Datos
    st.markdown(replace_emojis("### 🧹 Limpieza Automática de Datos"), unsafe_allow_html=True)
    st.markdown("""
    **Herramienta especializada para preparar y limpiar datos antes del análisis.**
    
    **Operaciones disponibles:**
    - **Limpieza de espacios:** Elimina espacios en blanco al inicio y final
    - **Normalización de texto:** Convierte a mayúsculas, minúsculas o título
    - **Reemplazo de valores:** Sustituye valores específicos
    - **Estandarización de teléfonos:** Formatea números telefónicos
    - **Estandarización de emails:** Valida y normaliza direcciones de correo
    - **Manejo de valores faltantes:** Elimina o reemplaza valores nulos
    - **Eliminación de duplicados:** Remueve filas duplicadas
    - **Eliminación de columnas:** Quita columnas innecesarias
    
    **Características:**
    - Vista previa antes/después de cada operación
    - Estadísticas de comparación (filas/columnas removidas)
    - Descarga de datos limpios en CSV
    - Soporte para archivos CSV (con detección de delimitador) y Excel (con selección de hoja)
    
    **Cuándo usar:**
      - Tienes datos con errores de formato
      - Necesitas estandarizar valores antes de analizar
      - Quieres eliminar datos duplicados o incorrectos
      - Necesitas preparar datos para importar a otras herramientas
    """)
    
    # Carga de Datos
    st.markdown(replace_emojis("### 📤 Carga de Datos"), unsafe_allow_html=True)
    st.markdown("""
    **Sistema inteligente de carga de archivos con detección automática.**
    
    **Formatos soportados:**
    - **CSV:** Con detección automática de delimitador (coma, punto y coma, tabulador, pipe)
    - **Excel (.xlsx, .xls):** Con selección de hoja cuando hay múltiples hojas
    
    **Características:**
    - Detección automática de delimitadores CSV
    - Selección manual de delimitador si la detección falla
    - Selección de hoja en archivos Excel con múltiples hojas
    - Soporte para múltiples codificaciones (UTF-8, Latin-1, ISO-8859-1, CP1252)
    - Validación automática de estructura de datos
    - Vista previa inmediata después de la carga
    """)
    
    # Datasets de Ejemplo
    st.markdown(replace_emojis("### 📊 Datasets de Ejemplo"), unsafe_allow_html=True)
    st.markdown("""
    **Colección de datasets pre-configurados para práctica y aprendizaje.**
    
    **Datasets disponibles:**
    - **E-commerce (TechStore):** 1,000 registros de ventas - Ideal para el camino de aprendizaje principal
    - **Dataset Sucio:** 225 registros con problemas de calidad - Para practicar limpieza
    - **Healthcare:** 800 registros médicos - Para análisis intermedio
    - **Finance:** 1,200 registros financieros - Para análisis financiero
    - **Sales:** 1,500 registros de ventas - Para patrones estacionales
    - **Education:** 500 registros académicos - Para datos educativos
    
    **Uso recomendado:**
    - Practicar sin necesidad de preparar tus propios datos
    - Entender diferentes tipos de análisis
    - Aprender con datos de calidad conocida
    """)
    
    st.markdown("---")

def create_general_concepts_section():
    """Create section with general data analysis concepts"""
    st.markdown('<div id="conceptos-generales"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 📖 3. Conceptos Generales de Análisis de Datos"), unsafe_allow_html=True)
    
    st.markdown("""
    ### ¿Qué es el Análisis de Datos?
    
    El análisis de datos es el proceso de examinar, limpiar, transformar y modelar datos 
    con el objetivo de descubrir información útil, llegar a conclusiones y apoyar la toma de decisiones.
    """)
    
    with st.expander(replace_emojis("📊 Tipos de Datos")):
        st.markdown("""
        **Datos Numéricos:**
        - **Enteros:** Números sin decimales (1, 2, 100)
        - **Decimales:** Números con decimales (3.14, 99.99)
        - **Porcentajes:** Valores entre 0 y 100 (25%, 50%)
        
        **Datos de Texto:**
        - **Nombres:** Identificadores de personas, productos, lugares
        - **Categorías:** Clasificaciones (Electrónica, Ropa, Libros)
        - **Descripciones:** Texto libre con información adicional
        
        **Datos de Fecha y Hora:**
        - **Fechas:** Días, meses, años (2024-01-15)
        - **Horas:** Tiempo del día (14:30:00)
        - **Fechas y hora combinadas:** Timestamps completos
        
        **Datos Booleanos:**
        - **Sí/No:** Valores binarios (True/False, 1/0)
        - **Verdadero/Falso:** Estados lógicos
        """)
    
    with st.expander(replace_emojis("📋 Estructura de Datos")):
        st.markdown("""
        **Tablas (DataFrames):**
        - **Filas (Registros):** Cada fila representa una observación o caso individual
        - **Columnas (Variables):** Cada columna representa un tipo de información
        - **Celdas:** Intersección de fila y columna, contiene un valor específico
        
        **Ejemplo:**
        ```
        | Fecha      | Producto | Cantidad | Precio | Cliente |
        |------------|----------|----------|--------|---------|
        | 2024-01-15 | Laptop   | 1        | 800    | Juan    |
        | 2024-01-16 | Mouse    | 2        | 25     | María   |
        ```
        
        **Reglas importantes:**
        - Una fila = un registro completo
        - Una columna = un tipo de dato consistente
        - Encabezados claros y descriptivos
        - Sin filas o columnas completamente vacías
        """)
    
    with st.expander(replace_emojis("📈 Métricas y KPIs")):
        st.markdown("""
        **Métricas Básicas:**
        - **Suma:** Total de valores (ej: ventas totales)
        - **Promedio (Media):** Valor típico (ej: venta promedio)
        - **Conteo:** Número de registros (ej: número de clientes)
        - **Máximo:** Valor más alto (ej: venta más grande)
        - **Mínimo:** Valor más bajo (ej: venta más pequeña)
        
        **Métricas Avanzadas:**
        - **Mediana:** Valor del medio cuando se ordenan los datos
        - **Desviación Estándar:** Qué tan dispersos están los datos
        - **Percentiles:** Valores que dividen los datos en partes (25%, 50%, 75%)
        
        **KPIs (Indicadores Clave de Rendimiento):**
        - Métricas que miden el éxito de objetivos específicos
        - Deben ser relevantes para tu negocio o análisis
        - Ejemplos: Tasa de conversión, Retención de clientes, Margen de ganancia
        """)
    
    with st.expander(replace_emojis("🔍 Filtros y Segmentación")):
        st.markdown("""
        **Filtros básicos:**
        - **Por texto:** Encuentra registros que contengan texto específico
        - **Por número:** Filtra por rangos de valores (mayor que, menor que, igual a)
        - **Por fecha:** Selecciona períodos temporales específicos
        
        **Filtros combinados:**
        - **AND:** Debe cumplir todas las condiciones (ej: Ventas > 100 AND Categoría = "Electrónica")
        - **OR:** Debe cumplir al menos una condición (ej: Región = "Norte" OR Región = "Sur")
        
        **Segmentación:**
        - Dividir datos en grupos para análisis comparativo
        - Ejemplos: Por región, por categoría, por período de tiempo
        """)
    
    st.markdown("---")

def create_best_practices_section():
    """Create section with best practices for data analysis"""
    st.markdown('<div id="buenas-practicas"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## ✅ 4. Buenas Prácticas de Análisis de Datos"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_step_card(
            step_number="1",
            title="Preparación de Datos",
            description="**Siempre limpia tus datos primero:**\n"
                       "- Verifica la calidad antes de analizar\n"
                       "- Elimina duplicados y errores obvios\n"
                       "- Estandariza formatos (fechas, números, texto)\n"
                       "- Maneja valores faltantes apropiadamente\n\n"
                       "**💡 Consejo:** Datos limpios = Análisis confiables"
        )
        
        create_step_card(
            step_number="2",
            title="Estructura Correcta",
            description="**Organiza tus datos adecuadamente:**\n"
                       "- Una fila = un registro completo\n"
                       "- Una columna = un tipo de dato\n"
                       "- Encabezados claros y descriptivos\n"
                       "- Sin filas o columnas vacías\n\n"
                       "**💡 Consejo:** La estructura correcta facilita todo el análisis"
        )
        
        create_step_card(
            step_number="3",
            title="Validación de Resultados",
            description="**Verifica que tus análisis tengan sentido:**\n"
                       "- Compara con períodos anteriores\n"
                       "- Busca explicaciones para cambios grandes\n"
                       "- Identifica y explica valores atípicos\n"
                       "- Usa múltiples métricas para confirmar\n\n"
                       "**💡 Consejo:** Si algo parece demasiado bueno o malo, investiga"
        )
    
    with col2:
        create_step_card(
            step_number="4",
            title="Visualizaciones Apropiadas",
            description="**Elige el gráfico correcto:**\n"
                       "- Tendencias → Gráficos de líneas\n"
                       "- Comparaciones → Gráficos de barras\n"
                       "- Proporciones → Gráficos circulares\n"
                       "- Relaciones → Gráficos de dispersión\n\n"
                       "**💡 Consejo:** El gráfico debe responder a tu pregunta"
        )
        
        create_step_card(
            step_number="5",
            title="Interpretación Cuidadosa",
            description="**Evita errores comunes:**\n"
                       "- No confundas correlación con causalidad\n"
                       "- Considera el contexto (eventos, campañas)\n"
                       "- No bases conclusiones en períodos muy cortos\n"
                       "- Compara datos similares (mismo período, mismo contexto)\n\n"
                       "**💡 Consejo:** Los datos cuentan una historia, pero necesitas entender el contexto"
        )
        
        create_step_card(
            step_number="6",
            title="Documentación",
            description="**Documenta tu trabajo:**\n"
                       "- Guarda tus dashboards con nombres descriptivos\n"
                       "- Anota decisiones importantes de limpieza\n"
                       "- Explica filtros y cálculos personalizados\n"
                       "- Guarda versiones de datos limpios\n\n"
                       "**💡 Consejo:** La documentación te ayuda a ti y a otros a entender el análisis"
        )
    
    st.markdown("---")

def create_external_tools_section():
    """Create section about other tools and when to use them"""
    st.markdown('<div id="herramientas-externas"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 🛠️ 5. Otras Herramientas de Análisis de Datos"), unsafe_allow_html=True)
    
    st.markdown("""
    ### Herramientas por Nivel de Complejidad
    """)
    
    with st.expander(replace_emojis("📊 Nivel Básico - Excel/Google Sheets")):
        st.markdown("""
        **Cuándo usar:**
        - Análisis simples y exploratorios
        - Datos pequeños a medianos (< 100,000 filas)
        - Necesitas trabajar colaborativamente
        - Requieres fórmulas y cálculos básicos
        
        **Ventajas:**
        - Fácil de aprender
        - Ampliamente disponible
        - Interfaz familiar
        - Bueno para presentaciones
        
        **Limitaciones:**
        - Limitado con datos muy grandes
        - Visualizaciones básicas
        - Difícil automatizar procesos complejos
        """)
    
    with st.expander(replace_emojis("📈 Nivel Intermedio - Power BI / Tableau")):
        st.markdown("""
        **Cuándo usar:**
        - Necesitas visualizaciones avanzadas y profesionales
        - Trabajas con múltiples fuentes de datos
        - Requieres dashboards interactivos complejos
        - Necesitas compartir análisis con equipos
        
        **Ventajas:**
        - Visualizaciones muy potentes
        - Conexión a múltiples fuentes de datos
        - Dashboards interactivos profesionales
        - Buen soporte para grandes volúmenes
        
        **Limitaciones:**
        - Curva de aprendizaje más pronunciada
        - Puede ser costoso
        - Requiere más recursos computacionales
        """)
    
    with st.expander(replace_emojis("🐍 Nivel Avanzado - Python / R")):
        st.markdown("""
        **Cuándo usar:**
        - Necesitas análisis estadísticos complejos
        - Quieres automatizar procesos de análisis
        - Trabajas con datos muy grandes
        - Requieres machine learning o análisis predictivo
        
        **Ventajas:**
        - Máxima flexibilidad
        - Librerías especializadas (pandas, numpy, scikit-learn)
        - Automatización completa
        - Reproducibilidad
        
        **Limitaciones:**
        - Requiere programación
        - Curva de aprendizaje significativa
        - Más tiempo de desarrollo inicial
        """)
    
    with st.expander(replace_emojis("🗄️ Bases de Datos - SQL")):
        st.markdown("""
        **Cuándo usar:**
        - Trabajas con bases de datos grandes
        - Necesitas consultar datos estructurados
        - Requieres combinar datos de múltiples tablas
        - Necesitas eficiencia en consultas
        
        **Ventajas:**
        - Muy eficiente con grandes volúmenes
        - Estándar en la industria
        - Potente para consultas complejas
        - Integración con otras herramientas
        
        **Limitaciones:**
        - Requiere conocimiento de SQL
        - Menos visual que otras herramientas
        - Principalmente para consultas, no análisis completo
        """)
    
    st.markdown("---")

def create_decision_guide_section():
    """Create decision guide for choosing the right tool"""
    st.markdown('<div id="guia-decision"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 🎯 6. Guía de Decisión: ¿Qué Herramienta Usar?"), unsafe_allow_html=True)
    
    st.markdown("""
    ### Árbol de Decisión Rápido
    """)
    
    create_info_box(
        "info-box",
        replace_emojis("🤔 ¿Estás empezando a aprender análisis de datos?"),
        "**→ Usa esta plataforma (TCC)**\n\n"
        "Esta plataforma está diseñada específicamente para aprender análisis de datos de manera práctica. "
        "Completa los 5 niveles para construir una base sólida antes de pasar a herramientas más complejas."
    )
    
    create_info_box(
        "info-box",
        replace_emojis("📊 ¿Necesitas análisis rápidos y simples?"),
        "**→ Excel/Google Sheets**\n\n"
        "Ideal para análisis exploratorios rápidos, cálculos básicos, y cuando necesitas trabajar "
        "colaborativamente con personas que no tienen experiencia técnica."
    )
    
    create_info_box(
        "info-box",
        replace_emojis("📈 ¿Necesitas dashboards profesionales para presentar?"),
        "**→ Power BI / Tableau**\n\n"
        "Perfecto cuando necesitas crear visualizaciones impresionantes para presentaciones ejecutivas, "
        "dashboards interactivos complejos, o trabajar con múltiples fuentes de datos."
    )
    
    create_info_box(
        "info-box",
        replace_emojis("🔬 ¿Necesitas análisis estadísticos avanzados o automatización?"),
        "**→ Python / R**\n\n"
        "Ideal cuando necesitas análisis estadísticos complejos, machine learning, procesamiento de datos "
        "muy grandes, o automatizar procesos de análisis repetitivos."
    )
    
    create_info_box(
        "info-box",
        replace_emojis("🗄️ ¿Trabajas principalmente con bases de datos grandes?"),
        "**→ SQL**\n\n"
        "Esencial cuando necesitas consultar y combinar datos de bases de datos estructuradas, "
        "especialmente cuando el volumen de datos es muy grande."
    )
    
    st.markdown("""
    ### Recomendación de Progresión
    
    **Camino de Aprendizaje Recomendado:**
    
    1. **Comienza aquí (TCC Platform)** → Aprende conceptos fundamentales y prácticas básicas
    2. **Practica con Excel/Google Sheets** → Refuerza conceptos con herramientas familiares
    3. **Explora Power BI/Tableau** → Aprende visualizaciones profesionales
    4. **Aprende Python/R** → Para análisis avanzados y automatización
    5. **Domina SQL** → Para trabajar con bases de datos
    
    **💡 Consejo:** No necesitas aprender todas las herramientas. Elige según tus necesidades y objetivos profesionales.
    """)
    
    st.markdown("---")

def create_visualization_guide():
    """Create the data visualization guide section"""
    st.markdown('<div id="visualizaciones"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 📊 7. Guía de Visualizaciones"), unsafe_allow_html=True)
    
    st.markdown("**Los gráficos correctos te ayudan a contar historias con tus datos.**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_step_card(
            step_number="1",
            title=replace_emojis("📊 Gráfico de Barras"),
            description=replace_emojis(
                "**Usa para:**\n"
                "- Comparar cantidades entre categorías\n"
                "- Mostrar rankings (mejor a peor)\n"
                "- Datos categóricos simples\n\n"
                "**Ejemplos:**\n"
                "- Ventas por producto\n"
                "- Ingresos por región\n"
                "- Número de clientes por categoría\n\n"
                "**💡 Consejo:** Ordena las barras de mayor a menor para mejor lectura"
            )
        )
        
        create_step_card(
            step_number="2",
            title=replace_emojis("📈 Gráfico de Líneas"),
            description=replace_emojis(
                "**Usa para:**\n"
                "- Mostrar cambios a lo largo del tiempo\n"
                "- Ver tendencias y patrones\n"
                "- Comparar múltiples series temporales\n\n"
                "**Ejemplos:**\n"
                "- Ventas diarias/mensuales\n"
                "- Evolución de precios\n"
                "- Crecimiento de usuarios\n\n"
                "**💡 Consejo:** Usa colores diferentes para cada línea"
            )
        )
        
        create_step_card(
            step_number="3",
            title="🥧 Gráfico Circular (Torta)",
            description="**Usa para:**\n"
                       "- Mostrar proporciones de un total\n"
                       "- Máximo 5-6 categorías\n"
                       "- Cuando quieres mostrar 'parte del todo'\n\n"
                       "**Ejemplos:**\n"
                       "- Distribución de gastos\n"
                       "- Participación de mercado\n"
                       "- Fuentes de tráfico web\n\n"
                       "**⚠️ Evita:** Muchas categorías pequeñas (se vuelve confuso)"
        )
    
    with col2:
        create_step_card(
            step_number="4",
            title=replace_emojis("🔄 Gráfico de Dispersión"),
            description=replace_emojis(
                "**Usa para:**\n"
                "- Ver relaciones entre dos variables\n"
                "- Identificar correlaciones\n"
                "- Encontrar valores atípicos\n\n"
                "**Ejemplos:**\n"
                "- Precio vs Calificación\n"
                "- Edad vs Gasto\n"
                "- Tiempo vs Satisfacción\n\n"
                "**💡 Consejo:** Agrega una línea de tendencia para ver la relación"
            )
        )
        
        create_step_card(
            step_number="5",
            title=replace_emojis("📊 Histograma"),
            description=replace_emojis(
                "**Usa para:**\n"
                "- Ver distribución de una variable\n"
                "- Identificar patrones en los datos\n"
                "- Encontrar valores más comunes\n\n"
                "**Ejemplos:**\n"
                "- Distribución de edades\n"
                "- Distribución de precios\n"
                "- Distribución de ingresos\n\n"
                "**💡 Consejo:** Ajusta el número de bins para mejor visualización"
            )
        )
        
        create_step_card(
            step_number="6",
            title=replace_emojis("🔗 Matriz de Correlación"),
            description=replace_emojis(
                "**Usa para:**\n"
                "- Ver relaciones entre múltiples variables\n"
                "- Identificar variables relacionadas\n"
                "- Encontrar patrones complejos\n\n"
                "**Ejemplos:**\n"
                "- Relaciones entre métricas de negocio\n"
                "- Correlaciones en datos financieros\n"
                "- Relaciones en datos de salud\n\n"
                "**💡 Consejo:** Los colores más intensos indican correlaciones más fuertes"
            )
        )
    
    st.markdown("---")

def create_common_scenarios():
    """Create common analysis scenarios section"""
    st.markdown('<div id="casos-uso"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 🎯 8. Casos de Uso Comunes"), unsafe_allow_html=True)
    
    with st.expander("🛒 Análisis de Ventas"):
        st.markdown("""
        **Preguntas típicas que puedes responder:**
        
        #### 📊 ¿Qué productos venden mejor?
        - Agrupa por producto y suma cantidades
        - Ordena de mayor a menor
        - Identifica los top 10-20%
        - Visualiza con gráfico de barras
        
        #### 📅 ¿Cuándo vendo más?
        - Analiza ventas por día de la semana
        - Busca patrones mensuales/estacionales
        - Identifica fechas especiales (Black Friday, etc.)
        - Visualiza con gráfico de líneas temporal
        
        #### 👥 ¿Quiénes son mis mejores clientes?
        - Agrupa por cliente y suma compras
        - Identifica patrones de compra
        - Segmenta por valor de cliente
        - Crea análisis de frecuencia y valor
        """)
    
    with st.expander(replace_emojis("📈 Análisis de Tendencias")):
        st.markdown("""
        **Cómo identificar y analizar tendencias:**
        
        #### 📊 Compara períodos:
        - Este mes vs mes pasado
        - Este año vs año pasado
        - Busca patrones: ¿Qué días/meses son mejores?
        - Identifica estacionalidad: ¿Hay épocas del año mejores?
        - Proyecta el futuro: Basándote en tendencias pasadas
        
        #### 💡 Consejos:
        - Siempre considera el contexto (eventos, campañas, etc.)
        - No confíes solo en un período corto
        - Busca explicaciones para los cambios
        - Usa promedios móviles para suavizar variaciones
        """)
    
    with st.expander(replace_emojis("💰 Análisis Financiero")):
        st.markdown("""
        **Métricas clave para análisis financiero:**
        
        #### 📊 Ingresos y Gastos:
        - Calcula ingresos totales por período
        - Identifica gastos principales
        - Calcula margen de ganancia
        - Analiza tendencias de rentabilidad
        
        #### 📈 KPIs Financieros:
        - Crecimiento mes a mes
        - Tasa de crecimiento anual
        - Rentabilidad por producto/categoría
        - Análisis de flujo de caja
        """)
    
    st.markdown("---")

def create_troubleshooting_section():
    """Create troubleshooting and common mistakes section"""
    st.markdown('<div id="solucion-problemas"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 🔧 9. Solución de Problemas Comunes"), unsafe_allow_html=True)
    
    with st.expander(replace_emojis("🔍 ¿Por qué mis análisis no tienen sentido?")):
        st.markdown("""
        **Errores comunes de interpretación:**
        
        #### 📊 Comparando peras con manzanas:
        - **Problema:** Comparar datos de diferentes períodos o contextos
        - **Solución:** Asegúrate de que las comparaciones sean justas
        - **Ejemplo:** No compares ventas de enero (post-navidad) con diciembre
        
        #### 📈 Confundiendo correlación con causalidad:
        - **Problema:** Asumir que A causa B solo porque van juntos
        - **Solución:** Busca explicaciones lógicas y evidencia adicional
        - **Ejemplo:** Más helados se venden cuando hace calor, pero el calor no causa ventas
        
        #### 📊 Ignorando valores atípicos:
        - **Problema:** No investigar datos que se salen del patrón
        - **Solución:** Identifica y explica los valores atípicos
        - **Ejemplo:** Una venta muy alta puede ser un error o un cliente VIP
        
        #### 📅 Períodos de tiempo muy cortos:
        - **Problema:** Basar conclusiones en pocos datos
        - **Solución:** Usa períodos más largos para tendencias
        - **Ejemplo:** Una semana no es suficiente para ver patrones estacionales
        """)
    
    with st.expander(replace_emojis("❌ Problemas Técnicos Comunes")):
        st.markdown("""
        **Soluciones rápidas:**
        
        #### 📁 Archivo no se carga:
        - Verifica el formato (CSV o Excel)
        - Revisa que el delimitador sea correcto (para CSV)
        - Selecciona la hoja correcta (para Excel)
        - Verifica que el archivo no esté corrupto
        
        #### 🔍 Filtros no funcionan:
        - Verifica que los datos estén cargados
        - Asegúrate de que el tipo de dato sea correcto
        - Resetea los filtros y vuelve a intentar
        - Verifica que los valores existan en los datos
        
        #### 📊 Gráficos no se muestran:
        - Verifica que hayas seleccionado columnas válidas
        - Asegúrate de que los datos tengan el formato correcto
        - Revisa que no haya valores faltantes críticos
        - Intenta con un dataset de ejemplo para verificar
        
        #### 💾 Dashboard no se guarda:
        - Verifica que estés autenticado
        - Asegúrate de tener conexión a internet
        - Intenta guardar con un nombre diferente
        - Revisa que no haya caracteres especiales en el nombre
        """)
    
    st.markdown("---")

def create_learning_resources():
    """Create additional learning resources section"""
    st.markdown('<div id="recursos-aprendizaje"></div>', unsafe_allow_html=True)
    st.markdown(replace_emojis("## 📚 10. Recursos para Seguir Aprendiendo"), unsafe_allow_html=True)
    
    st.markdown("""
    **Para profundizar en análisis de datos:**
    
    ### 📖 Conceptos Fundamentales:
    - **Estadística básica:** Promedios, medianas, desviación estándar
    - **Probabilidad:** Entender incertidumbre en los datos
    - **Muestreo:** Cómo obtener datos representativos
    - **Validación:** Verificar que tus conclusiones sean correctas
    
    ### 🛠️ Herramientas Recomendadas (por nivel):
    - **Principiante:** Excel/Google Sheets - Para análisis básicos y exploratorios
    - **Intermedio:** Power BI/Tableau - Para visualizaciones avanzadas
    - **Avanzado:** Python/R - Para análisis más complejos y automatización
    - **Especializado:** SQL - Para consultar bases de datos grandes
    
    ### 🎯 Próximos Pasos:
    - **Practica con datos reales** de tu negocio o área de interés
    - **Únete a comunidades** de análisis de datos (Reddit r/dataanalysis, Kaggle)
    - **Toma cursos online** sobre estadística y visualización (Coursera, edX, Udemy)
    - **Lee blogs y artículos** sobre mejores prácticas (Towards Data Science, DataCamp Blog)
    - **Participa en proyectos** de análisis de datos en GitHub o Kaggle
    
    ### 💡 Consejo Final
    
    **El análisis de datos es una habilidad que se mejora con la práctica.** 
    Comienza con preguntas simples y ve aumentando la complejidad gradualmente. 
    ¡No tengas miedo de experimentar y cometer errores - es parte del aprendizaje!
    
    **Recuerda:** Esta plataforma es tu punto de partida. Una vez que domines los conceptos aquí, 
    estarás listo para explorar herramientas más avanzadas según tus necesidades profesionales.
    """)
    
    st.markdown("---")

def create_dashboard_blanco_section():
    """Create the Dashboard en Blanco section"""
    st.markdown(replace_emojis("## 🎨 Dashboard en Blanco - Herramienta Avanzada"), unsafe_allow_html=True)
    
    st.markdown("""
    **El Dashboard en Blanco** es una herramienta especial que te permite crear dashboards completamente personalizados 
    desde cero, sin restricciones de plantillas predefinidas.
    """)
    
    create_info_box(
        "info-box",
        replace_emojis("🎯 ¿Cuándo usar el Dashboard en Blanco?"),
        "- **Tienes experiencia** con análisis de datos y visualizaciones\n"
        "- **Necesitas control total** sobre cada componente de tu dashboard\n"
        "- **Quieres crear visualizaciones específicas** para tu negocio\n"
        "- **Las plantillas predefinidas** no cubren tus necesidades\n"
        "- **Deseas experimentar** con diferentes tipos de gráficos y métricas"
    )
    
    create_info_box(
        "info-box",
        replace_emojis("🚀 Características Principales"),
        replace_emojis(
            "- **📈 Métricas personalizadas**: Crea KPIs específicos para tu análisis\n"
            "- **📊 Gráficos básicos**: Líneas, barras, circulares, áreas\n"
            "- **🔬 Gráficos avanzados**: Dispersión, histogramas, box plots, violín\n"
            "- **🔍 Análisis estadístico**: Matrices de correlación, tablas de datos\n"
            "- **💾 Guardado y exportación**: Conserva tu trabajo y compártelo"
        )
    )

def create_quick_reference():
    """Create quick reference section for Dashboard en Blanco"""
    st.markdown("""
    ---
    ### 🎨 Referencia Rápida - Dashboard en Blanco
    
    **Comandos y atajos útiles:**
    
    #### ⚡ **Acceso Rápido:**
    - **Desde el inicio**: Selecciona "Dashboard en Blanco" en las plantillas
    - **Navegación directa**: Usa el menú lateral o el botón de arriba
    - **Requisito**: Debes tener datos cargados previamente
    
    #### 🔧 **Controles Principales:**
    - **Agregar componente**: Usa los botones en el panel lateral
    - **Configurar**: Haz clic en "⚙️ Configurar" en cada componente
    - **Actualizar**: Usa "🔄 Actualizar" para aplicar cambios
    - **Eliminar**: "🗑️ Eliminar" para quitar componentes
    - **Guardar**: "💾 Guardar" para conservar tu trabajo
    
    #### 📊 **Tipos de Gráficos por Uso:**
    - **Tendencias**: Gráficos de líneas y área
    - **Comparaciones**: Gráficos de barras (vertical/horizontal)
    - **Proporciones**: Gráficos circulares
    - **Relaciones**: Gráficos de dispersión
    - **Distribuciones**: Histogramas, box plots, violín
    - **Correlaciones**: Matriz de correlación
    
    #### 💡 **Consejos de Productividad:**
    - Comienza con métricas básicas para tener KPIs
    - Usa títulos descriptivos para cada componente
    - Prueba diferentes configuraciones antes de decidir
    - Guarda tu trabajo regularmente
    """)

def create_navigation_section():
    """Create the navigation section with action buttons"""
    st.divider()
    st.markdown(replace_emojis("## 🎯 ¿Listo para Comenzar?"), unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🌟 Comenzar Nivel 0", type="primary", key="ayuda_nivel0"):
            st.switch_page("pages/00_Nivel_0_Introduccion.py")
    
    with col2:
        if st.button("📚 Nivel 1 Básico", key="ayuda_nivel1"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col3:
        if st.button("🔍 Nivel 2 Filtros", key="ayuda_nivel2"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col4:
        if st.button("📊 Nivel 3 Métricas", key="ayuda_nivel3"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col5:
        if st.button("🚀 Nivel 4 Avanzado", key="ayuda_nivel4"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col6:
        if st.button("🏠 Dashboard Principal", key="ayuda_dashboard"):
            st.switch_page("Inicio.py")
