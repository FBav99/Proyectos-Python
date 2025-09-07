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
    page_title="Nivel 0: Introducción - Conceptos de Datos",
    page_icon="🌟",
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

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
    st.title("🌟 Nivel 0: Introducción")
    st.subheader("Conceptos Fundamentales de Datos")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Introduction Section (what the user will learn)
    st.header("🎯 ¿Qué aprenderás en este nivel?")
    st.markdown("""
    En este nivel aprenderás los conceptos básicos sobre qué son los datos, qué tipos existen, 
    y qué puedes hacer con ellos. Es la base fundamental para entender todo lo que viene después.
    """)
    
    # 4. Steps Section (clear, actionable instructions)
    st.header("📋 Conceptos Fundamentales de Datos")
    
    # Step 1
    create_step_card(
        step_number="1",
        title="¿Qué son los datos?",
        description="<strong>¿Qué son los datos?</strong> Los datos son información que se puede medir, contar o describir. Son como las piezas de un rompecabezas que, cuando las organizas, te cuentan una historia.",
        sections={
            "📊 Ejemplos de datos en la vida real:": [
                "<strong>En una tienda:</strong> Cuántos productos vendiste, cuánto dinero ganaste",
                "<strong>En un restaurante:</strong> Qué platos pidieron más, cuánto tiempo tardan en servir",
                "<strong>En tu teléfono:</strong> Cuántos pasos caminaste, cuántas horas dormiste",
                "<strong>En el clima:</strong> La temperatura, si llovió, qué tan fuerte sopló el viento"
            ],
            "💡 ¿Por qué son importantes?": [
                "Te ayudan a tomar mejores decisiones",
                "Te muestran patrones que no ves a simple vista",
                "Te permiten medir si algo está funcionando bien o mal",
                "Te dan evidencia para respaldar tus ideas"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="2",
        title="Tipos de datos que existen",
        description="<strong>¿Qué tipos hay?</strong> Los datos vienen en diferentes formas. Conocer estos tipos te ayuda a entender mejor tu información y saber qué puedes hacer con ella.",
        sections={
            "🔢 Datos numéricos:": [
                "<strong>Números enteros:</strong> 1, 2, 3, 100 (cantidades, edades)",
                "<strong>Números decimales:</strong> 1.5, 3.14, 99.99 (precios, medidas)",
                "<strong>Porcentajes:</strong> 25%, 50%, 100% (descuentos, tasas de éxito)"
            ],
            "🔤 Datos de texto:": [
                "<strong>Nombres:</strong> Juan, María, Empresa ABC",
                "<strong>Categorías:</strong> Rojo, Azul, Verde / Pequeño, Mediano, Grande",
                "<strong>Descripciones:</strong> 'Producto de alta calidad'"
            ],
            "📅 Datos de fecha y hora:": [
                "<strong>Fechas:</strong> 15/03/2024, 2024-03-15",
                "<strong>Horas:</strong> 14:30, 2:30 PM",
                "<strong>Períodos:</strong> Enero 2024, Q1 2024"
            ],
            "✅ Datos de sí/no:": [
                "<strong>Verdadero/Falso:</strong> ¿Está activo? ¿Compró el producto?",
                "<strong>Sí/No:</strong> ¿Tiene seguro? ¿Es cliente VIP?"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="3",
        title="¿Qué puedes hacer con los datos?",
        description="<strong>¿Para qué sirven?</strong> Los datos te permiten hacer muchas cosas útiles. Aquí te mostramos las principales formas de usar la información.",
        sections={
            "📈 Descubrir tendencias:": [
                "<strong>¿Qué está pasando?</strong> Ver si las ventas suben o bajan",
                "<strong>¿Cuándo pasa?</strong> Identificar en qué momentos del año hay más actividad",
                "<strong>¿Por qué pasa?</strong> Entender las causas de los cambios"
            ],
            "🔍 Hacer comparaciones:": [
                "<strong>Comparar períodos:</strong> Este mes vs el mes pasado",
                "<strong>Comparar categorías:</strong> Producto A vs Producto B",
                "<strong>Comparar regiones:</strong> Norte vs Sur vs Este vs Oeste"
            ],
            "🎯 Encontrar patrones:": [
                "<strong>Patrones de tiempo:</strong> Los lunes siempre hay más ventas",
                "<strong>Patrones de comportamiento:</strong> Los clientes jóvenes compran más online",
                "<strong>Patrones estacionales:</strong> En diciembre siempre suben las ventas"
            ],
            "📊 Tomar decisiones:": [
                "<strong>Decidir qué hacer:</strong> ¿Abro una nueva sucursal?",
                "<strong>Decidir cuándo hacerlo:</strong> ¿Cuál es el mejor momento?",
                "<strong>Decidir cómo hacerlo:</strong> ¿Qué estrategia funciona mejor?"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="4",
        title="¿Cómo se ven los datos organizados?",
        description="<strong>¿Cómo se organizan?</strong> Los datos se organizan en tablas, como una hoja de Excel, donde cada fila es un registro y cada columna es un tipo de información.",
        sections={
            "📋 Estructura de una tabla:": [
                "<strong>Filas:</strong> Cada fila representa un registro (una venta, un cliente, un producto)",
                "<strong>Columnas:</strong> Cada columna representa un tipo de información (fecha, precio, cantidad)",
                "<strong>Encabezados:</strong> La primera fila tiene los nombres de las columnas"
            ],
            "📊 Ejemplo de datos de ventas:": [
                "| Fecha | Producto | Cantidad | Precio | Cliente |",
                "|-------|----------|----------|--------|---------|",
                "| 15/03 | Laptop   | 1        | $800   | Juan    |",
                "| 15/03 | Mouse    | 2        | $25    | María   |",
                "| 16/03 | Teclado  | 1        | $50    | Pedro   |"
            ],
            "💡 ¿Qué puedes ver en esta tabla?": [
                "Cuántas ventas hubo cada día",
                "Qué productos se vendieron más",
                "Cuánto dinero se ganó en total",
                "Quiénes son los clientes más activos"
            ]
        }
    )
    
    # Step 5
    create_step_card(
        step_number="5",
        title="¿Qué es el análisis de datos?",
        description="<strong>¿Qué significa analizar?</strong> Analizar datos significa examinar la información para encontrar respuestas, patrones y insights que te ayuden a tomar mejores decisiones.",
        sections={
            "🔍 Proceso de análisis:": [
                "<strong>1. Preguntar:</strong> ¿Qué quiero saber? ¿Qué problema quiero resolver?",
                "<strong>2. Recopilar:</strong> Obtener los datos necesarios",
                "<strong>3. Limpiar:</strong> Asegurarse de que los datos estén correctos",
                "<strong>4. Explorar:</strong> Ver qué hay en los datos",
                "<strong>5. Analizar:</strong> Buscar patrones y respuestas",
                "<strong>6. Comunicar:</strong> Contar lo que encontraste"
            ],
            "🎯 Tipos de preguntas que puedes responder:": [
                "<strong>¿Qué pasó?</strong> Las ventas bajaron 10% este mes",
                "<strong>¿Por qué pasó?</strong> Porque llovió mucho y la gente no salió",
                "<strong>¿Qué va a pasar?</strong> Si sigue lloviendo, las ventas seguirán bajando",
                "<strong>¿Qué debería hacer?</strong> Crear una campaña online para compensar"
            ],
            "💡 Beneficios del análisis:": [
                "Te ayuda a tomar decisiones basadas en hechos, no en suposiciones",
                "Te permite encontrar oportunidades que otros no ven",
                "Te ayuda a evitar problemas antes de que pasen",
                "Te da ventaja sobre la competencia"
            ]
        }
    )
    
    # 5. Optional media (images, diagrams, icons)
    st.header("🎥 Demostración Visual")
    try:
        display_level_gif("nivel0", "conceptos_datos")
    except:
        st.info("📹 GIF de demostración no disponible. Los conceptos incluyen: 1) Qué son los datos, 2) Tipos de datos, 3) Cómo organizarlos, 4) Qué puedes hacer con ellos.")
    
    # Example section
    st.header("🎯 Ejemplo Práctico")
    
    create_info_box(
        "info-box",
        "📊 Vamos a ver un ejemplo con datos de una tienda",
        "<p>Te mostraré cómo se ven los datos en la vida real y qué información puedes obtener de ellos.</p>"
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
    
    st.subheader("🔍 ¿Qué tipos de datos vemos aquí?")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**📋 Tipos de datos en esta tabla:**")
        
        create_info_box(
            "info-box",
            "📊 Tipos de datos identificados",
            "<p><strong>📅 Fecha:</strong> Datos de fecha y hora</p><p><strong>🔤 Producto:</strong> Datos de texto (nombres)</p><p><strong>🔤 Categoría:</strong> Datos de texto (categorías)</p><p><strong>🔢 Cantidad:</strong> Datos numéricos (números enteros)</p><p><strong>💰 Ventas:</strong> Datos numéricos (números decimales)</p><p><strong>🔤 Región:</strong> Datos de texto (ubicaciones)</p><p><strong>⭐ Calificación:</strong> Datos numéricos (escala 1-5)</p>"
        )
    
    with col2:
        st.markdown("**💡 ¿Qué puedes hacer con estos datos?**")
        
        create_info_box(
            "success-box",
            "🚀 Posibilidades de análisis",
            "<h4>📈 Descubrir tendencias:</h4><p>• Ver si las ventas suben o bajan con el tiempo</p><p>• Identificar qué días hay más ventas</p><h4>🔍 Hacer comparaciones:</h4><p>• Comparar ventas entre regiones</p><p>• Ver qué categorías venden más</p><h4>🎯 Encontrar patrones:</h4><p>• Productos con mejores calificaciones</p><p>• Relación entre cantidad y ventas</p>"
        )
    
    # Tips section
    st.header("💡 Consejos Importantes")
    
    create_info_box(
        "warning-box",
        "⚠️ Errores comunes a evitar",
        "<ul><li><strong>No entender qué son los datos:</strong> Los datos son información, no solo números</li><li><strong>Ignorar el contexto:</strong> Los datos sin contexto no te dicen nada útil</li><li><strong>Buscar solo números grandes:</strong> A veces los datos pequeños son más importantes</li><li><strong>No hacer preguntas:</strong> Sin preguntas claras, los datos no te ayudan</li></ul>"
    )
    
    create_info_box(
        "success-box",
        "✅ Buenas prácticas",
        "<ul><li><strong>Haz preguntas claras:</strong> Antes de analizar, define qué quieres saber</li><li><strong>Entiende el contexto:</strong> Conoce de dónde vienen los datos y qué representan</li><li><strong>Empieza simple:</strong> Comienza con preguntas básicas antes de las complejas</li><li><strong>Busca patrones:</strong> Los datos te cuentan historias, aprende a escucharlas</li></ul>"
    )
    
    # Practice activity
    st.header("🎯 Actividad Práctica")
    
    create_info_box(
        "card",
        "📝 Ejercicio para practicar",
        "<ol><li><strong>Observa los datos de ejemplo:</strong> Mira la tabla de ventas de arriba</li><li><strong>Identifica los tipos de datos:</strong> ¿Qué columnas son números? ¿Cuáles son texto?</li><li><strong>Haz preguntas:</strong> ¿Qué quieres saber sobre estos datos?</li><li><strong>Busca patrones:</strong> ¿Ves algo interesante en los números?</li><li><strong>Piensa en aplicaciones:</strong> ¿Cómo podrías usar esta información?</li></ol>"
    )
    
    # Interactive example
    st.header("🎮 Ejemplo Interactivo")
    
    create_info_box(
        "info-box",
        "🚀 Explora los datos por ti mismo",
        "<p>Usa los controles de abajo para ver diferentes aspectos de los datos y entender mejor cómo funcionan.</p>"
    )
    
    # Simple interactive controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Ver datos por categoría:**")
        categoria_seleccionada = st.selectbox(
            "Selecciona una categoría",
            ['Todas'] + list(df['Categoria'].unique())
        )
    
    with col2:
        st.markdown("**📊 Ver estadísticas básicas:**")
        mostrar_estadisticas = st.checkbox("Mostrar estadísticas", value=True)
    
    # Apply filters and show results
    if categoria_seleccionada != 'Todas':
        df_filtrado = df[df['Categoria'] == categoria_seleccionada]
        st.markdown(f"**📋 Datos filtrados por categoría: {categoria_seleccionada}**")
        st.dataframe(df_filtrado, use_container_width=True)
        
        if mostrar_estadisticas:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de ventas", f"${df_filtrado['Ventas'].sum():,.2f}")
            with col2:
                st.metric("Promedio de ventas", f"${df_filtrado['Ventas'].mean():.2f}")
            with col3:
                st.metric("Registros", len(df_filtrado))
    else:
        st.markdown("**📋 Todos los datos:**")
        st.dataframe(df, use_container_width=True)
        
        if mostrar_estadisticas:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de ventas", f"${df['Ventas'].sum():,.2f}")
            with col2:
                st.metric("Promedio de ventas", f"${df['Ventas'].mean():.2f}")
            with col3:
                st.metric("Registros", len(df))
    
    # 6. Navigation or next steps
    st.header("✅ Verificación del Nivel")
    nivel0_completed = st.checkbox(
        "He completado todos los pasos del Nivel 0",
        value=st.session_state.get('nivel0_completed', False),
        key='nivel0_checkbox'
    )
    
    if nivel0_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel0', True):
            st.session_state['nivel0_completed'] = True
        else:
            st.error("❌ Error al guardar el progreso. Intenta de nuevo.")
            return
        
        create_info_box(
            "success-box",
            "🎉 ¡Felicidades! Has completado el Nivel 0",
            "<p>Ahora entiendes los conceptos básicos de los datos. Estás listo para continuar con el siguiente nivel donde aprenderás a preparar y cargar datos.</p>"
        )
        
        st.subheader("🚀 ¿Qué sigue?")
        st.markdown("En el **Nivel 1** aprenderás a preparar y cargar datos correctamente.")
        
        if st.button("Continuar al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    # Additional resources
    create_info_box(
        "info-box",
        "📚 ¿Quieres saber más?",
        "<p>Este nivel está basado en fundamentos de ciencia de datos y mejores prácticas de la industria. Los conceptos que aprendiste aquí son la base para todo análisis de datos.</p>"
    )

if __name__ == "__main__":
    main()
