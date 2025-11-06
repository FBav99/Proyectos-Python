"""
Initial Survey - Before Starting Levels
Asks about user's data analysis experience, Excel usage, etc.
"""

import streamlit as st
from datetime import datetime
from core.survey_system import survey_system
from utils.ui import auth_ui
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

init_sidebar = auth_ui.init_sidebar

configure_streamlit_error_handling()

st.set_page_config(
    page_title="Encuesta Inicial",
    page_icon="📋",
    layout="wide"
)

@safe_main
def main():
    # Initialize sidebar
    current_user = init_sidebar()
    
    # Check if user is authenticated
    if not current_user:
        st.error("🔐 Por favor inicia sesión para acceder a esta encuesta.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    user_id = current_user['id']
    
    # Check if user has already completed this survey
    if survey_system.has_completed_survey(user_id, 'initial'):
        st.success("✅ Ya completaste esta encuesta. ¡Gracias por tu participación!")
        st.info("Puedes continuar con los niveles de aprendizaje.")
        if st.button("Ir a los Niveles", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    st.title("📋 Encuesta Inicial")
    st.markdown("### Antes de comenzar, nos gustaría conocer un poco sobre ti")
    st.markdown("Esta encuesta nos ayuda a mejorar la experiencia de aprendizaje. Toma aproximadamente 2 minutos.")
    
    st.divider()
    
    # Survey questions
    with st.form("initial_survey_form"):
        st.subheader("📊 Experiencia con Análisis de Datos")
        
        # Question 1: Data analysis experience
        data_analysis_exp = st.selectbox(
            "¿Cuál es tu nivel de experiencia con análisis de datos?",
            [
                "Sin experiencia - Es la primera vez que trabajo con datos",
                "Principiante - He usado Excel básico o herramientas similares",
                "Intermedio - He creado tablas y gráficos básicos",
                "Avanzado - He usado herramientas como Power BI, Tableau, o Python",
                "Experto - Trabajo profesionalmente con análisis de datos"
            ],
            key="data_exp"
        )
        
        st.divider()
        
        st.subheader("💼 Contexto Profesional")
        
        # Question 2: What they do
        what_they_do = st.text_area(
            "¿A qué te dedicas? (Ej: Estudiante de ingeniería, Analista de ventas, Gerente de marketing, etc.)",
            placeholder="Describe brevemente tu trabajo o área de estudio...",
            key="what_do"
        )
        
        # Question 3: Excel usage
        excel_usage = st.selectbox(
            "¿Con qué frecuencia usas Excel o herramientas similares?",
            [
                "Nunca - No he usado Excel",
                "Raramente - Solo ocasionalmente",
                "Mensualmente - Lo uso algunas veces al mes",
                "Semanalmente - Lo uso con regularidad",
                "Diariamente - Lo uso todos los días en mi trabajo"
            ],
            key="excel_freq"
        )
        
        st.divider()
        
        st.subheader("🎯 Objetivos de Aprendizaje")
        
        # Question 4: Learning goals
        learning_goals = st.multiselect(
            "¿Qué te gustaría aprender? (Puedes seleccionar múltiples opciones)",
            [
                "Preparar y organizar datos",
                "Filtrar y buscar información específica",
                "Calcular métricas y KPIs",
                "Crear visualizaciones y gráficos",
                "Construir dashboards interactivos",
                "Limpiar datos sucios o incompletos",
                "Comunicar insights de datos"
            ],
            key="goals"
        )
        
        # Question 5: Motivation
        motivation = st.selectbox(
            "¿Por qué estás interesado en aprender análisis de datos?",
            [
                "Mejora profesional - Para avanzar en mi carrera",
                "Requisito académico - Para un curso o proyecto",
                "Curiosidad personal - Quiero aprender algo nuevo",
                "Necesidad laboral - Lo necesito para mi trabajo actual",
                "Emprendimiento - Para mi propio negocio o proyecto"
            ],
            key="motivation"
        )
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button("✅ Enviar Encuesta", type="primary", use_container_width=True)
        
        if submitted:
            # Validate required fields
            if not what_they_do.strip():
                st.error("Por favor completa el campo sobre a qué te dedicas.")
                return
            
            # Compile responses
            responses = {
                'data_analysis_experience': data_analysis_exp,
                'what_they_do': what_they_do.strip(),
                'excel_usage_frequency': excel_usage,
                'learning_goals': learning_goals,
                'motivation': motivation,
                'completed_at': datetime.now().isoformat()
            }
            
            # Save to database
            if survey_system.save_survey_response(user_id, 'initial', responses):
                st.success("✅ ¡Gracias por completar la encuesta!")
                st.balloons()
                st.info("Ahora puedes comenzar con los niveles de aprendizaje.")
                
                # Auto-redirect after 2 seconds
                st.session_state.initial_survey_completed = True
                
                if st.button("Comenzar con los Niveles", type="primary", use_container_width=True):
                    st.switch_page("Inicio.py")
            else:
                st.error("❌ Hubo un error al guardar tus respuestas. Por favor intenta de nuevo.")

if __name__ == "__main__":
    main()

