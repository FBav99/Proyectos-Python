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
    page_title="Nivel 3: Métricas - Análisis de Datos",
    page_icon=get_icon("📊", 20),
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
    
    # 1. Title (level name and description)
    st.title(replace_emojis("📊 Nivel 3: Métricas"))
    st.subheader("KPIs y Análisis de Rendimiento")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Verificar que los niveles anteriores estén completados
    if not progress['nivel1'] or not progress['nivel2']:
        st.warning("⚠️ Primero debes completar los Niveles 1 y 2 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # 3. Progression Summary
    create_progression_summary(progress)
    
    # 4. Show achievement for previous level if completed
    if progress.get('nivel2', False):
        create_achievement_display('nivel2', progress)
    
    # 5. Level Preview
    create_level_preview('nivel3')
    
    # 6. Introduction Section (what the user will learn)
    st.header(replace_emojis("🎯 ¿Qué aprenderás en este nivel?"))
    st.markdown("Ahora que ya sabes **preparar datos** (Nivel 1) y **filtrar información** (Nivel 2), en este nivel aprenderás a entender qué son las métricas y KPIs, cómo interpretarlas y cómo usarlas para tomar mejores decisiones basadas en datos.")
    
    # Add connection to previous levels
    create_info_box(
        "info-box",
        "🔗 Conectando con Niveles Anteriores",
        "<p>En el <strong>Nivel 0</strong> aprendiste qué son los datos y cómo se organizan. En el <strong>Nivel 1</strong> aprendiste a prepararlos correctamente. En el <strong>Nivel 2</strong> aprendiste a filtrarlos para encontrar información específica. Ahora es hora de calcular métricas importantes con esos datos filtrados.</p>"
    )
    
    # 7. Steps Section (clear, actionable instructions)
    st.header(replace_emojis("📋 Pasos para Entender Métricas y KPIs"))
    
    # Step 1
    create_step_card(
        step_number="3.1",
        title="Entender qué son las métricas y KPIs",
        description="<strong>¿Qué son las métricas?</strong> Las métricas son números que te dicen algo importante sobre tu negocio o actividad. Son como 'termómetros' que miden el estado de las cosas.",
        sections={
            replace_emojis("📊 Tipos de métricas:"): [
                "<strong>Métricas de cantidad:</strong> Cuántos productos vendiste, cuántos clientes tienes",
                "<strong>Métricas de dinero:</strong> Cuánto dinero ganaste, cuánto gastaste",
                "<strong>Métricas de tiempo:</strong> Cuánto tiempo tardas en hacer algo",
                "<strong>Métricas de calidad:</strong> Qué tan bien funciona algo, qué tan satisfechos están los clientes"
            ],
            replace_emojis("🎯 ¿Qué son los KPIs?"): [
                "<strong>KPI</strong> significa 'Indicador Clave de Rendimiento'. Son las métricas más importantes que te ayudan a saber si tu negocio va bien o mal."
            ],
            replace_emojis("✅ Ejemplos de KPIs comunes:"): [
                "<strong>Ventas totales:</strong> Cuánto dinero generaste en total",
                "<strong>Número de clientes:</strong> Cuántas personas compran de ti",
                "<strong>Satisfacción del cliente:</strong> Qué tan contentos están con tu servicio",
                "<strong>Tiempo de entrega:</strong> Cuánto tardas en entregar un producto"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="3.2",
        title="Identificar métricas clave para tu negocio",
        description="<strong>¿Por qué es importante?</strong> No todas las métricas son igual de importantes. Necesitas enfocarte en las que realmente importan para tu objetivo.",
        sections={
            replace_emojis("🔍 Cómo identificar métricas clave:"): [
                "Pregúntate: ¿Qué quiero lograr?",
                "Identifica qué números te dirán si lo estás logrando",
                "Elige 3-5 métricas principales para enfocarte",
                "Evita medir todo, enfócate en lo importante"
            ],
            replace_emojis("💡 Ejemplos por tipo de negocio:"): [
                "<strong>Tienda online:</strong> Ventas, visitantes, tasa de conversión",
                "<strong>Servicio de consultoría:</strong> Horas facturables, satisfacción del cliente, proyectos completados",
                "<strong>Restaurante:</strong> Ventas por mesa, tiempo de espera, calificaciones de clientes"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="3.3",
        title="Interpretar y analizar métricas",
        description="<strong>¿Qué significa interpretar?</strong> No solo ver los números, sino entender qué te están diciendo y qué acciones tomar.",
        sections={
            replace_emojis("📈 Tipos de análisis:"): [
                "<strong>Análisis de tendencias:</strong> ¿Los números van subiendo o bajando?",
                "<strong>Comparaciones:</strong> ¿Cómo se comparan con el mes pasado o el año anterior?",
                "<strong>Análisis de patrones:</strong> ¿Hay patrones que se repiten?",
                "<strong>Análisis de correlación:</strong> ¿Cuando una cosa sube, otra también sube?"
            ],
            replace_emojis("✅ Preguntas clave para interpretar:"): [
                "¿Este número es bueno o malo?",
                "¿Por qué cambió este número?",
                "¿Qué puedo hacer para mejorarlo?",
                "¿Qué consecuencias tiene este cambio?"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="3.4",
        title="Usar métricas para tomar decisiones",
        description="<strong>¿Cómo usar las métricas?</strong> Las métricas no son solo para ver, son para actuar. Te ayudan a tomar decisiones informadas.",
        sections={
            replace_emojis("🎯 Proceso de decisión basada en datos:"): [
                "Revisa las métricas regularmente",
                "Identifica problemas o oportunidades",
                "Genera hipótesis sobre qué está pasando",
                "Toma acción basada en los datos",
                "Mide el resultado de tus acciones"
            ],
            "⚠️ Errores comunes a evitar:": [
                "Enfocarse solo en una métrica",
                "No considerar el contexto",
                "Tomar decisiones sin entender la causa",
                "Ignorar tendencias a largo plazo"
            ]
        }
    )
    
    # 5. Practical Example Section
    st.header(replace_emojis("💡 Ejemplo Práctico: Análisis de Ventas"))
    
    # Show data quality insight for this level
    create_data_quality_insight('nivel3', 'clean')
    
    # Create sample data
    df = create_sample_data('clean')  # Use clean data for Level 3
    
    # Show data overview
    st.subheader(replace_emojis("📊 Datos de Ejemplo"))
    
    # Reinforce data types concept
    create_info_box(
        "info-box",
        replace_emojis("📚 Recordando Tipos de Datos"),
        "<p>Como aprendiste en el <strong>Nivel 0</strong>, los datos tienen diferentes tipos. En este análisis usaremos principalmente los datos <strong>numéricos</strong> (Ventas, Cantidad, Calificación) para calcular métricas importantes.</p>"
    )
    
    st.dataframe(df.head(10), use_container_width=True)
    
    # Basic metrics calculation
    st.subheader(replace_emojis("🔢 Cálculo de Métricas Básicas"))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Ventas'].sum()
        st.metric(replace_emojis("💰 Ventas Totales"), f"${total_sales:,.2f}")
    
    with col2:
        avg_sales = df['Ventas'].mean()
        st.metric(replace_emojis("📊 Promedio de Ventas"), f"${avg_sales:.2f}")
    
    with col3:
        total_quantity = df['Cantidad'].sum()
        st.metric("📦 Cantidad Total", f"{total_quantity:,}")
    
    with col4:
        avg_rating = df['Calificacion'].mean()
        st.metric("⭐ Calificación Promedio", f"{avg_rating:.1f}")
    
    # Category analysis
    st.subheader("🏷️ Análisis por Categoría")
    category_sales = df.groupby('Categoria')['Ventas'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.bar_chart(category_sales)
    
    with col2:
        st.dataframe(category_sales.reset_index().rename(columns={'Ventas': 'Ventas Totales'}), use_container_width=True)
    
    # Regional analysis
    st.subheader("🌍 Análisis por Región")
    region_sales = df.groupby('Region')['Ventas'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.bar_chart(region_sales)
    
    with col2:
        st.dataframe(region_sales.reset_index().rename(columns={'Ventas': 'Ventas Totales'}), use_container_width=True)
    
    # 6. Interactive Practice Section
    st.header(replace_emojis("🎯 Práctica Interactiva"))
    
    st.markdown("Ahora es tu turno de practicar. Usa los filtros de abajo para analizar diferentes aspectos de los datos.")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_category = st.selectbox(
            "🏷️ Seleccionar Categoría",
            ['Todas'] + list(df['Categoria'].unique())
        )
    
    with col2:
        selected_region = st.selectbox(
            "🌍 Seleccionar Región",
            ['Todas'] + list(df['Region'].unique())
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_category != 'Todas':
        filtered_df = filtered_df[filtered_df['Categoria'] == selected_category]
    
    if selected_region != 'Todas':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    # Show filtered results
    st.subheader(replace_emojis("📊 Resultados Filtrados"))
    
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtered_sales = filtered_df['Ventas'].sum()
            st.metric(replace_emojis("💰 Ventas Filtradas"), f"${filtered_sales:,.2f}")
        
        with col2:
            filtered_avg = filtered_df['Ventas'].mean()
            st.metric(replace_emojis("📊 Promedio Filtrado"), f"${filtered_avg:.2f}")
        
        with col3:
            filtered_count = len(filtered_df)
            st.metric(replace_emojis("📋 Registros"), f"{filtered_count}")
        
        with col4:
            filtered_rating = filtered_df['Calificacion'].mean()
            st.metric("⭐ Calificación", f"{filtered_rating:.1f}")
        
        # Show filtered data
        st.dataframe(filtered_df, use_container_width=True)
        
        # Show filtered charts
        if len(filtered_df) > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                if 'Fecha' in filtered_df.columns:
                    daily_sales = filtered_df.groupby(filtered_df['Fecha'].dt.date)['Ventas'].sum()
                    st.line_chart(daily_sales)
            
            with col2:
                if 'Categoria' in filtered_df.columns:
                    cat_sales = filtered_df.groupby('Categoria')['Ventas'].sum()
                    st.bar_chart(cat_sales)
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")
    
    # 7. Quiz Section - Must complete quiz before marking level as complete
    st.header("🧠 Quiz del Nivel")
    st.markdown("### Pon a prueba tus conocimientos")
    st.info(replace_emojis("📝 **Importante:** Debes aprobar el quiz (al menos 3 de 5 preguntas correctas) antes de poder marcar el nivel como completado."))
    
    # Check if user passed the quiz
    quiz_passed = st.session_state.get(f'quiz_nivel3_passed', False)
    quiz_completed = st.session_state.get(f'quiz_nivel3_completed', False)
    
    # Always show quiz and results if quiz is completed (whether passed or not)
    # This ensures results are always visible after completing the quiz
    from core.quiz_system import create_quiz
    create_quiz('nivel3', user['username'])
    
    # Show passed message if quiz is passed
    if quiz_passed:
        st.markdown(replace_emojis("✅ ¡Has aprobado el quiz! Ahora puedes marcar el nivel como completado."), unsafe_allow_html=True)
    
    # Check if quiz was just completed and passed (for first-time completion)
    if quiz_completed and not quiz_passed:
        score = st.session_state.get(f'quiz_nivel3_score', 0)
        if score >= 3:
            st.session_state[f'quiz_nivel3_passed'] = True
            st.rerun()
    
    st.divider()
    
    # 8. Navigation or next steps
    st.header(replace_emojis("✅ Verificación del Nivel"))
    
    # Only allow marking as complete if quiz is passed
    if not quiz_passed:
        st.warning("⚠️ Debes aprobar el quiz antes de poder marcar el nivel como completado.")
        nivel3_completed = False
    else:
        nivel3_completed = st.checkbox(
            "He completado todos los pasos del Nivel 3 y aprobé el quiz",
            value=st.session_state.get('nivel3_completed', False),
            key='nivel3_checkbox'
        )
    
    if nivel3_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel3', True):
            st.session_state['nivel3_completed'] = True
        else:
            st.markdown(replace_emojis("❌ Error al guardar el progreso. Intenta de nuevo."), unsafe_allow_html=True)
            return
        
        # Show achievement
        create_achievement_display('nivel3', progress)
        
        st.markdown(replace_emojis("✅ ¡Nivel 3 completado! Puedes continuar al siguiente nivel."), unsafe_allow_html=True)
        
        # Show next level preview
        create_level_preview('nivel4')
        
        st.markdown("Antes de continuar, nos gustaría conocer tu opinión sobre este nivel.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Completar Encuesta del Nivel", type="primary"):
                st.session_state.survey_level = 'nivel3'
                st.switch_page("pages/99_Survey_Nivel.py")
        with col2:
            if st.button("🏠 Volver al Inicio"):
                st.switch_page("Inicio.py")
    
    # 8. Navigation
    st.markdown("---")
    st.header("🧭 Navegación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬅️ Nivel 2", use_container_width=True):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col2:
        if st.button("🏠 Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col3:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")
    
    with col4:
        if st.button("🚀 Nivel 4", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")

if __name__ == "__main__":
    main()
