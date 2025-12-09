from utils.ui.icon_system import get_icon, replace_emojis
# Initial Survey - Before Starting Levels
# Asks about user's data analysis experience, Excel usage, etc.

import streamlit as st
from datetime import datetime
from core.survey_system import survey_system
from utils.ui import auth_ui
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

init_sidebar = auth_ui.init_sidebar

configure_streamlit_error_handling()

st.set_page_config(
    page_title="Encuesta Inicial",
    page_icon=get_icon("📋", 20),
    layout="wide"
)

@safe_main
def main():
    # UI - Inicializar Sidebar
    current_user = init_sidebar()
    
    # Validacion - Verificar si Usuario esta Autenticado
    if not current_user:
        st.markdown(replace_emojis("🔐 Por favor inicia sesión para acceder a esta encuesta."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    user_id = current_user['id']
    
    # Validacion - Verificar si Usuario ya Completo esta Encuesta
    if survey_system.has_completed_survey(user_id, 'initial'):
        st.markdown(replace_emojis("✅ Ya completaste esta encuesta. ¡Gracias por tu participación!"), unsafe_allow_html=True)
        st.info("Puedes continuar con los niveles de aprendizaje.")
        if st.button("Ir a los Niveles", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    st.title(replace_emojis("📋 Encuesta Inicial"))
    st.markdown("### Antes de comenzar, nos gustaría conocer un poco sobre ti")
    st.markdown("Esta encuesta nos ayuda a mejorar la experiencia de aprendizaje. Toma aproximadamente 2 minutos.")
    
    st.divider()
    
    # UI - Mostrar Preguntas de Encuesta
    with st.form("initial_survey_form"):
        st.subheader(replace_emojis("📊 Experiencia con Análisis de Datos"))
        
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

        occupation_options = [
            "Estudiante",
            "Empleado/a en área administrativa",
            "Empleado/a en ventas o atención al cliente",
            "Analista o especialista en datos/BI",
            "Profesional independiente / freelance",
            "Liderazgo o gerencia",
            "Docencia / capacitación",
            "Emprendimiento o negocio propio",
            "Buscando empleo",
            "Otro (especificar)"
        ]

        occupation_selection = st.selectbox(
            "¿A qué te dedicas actualmente?",
            occupation_options,
            key="occupation_selection"
        )

        occupation_detail = ""
        if occupation_selection == "Otro (especificar)":
            occupation_detail = st.text_input(
                "Cuéntanos tu ocupación",
                placeholder="Ej: Diseñador UX, Enfermera, Consultor financiero...",
                key="occupation_other_input"
            )
        else:
            occupation_detail = st.text_input(
                "¿En qué área o industria trabajas? (opcional)",
                placeholder="Ej: Retail, Educación, Salud...",
                key="occupation_context_input"
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
        
        st.subheader(replace_emojis("🎯 Objetivos de Aprendizaje"))
        
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
        submitted = st.form_submit_button(replace_emojis("✅ Enviar Encuesta"), type="primary", use_container_width=True)
        
        if submitted:
            # Validate required fields
            occupation_value = occupation_detail.strip() if occupation_selection == "Otro (especificar)" else occupation_selection

            if not occupation_value:
                st.error("Por favor selecciona o especifica tu ocupación.")
                return
            
            # Compile responses
            responses = {
                'data_analysis_experience': data_analysis_exp,
                'occupation_selection': occupation_selection,
                'what_they_do': occupation_value,
                'occupation_detail': occupation_detail.strip(),
                'excel_usage_frequency': excel_usage,
                'learning_goals': learning_goals,
                'motivation': motivation,
                'completed_at': datetime.now().isoformat()
            }
            
            # Save to database
            if survey_system.save_survey_response(user_id, 'initial', responses):
                st.markdown(replace_emojis("✅ ¡Gracias por completar la encuesta!"), unsafe_allow_html=True)
                st.balloons()
                st.info("Ahora puedes comenzar con los niveles de aprendizaje.")
                
                # Auto-redirect after 2 seconds
                st.session_state.initial_survey_completed = True
            else:
                st.markdown(replace_emojis("❌ Hubo un error al guardar tus respuestas. Por favor intenta de nuevo."), unsafe_allow_html=True)
    
    if st.session_state.get("initial_survey_completed"):
        if st.button("Comenzar con los Niveles", type="primary", use_container_width=True):
            st.switch_page("Inicio.py")

if __name__ == "__main__":
    main()

