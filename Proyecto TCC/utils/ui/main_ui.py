import streamlit as st

from utils.ui.icon_system import get_icon, replace_emojis
def show_header(name):
    """Show the main header with welcome message"""
    st.markdown(f'<h1 class="main-header">{get_icon("📊", 20)} Panel de Análisis de Datos</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.2rem;">Bienvenido, <strong>{name}</strong>! 👋</p>', unsafe_allow_html=True)

def show_quick_start_section():
    """Show the quick start section with main action buttons"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.8rem;">{get_icon("🚀", 28)} ¿Qué quieres hacer hoy?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    quick_actions = [
        {
            "card_html": f"""
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); margin-bottom: 1rem; border: 2px solid rgba(118,75,162,0.2);">
                <h3 style="color: #764ba2; margin-bottom: 1rem;">{get_icon("📚", 24)} Aprender</h3>
                <p style="color: #666; margin-bottom: 1.25rem;">Comienza por los niveles guiados paso a paso</p>
            </div>
            """,
            "button_label": "🎓 Ver Niveles",
            "button_type": "primary",
            "state_key": "show_learning_section",
            "button_key": "learn_main"
        },
        {
            "card_html": f"""
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h3 style="color: #28a745; margin-bottom: 1rem;">{get_icon("📤", 24)} Subir Datos</h3>
                <p style="color: #666; margin-bottom: 1.25rem;">Importa tus propios archivos para analizarlos</p>
            </div>
            """,
            "button_label": "📁 Subir Archivo",
            "button_type": "secondary",
            "state_key": "show_upload_section",
            "button_key": "upload_main"
        },
        {
            "card_html": f"""
            <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h3 style="color: #007bff; margin-bottom: 1rem;">{get_icon("📊", 24)} Datos de Ejemplo</h3>
                <p style="color: #666; margin-bottom: 1.25rem;">Practica con datasets listos para explorar</p>
            </div>
            """,
            "button_label": "🎯 Usar Ejemplos",
            "button_type": "secondary",
            "state_key": "show_examples_section",
            "button_key": "examples_main"
        },
    ]

    action_columns = st.columns(len(quick_actions))

    for col, action in zip(action_columns, quick_actions):
        with col:
            st.markdown(action["card_html"], unsafe_allow_html=True)
            if st.button(action["button_label"], type=action["button_type"], use_container_width=True, key=action["button_key"]):
                st.session_state[action["state_key"]] = True
                st.rerun()

def should_show_main_content():
    """Check if we should show the main content (not in any specific section)"""
    return not any([
        st.session_state.get('show_upload_section', False), 
        st.session_state.get('show_examples_section', False),
        st.session_state.get('show_learning_section', False),
        st.session_state.get('show_data_quality', False),
        st.session_state.get('show_dashboard', False)
    ])

def clear_selected_template():
    """Clear selected_template when showing main page to avoid redirect loops"""
    if 'selected_template' in st.session_state:
        del st.session_state.selected_template
