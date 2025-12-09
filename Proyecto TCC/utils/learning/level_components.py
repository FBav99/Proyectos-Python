import streamlit as st
from core.progress_tracker import progress_tracker
from .progression_tracker import get_level_achievements, get_progression_summary, get_achievement_badge, get_data_quality_insights

from utils.ui.icon_system import get_icon, replace_emojis
def create_step_card(step_number, title, description, sections=None):
    """Create a step card with proper HTML structure"""
    html_content = f"""
    <div class="step-card">
        <div class="step-number">{step_number}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    """
    
    if sections:
        for section_title, items in sections.items():
            html_content += f"<h4>{section_title}</h4>"
            if isinstance(items, list):
                html_content += "<ul>"
                for item in items:
                    html_content += f"<li>{item}</li>"
                html_content += "</ul>"
            else:
                html_content += f"<ol>"
                for i, item in enumerate(items, 1):
                    html_content += f"<li>{item}</li>"
                html_content += "</ol>"
    
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)

def create_info_box(box_type, title, content):
    """Create info boxes with different styles"""
    html_content = f"""
    <div class="{box_type}">
        <h3>{title}</h3>
        {content}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def create_achievement_display(level, user_progress):
    """Create achievement display for completed levels"""
    achievements = get_level_achievements()
    
    if level not in achievements:
        return
    
    achievement_info = achievements[level]
    badge = get_achievement_badge(level)
    
    if badge:
        html_content = f"""
        <div class="achievement-card" style="border-left: 5px solid {badge['color']};">
            <div class="achievement-header">
                <span class="achievement-icon" style="color: {badge['color']};">{badge['icon']}</span>
                <h3 style="color: {badge['color']};">{badge['title']}</h3>
            </div>
            <p><strong>{achievement_info['description']}</strong></p>
            <h4>🎯 Habilidades Adquiridas:</h4>
            <ul>
        """
        
        for skill in achievement_info['skills_gained']:
            html_content += f"<li>{get_icon("✅", 20)} {skill}</li>"
        
        html_content += """
            </ul>
        </div>
        """
        
        st.markdown(html_content, unsafe_allow_html=True)

def create_progression_summary(user_progress):
    """Create a summary of user's progression"""
    summary = get_progression_summary(user_progress)
    achievements = get_level_achievements()
    
    # UI - Titulo Principal
    st.markdown(replace_emojis("### 📊 Tu Progreso de Aprendizaje"), unsafe_allow_html=True)
    
    # UI - Estadisticas de Progreso en Columnas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Niveles Completados", len(summary['completed_levels']))
    with col2:
        st.metric("Habilidades Aprendidas", summary['total_skills_learned'])
    with col3:
        st.metric("Progreso Total", f"{summary['completion_percentage']:.0f}%")
    
    # UI - Seccion de Logros
    if summary['completed_levels']:
        st.markdown(replace_emojis("#### 🏆 Logros Desbloqueados:"), unsafe_allow_html=True)
        
        # Create achievement badges in columns
        achievement_cols = st.columns(min(len(summary['completed_levels']), 3))
        for i, level in enumerate(summary['completed_levels']):
            if level in achievements:
                badge = get_achievement_badge(level)
                col_idx = i % 3
                with achievement_cols[col_idx]:
                    with st.container():
                        st.markdown(f"**{badge['icon']} {badge['title']}**")
    
    # UI - Proxima Meta
    next_milestone = summary['next_milestone']
    st.markdown(replace_emojis("#### 🎯 Siguiente Meta:"), unsafe_allow_html=True)
    st.markdown(f"**{next_milestone['title']}**", unsafe_allow_html=True)
    st.markdown(next_milestone['description'], unsafe_allow_html=True)

def create_data_quality_insight(level, data_type):
    """Create data quality insight display"""
    insight = get_data_quality_insights(level, data_type)
    
    quality_color = '#4CAF50' if insight['quality_score'] == '100%' else '#FF9800' if insight['quality_score'] == '95%' else '#F44336'
    
    html_content = f"""
    <div class="data-quality-card">
        <div class="quality-header">
            <h4>📊 {insight['title']}</h4>
            <span class="quality-score" style="color: {quality_color};">{insight['quality_score']}</span>
        </div>
        <p>{insight['description']}</p>
        <div class="quality-details">
            <strong>Estado de los datos:</strong> {insight['issues']}
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)

def create_level_preview(level):
    """Create preview of what user will achieve in this level"""
    achievements = get_level_achievements()
    
    if level not in achievements:
        return
    
    achievement_info = achievements[level]
    
    html_content = f"""
    <div class="level-preview">
        <h3>🎯 ¿Qué lograrás en este nivel?</h3>
        <div class="preview-content">
            <p><strong>{achievement_info['description']}</strong></p>
            <h4>🚀 Habilidades que desarrollarás:</h4>
            <ul>
    """
    
    for skill in achievement_info['skills_gained']:
        html_content += f"<li>{get_icon("🎯", 20)} {skill}</li>"
    
    html_content += f"""
            </ul>
            <div class="preview-next">
                <p><strong>Después de este nivel:</strong> {achievement_info['next_level_preview']}</p>
            </div>
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
