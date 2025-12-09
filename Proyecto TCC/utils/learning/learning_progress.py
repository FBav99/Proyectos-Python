import streamlit as st
from core.progress_tracker import progress_tracker
from utils.ui.icon_system import get_icon, replace_emojis

# Progreso - Obtener Progreso de Niveles
@st.cache_data(show_spinner=False, ttl=60)
def get_level_progress(user_id):
    """Get current progress across all levels from database
    
    Cached for 60 seconds to reduce database queries while allowing
    real-time updates when progress changes.
    """
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

# UI - Mostrar Seccion de Aprendizaje
def show_learning_section(total_progress, completed_count, progress):
    """Show the learning section with progress tracking"""
    st.markdown("---")
    
    
    st.markdown(f'<div style="background: rgba(255, 193, 7, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #ffc107;"><h3 style="color: #ffc107; margin-bottom: 1rem;">{get_icon("🎓", 20)} Sistema de Aprendizaje por Niveles</h3><p style="color: #666; margin-bottom: 1rem;">Completa nuestros niveles paso a paso para dominar todas las funcionalidades</p></div>', unsafe_allow_html=True)
    
    # UI - Indicador de Progreso
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
            ('nivel0', 'Nivel 0', 'Introducción', 'pages/00_Nivel_0_Introduccion.py'),
            ('nivel1', 'Nivel 1', 'Básico', 'pages/01_Nivel_1_Basico.py'),
            ('nivel2', 'Nivel 2', 'Filtros', 'pages/02_Nivel_2_Filtros.py'),
            ('nivel3', 'Nivel 3', 'Métricas', 'pages/03_Nivel_3_Metricas.py'),
            ('nivel4', 'Nivel 4', 'Avanzado', 'pages/04_Nivel_4_Avanzado.py'),
        ]
        next_pending_level = next((level for level, _, _, _ in level_definitions if not progress.get(level, False)), None)
        
        # Determine which levels are enabled (previous level completed or nivel0)
        def is_level_enabled(level_key):
            if level_key == 'nivel0':
                return True
            prev_level_map = {
                'nivel1': 'nivel0',
                'nivel2': 'nivel1',
                'nivel3': 'nivel2',
                'nivel4': 'nivel3'
            }
            prev_level = prev_level_map.get(level_key)
            return prev_level and progress.get(prev_level, False)
        
        # Create cards using Streamlit columns
        level_cols = st.columns(5)
        for col, (level_key, level_title, level_subtitle, target_page) in zip(level_cols, level_definitions):
            with col:
                completed = progress.get(level_key, False)
                enabled = is_level_enabled(level_key)
                is_next = (not completed and level_key == next_pending_level)
                is_next_and_nivel0 = (is_next and level_key == 'nivel0')
                
                # Determine card styling
                if completed:
                    card_style = "background: linear-gradient(135deg, rgba(46, 204, 113, 0.22), rgba(34, 197, 94, 0.12)); border: 1px solid rgba(34, 197, 94, 0.45); border-radius: 14px 14px 0 0; padding: 1.25rem 1rem; text-align: center; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15); min-height: 180px; display: flex; flex-direction: column; justify-content: space-between;"
                elif is_next:
                    card_style = "background: linear-gradient(135deg, rgba(249, 115, 22, 0.18), rgba(249, 115, 22, 0.06)); border: 1px solid rgba(249, 115, 22, 0.6); border-radius: 14px 14px 0 0; padding: 1.25rem 1rem; text-align: center; box-shadow: 0 4px 12px rgba(249, 115, 22, 0.15); min-height: 180px; display: flex; flex-direction: column; justify-content: space-between;"
                else:
                    card_style = "background: rgba(148, 163, 184, 0.12); border: 1px solid rgba(148, 163, 184, 0.32); border-radius: 14px 14px 0 0; padding: 1.25rem 1rem; text-align: center; min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.45;"
                
                icon = get_icon("✅", 20) if completed else get_icon("⏳", 20)
                state_text = "Completado" if completed else ("Siguiente paso" if is_next else "Pendiente")
                
                # Build card content HTML
                card_content = f'<div style="{card_style}"><div style="flex: 1;">'
                card_content += f'<div style="font-size: 1.3rem; display: block; margin-bottom: 0.5rem;">{icon}</div>'
                card_content += f'<div style="font-weight: 600; color: #1f2937; display: block; margin-bottom: 0.3rem; font-size: 1rem;">{level_title}</div>'
                card_content += f'<div style="font-size: 0.85rem; color: rgba(71, 85, 105, 0.9); display: block; margin-bottom: 0.4rem;">{level_subtitle}</div>'
                card_content += f'<div style="font-size: 0.8rem; color: rgba(71, 85, 105, 0.85); display: block; margin-bottom: 0.5rem;">{state_text}</div>'
                
                if is_next_and_nivel0:
                    card_content += '<div style="font-size: 0.75rem; color: rgba(249, 115, 22, 0.9); display: block; margin-bottom: 0.5rem; font-weight: 500;">⭐ Comienza aquí</div>'
                
                card_content += '</div>'
                
                # Add button or blocked text inside card
                if enabled:
                    button_label = "Ver Nivel" if not completed else "Revisar"
                    card_content += '<div style="margin-top: auto; padding-top: 0.75rem;"></div>'
                else:
                    card_content += '<div style="margin-top: auto; padding-top: 0.75rem; text-align: center; font-size: 0.75rem; color: rgba(148, 163, 184, 0.8);">Bloqueado</div>'
                
                card_content += '</div>'
                
                st.markdown(card_content, unsafe_allow_html=True)
                
                # Add button using Streamlit (positioned below card but visually connected)
                if enabled:
                    button_label = "Ver Nivel" if not completed else "Revisar"
                    # Style button container to match card
                    button_style = ""
                    if completed:
                        button_style = "background: linear-gradient(135deg, rgba(46, 204, 113, 0.3), rgba(34, 197, 94, 0.2)); border: 1px solid rgba(34, 197, 94, 0.45); border-radius: 0 0 14px 14px; padding: 0.5rem; margin-top: -1px;"
                    elif is_next:
                        button_style = "background: linear-gradient(135deg, rgba(249, 115, 22, 0.25), rgba(249, 115, 22, 0.15)); border: 1px solid rgba(249, 115, 22, 0.6); border-radius: 0 0 14px 14px; padding: 0.5rem; margin-top: -1px;"
                    else:
                        button_style = "background: rgba(148, 163, 184, 0.15); border: 1px solid rgba(148, 163, 184, 0.32); border-radius: 0 0 14px 14px; padding: 0.5rem; margin-top: -1px;"
                    
                    st.markdown(f'<div style="{button_style}">', unsafe_allow_html=True)
                    if st.button(button_label, key=f"card_btn_{level_key}", use_container_width=True):
                        st.switch_page(target_page)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # UI - Agregar Boton de Reinicio de Progreso en Seccion de Aprendizaje
    st.markdown("---")
    st.markdown(f"### {get_icon('🔄', 20)} Opciones de Progreso", unsafe_allow_html=True)
    
    # Consulta - Obtener ID de Usuario para Funcionalidad de Reinicio
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
            st.markdown(f'<div style="background: rgba(220, 53, 69, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc3545;"><h4 style="color: #dc3545; margin-bottom: 1rem;">{get_icon("⚠️", 18)} Confirmar Reinicio de Progreso</h4><p style="color: #666; margin-bottom: 1rem;">Esta acción eliminará todo tu progreso en los niveles. <strong>Esta acción no se puede deshacer.</strong></p></div>', unsafe_allow_html=True)
            
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
    
    # UI - Botones de Navegacion
    level_columns = st.columns(5)

    level_navigation = [
        ("nivel0", "🧭 Nivel 0: Introducción", "pages/00_Nivel_0_Introduccion.py"),
        ("nivel1", "📚 Nivel 1: Básico", "pages/01_Nivel_1_Basico.py"),
        ("nivel2", "🔍 Nivel 2: Filtros", "pages/02_Nivel_2_Filtros.py"),
        ("nivel3", "📊 Nivel 3: Métricas", "pages/03_Nivel_3_Metricas.py"),
        ("nivel4", "🚀 Nivel 4: Avanzado", "pages/04_Nivel_4_Avanzado.py"),
    ]
    
    # Si todos los niveles están completados, agregar enlace a conclusión
    all_levels_completed = all([progress.get(key, False) for key in ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']])
    if all_levels_completed:
        st.markdown("")
        if st.button("🎓 Conclusión y Próximos Pasos", use_container_width=True, type="primary", key="conclusion_button"):
            st.switch_page("pages/05_Conclusion.py")

    next_pending_level = next((level for level, _, _ in level_navigation if not progress.get(level, False)), None)

    for col, (level_key, label, target_page) in zip(level_columns, level_navigation):
        with col:
            button_type = "primary" if progress.get(level_key, False) else "secondary"
            if st.button(label, type=button_type, use_container_width=True, key=f"learn_{level_key}"):
                st.switch_page(target_page)
    
    st.markdown("")
    if st.button("❓ Ayuda y Recursos", use_container_width=True, key="learn_ayuda"):
        st.switch_page("pages/00_Ayuda.py")
    
    # UI - Boton de Regreso
    if st.button("⬅️ Volver", key="back_from_learning"):
        st.session_state.show_learning_section = False
        # Clear selected_template to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        st.rerun()

# UI - Mostrar Perfil de Usuario
def show_user_profile_section(username, total_progress, completed_count, user_id):
    """Show user profile section with progress metrics"""
    st.markdown("---")
    st.markdown(replace_emojis("### 👤 Tu Progreso"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Niveles Completados", f"{completed_count}/5")
    with col2:
        st.metric("📈 Progreso Total", f"{total_progress:.1f}%")
    with col3:
        st.metric("🎯 Usuario", username)
    
    # UI - Opciones de Reinicio de Progreso y Vista Detallada
    if user_id:
        show_progress_reset_button(user_id)
        show_detailed_progress(user_id)
    
    # UI - Navegacion Rapida para Usuarios con Experiencia
    if completed_count >= 2:
        st.markdown(f'<div style="background: rgba(40, 167, 69, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #28a745;"><p style="color: #28a745; margin: 0; font-weight: 500;">{get_icon("💡", 16)} <strong>¡Ya tienes experiencia!</strong> Puedes ir directamente a crear dashboards avanzados.</p></div>', unsafe_allow_html=True)
        
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

# Base de Datos - Guardar Progreso de Nivel
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
        
        # Invalidate cache to ensure fresh data on next call
        get_level_progress.clear()
        
        # Also update session state for immediate UI feedback
        st.session_state[f'{level_name}_completed'] = completed
        return True
    except Exception as e:
        st.error(f"Error saving progress: {e}")
        return False

# Progreso - Reiniciar Todo el Progreso
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
        
        # Invalidate cache to ensure fresh data on next call
        get_level_progress.clear()
        
        # Clear session state
        for level in ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']:
            if f'{level}_completed' in st.session_state:
                del st.session_state[f'{level}_completed']
        
        return True
    except Exception as e:
        st.error(f"Error resetting progress: {e}")
        return False

# UI - Mostrar Boton de Reinicio de Progreso
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
    
    # UI - Dialogo de Confirmacion de Reinicio
    if st.session_state.get('show_reset_confirmation', False):
        st.markdown(f'<div style="background: rgba(220, 53, 69, 0.1); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #dc3545;"><h4 style="color: #dc3545; margin-bottom: 1rem;">{get_icon("⚠️", 18)} Confirmar Reinicio de Progreso</h4><p style="color: #666; margin-bottom: 1rem;">Esta acción eliminará todo tu progreso en los niveles. <strong>Esta acción no se puede deshacer.</strong></p></div>', unsafe_allow_html=True)
        
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

# UI - Mostrar Progreso Detallado
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
