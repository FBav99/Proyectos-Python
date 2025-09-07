import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data
from utils.learning.learning_progress import save_level_progress

# Page config
st.set_page_config(
    page_title="Nivel 3: Métricas - Análisis de Datos",
    page_icon="📊",
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
    st.title("📊 Nivel 3: Métricas")
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
    
    # 3. Introduction Section (what the user will learn)
    st.header("🎯 ¿Qué aprenderás en este nivel?")
    st.markdown("""
    En este nivel aprenderás a entender qué son las métricas y KPIs, cómo interpretarlas y 
    cómo usarlas para tomar mejores decisiones basadas en datos.
    """)
    
    # 4. Steps Section (clear, actionable instructions)
    st.header("📋 Pasos para Entender Métricas y KPIs")
    
    # Step 1
    create_step_card(
        step_number="1",
        title="Entender qué son las métricas y KPIs",
        description="<strong>¿Qué son las métricas?</strong> Las métricas son números que te dicen algo importante sobre tu negocio o actividad. Son como 'termómetros' que miden el estado de las cosas.",
        sections={
            "📊 Tipos de métricas:": [
                "<strong>Métricas de cantidad:</strong> Cuántos productos vendiste, cuántos clientes tienes",
                "<strong>Métricas de dinero:</strong> Cuánto dinero ganaste, cuánto gastaste",
                "<strong>Métricas de tiempo:</strong> Cuánto tiempo tardas en hacer algo",
                "<strong>Métricas de calidad:</strong> Qué tan bien funciona algo, qué tan satisfechos están los clientes"
            ],
            "🎯 ¿Qué son los KPIs?": [
                "<strong>KPI</strong> significa 'Indicador Clave de Rendimiento'. Son las métricas más importantes que te ayudan a saber si tu negocio va bien o mal."
            ],
            "✅ Ejemplos de KPIs comunes:": [
                "<strong>Ventas totales:</strong> Cuánto dinero generaste en total",
                "<strong>Número de clientes:</strong> Cuántas personas compran de ti",
                "<strong>Satisfacción del cliente:</strong> Qué tan contentos están con tu servicio",
                "<strong>Tiempo de entrega:</strong> Cuánto tardas en entregar un producto"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="2",
        title="Identificar métricas clave para tu negocio",
        description="<strong>¿Por qué es importante?</strong> No todas las métricas son igual de importantes. Necesitas enfocarte en las que realmente importan para tu objetivo.",
        sections={
            "🔍 Cómo identificar métricas clave:": [
                "Pregúntate: ¿Qué quiero lograr?",
                "Identifica qué números te dirán si lo estás logrando",
                "Elige 3-5 métricas principales para enfocarte",
                "Evita medir todo, enfócate en lo importante"
            ],
            "💡 Ejemplos por tipo de negocio:": [
                "<strong>Tienda online:</strong> Ventas, visitantes, tasa de conversión",
                "<strong>Servicio de consultoría:</strong> Horas facturables, satisfacción del cliente, proyectos completados",
                "<strong>Restaurante:</strong> Ventas por mesa, tiempo de espera, calificaciones de clientes"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="3",
        title="Interpretar y analizar métricas",
        description="<strong>¿Qué significa interpretar?</strong> No solo ver los números, sino entender qué te están diciendo y qué acciones tomar.",
        sections={
            "📈 Tipos de análisis:": [
                "<strong>Análisis de tendencias:</strong> ¿Los números van subiendo o bajando?",
                "<strong>Comparaciones:</strong> ¿Cómo se comparan con el mes pasado o el año anterior?",
                "<strong>Análisis de patrones:</strong> ¿Hay patrones que se repiten?",
                "<strong>Análisis de correlación:</strong> ¿Cuando una cosa sube, otra también sube?"
            ],
            "✅ Preguntas clave para interpretar:": [
                "¿Este número es bueno o malo?",
                "¿Por qué cambió este número?",
                "¿Qué puedo hacer para mejorarlo?",
                "¿Qué consecuencias tiene este cambio?"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="4",
        title="Usar métricas para tomar decisiones",
        description="<strong>¿Cómo usar las métricas?</strong> Las métricas no son solo para ver, son para actuar. Te ayudan a tomar decisiones informadas.",
        sections={
            "🎯 Proceso de decisión basada en datos:": [
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
    st.header("💡 Ejemplo Práctico: Análisis de Ventas")
    
    # Create sample data
    df = create_sample_data()
    
    # Show data overview
    st.subheader("📊 Datos de Ejemplo")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Basic metrics calculation
    st.subheader("🔢 Cálculo de Métricas Básicas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Ventas'].sum()
        st.metric("💰 Ventas Totales", f"${total_sales:,.2f}")
    
    with col2:
        avg_sales = df['Ventas'].mean()
        st.metric("📊 Promedio de Ventas", f"${avg_sales:.2f}")
    
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
    st.header("🎯 Práctica Interactiva")
    
    st.markdown("""
    Ahora es tu turno de practicar. Usa los filtros de abajo para analizar diferentes aspectos de los datos.
    """)
    
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
    st.subheader("📊 Resultados Filtrados")
    
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtered_sales = filtered_df['Ventas'].sum()
            st.metric("💰 Ventas Filtradas", f"${filtered_sales:,.2f}")
        
        with col2:
            filtered_avg = filtered_df['Ventas'].mean()
            st.metric("📊 Promedio Filtrado", f"${filtered_avg:.2f}")
        
        with col3:
            filtered_count = len(filtered_df)
            st.metric("📋 Registros", f"{filtered_count}")
        
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
    
    # 7. Quiz Section
    st.header("🧠 Quiz de Comprensión")
    
    st.markdown("""
    Responde estas preguntas para verificar que entiendes los conceptos del nivel.
    """)
    
    # Quiz questions
    quiz_questions = [
        {
            "question": "¿Qué significa KPI?",
            "options": [
                "Indicador Clave de Rendimiento",
                "Indicador de Progreso Importante",
                "Indicador de Calidad Principal",
                "Indicador de Rendimiento Clave"
            ],
            "correct": 0
        },
        {
            "question": "¿Cuál es el primer paso para usar métricas efectivamente?",
            "options": [
                "Calcular muchas métricas",
                "Identificar qué métricas son importantes para tu objetivo",
                "Comparar con la competencia",
                "Crear gráficos bonitos"
            ],
            "correct": 1
        },
        {
            "question": "¿Por qué es importante interpretar métricas, no solo verlas?",
            "options": [
                "Para impresionar a otros",
                "Para entender qué significan y qué acciones tomar",
                "Para llenar reportes",
                "Para cumplir requisitos"
            ],
            "correct": 1
        }
    ]
    
    # Initialize quiz state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    
    # Display quiz
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**Pregunta {i+1}:** {q['question']}")
        
        answer = st.radio(
            f"Selecciona la respuesta correcta:",
            q['options'],
            key=f"quiz_{i}",
            label_visibility="collapsed"
        )
        
        st.session_state.quiz_answers[i] = q['options'].index(answer)
    
    # Quiz submission
    if st.button("📝 Enviar Respuestas", type="primary"):
        correct_answers = 0
        total_questions = len(quiz_questions)
        
        for i, q in enumerate(quiz_questions):
            if st.session_state.quiz_answers.get(i) == q['correct']:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100
        
        if score >= 80:
            st.success(f"🎉 ¡Excelente! Obtuviste {score:.0f}% - Has completado este nivel exitosamente!")
            
            # Save progress
            if save_level_progress(user['id'], 'nivel3', True):
                st.session_state.quiz_completed = True
                st.balloons()
        else:
            st.warning(f"📚 Obtuviste {score:.0f}%. Necesitas al menos 80% para completar el nivel. ¡Sigue estudiando!")
    
    # Show completion status
    if st.session_state.get('quiz_completed', False):
        st.success("✅ ¡Nivel 3 completado! Puedes continuar al siguiente nivel.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Ir al Nivel 4", type="primary"):
                st.switch_page("pages/04_Nivel_4_Avanzado.py")
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
