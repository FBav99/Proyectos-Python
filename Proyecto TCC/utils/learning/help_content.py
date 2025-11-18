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

def create_help_header():
    """Create the main help header"""
    st.markdown("## ❓ Centro de Ayuda")
    st.markdown("### Guía Completa de Usuario")
    st.divider()

def create_learning_levels_section():
    """Create the learning levels overview section"""
    st.markdown(replace_emojis("## 📚 Niveles de Aprendizaje"), unsafe_allow_html=True)
    
    st.markdown("""
    Hemos creado **5 niveles progresivos** para guiarte paso a paso en el análisis de datos:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_step_card(
            step_number="0",
            title=replace_emojis("🌟 Nivel 0: Introducción"),
            description="Conceptos fundamentales de datos. Comienza aquí si eres completamente nuevo en análisis de datos"
        )
        
        create_step_card(
            step_number="1",
            title=replace_emojis("📚 Nivel 1: Básico"),
            description="Preparación y carga de datos. Aprende a preparar y cargar datos correctamente"
        )
        
        create_step_card(
            step_number="2",
            title=replace_emojis("🔍 Nivel 2: Filtros"), 
            description="Análisis y segmentación. Aprende a filtrar y segmentar tus datos"
        )
    
    with col2:
        create_step_card(
            step_number="3",
            title=replace_emojis("📊 Nivel 3: Métricas"),
            description="KPIs e interpretación. Crea métricas clave y entiende tus datos"
        )
        
        create_step_card(
            step_number="4",
            title=replace_emojis("🚀 Nivel 4: Avanzado"),
            description="Cálculos y visualizaciones. Análisis avanzado y visualizaciones complejas"
        )
    
    create_info_box(
        "info-box",
        replace_emojis("💡 Consejo"),
        "Si eres completamente nuevo, comienza con el Nivel 0. Si ya entiendes los conceptos básicos, puedes empezar en el Nivel 1."
    )

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

def create_visualization_guide():
    """Create the data visualization guide section"""
    st.markdown(replace_emojis("### 📊 Guía de Visualizaciones"), unsafe_allow_html=True)
    
    st.markdown("**Los gráficos correctos te ayudan a contar historias con tus datos.**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_step_card(
            step_number="1",
            title=replace_emojis("📊 Gráfico de Barras"),
            description=replace_emojis(
                "Comparar cantidades entre categorías\n"
                "Mostrar rankings (mejor a peor)\n"
                "Datos categóricos simples\n\n"
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
                "Mostrar cambios a lo largo del tiempo\n"
                "Ver tendencias y patrones\n"
                "Comparar múltiples series temporales\n\n"
                "**Ejemplos:**\n"
                "- Ventas diarias/mensuales\n"
                "- Evolución de precios\n"
                "- Crecimiento de usuarios\n\n"
                "**💡 Consejo:** Usa colores diferentes para cada línea"
            )
        )
    
    with col2:
        create_step_card(
            step_number="3",
            title="🥧 Gráfico Circular (Torta)",
            description="Mostrar proporciones de un total\n"
            "Máximo 5-6 categorías\n"
            "Cuando quieres mostrar 'parte del todo'\n\n"
            "**Ejemplos:**\n"
            "- Distribución de gastos\n"
            "- Participación de mercado\n"
            "- Fuentes de tráfico web\n\n"
            "**⚠️ Evita:** Muchas categorías pequeñas (se vuelve confuso)"
        )
        
        create_step_card(
            step_number="4",
            title=replace_emojis("🔄 Gráfico de Dispersión"),
            description=replace_emojis(
                "Ver relaciones entre dos variables\n"
                "Identificar correlaciones\n"
                "Encontrar valores atípicos\n\n"
                "**Ejemplos:**\n"
                "- Precio vs Calificación\n"
                "- Edad vs Gasto\n"
                "- Tiempo vs Satisfacción\n\n"
                "**💡 Consejo:** Agrega una línea de tendencia para ver la relación"
            )
        )

def create_common_scenarios():
    """Create common analysis scenarios section"""
    st.markdown(replace_emojis("### 🎯 Casos de Uso Comunes"), unsafe_allow_html=True)
    
    with st.expander("🛒 Análisis de Ventas"):
        st.markdown("""
        **Preguntas típicas que puedes responder:**
        
        #### 📊 ¿Qué productos venden mejor?
        - Agrupa por producto y suma cantidades
        - Ordena de mayor a menor
        - Identifica los top 10-20%
        
        #### 📅 ¿Cuándo vendo más?
        - Analiza ventas por día de la semana
        - Busca patrones mensuales/estacionales
        - Identifica fechas especiales (Black Friday, etc.)
        
        #### 👥 ¿Quiénes son mis mejores clientes?
        - Agrupa por cliente y suma compras
        - Identifica patrones de compra
        - Segmenta por valor de cliente
        """)
    
    with st.expander(replace_emojis("📈 Análisis de Tendencias")):
        st.markdown("""
        **Cómo identificar y analizar tendencias:**
        
        #### 📊 Compara períodos:
        - Este mes vs mes pasado
        - Busca patrones: ¿Qué días/meses son mejores?
        - Identifica estacionalidad: ¿Hay épocas del año mejores?
        - Proyecta el futuro: Basándote en tendencias pasadas
        
        #### 💡 Consejos:
        - Siempre considera el contexto (eventos, campañas, etc.)
        - No confíes solo en un período corto
        - Busca explicaciones para los cambios
        """)

def create_troubleshooting_section():
    """Create troubleshooting and common mistakes section"""
    st.markdown(replace_emojis("### 🔧 Solución de Problemas Comunes"), unsafe_allow_html=True)
    
    with st.expander(replace_emojis("🔍 ¿Por qué mis análisis no tienen sentido?")):
        st.markdown("""
        **Errores comunes de interpretación:**
        
        #### 📊 Comparando peras con manzanas:
        - **Problema**: Comparar datos de diferentes períodos o contextos
        - **Solución**: Asegúrate de que las comparaciones sean justas
        - **Ejemplo**: No compares ventas de enero (post-navidad) con diciembre
        
        #### 📈 Confundiendo correlación con causalidad:
        - **Problema**: Asumir que A causa B solo porque van juntos
        - **Solución**: Busca explicaciones lógicas y evidencia adicional
        - **Ejemplo**: Más helados se venden cuando hace calor, pero el calor no causa ventas
        
        #### 📊 Ignorando valores atípicos:
        - **Problema**: No investigar datos que se salen del patrón
        - **Solución**: Identifica y explica los valores atípicos
        - **Ejemplo**: Una venta muy alta puede ser un error o un cliente VIP
        
        #### 📅 Períodos de tiempo muy cortos:
        - **Problema**: Basar conclusiones en pocos datos
        - **Solución**: Usa períodos más largos para tendencias
        - **Ejemplo**: Una semana no es suficiente para ver patrones estacionales
        """)

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
    - **Actualizar**: Usa replace_emojis("🔄 Actualizar") para aplicar cambios
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

def create_learning_resources():
    """Create additional learning resources section"""
    st.markdown("""
    ---
    ### 📚 Recursos para Seguir Aprendiendo
    
    **Para profundizar en análisis de datos:**
    
    #### 📖 Conceptos Fundamentales:
    - **Estadística básica**: Promedios, medianas, desviación estándar
    - **Probabilidad**: Entender incertidumbre en los datos
    - **Muestreo**: Cómo obtener datos representativos
    - **Validación**: Verificar que tus conclusiones sean correctas
    
    #### 🛠️ Herramientas Recomendadas:
    - **Excel/Google Sheets**: Para análisis básicos y exploratorios
    - **Power BI/Tableau**: Para visualizaciones avanzadas
    - **Python/R**: Para análisis más complejos y automatización
    - **SQL**: Para consultar bases de datos grandes
    
    #### 🎯 Próximos Pasos:
    - **Practica con datos reales** de tu negocio o área de interés
    - **Únete a comunidades** de análisis de datos
    - **Toma cursos online** sobre estadística y visualización
    - **Lee blogs y artículos** sobre mejores prácticas
    
    ### 💡 Consejo Final
    
    **El análisis de datos es una habilidad que se mejora con la práctica.** 
    Comienza con preguntas simples y ve aumentando la complejidad gradualmente. 
    ¡No tengas miedo de experimentar y cometer errores - es parte del aprendizaje!
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
