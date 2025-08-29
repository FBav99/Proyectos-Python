import streamlit as st
from core.auth_service import auth_service

def get_level_progress(user_id):
    """Get current progress across all levels from database"""
    try:
        progress = auth_service.get_user_progress(user_id)
        level_progress = {
            'nivel1': progress.get('nivel1_completed', False),
            'nivel2': progress.get('nivel2_completed', False),
            'nivel3': progress.get('nivel3_completed', False),
            'nivel4': progress.get('nivel4_completed', False)
        }
        
        completed_count = sum(level_progress.values())
        total_progress = (completed_count / 4) * 100
        
        return total_progress, completed_count, level_progress
    except Exception as e:
        st.error(f"Error getting progress: {e}")
        return 0, 0, {'nivel1': False, 'nivel2': False, 'nivel3': False, 'nivel4': False}

def show_learning_section(total_progress, completed_count, progress):
    """Show the learning section with progress tracking"""
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(255, 193, 7, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #ffc107;">
        <h3 style="color: #ffc107; margin-bottom: 1rem;">🎓 Sistema de Aprendizaje por Niveles</h3>
        <p style="color: #666; margin-bottom: 1rem;">Completa nuestros niveles paso a paso para dominar todas las funcionalidades</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso: {total_progress:.0f}% - {completed_count} de 4 niveles completados")
        
        # Show completion status for each level
        st.markdown("**Estado de Niveles:**")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            status = "✅" if progress['nivel1'] else "⏳"
            st.markdown(f"{status} Nivel 1")
        with col_b:
            status = "✅" if progress['nivel2'] else "⏳"
            st.markdown(f"{status} Nivel 2")
        with col_c:
            status = "✅" if progress['nivel3'] else "⏳"
            st.markdown(f"{status} Nivel 3")
        with col_d:
            status = "✅" if progress['nivel4'] else "⏳"
            st.markdown(f"{status} Nivel 4")
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📚 Nivel 1: Básico", type="primary", use_container_width=True, key="learn_nivel1"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col2:
        if st.button("🔍 Nivel 2: Filtros", use_container_width=True, key="learn_nivel2"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col3:
        if st.button("📊 Nivel 3: Métricas", use_container_width=True, key="learn_nivel3"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col4:
        if st.button("🚀 Nivel 4: Avanzado", use_container_width=True, key="learn_nivel4"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col5:
        if st.button("❓ Ayuda", use_container_width=True, key="learn_ayuda"):
            st.switch_page("pages/00_Ayuda.py")
    
    # Back button
    if st.button("⬅️ Volver", key="back_from_learning"):
        st.session_state.show_learning_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

def show_user_profile_section(username, total_progress, completed_count):
    """Show user profile section with progress metrics"""
    st.markdown("---")
    st.markdown("### 👤 Tu Progreso")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Niveles Completados", f"{completed_count}/4")
    with col2:
        st.metric("📈 Progreso Total", f"{total_progress:.1f}%")
    with col3:
        st.metric("🎯 Usuario", username)
    
    # Quick navigation for experienced users
    if completed_count >= 2:
        st.markdown("""
        <div style="background: rgba(40, 167, 69, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #28a745;">
            <p style="color: #28a745; margin: 0; font-weight: 500;">💡 <strong>¡Ya tienes experiencia!</strong> Puedes ir directamente a crear dashboards avanzados.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Dashboard Avanzado", use_container_width=True):
                st.switch_page("pages/04_Nivel_4_Avanzado.py")
        with col2:
            if st.button("📊 Métricas", use_container_width=True):
                st.switch_page("pages/03_Nivel_3_Metricas.py")
        with col3:
            if st.button("❓ Ayuda", use_container_width=True):
                st.switch_page("pages/00_Ayuda.py")
