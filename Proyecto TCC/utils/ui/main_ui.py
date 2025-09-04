import streamlit as st

def show_header(name):
    """Show the main header with welcome message"""
    st.markdown(f'<h1 class="main-header">📊 Panel de Análisis de Datos</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.2rem;">Bienvenido, <strong>{name}</strong>! 👋</p>', unsafe_allow_html=True)

def show_quick_start_section():
    """Show the quick start section with main action buttons"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.8rem;">🚀 ¿Qué quieres hacer hoy?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Main action buttons in a clean grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #28a745; margin-bottom: 1rem;">📤 Subir Datos</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Comienza con tus propios archivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📁 Subir Archivo", type="primary", use_container_width=True, key="upload_main"):
            st.session_state.show_upload_section = True
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #007bff; margin-bottom: 1rem;">📊 Datos de Ejemplo</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Practica con datasets predefinidos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Usar Ejemplos", type="secondary", use_container_width=True, key="examples_main"):
            st.session_state.show_examples_section = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #ffc107; margin-bottom: 1rem;">📚 Aprender</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Completa los niveles de aprendizaje</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎓 Ver Niveles", type="secondary", use_container_width=True, key="learn_main"):
            st.session_state.show_learning_section = True
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
