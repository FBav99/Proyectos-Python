import streamlit as st

# Page config
st.set_page_config(
    page_title="Ayuda - Guía de Usuario",
    page_icon="❓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .help-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .level-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .feature-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="help-header">❓ Centro de Ayuda</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Guía Completa de Usuario</h2>', unsafe_allow_html=True)
    
    st.divider()
    
    # Introduction
    st.markdown("""
    ## 🎯 Bienvenido al Panel de Análisis de Datos
    
    Esta herramienta te permite analizar tus datos de manera fácil e intuitiva. 
    Ya seas un principiante o un usuario avanzado, encontrarás funcionalidades útiles para tu análisis.
    """)
    
    # Learning Levels Overview
    st.markdown("## 📚 Niveles de Aprendizaje")
    
    st.markdown("""
    Hemos creado **4 niveles progresivos** para guiarte paso a paso en el análisis de datos:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📚 Nivel 1: Básico** - Preparación y carga de datos  
        **🔍 Nivel 2: Filtros** - Análisis y segmentación  
        """)
    
    with col2:
        st.markdown("""
        **📊 Nivel 3: Métricas** - KPIs e interpretación  
        **🚀 Nivel 4: Avanzado** - Cálculos y visualizaciones  
        """)
    
    st.info("💡 **Consejo**: Si eres nuevo, comienza con el Nivel 1. Si ya tienes experiencia, puedes saltar al nivel que necesites.")
    
    # Quick Start Guide
    st.markdown("## 🚀 Guía de Inicio Rápido")
    
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 📋 Para Principiantes:")
    st.markdown("""
    1. **Comienza con el Nivel 1** - Aprende a preparar y cargar datos
    2. **Practica con datos de ejemplo** - Usa los datos incluidos para familiarizarte
    3. **Sigue los pasos paso a paso** - Cada nivel tiene ejercicios prácticos
    4. **No tengas miedo de experimentar** - Puedes volver a cualquier nivel
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 🔧 Para Usuarios Avanzados:")
    st.markdown("""
    1. **Ve directamente al Nivel 4** - Si ya conoces los conceptos básicos
    2. **Carga tus propios datos** - Usa archivos CSV o Excel de tu negocio
    3. **Explora cálculos personalizados** - Crea métricas específicas para tu análisis
    4. **Genera visualizaciones** - Crea gráficos informativos para presentaciones
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comprehensive Data Analysis Help
    st.markdown("## 📚 Guía Completa de Análisis de Datos")
    
    st.markdown("""
    Esta sección te ayudará a entender los conceptos fundamentales del análisis de datos, 
    independientemente de la herramienta que uses. ¡Aprende los principios que te servirán para siempre!
    """)
    
    # Data Preparation Section
    st.markdown("### 📋 Preparación de Datos")
    
    with st.expander("🔧 ¿Cómo preparar mis datos correctamente?"):
        st.markdown("""
        **La preparación de datos es el 80% del trabajo de análisis. ¡Hazlo bien desde el principio!**
        
        #### ✅ Estructura Correcta:
        - **Una fila = un registro** (ej: una venta, un cliente, una transacción)
        - **Una columna = una característica** (ej: fecha, producto, precio)
        - **Primera fila = nombres de columnas** (encabezados)
        - **Sin filas vacías** en medio de los datos
        
        #### 📊 Tipos de Datos:
        - **Texto**: Nombres, categorías, descripciones
        - **Números**: Precios, cantidades, edades
        - **Fechas**: Fechas de venta, nacimiento, etc.
        - **Booleanos**: Sí/No, Verdadero/Falso
        
        #### ⚠️ Errores Comunes:
        - Mezclar tipos de datos en la misma columna
        - Usar formatos de fecha inconsistentes
        - Tener valores vacíos sin manejar
        - Nombres de columnas con espacios o caracteres especiales
        """)
    
    # Data Analysis Concepts
    st.markdown("### 🔍 Conceptos de Análisis")
    
    with st.expander("📊 ¿Qué son las métricas y KPIs?"):
        st.markdown("""
        **Las métricas son números que te dicen algo importante sobre tu negocio.**
        
        #### 💰 Métricas Financieras:
        - **Ingresos**: Dinero que entra a tu negocio
        - **Gastos**: Dinero que sale de tu negocio
        - **Ganancia**: Ingresos - Gastos
        - **Margen**: (Ganancia / Ingresos) × 100
        
        #### 📈 Métricas de Rendimiento:
        - **Cantidad vendida**: Cuántas unidades vendiste
        - **Valor promedio**: Ingresos totales ÷ Número de ventas
        - **Tasa de conversión**: (Ventas / Visitas) × 100
        - **Retención**: Porcentaje de clientes que regresan
        
        #### 🎯 KPIs (Indicadores Clave):
        - **Son las métricas más importantes** para tu negocio
        - **Te ayudan a tomar decisiones** rápidas
        - **Deben ser fáciles de entender** y medir
        - **Deben cambiar con el tiempo** para ver tendencias
        """)
    
    with st.expander("📅 ¿Cómo analizar tendencias temporales?"):
        st.markdown("""
        **Las tendencias te muestran cómo cambian las cosas a lo largo del tiempo.**
        
        #### 📈 Tipos de Tendencias:
        - **Crecimiento**: Los números van subiendo
        - **Decrecimiento**: Los números van bajando
        - **Estable**: Los números se mantienen igual
        - **Estacional**: Patrones que se repiten (ej: ventas navideñas)
        
        #### 🔍 Análisis Temporal:
        - **Compara períodos**: Este mes vs mes pasado
        - **Busca patrones**: ¿Qué días/meses son mejores?
        - **Identifica estacionalidad**: ¿Hay épocas del año mejores?
        - **Proyecta el futuro**: Basándote en tendencias pasadas
        
        #### 💡 Consejos:
        - Siempre considera el contexto (eventos, campañas, etc.)
        - No confíes solo en un período corto
        - Busca explicaciones para los cambios
        """)
    
    # Data Visualization Guide
    st.markdown("### 📊 Guía de Visualizaciones")
    
    st.markdown("""
    **Los gráficos correctos te ayudan a contar historias con tus datos.**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📊 Gráfico de Barras
        **Cuándo usarlo:**
        - Comparar cantidades entre categorías
        - Mostrar rankings (mejor a peor)
        - Datos categóricos simples
        
        **Ejemplos:**
        - Ventas por producto
        - Ingresos por región
        - Número de clientes por categoría
        
        **💡 Consejo:** Ordena las barras de mayor a menor para mejor lectura
        """)
        
        st.markdown("""
        #### 📈 Gráfico de Líneas
        **Cuándo usarlo:**
        - Mostrar cambios a lo largo del tiempo
        - Ver tendencias y patrones
        - Comparar múltiples series temporales
        
        **Ejemplos:**
        - Ventas diarias/mensuales
        - Evolución de precios
        - Crecimiento de usuarios
        
        **💡 Consejo:** Usa colores diferentes para cada línea
        """)
    
    with col2:
        st.markdown("""
        #### 🥧 Gráfico Circular (Torta)
        **Cuándo usarlo:**
        - Mostrar proporciones de un total
        - Máximo 5-6 categorías
        - Cuando quieres mostrar "parte del todo"
        
        **Ejemplos:**
        - Distribución de gastos
        - Participación de mercado
        - Fuentes de tráfico web
        
        **⚠️ Evita:** Muchas categorías pequeñas (se vuelve confuso)
        """)
        
        st.markdown("""
        #### 🔄 Gráfico de Dispersión
        **Cuándo usarlo:**
        - Ver relaciones entre dos variables
        - Identificar correlaciones
        - Encontrar valores atípicos
        
        **Ejemplos:**
        - Precio vs Calificación
        - Edad vs Gasto
        - Tiempo vs Satisfacción
        
        **💡 Consejo:** Agrega una línea de tendencia para ver la relación
        """)
    
    # Common Analysis Scenarios
    st.markdown("### 🎯 Casos de Uso Comunes")
    
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
        - Calcula frecuencia de compra
        - Identifica valor promedio por cliente
        
        #### 💰 ¿Cuál es mi margen por producto?
        - Calcula: (Precio de venta - Costo) / Precio de venta
        - Identifica productos más rentables
        - Enfócate en productos de alto margen
        """)
    
    with st.expander("📈 Análisis de Marketing"):
        st.markdown("""
        **Métricas clave para evaluar campañas:**
        
        #### 🎯 Efectividad de Campañas:
        - **ROI**: (Ganancia - Inversión) / Inversión × 100
        - **Costo por adquisición**: Inversión / Nuevos clientes
        - **Tasa de conversión**: Ventas / Visitas × 100
        
        #### 📊 Canales de Marketing:
        - Compara rendimiento por canal
        - Identifica canales más rentables
        - Optimiza presupuesto por canal
        
        #### 👥 Segmentación de Audiencia:
        - Analiza comportamiento por edad, ubicación, etc.
        - Personaliza mensajes por segmento
        - Identifica segmentos más valiosos
        """)
    
    with st.expander("📊 Análisis de Satisfacción"):
        st.markdown("""
        **Cómo interpretar feedback de clientes:**
        
        #### ⭐ Calificaciones:
        - **Promedio general**: Suma todas las calificaciones ÷ Número total
        - **Distribución**: Cuántos dan 1, 2, 3, 4, 5 estrellas
        - **Tendencia**: ¿Mejoran o empeoran las calificaciones?
        
        #### 📝 Comentarios:
        - Identifica palabras más frecuentes
        - Categoriza por sentimiento (positivo/negativo)
        - Busca temas recurrentes
        
        #### 🔄 Correlaciones:
        - ¿Qué factores afectan la satisfacción?
        - ¿Clientes satisfechos compran más?
        - ¿Productos con mejor calificación venden más?
        """)
    
    # Best Practices
    st.markdown("### 💡 Mejores Prácticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ✅ Hacer:
        - **Define tu pregunta** antes de analizar
        - **Limpia tus datos** antes de empezar
        - **Usa gráficos apropiados** para cada tipo de dato
        - **Contextualiza** tus hallazgos
        - **Documenta** tus análisis
        
        #### ❌ Evitar:
        - Analizar sin un objetivo claro
        - Ignorar valores atípicos sin investigar
        - Usar gráficos complejos cuando simples funcionan
        - Confundir correlación con causalidad
        - Olvidar el contexto del negocio
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Consejos para Presentaciones:
        - **Una gráfica = una idea** principal
        - **Usa títulos descriptivos** y claros
        - **Incluye contexto** (período, fuente, etc.)
        - **Destaca insights** importantes
        - **Prepara respuestas** a preguntas comunes
        
        #### 🔍 Preguntas para Validar:
        - ¿Los datos tienen sentido?
        - ¿Hay valores atípicos que explican?
        - ¿La muestra es representativa?
        - ¿Los cambios son significativos?
        - ¿Qué más necesito saber?
        """)
    
    # Tips and Best Practices
    st.markdown("## 💡 Consejos y Mejores Prácticas")
    
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 📋 Preparación de Datos:")
    st.markdown("""
    - **Formato consistente**: Usa el mismo formato para fechas (YYYY-MM-DD)
    - **Encabezados claros**: Nombres descriptivos sin espacios
    - **Datos limpios**: Elimina valores duplicados o inconsistentes
    - **Tamaño de archivo**: Para mejor rendimiento, usa archivos < 10MB
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 🔍 Análisis Efectivo:")
    st.markdown("""
    - **Pregunta específica**: Define qué quieres descubrir
    - **Filtros graduales**: Aplica filtros uno por uno
    - **Compara períodos**: Analiza tendencias temporales
    - **Documenta insights**: Guarda tus hallazgos importantes
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Troubleshooting
    st.markdown("## 🔧 Solución de Problemas Comunes")
    
    with st.expander("❌ ¿Por qué mis datos no se ven correctamente?"):
        st.markdown("""
        **Problemas frecuentes y cómo solucionarlos:**
        
        #### 📊 Datos mezclados o confusos:
        - **Problema**: Números y texto en la misma columna
        - **Solución**: Separa en columnas diferentes o limpia los datos
        - **Ejemplo**: "100 unidades" → Columna "Cantidad": 100, Columna "Unidad": "unidades"
        
        #### 📅 Fechas que no se reconocen:
        - **Problema**: Formato inconsistente (01/01/2023 vs 2023-01-01)
        - **Solución**: Usa un formato consistente como YYYY-MM-DD
        - **Ejemplo**: Convierte "01/01/2023" a "2023-01-01"
        
        #### 🔢 Números que se ven como texto:
        - **Problema**: Números con comas, puntos o símbolos de moneda
        - **Solución**: Limpia los caracteres especiales
        - **Ejemplo**: "$1,234.56" → 1234.56
        
        #### 📋 Valores vacíos o faltantes:
        - **Problema**: Celdas vacías o con "N/A", "NULL", etc.
        - **Solución**: Decide si eliminar filas o usar valores por defecto
        - **Ejemplo**: Reemplaza vacíos con 0 o "Sin especificar"
        """)
    
    with st.expander("📈 ¿Por qué mis gráficos no se ven bien?"):
        st.markdown("""
        **Problemas comunes de visualización:**
        
        #### 🥧 Gráfico circular muy confuso:
        - **Problema**: Demasiadas categorías pequeñas
        - **Solución**: Agrupa categorías pequeñas en "Otros"
        - **Regla**: Máximo 5-6 categorías principales
        
        #### 📊 Barras muy pequeñas o grandes:
        - **Problema**: Escala inapropiada para los datos
        - **Solución**: Ajusta el rango del eje Y
        - **Consejo**: Comienza el eje en 0 para comparaciones justas
        
        #### 📈 Línea temporal sin patrón claro:
        - **Problema**: Demasiados puntos de datos
        - **Solución**: Agrupa por períodos (días → semanas → meses)
        - **Ejemplo**: Ventas diarias → Ventas semanales para ver tendencias
        
        #### 🎨 Colores que no se distinguen:
        - **Problema**: Colores muy similares
        - **Solución**: Usa paletas de colores contrastantes
        - **Consejo**: Considera usuarios con daltonismo
        """)
    
    with st.expander("🔍 ¿Por qué mis análisis no tienen sentido?"):
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
    
    # Navigation
    st.divider()
    
    st.markdown("## 🎯 ¿Listo para Comenzar?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 Comenzar Nivel 1", type="primary", key="ayuda_nivel1"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col2:
        if st.button("🏠 Dashboard Principal", key="ayuda_dashboard"):
            st.switch_page("Inicio.py")
    
    with col3:
        if st.button("📊 Nivel 4 Avanzado", key="ayuda_nivel4"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col4:
        if st.button("🔍 Nivel 2 Filtros", key="ayuda_nivel2"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    # Additional Learning Resources
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

if __name__ == "__main__":
    main()
