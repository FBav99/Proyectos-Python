import streamlit as st
from core.progress_tracker import progress_tracker
from utils.ui.icon_system import get_icon, replace_emojis

def get_level_progress(user_id):
    """Get current progress across all levels from database"""
    try:
        progress = progress_tracker.get_user_progress(user_id)
        level_progress = {
            'nivel0': progress.get('nivel0_completed', False),
            'nivel1': progress.get('nivel1_completed', False),
            'nivel2': progress.get('nivel2_completed', False),
            'nivel3': progress.get('nivel3_completed', False),
            'nivel4': progress.get('nivel4_completed', False)
        }
        
        completed_count = sum(level_progress.values())
        total_progress = (completed_count / 5) * 100
        
        return total_progress, completed_count, level_progress
    except Exception as e:
        st.error(f"Error getting progress: {e}")
        return 0, 0, {'nivel0': False, 'nivel1': False, 'nivel2': False, 'nivel3': False, 'nivel4': False}

def show_learning_section(total_progress, completed_count, progress):
    """Show the learning section with progress tracking"""
    st.markdown("---")
    
    # Check if user has completed initial survey
    from core.survey_system import survey_system
    user = st.session_state.get('user')
    if user and user.get('id'):
        user_id = user['id']
        if not survey_system.has_completed_survey(user_id, 'initial'):
            st.markdown(f"""
            <div style="background: rgba(0, 123, 255, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #007bff;">
                <h3 style="color: #007bff; margin-bottom: 1rem;">{get_icon('📋', 20)} Encuesta Inicial</h3>
                <p style="color: #666; margin-bottom: 1rem;">Antes de comenzar con los niveles, nos gustaría conocer un poco sobre ti. Esto nos ayuda a mejorar la experiencia.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📝 Completar Encuesta Inicial", type="primary", use_container_width=True):
                st.switch_page("pages/99_Survey_Inicial.py")
            
            st.markdown(replace_emojis("💡 Puedes completar la encuesta más tarde, pero te recomendamos hacerlo antes de comenzar."), unsafe_allow_html=True)
            st.markdown("---")
    
    st.markdown(f"""
    <div style="background: rgba(255, 193, 7, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #ffc107;">
        <h3 style="color: #ffc107; margin-bottom: 1rem;">{get_icon('🎓', 20)} Sistema de Aprendizaje por Niveles</h3>
        <p style="color: #666; margin-bottom: 1rem;">Completa nuestros niveles paso a paso para dominar todas las funcionalidades</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso: {total_progress:.0f}% - {completed_count} de 5 niveles completados")
        if not st.session_state.get('_level_status_styles_injected'):
            st.markdown("""
            <style>
                .level-status-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 1rem;
                    margin-top: 1rem;
                }
                .level-status-card {
                    background: rgba(148, 163, 184, 0.12);
                    border: 1px solid rgba(148, 163, 184, 0.32);
                    border-radius: 14px;
                    padding: 1rem;
                    text-align: center;
                    transition: all 0.3s ease;
                    opacity: 0.45;
                }
                .level-status-card.completed {
                    background: linear-gradient(135deg, rgba(46, 204, 113, 0.22), rgba(34, 197, 94, 0.12));
                    border-color: rgba(34, 197, 94, 0.45);
                    opacity: 1;
                    box-shadow: 0 8px 18px rgba(34, 197, 94, 0.18);
                }
                .level-status-card.next {
                    border-color: rgba(249, 115, 22, 0.6);
                    background: linear-gradient(135deg, rgba(249, 115, 22, 0.18), rgba(249, 115, 22, 0.06));
                    opacity: 0.85;
                    box-shadow: 0 8px 18px rgba(249, 115, 22, 0.18);
                }
                .level-status-card .level-icon {
                    font-size: 1.3rem;
                    display: block;
                    margin-bottom: 0.35rem;
                }
                .level-status-card .level-label {
                    font-weight: 600;
                    color: var(--text-color, #1f2937);
                    display: block;
                    margin-bottom: 0.2rem;
                }
                .level-status-card .level-subtitle {
                    font-size: 0.85rem;
                    color: rgba(71, 85, 105, 0.9);
                    display: block;
                    margin-bottom: 0.35rem;
                }
                .level-status-card .level-state {
                    font-size: 0.8rem;
                    color: rgba(71, 85, 105, 0.85);
                    display: block;
                }
                @media (max-width: 768px) {
                    .level-status-grid {
                        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                    }
                }
            </style>
            """, unsafe_allow_html=True)
            st.session_state['_level_status_styles_injected'] = True

        level_definitions = [
            ('nivel0', 'Nivel 0', 'Introducción'),
            ('nivel1', 'Nivel 1', 'Básico'),
            ('nivel2', 'Nivel 2', 'Filtros'),
            ('nivel3', 'Nivel 3', 'Métricas'),
            ('nivel4', 'Nivel 4', 'Avanzado'),
        ]
        next_pending_level = next((level for level, _, _ in level_definitions if not progress.get(level, False)), None)

        status_cards_html = ['<div class="level-status-grid">']
        for level_key, level_title, level_subtitle in level_definitions:
            completed = progress.get(level_key, False)
            classes = ["level-status-card"]
            classes.append("completed" if completed else "pending")
            if not completed and level_key == next_pending_level:
                classes.append("next")
            icon = get_icon("✅", 20) if completed else get_icon("⏳", 20)
            state_text = "Completado" if completed else ("Siguiente paso" if level_key == next_pending_level else "Pendiente")
            status_cards_html.append(
                f"""
                <div class="{' '.join(classes)}">
                    <span class="level-icon">{icon}</span>
                    <span class="level-label">{level_title}</span>
                    <span class="level-subtitle">{level_subtitle}</span>
                    <span class="level-state">{state_text}</span>
                </div>
                """
            )
        status_cards_html.append("</div>")
        st.markdown("".join(status_cards_html), unsafe_allow_html=True)
    
    # Add progress reset button in learning section
    st.markdown("---")
    st.markdown(f"### {get_icon('🔄', 20)} Opciones de Progreso", unsafe_allow_html=True)
    
    # Get user ID for reset functionality
    user = st.session_state.get('user')
    if user and user.get('id'):
        user_id = user['id']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔄 Reiniciar Progreso", type="secondary", use_container_width=True):
                st.session_state.show_reset_confirmation = True
        
        with col2:
            if st.button("📊 Ver Progreso Detallado", use_container_width=True):
                st.session_state.show_detailed_progress = True
        
        # Reset confirmation dialog
        if st.session_state.get('show_reset_confirmation', False):
            st.markdown(f"""
            <div style="background: rgba(220, 53, 69, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc3545;">
                <h4 style="color: #dc3545; margin-bottom: 1rem;">{get_icon("⚠️", 18)} Confirmar Reinicio de Progreso</h4>
                <p style="color: #666; margin-bottom: 1rem;">Esta acción eliminará todo tu progreso en los niveles. <strong>Esta acción no se puede deshacer.</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("✅ Sí, Reiniciar", type="primary", use_container_width=True):
                    if reset_all_progress(user_id):
                        st.markdown(replace_emojis("✅ Progreso reiniciado exitosamente"), unsafe_allow_html=True)
                        st.session_state.show_reset_confirmation = False
                        st.rerun()
                    else:
                        st.markdown(replace_emojis("❌ Error al reiniciar el progreso"), unsafe_allow_html=True)
            
            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.session_state.show_reset_confirmation = False
                    st.rerun()
            
            with col3:
                if st.button("🔒 Cerrar", use_container_width=True):
                    st.session_state.show_reset_confirmation = False
                    st.rerun()
        
        # Detailed progress view
        if st.session_state.get('show_detailed_progress', False):
            st.markdown("---")
            st.markdown(replace_emojis("### 📊 Progreso Detallado"), unsafe_allow_html=True)
            
            try:
                progress_detail = progress_tracker.get_user_progress(user_id)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    status = replace_emojis("✅ Completado") if progress_detail.get('nivel1_completed', False) else "⏳ Pendiente"
                    st.metric("Nivel 1: Básico", status)
                
                with col2:
                    status = replace_emojis("✅ Completado") if progress_detail.get('nivel2_completed', False) else "⏳ Pendiente"
                    st.metric("Nivel 2: Filtros", status)
                
                with col3:
                    status = replace_emojis("✅ Completado") if progress_detail.get('nivel3_completed', False) else "⏳ Pendiente"
                    st.metric("Nivel 3: Métricas", status)
                
                with col4:
                    status = replace_emojis("✅ Completado") if progress_detail.get('nivel4_completed', False) else "⏳ Pendiente"
                    st.metric("Nivel 4: Avanzado", status)
                
                # Additional metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("⏱️ Tiempo Total", f"{progress_detail.get('total_time_spent', 0)} min")
                with col2:
                    st.metric(replace_emojis("📊 Análisis Creados"), f"{progress_detail.get('data_analyses_created', 0)}")
                
                # Last updated
                last_updated = progress_detail.get('last_updated', 'N/A')
                st.caption(f"Última actualización: {last_updated}")
                
                if st.button("🔒 Cerrar", use_container_width=True):
                    st.session_state.show_detailed_progress = False
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error al obtener progreso detallado: {e}")
    
    # Navigation buttons
    level_columns = st.columns(5)

    level_navigation = [
        ("nivel0", "🧭 Nivel 0: Introducción", "pages/00_Nivel_0_Introduccion.py"),
        ("nivel1", replace_emojis("📚 Nivel 1: Básico"), "pages/01_Nivel_1_Basico.py"),
        ("nivel2", replace_emojis("🔍 Nivel 2: Filtros"), "pages/02_Nivel_2_Filtros.py"),
        ("nivel3", replace_emojis("📊 Nivel 3: Métricas"), "pages/03_Nivel_3_Metricas.py"),
        ("nivel4", replace_emojis("🚀 Nivel 4: Avanzado"), "pages/04_Nivel_4_Avanzado.py"),
    ]

    next_pending_level = next((level for level, _, _ in level_navigation if not progress.get(level, False)), None)

    for col, (level_key, label, target_page) in zip(level_columns, level_navigation):
        with col:
            button_type = "primary" if progress.get(level_key, False) else "secondary"
            if st.button(label, type=button_type, use_container_width=True, key=f"learn_{level_key}"):
                st.switch_page(target_page)
            if level_key == next_pending_level and not progress.get(level_key, False):
                st.caption("⭐ Comienza aquí")
    
    st.markdown("")
    if st.button("❓ Ayuda y Recursos", use_container_width=True, key="learn_ayuda"):
        st.switch_page("pages/00_Ayuda.py")
    
    # Back button
    if st.button("⬅️ Volver", key="back_from_learning"):
        st.session_state.show_learning_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

def show_user_profile_section(username, total_progress, completed_count, user_id):
    """Show user profile section with progress metrics"""
    st.markdown("---")
    st.markdown(replace_emojis("### 👤 Tu Progreso"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(replace_emojis("📊 Niveles Completados"), f"{completed_count}/5")
    with col2:
        st.metric(replace_emojis("📈 Progreso Total"), f"{total_progress:.1f}%")
    with col3:
        st.metric(replace_emojis("🎯 Usuario"), username)
    
    # Progress reset and detailed view options
    if user_id:
        show_progress_reset_button(user_id)
        show_detailed_progress(user_id)
    
    # Quick navigation for experienced users
    if completed_count >= 2:
        st.markdown(f"""
        <div style="background: rgba(40, 167, 69, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #28a745;">
            <p style="color: #28a745; margin: 0; font-weight: 500;">{get_icon("💡", 16)} <strong>¡Ya tienes experiencia!</strong> Puedes ir directamente a crear dashboards avanzados.</p>
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

def save_level_progress(user_id, level_name, completed=True):
    """Save level completion progress to database"""
    try:
        if level_name == 'nivel0':
            progress_tracker.update_user_progress(user_id, nivel0_completed=completed)
        elif level_name == 'nivel1':
            progress_tracker.update_user_progress(user_id, nivel1_completed=completed)
        elif level_name == 'nivel2':
            progress_tracker.update_user_progress(user_id, nivel2_completed=completed)
        elif level_name == 'nivel3':
            progress_tracker.update_user_progress(user_id, nivel3_completed=completed)
        elif level_name == 'nivel4':
            progress_tracker.update_user_progress(user_id, nivel4_completed=completed)
        
        # Also update session state for immediate UI feedback
        st.session_state[f'{level_name}_completed'] = completed
        return True
    except Exception as e:
        st.error(f"Error saving progress: {e}")
        return False

def reset_all_progress(user_id):
    """Reset all level progress to incomplete"""
    try:
        progress_tracker.update_user_progress(
            user_id, 
            nivel0_completed=False,
            nivel1_completed=False,
            nivel2_completed=False,
            nivel3_completed=False,
            nivel4_completed=False
        )
        
        # Clear session state
        for level in ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']:
            if f'{level}_completed' in st.session_state:
                del st.session_state[f'{level}_completed']
        
        return True
    except Exception as e:
        st.error(f"Error resetting progress: {e}")
        return False

def show_progress_reset_button(user_id):
    """Show a button to reset progress with confirmation"""
    st.markdown("---")
    st.markdown(replace_emojis("### 🔄 Opciones de Progreso"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔄 Reiniciar Progreso", type="secondary", use_container_width=True):
            st.session_state.show_reset_confirmation = True
    
    with col2:
        if st.button("📊 Ver Progreso Detallado", use_container_width=True):
            st.session_state.show_detailed_progress = True
    
    # Reset confirmation dialog
    if st.session_state.get('show_reset_confirmation', False):
        st.markdown(f"""
        <div style="background: rgba(220, 53, 69, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc3545;">
            <h4 style="color: #dc3545; margin-bottom: 1rem;">{get_icon("⚠️", 18)} Confirmar Reinicio de Progreso</h4>
            <p style="color: #666; margin-bottom: 1rem;">Esta acción eliminará todo tu progreso en los niveles. <strong>Esta acción no se puede deshacer.</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Sí, Reiniciar", type="primary", use_container_width=True):
                if reset_all_progress(user_id):
                    st.markdown(replace_emojis("✅ Progreso reiniciado exitosamente"), unsafe_allow_html=True)
                    st.session_state.show_reset_confirmation = False
                    st.rerun()
                else:
                    st.markdown(replace_emojis("❌ Error al reiniciar el progreso"), unsafe_allow_html=True)
        
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.show_reset_confirmation = False
                st.rerun()
        
        with col3:
            if st.button("🔒 Cerrar", use_container_width=True):
                st.session_state.show_reset_confirmation = False
                st.rerun()

def show_detailed_progress(user_id):
    """Show detailed progress information"""
    if st.session_state.get('show_detailed_progress', False):
        st.markdown("---")
        st.markdown(replace_emojis("### 📊 Progreso Detallado"), unsafe_allow_html=True)
        
        try:
            progress = progress_tracker.get_user_progress(user_id)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status = replace_emojis("✅ Completado") if progress.get('nivel1_completed', False) else "⏳ Pendiente"
                st.metric("Nivel 1: Básico", status)
            
            with col2:
                status = replace_emojis("✅ Completado") if progress.get('nivel2_completed', False) else "⏳ Pendiente"
                st.metric("Nivel 2: Filtros", status)
            
            with col3:
                status = replace_emojis("✅ Completado") if progress.get('nivel3_completed', False) else "⏳ Pendiente"
                st.metric("Nivel 3: Métricas", status)
            
            with col4:
                status = replace_emojis("✅ Completado") if progress.get('nivel4_completed', False) else "⏳ Pendiente"
                st.metric("Nivel 4: Avanzado", status)
            
            # Additional metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("⏱️ Tiempo Total", f"{progress.get('total_time_spent', 0)} min")
            with col2:
                st.metric(replace_emojis("📊 Análisis Creados"), f"{progress.get('data_analyses_created', 0)}")
            
            # Last updated
            last_updated = progress.get('last_updated', 'N/A')
            st.caption(f"Última actualización: {last_updated}")
            
            if st.button("🔒 Cerrar", use_container_width=True):
                st.session_state.show_detailed_progress = False
                st.rerun()
                
        except Exception as e:
            st.error(f"Error al obtener progreso detallado: {e}")
