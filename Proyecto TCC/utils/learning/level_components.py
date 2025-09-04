import streamlit as st
from core.progress_tracker import progress_tracker

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
