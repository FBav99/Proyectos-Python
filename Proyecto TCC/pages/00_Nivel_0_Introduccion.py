import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data, analyze_uploaded_data
from utils.learning.learning_progress import save_level_progress
from utils.learning.level_components import create_progression_summary, create_level_preview, create_achievement_display
from utils.learning.level_data import get_data_progression_info
from utils.ui import auth_ui
from utils.ui.icon_system import get_icon, replace_emojis
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Nivel 0: Introducción - Conceptos de Datos",
    page_icon=get_icon("🌟", 20),
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Principal - Nivel 0 Introduccion
@safe_main
def main():
    # UI - Inicializar Sidebar con Info de Usuario
    current_user = init_sidebar()
    
    # Validacion - Verificar Autenticacion de Usuario
    if not current_user:
        st.markdown(replace_emojis("🔐 Por favor inicia sesión para acceder a este nivel."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Usuario - Obtener Usuario Actual
    user = current_user
    if not user or 'id' not in user:
        st.markdown(replace_emojis("❌ Error: No se pudo obtener la información del usuario."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Title (level name and description)
    st.title(replace_emojis("🌟 Nivel 0: Introducción"))
    st.subheader("Conceptos Fundamentales de Datos")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Progression Summary
    create_progression_summary(progress)
    
    # 4. Level Preview
    create_level_preview('nivel0')
    
    # 5. Introduction Section (what the user will learn)
    st.header(replace_emojis("🎯 ¿Qué aprenderás en este nivel?"))
    st.markdown("En este nivel aprenderás los conceptos básicos sobre qué son los datos, qué tipos existen, y qué puedes hacer con ellos. Es la base fundamental para entender todo lo que viene después.")
    
    # UI - Agregar Contexto Narrativo
    create_info_box(
        "info-box",
        "🏪 Bienvenido a TechStore",
        "<p>Durante todo el curso, trabajaremos con datos de <strong>TechStore</strong>, una tienda de tecnología que necesita analizar sus ventas para tomar mejores decisiones. En este nivel, aprenderás los conceptos básicos que necesitas para entender estos datos.</p>"
    )
    
    # 6. Steps Section (clear, actionable instructions)
    st.header(replace_emojis("📋 Conceptos Fundamentales de Datos"))
    
    # Step 1
    create_step_card(
        step_number="0.1",
        title="¿Qué son los datos?",
        description="<strong>¿Qué son los datos?</strong> Los datos son información que se puede medir, contar o describir. Son como las piezas de un rompecabezas que, cuando las organizas, te cuentan una historia.",
        sections={
            replace_emojis("📊 Ejemplos de datos en la vida real:"): [
                "<strong>En una tienda:</strong> Cuántos productos vendiste, cuánto dinero ganaste",
                "<strong>En un restaurante:</strong> Qué platos pidieron más, cuánto tiempo tardan en servir",
                "<strong>En tu teléfono:</strong> Cuántos pasos caminaste, cuántas horas dormiste",
                "<strong>En el clima:</strong> La temperatura, si llovió, qué tan fuerte sopló el viento"
            ],
            replace_emojis("💡 ¿Por qué son importantes?"): [
                "Te ayudan a tomar mejores decisiones",
                "Te muestran patrones que no ves a simple vista",
                "Te permiten medir si algo está funcionando bien o mal",
                "Te dan evidencia para respaldar tus ideas"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="0.2",
        title="Tipos de datos que existen",
        description="<strong>¿Qué tipos hay?</strong> Los datos vienen en diferentes formas. Conocer estos tipos te ayuda a entender mejor tu información y saber qué puedes hacer con ella.",
        sections={
            replace_emojis("🔢 Datos numéricos:"): [
                "<strong>Números enteros:</strong> 1, 2, 3, 100 (cantidades, edades)",
                "<strong>Números decimales:</strong> 1.5, 3.14, 99.99 (precios, medidas)",
                "<strong>Porcentajes:</strong> 25%, 50%, 100% (descuentos, tasas de éxito)"
            ],
            replace_emojis("🔤 Datos de texto:"): [
                "<strong>Nombres:</strong> Juan, María, Empresa ABC",
                "<strong>Categorías:</strong> Rojo, Azul, Verde / Pequeño, Mediano, Grande",
                "<strong>Descripciones:</strong> 'Producto de alta calidad'"
            ],
            replace_emojis("📅 Datos de fecha y hora:"): [
                "<strong>Fechas:</strong> 15/03/2024, 2024-03-15",
                "<strong>Horas:</strong> 14:30, 2:30 PM",
                "<strong>Períodos:</strong> Enero 2024, Q1 2024"
            ],
            replace_emojis("✅ Datos de sí/no:"): [
                "<strong>Verdadero/Falso:</strong> ¿Está activo? ¿Compró el producto?",
                "<strong>Sí/No:</strong> ¿Tiene seguro? ¿Es cliente VIP?"
            ],
            "🛰️ Datos especiales:": [
                "<strong>Datos geográficos:</strong> Coordenadas, mapas, direcciones, rutas de entrega",
                "<strong>Imágenes:</strong> Fotos de productos, radiografías, planos de ingeniería",
                "<strong>Audio y video:</strong> Grabaciones de llamadas, entrevistas, cámaras de seguridad",
                "<strong>Sensores e IoT:</strong> Temperatura, humedad, pulso cardiaco, datos de dispositivos inteligentes"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="0.3",
        title="¿Qué puedes hacer con los datos?",
        description="<strong>¿Para qué sirven?</strong> Los datos te permiten hacer muchas cosas útiles. Aquí te mostramos las principales formas de usar la información.",
        sections={
            replace_emojis("📈 Descubrir tendencias:"): [
                "<strong>¿Qué está pasando?</strong> Ver si las ventas suben o bajan",
                "<strong>¿Cuándo pasa?</strong> Identificar en qué momentos del año hay más actividad",
                "<strong>¿Por qué pasa?</strong> Entender las causas de los cambios"
            ],
            replace_emojis("🔍 Hacer comparaciones:"): [
                "<strong>Comparar períodos:</strong> Este mes vs el mes pasado",
                "<strong>Comparar categorías:</strong> Producto A vs Producto B",
                "<strong>Comparar regiones:</strong> Norte vs Sur vs Este vs Oeste"
            ],
            replace_emojis("🎯 Encontrar patrones:"): [
                "<strong>Patrones de tiempo:</strong> Los lunes siempre hay más ventas",
                "<strong>Patrones de comportamiento:</strong> Los clientes jóvenes compran más online",
                "<strong>Patrones estacionales:</strong> En diciembre siempre suben las ventas"
            ],
            replace_emojis("📊 Tomar decisiones:"): [
                "<strong>Decidir qué hacer:</strong> ¿Abro una nueva sucursal?",
                "<strong>Decidir cuándo hacerlo:</strong> ¿Cuál es el mejor momento?",
                "<strong>Decidir cómo hacerlo:</strong> ¿Qué estrategia funciona mejor?"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="0.4",
        title="¿Cómo se ven los datos organizados?",
        description="<strong>¿Cómo se organizan?</strong> Los datos se organizan en tablas, como una hoja de Excel, donde cada fila es un registro y cada columna es un tipo de información.",
        sections={
            replace_emojis("📋 Estructura de una tabla:"): [
                "<strong>Filas:</strong> Cada fila representa un registro (una venta, un cliente, un producto)",
                "<strong>Columnas:</strong> Cada columna representa un tipo de información (fecha, precio, cantidad)",
                "<strong>Encabezados:</strong> La primera fila tiene los nombres de las columnas"
            ],
            replace_emojis("📊 Ejemplo de datos de ventas:"): [
                "| Fecha | Producto | Cantidad | Precio | Cliente |",
                "|-------|----------|----------|--------|---------|",
                "| 15/03 | Laptop   | 1        | $800   | Juan    |",
                "| 15/03 | Mouse    | 2        | $25    | María   |",
                "| 16/03 | Teclado  | 1        | $50    | Pedro   |"
            ],
            replace_emojis("💡 ¿Qué puedes ver en esta tabla?"): [
                "Cuántas ventas hubo cada día",
                "Qué productos se vendieron más",
                "Cuánto dinero se ganó en total",
                "Quiénes son los clientes más activos"
            ]
        }
    )
    
    # Step 5
    create_step_card(
        step_number="0.5",
        title="¿Qué es el análisis de datos?",
        description="<strong>¿Qué significa analizar?</strong> Analizar datos significa examinar la información para encontrar respuestas, patrones y insights que te ayuden a tomar mejores decisiones.",
        sections={
            replace_emojis("🔍 Proceso de análisis:"): [
                "<strong>1. Preguntar:</strong> ¿Qué quiero saber? ¿Qué problema quiero resolver?",
                "<strong>2. Recopilar:</strong> Obtener los datos necesarios",
                "<strong>3. Limpiar:</strong> Asegurarse de que los datos estén correctos",
                "<strong>4. Explorar:</strong> Ver qué hay en los datos",
                "<strong>5. Analizar:</strong> Buscar patrones y respuestas",
                "<strong>6. Comunicar:</strong> Contar lo que encontraste"
            ],
            replace_emojis("🎯 Tipos de preguntas que puedes responder:"): [
                "<strong>¿Qué pasó?</strong> Las ventas bajaron 10% este mes",
                "<strong>¿Por qué pasó?</strong> Porque llovió mucho y la gente no salió",
                "<strong>¿Qué va a pasar?</strong> Si sigue lloviendo, las ventas seguirán bajando",
                "<strong>¿Qué debería hacer?</strong> Crear una campaña online para compensar"
            ],
            replace_emojis("💡 Beneficios del análisis:"): [
                "Te ayuda a tomar decisiones basadas en hechos, no en suposiciones",
                "Te permite encontrar oportunidades que otros no ven",
                "Te ayuda a evitar problemas antes de que pasen",
                "Te da ventaja sobre la competencia"
            ]
        }
    )
    
    # 5. Optional media (images, diagrams, icons)
    st.header(replace_emojis("🎥 Demostración Visual"))
    try:
        display_level_gif("nivel0", "conceptos_datos")
    except:
        st.info(replace_emojis("📹 GIF de demostración no disponible. Los conceptos incluyen: 1) Qué son los datos, 2) Tipos de datos, 3) Cómo organizarlos, 4) Qué puedes hacer con ellos."))
    
    # UI - Mostrar Seccion de Ejemplo
    st.header(replace_emojis("🎯 Ejemplo Práctico"))
    
    create_info_box(
        "info-box",
        replace_emojis("📊 Vamos a ver un ejemplo con datos de TechStore"),
        "<p>Te mostraré cómo se ven los datos de TechStore en la vida real y qué información puedes obtener de ellos. Estos mismos datos los usarás en todos los niveles del curso, pero en diferentes estados de calidad.</p>"
    )
    
    # UI - Mostrar Progresion de Datos
    create_info_box(
        "success-box",
        replace_emojis("🔄 Progresión de Datos en el Curso"),
        "<p><strong>Nivel 0:</strong> Datos organizados para aprender conceptos<br/><strong>Nivel 1:</strong> Datos con problemas para aprender preparación<br/><strong>Nivel 2-4:</strong> Datos limpios para análisis avanzados</p>"
    )
    
    df = create_sample_data('clean')  # Use clean data for Level 0
    st.subheader(replace_emojis("📁 Datos de ejemplo (Ventas de TechStore)"))
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df.head(10), use_container_width=True)
        st.caption("Primeras 10 filas de datos")
    with col2:
        st.markdown(replace_emojis("**📊 Información básica:**"), unsafe_allow_html=True)
        st.metric("Total de registros", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Período", f"{df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')}")
    
    st.subheader(replace_emojis("🔍 ¿Qué tipos de datos vemos aquí?"))
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(replace_emojis("**📋 Tipos de datos en esta tabla:**"), unsafe_allow_html=True)
        
        create_info_box(
            "info-box",
            replace_emojis("📊 Tipos de datos identificados"),
            replace_emojis("<p><strong>📅 Fecha:</strong> Datos de fecha y hora</p><p><strong>🔤 Producto:</strong> Datos de texto (nombres)</p><p><strong>🔤 Categoría:</strong> Datos de texto (categorías)</p><p><strong>🔢 Cantidad:</strong> Datos numéricos (números enteros)</p><p><strong>💰 Ventas:</strong> Datos numéricos (números decimales)</p><p><strong>🔤 Región:</strong> Datos de texto (ubicaciones)</p><p><strong>⭐ Calificación:</strong> Datos numéricos (escala 1-5)</p>")
        )
    
    with col2:
        st.markdown(replace_emojis("**💡 ¿Qué puedes hacer con estos datos?**"), unsafe_allow_html=True)
        
        create_info_box(
            "success-box",
            replace_emojis("🚀 Posibilidades de análisis"),
            replace_emojis("<h4>📈 Descubrir tendencias:</h4><p>• Ver si las ventas suben o bajan con el tiempo</p><p>• Identificar qué días hay más ventas</p><h4>🔍 Hacer comparaciones:</h4><p>• Comparar ventas entre regiones</p><p>• Ver qué categorías venden más</p><h4>🎯 Encontrar patrones:</h4><p>• Productos con mejores calificaciones</p><p>• Relación entre cantidad y ventas</p>")
        )
    
    # UI - Agregar Comparacion de Datos Sucios vs Limpios
    st.subheader(replace_emojis("🔄 Comparación: Datos Limpios vs Datos con Problemas"))
    
    create_info_box(
        "info-box",
        replace_emojis("📚 ¿Por qué es importante ver ambos tipos?"),
        "<p>En la vida real, los datos no siempre vienen perfectos. Es importante entender qué problemas pueden tener los datos y cómo afectan el análisis.</p>"
    )
    
    # Datos - Obtener Datos Sucios y Limpios
    df_clean = create_sample_data('clean')
    df_dirty = create_sample_data('dirty')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✨ Datos Limpios (Como los que viste arriba):**")
        st.dataframe(df_clean.head(6), use_container_width=True)
        
        st.markdown(replace_emojis("**✅ Características de datos limpios:**"), unsafe_allow_html=True)
        clean_features = [
            replace_emojis("✅ Todos los datos están completos"),
            "✅ Nombres consistentes (Electronica, no 'ELECTRONICA')",
            replace_emojis("✅ Calificaciones válidas (1-5)"),
            replace_emojis("✅ Fechas en formato correcto"),
            replace_emojis("✅ Sin filas duplicadas"),
            replace_emojis("✅ Valores realistas")
        ]
        for feature in clean_features:
            st.markdown(f"- {feature}")
    
    with col2:
        st.markdown("**⚠️ Datos con Problemas (Como vienen en la vida real):**")
        st.dataframe(df_dirty.head(6), use_container_width=True)
        
        st.markdown(replace_emojis("**❌ Problemas comunes en datos reales:**"), unsafe_allow_html=True)
        dirty_features = [
            replace_emojis("❌ Datos faltantes (celdas vacías)"),
            replace_emojis("❌ Nombres inconsistentes (Electronica vs ELECTRONICA)"),
            replace_emojis("❌ Calificaciones inválidas (6, 0, -1)"),
            replace_emojis("❌ Fechas en diferentes formatos"),
            replace_emojis("❌ Filas duplicadas"),
            replace_emojis("❌ Valores atípicos o imposibles")
        ]
        for feature in dirty_features:
            st.markdown(f"- {feature}")
    
    # UI - Mostrar Impacto de Limpieza
    st.markdown(replace_emojis("**📈 ¿Por qué importa esta diferencia?**"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Datos limpios", len(df_clean), "✅ Listos para analizar")
        st.metric("Datos con problemas", len(df_dirty), "⚠️ Necesitan limpieza")
    
    with col2:
        st.metric("Datos faltantes", df_dirty.isnull().sum().sum(), "❌ En datos problemáticos")
        st.metric("Filas duplicadas", df_dirty.duplicated().sum(), "❌ En datos problemáticos")
    
    with col3:
        st.metric("Calificaciones válidas", f"{(df_clean['Calificacion'].between(1, 5).sum() / len(df_clean) * 100):.0f}%", "✅ En datos limpios")
        st.metric("Calificaciones válidas", f"{(df_dirty['Calificacion'].between(1, 5).sum() / len(df_dirty) * 100):.0f}%", "⚠️ En datos problemáticos")
    
    create_info_box(
        "warning-box",
        "⚠️ ¿Qué pasa si usas datos con problemas?",
        "<ul><li><strong>Resultados incorrectos:</strong> Los cálculos pueden dar números equivocados</li><li><strong>Decisiones erróneas:</strong> Basar decisiones en datos malos lleva a errores</li><li><strong>Pérdida de tiempo:</strong> Es más difícil trabajar con datos desorganizados</li><li><strong>Frustración:</strong> Los errores constantes hacen el análisis más difícil</li></ul>"
    )
    
    create_info_box(
        "success-box",
        replace_emojis("✅ ¿Qué aprendiste sobre la calidad de datos?"),
        "<ul><li><strong>Los datos limpios son más fáciles de analizar</strong> - Todo está organizado y consistente</li><li><strong>Los datos con problemas son comunes</strong> - En la vida real, raramente vienen perfectos</li><li><strong>La calidad afecta los resultados</strong> - Datos malos = análisis malos</li><li><strong>Es importante verificar los datos</strong> - Siempre revisa antes de analizar</li></ul>"
    )
    
    # UI - Mostrar Seccion de Tips
    st.header(replace_emojis("💡 Consejos Importantes"))
    
    create_info_box(
        "warning-box",
        "⚠️ Errores comunes a evitar",
        "<ul><li><strong>No entender qué son los datos:</strong> Los datos son información, no solo números</li><li><strong>Ignorar problemas de calidad:</strong> Como viste arriba, los datos con problemas dan resultados incorrectos</li><li><strong>Ignorar el contexto:</strong> Los datos sin contexto no te dicen nada útil</li><li><strong>Buscar solo números grandes:</strong> A veces los datos pequeños son más importantes</li><li><strong>No hacer preguntas:</strong> Sin preguntas claras, los datos no te ayudan</li></ul>"
    )
    
    create_info_box(
        "success-box",
        replace_emojis("✅ Buenas prácticas"),
        "<ul><li><strong>Haz preguntas claras:</strong> Antes de analizar, define qué quieres saber</li><li><strong>Verifica la calidad:</strong> Siempre revisa si los datos tienen problemas como los que viste arriba</li><li><strong>Entiende el contexto:</strong> Conoce de dónde vienen los datos y qué representan</li><li><strong>Empieza simple:</strong> Comienza con preguntas básicas antes de las complejas</li><li><strong>Busca patrones:</strong> Los datos te cuentan historias, aprende a escucharlas</li></ul>"
    )
    
    # UI - Mostrar Actividad de Practica
    st.header(replace_emojis("🎯 Actividad Práctica"))
    
    create_info_box(
        "card",
        replace_emojis("📝 Ejercicio para practicar"),
        "<ol><li><strong>Observa los datos de ejemplo:</strong> Mira las tablas de ventas de arriba (limpios y con problemas)</li><li><strong>Identifica los tipos de datos:</strong> ¿Qué columnas son números? ¿Cuáles son texto?</li><li><strong>Compara la calidad:</strong> ¿Qué diferencias notas entre los datos limpios y los problemáticos?</li><li><strong>Haz preguntas:</strong> ¿Qué quieres saber sobre estos datos?</li><li><strong>Busca patrones:</strong> ¿Ves algo interesante en los números?</li><li><strong>Piensa en aplicaciones:</strong> ¿Cómo podrías usar esta información?</li></ol>"
    )
    
    # UI - Mostrar Ejemplo Interactivo
    st.header(replace_emojis("🎮 Ejemplo Interactivo"))
    
    create_info_box(
        "info-box",
        replace_emojis("🚀 Explora los datos por ti mismo"),
        "<p>Usa los controles de abajo para ver diferentes aspectos de los datos limpios y entender mejor cómo funcionan. Nota cómo es fácil trabajar con datos organizados.</p>"
    )
    
    # UI - Mostrar Controles Interactivos Simples
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(replace_emojis("**🔍 Ver datos por categoría:**"), unsafe_allow_html=True)
        categoria_seleccionada = st.selectbox(
            "Selecciona una categoría",
            ['Todas'] + list(df['Categoria'].unique())
        )
    
    with col2:
        st.markdown(replace_emojis("**📊 Ver estadísticas básicas:**"), unsafe_allow_html=True)
        mostrar_estadisticas = st.checkbox("Mostrar estadísticas", value=True)
    
    # Filtro - Aplicar Filtros y Mostrar Resultados
    if categoria_seleccionada != 'Todas':
        df_filtrado = df[df['Categoria'] == categoria_seleccionada]
        st.markdown(f"**{get_icon('📋', 20)} Datos filtrados por categoría: {categoria_seleccionada}**", unsafe_allow_html=True)
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
        st.markdown(replace_emojis("**📋 Todos los datos:**"), unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        
        if mostrar_estadisticas:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de ventas", f"${df['Ventas'].sum():,.2f}")
            with col2:
                st.metric("Promedio de ventas", f"${df['Ventas'].mean():.2f}")
            with col3:
                st.metric("Registros", len(df))
    
    # 6. Quiz Section - Must complete quiz before marking level as complete
    st.header("🧠 Quiz del Nivel")
    st.markdown("### Pon a prueba tus conocimientos")
    st.info(replace_emojis("📝 **Importante:** Debes aprobar el quiz (al menos 3 de 5 preguntas correctas) antes de poder marcar el nivel como completado."))
    
    # Validacion - Verificar si Usuario Aprobo Quiz
    quiz_passed = st.session_state.get(f'quiz_nivel0_passed', False)
    quiz_completed = st.session_state.get(f'quiz_nivel0_completed', False)
    
    # UI - Mostrar Quiz y Resultados si esta Completado
    # UI - Asegurar que Resultados sean Visibles Despues del Quiz
    from core.quiz_system import create_quiz
    create_quiz('nivel0', user['username'])
    
    # UI - Mostrar Mensaje de Aprobacion si Quiz Aprobado
    if quiz_passed:
        st.markdown(replace_emojis("✅ ¡Has aprobado el quiz! Ahora puedes marcar el nivel como completado."), unsafe_allow_html=True)
    
    # Validacion - Verificar si Quiz Fue Completado y Aprobado Recientemente
    if quiz_completed and not quiz_passed:
        score = st.session_state.get(f'quiz_nivel0_score', 0)
        if score >= 3:
            st.session_state[f'quiz_nivel0_passed'] = True
            st.rerun()
    
    st.divider()
    
    # 7. Navigation or next steps
    st.header(replace_emojis("✅ Verificación del Nivel"))
    
    # Validacion - Permitir Marcar Completado solo si Quiz Aprobado
    if not quiz_passed:
        st.warning("⚠️ Debes aprobar el quiz antes de poder marcar el nivel como completado.")
        nivel0_completed = False
    else:
        nivel0_completed = st.checkbox(
            "He completado todos los pasos del Nivel 0 y aprobé el quiz",
            value=st.session_state.get('nivel0_completed', False),
            key='nivel0_checkbox'
        )
    
    if nivel0_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel0', True):
            st.session_state['nivel0_completed'] = True
        else:
            st.markdown(replace_emojis("❌ Error al guardar el progreso. Intenta de nuevo."), unsafe_allow_html=True)
            return
        
        # Show achievement
        create_achievement_display('nivel0', progress)
        
        create_info_box(
            "success-box",
            replace_emojis("🎉 ¡Felicidades! Has completado el Nivel 0"),
            "<p>Ahora entiendes los conceptos básicos de los datos. Estás listo para continuar con el siguiente nivel donde aprenderás a preparar y cargar datos.</p>"
        )
        
        st.subheader(replace_emojis("🚀 ¿Qué sigue?"))
        st.markdown("Antes de continuar, nos gustaría conocer tu opinión sobre este nivel.")
        
        # Show next level preview
        create_level_preview('nivel1')
        
        if st.button("Completar Encuesta del Nivel", type="primary"):
            st.session_state.survey_level = 'nivel0'
            st.switch_page("pages/99_Survey_Nivel.py")
    
    # UI - Mostrar Recursos Adicionales
    create_info_box(
        "info-box",
        replace_emojis("📚 ¿Quieres saber más?"),
        "<p>Este nivel está basado en fundamentos de ciencia de datos y mejores prácticas de la industria. Los conceptos que aprendiste aquí son la base para todo análisis de datos.</p>"
    )

if __name__ == "__main__":
    main()
