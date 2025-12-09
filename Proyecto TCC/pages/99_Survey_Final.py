from utils.ui.icon_system import get_icon, replace_emojis
# Final Survey - After All Levels Completed
# General experience quiz and comment box

import streamlit as st
from datetime import datetime
from core.survey_system import survey_system
from utils.ui import auth_ui
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

init_sidebar = auth_ui.init_sidebar

configure_streamlit_error_handling()

st.set_page_config(
    page_title="Encuesta Final",
    page_icon=get_icon("🏆", 20),
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
    if survey_system.has_completed_survey(user_id, 'final'):
        st.markdown(replace_emojis("✅ Ya completaste la encuesta final. ¡Gracias por tu participación!"), unsafe_allow_html=True)
        st.info("Puedes continuar explorando la plataforma.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    st.title(replace_emojis("🏆 Encuesta Final"))
    st.markdown("### ¡Felicitaciones por completar todos los niveles!")
    st.markdown("Tu opinión es crucial para mejorar la plataforma. Por favor, comparte tu experiencia general.")
    
    st.divider()
    
    # UI - Mostrar Preguntas de Encuesta
    with st.form("final_survey_form"):
        st.subheader(replace_emojis("📊 Experiencia General"))
        
        # Question 1: Overall satisfaction
        overall_satisfaction = st.slider(
            "¿Qué tan satisfecho estás con la experiencia general de aprendizaje?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy insatisfecho, 5 = Muy satisfecho",
            key="satisfaction"
        )
        st.caption(f"Calificación: {overall_satisfaction}/5")
        
        # Question 2: Learning achievement
        learning_achievement = st.slider(
            "¿Qué tan bien lograste los objetivos de aprendizaje?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy poco, 5 = Completamente",
            key="achievement"
        )
        st.caption(f"Calificación: {learning_achievement}/5")
        
        # Question 3: Platform ease of use
        ease_of_use = st.slider(
            "¿Qué tan fácil fue usar la plataforma?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy difícil, 5 = Muy fácil",
            key="ease"
        )
        st.caption(f"Calificación: {ease_of_use}/5")
        
        # Question 4: Content quality
        content_quality = st.slider(
            "¿Qué tan buena fue la calidad del contenido?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy mala, 5 = Muy buena",
            key="quality"
        )
        st.caption(f"Calificación: {content_quality}/5")
        
        # Question 5: Recommendation likelihood
        recommendation = st.slider(
            "¿Qué tan probable es que recomiendes esta plataforma a otros?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Muy improbable, 5 = Muy probable",
            key="recommend"
        )
        st.caption(f"Calificación: {recommendation}/5")
        
        st.divider()
        
        st.subheader(replace_emojis("🎯 Aspectos Específicos"))
        
        # Question 6: Best aspect
        best_aspect = st.selectbox(
            "¿Qué aspecto te gustó más?",
            [
                "La estructura y organización de los niveles",
                "La claridad de las explicaciones",
                "Los ejemplos prácticos",
                "La facilidad de uso de la plataforma",
                "La progresión de dificultad",
                "Los ejercicios prácticos",
                "Otro (especifica en comentarios)"
            ],
            key="best"
        )
        
        # Question 7: Most challenging aspect
        most_challenging = st.selectbox(
            "¿Qué aspecto te resultó más desafiante?",
            [
                "Ninguno - Todo fue fácil",
                "Entender conceptos nuevos",
                "Aplicar lo aprendido en ejercicios",
                "Navegar por la plataforma",
                "El ritmo de aprendizaje",
                "La complejidad de algunos niveles",
                "Otro (especifica en comentarios)"
            ],
            key="challenging"
        )
        
        st.divider()
        
        st.subheader("💬 Comentarios Generales")
        
        # Question 8: General comments
        general_comments = st.text_area(
            "Comentarios generales sobre la plataforma, contenido, o experiencia:",
            placeholder="Comparte cualquier comentario, sugerencia, o feedback que tengas...",
            key="comments",
            height=150
        )
        
        # Question 9: What would you add
        what_to_add = st.text_area(
            "¿Qué te gustaría ver añadido o mejorado en la plataforma? (Opcional)",
            placeholder="Funcionalidades, contenido, características...",
            key="additions",
            height=100
        )
        
        # Question 10: Additional feedback
        additional_feedback = st.text_area(
            "Cualquier otro comentario o sugerencia: (Opcional)",
            placeholder="Comparte cualquier otra cosa que quieras mencionar...",
            key="feedback",
            height=100
        )
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button(replace_emojis("✅ Enviar Encuesta Final"), type="primary", use_container_width=True)
        
        if submitted:
            # Compile responses
            responses = {
                'overall_satisfaction': overall_satisfaction,
                'learning_achievement': learning_achievement,
                'ease_of_use': ease_of_use,
                'content_quality': content_quality,
                'recommendation_likelihood': recommendation,
                'best_aspect': best_aspect,
                'most_challenging_aspect': most_challenging,
                'general_comments': general_comments.strip() if general_comments else "",
                'what_to_add': what_to_add.strip() if what_to_add else "",
                'additional_feedback': additional_feedback.strip() if additional_feedback else "",
                'completed_at': datetime.now().isoformat()
            }
            
            # Save to database
            if survey_system.save_survey_response(user_id, 'final', responses):
                st.markdown(replace_emojis("✅ ¡Gracias por completar la encuesta final!"), unsafe_allow_html=True)
                st.balloons()
                st.balloons()
                st.markdown(replace_emojis("### 🎉 ¡Tu opinión es muy valiosa para nosotros!"), unsafe_allow_html=True)
                st.info("Hemos guardado todas tus respuestas. Gracias por ayudarnos a mejorar la plataforma.")
                
                if st.button("Volver al Inicio", type="primary", use_container_width=True):
                    st.switch_page("Inicio.py")
            else:
                st.markdown(replace_emojis("❌ Hubo un error al guardar tus respuestas. Por favor intenta de nuevo."), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

