import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data
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
    page_title="Nivel 2: Filtros - Análisis de Datos",
    page_icon=get_icon("🔍", 20),
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Helper functions are now imported from utils.level_components and utils.level_data

# Sample data functions are now imported from utils.level_data

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
    
    # 1. Title (level name and description)
    st.title(replace_emojis("🔍 Nivel 2: Filtros"))
    st.subheader("Organizar y Filtrar Información")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Verificar que el nivel anterior esté completado
    if not progress['nivel1']:
        st.warning("⚠️ Primero debes completar el Nivel 1 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # 3. Progression Summary
    create_progression_summary(progress)
    
    # 4. Show achievement for previous level if completed
    if progress.get('nivel1', False):
        create_achievement_display('nivel1', progress)
    
    # 5. Level Preview
    create_level_preview('nivel2')
    
    # 6. Introduction Section (what the user will learn)
    st.header(replace_emojis("🎯 ¿Qué aprenderás en este nivel?"))
    st.markdown("Ahora que ya sabes **preparar y cargar datos** correctamente (como aprendiste en el Nivel 1), en este nivel aprenderás a usar filtros para encontrar exactamente la información que necesitas. Los filtros te ayudan a organizar y analizar datos de manera más efectiva.")
    
    # Add connection to previous level
    create_info_box(
        "info-box",
        "🔗 Conectando con el Nivel 1",
        "<p>En el nivel anterior aprendiste a cargar y verificar datos. Ahora que tienes datos limpios y bien estructurados, puedes empezar a filtrarlos para encontrar información específica. ¡Es hora de explorar tus datos!</p>"
    )
    
    # 7. Steps Section (clear, actionable instructions)
    st.header(replace_emojis("📋 Pasos para Organizar y Filtrar Datos"))
    
    # Step 1
    create_step_card(
        step_number="2.1",
        title="Usar filtros de fecha para analizar períodos específicos",
        description="<strong>¿Por qué es útil?</strong> Los filtros de fecha te permiten ver información de un período específico, como las ventas del último mes o de un trimestre particular.",
        sections={
            replace_emojis("📅 Tipos de filtros de fecha:"): [
                "<strong>Rango de fechas:</strong> Desde una fecha hasta otra",
                "<strong>Período específico:</strong> Último mes, este año, etc.",
                "<strong>Fecha única:</strong> Un día específico"
            ],
            replace_emojis("✅ Ejemplos de uso:"): [
                "Ver ventas del último trimestre",
                "Comparar resultados entre dos meses",
                "Analizar tendencias por estación"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="2.2",
        title="Filtrar por categorías y regiones",
        description="<strong>¿Qué significa?</strong> Los filtros por categoría te permiten ver solo los productos o servicios que te interesan, y los filtros por región te muestran resultados de áreas geográficas específicas.",
        sections={
            "🏷️ Filtros por categoría:": [
                "<strong>Productos:</strong> Solo electrónicos, solo ropa, etc.",
                "<strong>Servicios:</strong> Solo consultoría, solo mantenimiento, etc.",
                "<strong>Tipos de cliente:</strong> Solo empresas, solo particulares, etc."
            ],
            "🌍 Filtros por región:": [
                "<strong>Países o estados:</strong> Solo México, solo California, etc.",
                "<strong>Ciudades:</strong> Solo Ciudad de México, solo Los Ángeles, etc.",
                "<strong>Zonas:</strong> Solo norte, solo sur, solo este, solo oeste"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="2.3",
        title="Aplicar filtros numéricos con deslizadores",
        description="<strong>¿Cómo funcionan?</strong> Los filtros numéricos te permiten establecer rangos de valores, como ver solo productos entre ciertos precios o ventas por encima de un monto mínimo.",
        sections={
            replace_emojis("🔢 Tipos de filtros numéricos:"): [
                "<strong>Rango de precios:</strong> Desde $100 hasta $500",
                "<strong>Ventas mínimas:</strong> Solo productos que vendieron más de 50 unidades",
                "<strong>Calificaciones:</strong> Solo productos con 4 estrellas o más",
                "<strong>Edad o antigüedad:</strong> Solo clientes entre 25 y 45 años"
            ],
            "🎛️ Cómo usar deslizadores:": {
                "Mueve el deslizador izquierdo para establecer el valor mínimo",
                "Mueve el deslizador derecho para establecer el valor máximo",
                "Los resultados se actualizan automáticamente"
            }
        }
    )
    
    # Step 4
    create_step_card(
        step_number="2.4",
        title="Combinar múltiples filtros para análisis detallado",
        description="<strong>¿Por qué combinar filtros?</strong> Al usar varios filtros juntos, puedes obtener información muy específica y relevante para tu análisis.",
        sections={
            "🔗 Ejemplos de combinaciones:": [
                "<strong>Fecha + Categoría:</strong> Ventas de electrónicos en diciembre",
                "<strong>Región + Precio:</strong> Productos caros en el norte",
                "<strong>Categoría + Calificación:</strong> Ropa con 5 estrellas",
                "<strong>Fecha + Región + Precio:</strong> Ventas altas en el sur este mes"
            ],
            replace_emojis("💡 Consejos para combinar filtros:"): [
                "Empieza con un filtro y ve agregando más gradualmente",
                "Verifica que no estés filtrando demasiado (pocos resultados)",
                "Usa filtros que tengan sentido juntos"
            ]
        }
    )
    
    # Step 5
    create_step_card(
        step_number="2.5",
        title="Entender cómo los filtros afectan las métricas",
        description="<strong>¿Qué significa?</strong> Cuando aplicas filtros, los totales, promedios y otras métricas cambian para mostrar solo la información filtrada.",
        sections={
            replace_emojis("📊 Métricas que cambian con filtros:"): [
                "<strong>Total de ventas:</strong> Solo suma los productos filtrados",
                "<strong>Promedio de precios:</strong> Solo considera los productos visibles",
                "<strong>Número de registros:</strong> Solo cuenta los resultados filtrados",
                "<strong>Porcentajes:</strong> Se recalculan con la nueva base de datos"
            ],
            "⚠️ Importante recordar:": [
                "Los filtros no cambian tus datos originales",
                "Siempre puedes quitar filtros para ver todo nuevamente",
                "Los filtros se aplican en tiempo real"
            ]
        }
    )
    
    # 5. Optional media (images, diagrams, icons)
    st.header(replace_emojis("🎥 Demostración Visual"))
    try:
        display_level_gif("nivel2", "filtros_demo")
    except:
        st.info(replace_emojis("📹 GIF de demostración no disponible. El proceso incluye: 1) Seleccionar filtros, 2) Aplicar criterios, 3) Ver resultados filtrados."))
    
    # Example section
    st.header(replace_emojis("🎯 Ejemplo Práctico"))
    
    create_info_box(
        "info-box",
        replace_emojis("📊 Vamos a practicar con filtros usando datos de ventas"),
        "<p>Te mostraré cómo aplicar diferentes tipos de filtros y ver cómo cambian los resultados.</p>"
    )
    
    # Show data quality insight for this level
    create_data_quality_insight('nivel2', 'clean')
    
    # Show data transformation
    create_info_box(
        "success-box",
        "✨ Transformación de Datos Completada",
        "<p>¡Excelente! Los datos que viste en el <strong>Nivel 1</strong> (con problemas de calidad) ahora están limpios y organizados. Como aprendiste en el Nivel 0, estos datos tienen una estructura clara: cada fila es una venta y cada columna es un tipo de información.</p>"
    )
    
    df = create_sample_data('clean')  # Use clean data for Level 2
    st.subheader(replace_emojis("📁 Datos de ejemplo (Ventas de TechStore - Datos preparados)"))
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(df.head(10), use_container_width=True)
        st.caption("Primeras 10 filas de datos")
    with col2:
        st.markdown(replace_emojis("**📊 Información básica:**"), unsafe_allow_html=True)
        st.metric("Total de registros", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Período", f"{df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')}")
    
    st.subheader(replace_emojis("🔍 Aplicar Filtros"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(replace_emojis("**📅 Filtro por fecha:**"), unsafe_allow_html=True)
        fecha_inicio = st.date_input(
            "Fecha de inicio",
            value=df['Fecha'].min().date(),
            min_value=df['Fecha'].min().date(),
            max_value=df['Fecha'].max().date()
        )
        fecha_fin = st.date_input(
            "Fecha de fin",
            value=df['Fecha'].max().date(),
            min_value=df['Fecha'].min().date(),
            max_value=df['Fecha'].max().date()
        )
        
        st.markdown("**🏷️ Filtro por categoría:**")
        categorias = ['Todas'] + list(df['Categoria'].unique())
        categoria_seleccionada = st.selectbox("Seleccionar categoría", categorias)
        
        st.markdown("**🌍 Filtro por región:**")
        regiones = ['Todas'] + list(df['Region'].unique())
        region_seleccionada = st.selectbox("Seleccionar región", regiones)
    
    with col2:
        st.markdown(replace_emojis("**🔢 Filtros numéricos:**"), unsafe_allow_html=True)
        
        st.markdown(replace_emojis("**💰 Rango de ventas:**"), unsafe_allow_html=True)
        ventas_min = st.slider(
            "Ventas mínimas",
            min_value=float(df['Ventas'].min()),
            max_value=float(df['Ventas'].max()),
            value=float(df['Ventas'].min()),
            step=50.0
        )
        ventas_max = st.slider(
            "Ventas máximas",
            min_value=float(df['Ventas'].min()),
            max_value=float(df['Ventas'].max()),
            value=float(df['Ventas'].max()),
            step=50.0
        )
        
        st.markdown("**⭐ Calificación mínima:**")
        calificacion_min = st.slider(
            "Calificación mínima",
            min_value=1,
            max_value=5,
            value=1
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    # Filtro de fechas
    df_filtrado = df_filtrado[
        (df_filtrado['Fecha'].dt.date >= fecha_inicio) &
        (df_filtrado['Fecha'].dt.date <= fecha_fin)
    ]
    
    # Filtro de categoría
    if categoria_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_seleccionada]
    
    # Filtro de región
    if region_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Region'] == region_seleccionada]
    
    # Filtros numéricos
    df_filtrado = df_filtrado[
        (df_filtrado['Ventas'] >= ventas_min) &
        (df_filtrado['Ventas'] <= ventas_max) &
        (df_filtrado['Calificacion'] >= calificacion_min)
    ]
    
    # Mostrar resultados filtrados
    st.markdown(replace_emojis("### 📊 Resultados Filtrados"), unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros originales", len(df))
        st.metric("Registros filtrados", len(df_filtrado))
    
    with col2:
        st.metric("Ventas totales", f"${df_filtrado['Ventas'].sum():,.0f}")
        st.metric("Promedio ventas", f"${df_filtrado['Ventas'].mean():,.0f}")
    
    with col3:
        st.metric("Ingresos totales", f"${df_filtrado['Ingresos'].sum():,.0f}")
        st.metric("Promedio ingresos", f"${df_filtrado['Ingresos'].mean():,.0f}")
    
    with col4:
        st.metric("Calificación promedio", f"{df_filtrado['Calificacion'].mean():.1f}")
        st.metric("Productos únicos", df_filtrado['Categoria'].nunique())
    
    # Mostrar datos filtrados
    if len(df_filtrado) > 0:
        st.markdown(replace_emojis("**📋 Datos filtrados:**"), unsafe_allow_html=True)
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados. Intenta ajustar los filtros.")
    
    # Tips section
    st.header(replace_emojis("💡 Consejos Importantes"))
    
    st.markdown('<div class="warning-box"><h3>⚠️ Errores comunes a evitar:</h3><ul><li><strong>Filtros muy restrictivos:</strong> Si filtras demasiado, podrías no obtener resultados</li><li><strong>Olvidar quitar filtros:</strong> Asegúrate de limpiar filtros cuando cambies de análisis</li><li><strong>Filtros contradictorios:</strong> No uses filtros que se contradigan entre sí</li><li><strong>Ignorar el contexto:</strong> Usa filtros que tengan sentido para tu análisis</li></ul></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="success-box"><h3>✅ Buenas prácticas:</h3><ul><li><strong>Planifica tu análisis:</strong> Piensa qué información necesitas antes de filtrar</li><li><strong>Usa filtros gradualmente:</strong> Empieza con uno y ve agregando más</li><li><strong>Verifica los resultados:</strong> Siempre revisa que los filtros den los resultados esperados</li><li><strong>Documenta tus filtros:</strong> Anota qué filtros usaste para poder repetir el análisis</li></ul></div>', unsafe_allow_html=True)
    
    # Practice activity
    st.header(replace_emojis("🎯 Actividad Práctica"))
    st.markdown('<div class="card"><h3>📝 Ejercicio para practicar:</h3><ol><li><strong>Analiza ventas por período:</strong> Usa filtros de fecha para ver ventas del último trimestre</li><li><strong>Filtra por categoría:</strong> Ve solo los productos de una categoría específica</li><li><strong>Aplica filtros numéricos:</strong> Establece un rango de precios o ventas</li><li><strong>Combina filtros:</strong> Usa fecha + categoría + región juntos</li><li><strong>Observa los cambios:</strong> Nota cómo cambian las métricas con cada filtro</li></ol></div>', unsafe_allow_html=True)
    
    # 6. Quiz Section - Must complete quiz before marking level as complete
    st.header("🧠 Quiz del Nivel")
    st.markdown("### Pon a prueba tus conocimientos")
    st.info(replace_emojis("📝 **Importante:** Debes aprobar el quiz (al menos 3 de 5 preguntas correctas) antes de poder marcar el nivel como completado."))
    
    # Check if user passed the quiz
    quiz_passed = st.session_state.get(f'quiz_nivel2_passed', False)
    quiz_completed = st.session_state.get(f'quiz_nivel2_completed', False)
    
    # Always show quiz and results if quiz is completed (whether passed or not)
    # This ensures results are always visible after completing the quiz
    from core.quiz_system import create_quiz
    create_quiz('nivel2', user['username'])
    
    # Show passed message if quiz is passed
    if quiz_passed:
        st.markdown(replace_emojis("✅ ¡Has aprobado el quiz! Ahora puedes marcar el nivel como completado."), unsafe_allow_html=True)
    
    # Check if quiz was just completed and passed (for first-time completion)
    if quiz_completed and not quiz_passed:
        score = st.session_state.get(f'quiz_nivel2_score', 0)
        if score >= 3:
            st.session_state[f'quiz_nivel2_passed'] = True
            st.rerun()
    
    st.divider()
    
    # 7. Navigation or next steps
    st.header(replace_emojis("✅ Verificación del Nivel"))
    
    # Only allow marking as complete if quiz is passed
    if not quiz_passed:
        st.warning("⚠️ Debes aprobar el quiz antes de poder marcar el nivel como completado.")
        nivel2_completed = False
    else:
        nivel2_completed = st.checkbox(
            "He completado todos los pasos del Nivel 2 y aprobé el quiz",
            value=st.session_state.get('nivel2_completed', False),
            key='nivel2_checkbox'
        )
    
    if nivel2_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel2', True):
            st.session_state['nivel2_completed'] = True
        else:
            st.markdown(replace_emojis("❌ Error al guardar el progreso. Intenta de nuevo."), unsafe_allow_html=True)
            return
        
        # Show achievement
        create_achievement_display('nivel2', progress)
        
        create_info_box(
            "success-box",
            replace_emojis("🎉 ¡Felicidades! Has completado el Nivel 2"),
            "<p>Ahora sabes cómo filtrar y organizar datos. Estás listo para continuar con el siguiente nivel.</p>"
        )
        
        st.subheader(replace_emojis("🚀 ¿Qué sigue?"))
        st.markdown("Antes de continuar, nos gustaría conocer tu opinión sobre este nivel.")
        
        # Show next level preview
        create_level_preview('nivel3')
        
        if st.button("Completar Encuesta del Nivel", type="primary"):
            st.session_state.survey_level = 'nivel2'
            st.switch_page("pages/99_Survey_Nivel.py")
    
    # Additional resources
    create_info_box(
        "info-box",
        replace_emojis("📚 ¿Quieres saber más?"),
        "<p>Este nivel está basado en metodologías de análisis exploratorio de datos y mejores prácticas de la industria. Si quieres profundizar en los fundamentos teóricos, consulta la documentación del proyecto.</p>"
    )

if __name__ == "__main__":
    main()
