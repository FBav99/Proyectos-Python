from utils.ui.icon_system import get_icon, replace_emojis
# Level-specific Survey - After Each Level
# Rating questions (1-5 scale) and suggestions box

import streamlit as st
from datetime import datetime
from core.survey_system import survey_system
from utils.ui import auth_ui
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

init_sidebar = auth_ui.init_sidebar

configure_streamlit_error_handling()

st.set_page_config(
    page_title="Encuesta de Nivel",
    page_icon=get_icon("📝", 20),
    layout="wide"
)

# Level information mapping
LEVEL_INFO = {
    'nivel0': {'name': 'Nivel 0: Introducción', 'number': '0'},
    'nivel1': {'name': 'Nivel 1: Básico', 'number': '1'},
    'nivel2': {'name': 'Nivel 2: Filtros', 'number': '2'},
    'nivel3': {'name': 'Nivel 3: Métricas', 'number': '3'},
    'nivel4': {'name': 'Nivel 4: Avanzado', 'number': '4'},
}

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
    
    # Estado - Obtener Nivel desde Session State
    level = st.session_state.get('survey_level', None)
    
    if not level or level not in LEVEL_INFO:
        st.markdown(replace_emojis("❌ No se especificó el nivel para la encuesta."), unsafe_allow_html=True)
        if st.button("Volver al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    level_info = LEVEL_INFO[level]
    
    # Validacion - Verificar si Usuario ya Completo Encuesta para este Nivel
    if survey_system.has_completed_survey(user_id, 'level', level):
        icon_html = get_icon('✅', 20)
        st.markdown(f"{icon_html} Ya completaste la encuesta para el {level_info['name']}.", unsafe_allow_html=True)
        
        # Determine next level
        next_level = get_next_level(level)
        if next_level:
            st.info("Puedes continuar con el siguiente nivel.")
            if st.button(f"Continuar al {LEVEL_INFO[next_level]['name']}", type="primary"):
                # Clear survey_level from session state
                if 'survey_level' in st.session_state:
                    del st.session_state['survey_level']
                # Get the correct page path using mapping
                page_path = get_level_page_path(next_level)
                st.switch_page(page_path)
        else:
            # All levels completed, go to final survey
            st.info("¡Has completado todos los niveles! Ahora puedes completar la encuesta final.")
            if st.button("Completar Encuesta Final", type="primary"):
                st.switch_page("pages/99_Survey_Final.py")
        return
    
    st.markdown(f"# {get_icon('📝', 24)} Encuesta: {level_info['name']}", unsafe_allow_html=True)
    st.markdown(f"### ¡Felicitaciones por completar el {level_info['name']}!")
    st.markdown("Tu opinión es muy valiosa. Por favor, comparte tus comentarios sobre esta experiencia.")
    
    st.divider()
    
    # UI - Mostrar Preguntas de Encuesta
    with st.form("level_survey_form"):
        st.subheader(replace_emojis("📊 Calificación del Contenido"))
        
        # Question 1: Clarity rating
        clarity_rating = st.slider(
            "¿Qué tan claro fue el contenido del nivel?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy confuso, 5 = Muy claro",
            key="clarity"
        )
        st.caption(f"Calificación: {clarity_rating}/5")
        
        # Question 2: Difficulty rating
        difficulty_rating = st.slider(
            "¿Qué tan difícil te pareció este nivel?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy fácil, 5 = Muy difícil",
            key="difficulty"
        )
        st.caption(f"Calificación: {difficulty_rating}/5")
        
        # Question 3: Usefulness rating
        usefulness_rating = st.slider(
            "¿Qué tan útil consideras este contenido?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Poco útil, 5 = Muy útil",
            key="usefulness"
        )
        st.caption(f"Calificación: {usefulness_rating}/5")
        
        # Question 4: Engagement rating
        engagement_rating = st.slider(
            "¿Qué tan interesante y atractivo fue este nivel?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Poco interesante, 5 = Muy interesante",
            key="engagement"
        )
        st.caption(f"Calificación: {engagement_rating}/5")
        
        # Question 5: Pace rating
        pace_rating = st.slider(
            "¿Qué tan adecuado fue el ritmo del nivel?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy lento, 5 = Muy rápido",
            key="pace"
        )
        st.caption(f"Calificación: {pace_rating}/5")
        
        st.divider()
        
        st.subheader("💬 Comentarios y Sugerencias")
        
        # Question 6: What did you like
        what_liked = st.text_area(
            "¿Qué te gustó más de este nivel?",
            placeholder="Comparte lo que más te gustó...",
            key="liked",
            height=100
        )
        
        # Question 7: What could be improved
        improvements = st.text_area(
            "¿Qué mejorarías o cambiarías?",
            placeholder="Comparte tus sugerencias para mejorar...",
            key="improvements",
            height=100
        )
        
        # Question 8: Additional comments
        additional_comments = st.text_area(
            "¿Tienes algún otro comentario? (Opcional)",
            placeholder="Cualquier otro comentario...",
            key="comments",
            height=100
        )
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button(replace_emojis("✅ Enviar Encuesta"), type="primary", use_container_width=True)
        
        if submitted:
            # Compile responses
            responses = {
                'clarity_rating': clarity_rating,
                'difficulty_rating': difficulty_rating,
                'usefulness_rating': usefulness_rating,
                'engagement_rating': engagement_rating,
                'pace_rating': pace_rating,
                'what_liked': what_liked.strip() if what_liked else "",
                'suggestions': improvements.strip() if improvements else "",
                'additional_comments': additional_comments.strip() if additional_comments else "",
                'completed_at': datetime.now().isoformat()
            }
            
            # Save to database
            if survey_system.save_survey_response(user_id, 'level', responses, level):
                st.session_state[f'survey_{level}_submitted'] = True
                st.markdown(replace_emojis("✅ ¡Gracias por tu feedback!"), unsafe_allow_html=True)
                st.balloons()
                st.rerun()
            else:
                st.markdown(replace_emojis("❌ Hubo un error al guardar tus respuestas. Por favor intenta de nuevo."), unsafe_allow_html=True)
    
    # UI - Mostrar Botones de Navegacion despues de Enviar Formulario
    if st.session_state.get(f'survey_{level}_submitted', False):
        st.divider()
        
        # Determine next level
        next_level = get_next_level(level)
        if next_level:
            st.info(f"Ahora puedes continuar con el {LEVEL_INFO[next_level]['name']}.")
            if st.button(f"Continuar al {LEVEL_INFO[next_level]['name']}", type="primary", use_container_width=True):
                # Clear survey_level from session state
                if 'survey_level' in st.session_state:
                    del st.session_state['survey_level']
                if f'survey_{level}_submitted' in st.session_state:
                    del st.session_state[f'survey_{level}_submitted']
                # Get the correct page path using mapping
                page_path = get_level_page_path(next_level)
                st.switch_page(page_path)
        else:
            # All levels completed
            st.info("¡Has completado todos los niveles! Ahora puedes completar la encuesta final.")
            if st.button("Completar Encuesta Final", type="primary", use_container_width=True):
                if 'survey_level' in st.session_state:
                    del st.session_state['survey_level']
                if f'survey_{level}_submitted' in st.session_state:
                    del st.session_state[f'survey_{level}_submitted']
                st.switch_page("pages/99_Survey_Final.py")


def get_next_level(current_level: str) -> str:
    """Get the next level after current level"""
    level_order = ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']
    try:
        current_index = level_order.index(current_level)
        if current_index < len(level_order) - 1:
            return level_order[current_index + 1]
    except ValueError:
        pass
    return None


def get_level_filename(level: str) -> str:
    """Get filename component for level"""
    mapping = {
        'nivel0': 'Introduccion',
        'nivel1': 'Basico',
        'nivel2': 'Filtros',
        'nivel3': 'Metricas',
        'nivel4': 'Avanzado'
    }
    return mapping.get(level, 'Basico')

def get_level_page_path(level: str) -> str:
    """Get the full page path for a level"""
    level_paths = {
        'nivel0': 'pages/00_Nivel_0_Introduccion.py',
        'nivel1': 'pages/01_Nivel_1_Basico.py',
        'nivel2': 'pages/02_Nivel_2_Filtros.py',
        'nivel3': 'pages/03_Nivel_3_Metricas.py',
        'nivel4': 'pages/04_Nivel_4_Avanzado.py'
    }
    return level_paths.get(level, 'pages/01_Nivel_1_Basico.py')


if __name__ == "__main__":
    main()

