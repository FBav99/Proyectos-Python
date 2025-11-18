from utils.ui.icon_system import get_icon, replace_emojis
"""
Project Timeline Page
Displays the project development timeline based on git commits
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.system.project_timeline import (
    get_git_commits,
    group_commits_by_week_and_action,
    get_timeline_summary,
    get_action_icon,
    get_action_color,
    format_week_label
)
from utils.ui import auth_ui
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Línea de Tiempo del Proyecto",
    page_icon=get_icon("📅", 20),
    layout="wide"
)

@safe_main
def main():
    # Initialize sidebar with user info
    auth_ui.init_sidebar()
    
    st.title(replace_emojis("📅 Línea de Tiempo del Proyecto"))
    st.markdown("---")
    
    # Load commits
    with st.spinner("Cargando commits del repositorio..."):
        commits = get_git_commits()
    
    if not commits:
        st.warning("⚠️ No se pudieron cargar los commits del repositorio. Asegúrate de que estás en un repositorio git válido.")
        return
    
    # Group commits by week and action
    grouped_commits = group_commits_by_week_and_action(commits)
    summary = get_timeline_summary(grouped_commits)
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(replace_emojis("📊 Total de Commits"), summary['total_commits'])
    
    with col2:
        st.metric(replace_emojis("📅 Semanas de Desarrollo"), summary['total_weeks'])
    
    with col3:
        if summary['first_week']:
            first_date = datetime.strptime(summary['first_week'], '%Y-%m-%d')
            st.metric(replace_emojis("🚀 Inicio"), first_date.strftime('%d/%m/%Y'))
    
    with col4:
        if summary['last_week']:
            last_date = datetime.strptime(summary['last_week'], '%Y-%m-%d')
            st.metric(replace_emojis("🔄 Última Semana"), last_date.strftime('%d/%m/%Y'))
    
    st.markdown("---")
    
    # Action type summary
    st.subheader(replace_emojis("📈 Resumen por Tipo de Acción"))
    action_counts = summary['action_counts']
    
    if action_counts:
        cols = st.columns(len(action_counts))
        for idx, (action_type, count) in enumerate(sorted(action_counts.items(), key=lambda x: x[1], reverse=True)):
            with cols[idx]:
                icon = get_action_icon(action_type)
                color = get_action_color(action_type)
                st.markdown(f"""
                <div style="background: {color}15; padding: 1rem; border-radius: 8px; 
                            border-left: 4px solid {color}; text-align: center;">
                    <h3 style="margin: 0; color: {color};">{icon} {action_type}</h3>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: bold;">{count}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Timeline visualization
    st.subheader(replace_emojis("📅 Línea de Tiempo por Semanas"))
    
    # Display timeline in reverse chronological order (most recent first)
    weeks = sorted(grouped_commits.keys(), reverse=True)
    
    for week_start in weeks:
        week_data = grouped_commits[week_start]
        week_label = format_week_label(week_start)
        
        # Week header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1.5rem 0 1rem 0;">
            <h3 style="color: white; margin: 0;">{week_label}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Group actions by type
        for action_type in sorted(week_data.keys()):
            action_commits = week_data[action_type]
            icon = get_action_icon(action_type)
            color = get_action_color(action_type)
            
            with st.expander(f"{icon} **{action_type}** ({len(action_commits)} commits)", expanded=False):
                # Group similar commits together
                commit_groups = {}
                for commit in action_commits:
                    # Extract main message (remove prefix)
                    message = commit['message']
                    if ':' in message:
                        main_msg = message.split(':', 1)[1].strip()
                    else:
                        main_msg = message
                    
                    # Normalize message for grouping (remove extra spaces, lowercase, first 35 chars)
                    normalized = ' '.join(main_msg.lower().split())
                    key = normalized[:35] if len(normalized) > 35 else normalized
                    
                    if key not in commit_groups:
                        commit_groups[key] = []
                    commit_groups[key].append(commit)
                
                # Display grouped commits
                for group_key, group_commits in sorted(commit_groups.items()):
                    if len(group_commits) == 1:
                        commit = group_commits[0]
                        message = commit['message']
                        if ':' in message:
                            main_msg = message.split(':', 1)[1].strip()
                        else:
                            main_msg = message
                        
                        date_obj = datetime.strptime(commit['date'], '%Y-%m-%d')
                        st.markdown(f"""
                        <div style="padding: 0.5rem; margin: 0.25rem 0; 
                                    border-left: 3px solid {color}; padding-left: 1rem;">
                            <p style="margin: 0; color: #333;"><strong>{main_msg}</strong></p>
                            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #666;">
                                📅 {date_obj.strftime('%d/%m/%Y')} | 🔑 {commit['hash'][:7]}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Multiple similar commits
                        commit = group_commits[0]
                        message = commit['message']
                        if ':' in message:
                            main_msg = message.split(':', 1)[1].strip()
                        else:
                            main_msg = message
                        
                        dates = sorted([datetime.strptime(c['date'], '%Y-%m-%d') for c in group_commits])
                        date_range = f"{dates[0].strftime('%d/%m')} - {dates[-1].strftime('%d/%m/%Y')}"
                        
                        st.markdown(f"""
                        <div style="padding: 0.5rem; margin: 0.25rem 0; 
                                    border-left: 3px solid {color}; padding-left: 1rem;">
                            <p style="margin: 0; color: #333;">
                                <strong>{main_msg}</strong> 
                                <span style="background: {color}20; padding: 0.2rem 0.5rem; 
                                             border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem;">
                                    {len(group_commits)} veces
                                </span>
                            </p>
                            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #666;">
                                📅 {date_range}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption(replace_emojis("💡 Esta línea de tiempo se genera automáticamente a partir de los commits del repositorio Git."))

if __name__ == "__main__":
    main()

