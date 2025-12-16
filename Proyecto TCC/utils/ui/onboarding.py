# Nombre del Archivo: onboarding.py
# Descripción: Sistema de Onboarding/Tour Guiado para Streamlit - Proporciona una experiencia guiada paso a paso para nuevos usuarios
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
from typing import List, Dict, Optional
from utils.ui.icon_system import get_icon, replace_emojis


@st.cache_data(show_spinner=False, ttl=300)
def check_onboarding_status(user_id: int, _db_manager) -> bool:
    """
    Verificar si el usuario ha completado el onboarding desde la base de datos
    Retorna True si el onboarding está completado, False en caso contrario
    
    Cacheado por 5 minutos para reducir consultas a la base de datos durante la carga de páginas.
    El caché se invalida cuando el onboarding se marca como completado.
    
    Nota: _db_manager tiene guión bajo inicial para indicarle a Streamlit que no lo hashee
    (los objetos DatabaseManager no son hasheables).
    """
    try:
        with _db_manager.get_connection() as conn:
            cursor = conn.cursor()
            if _db_manager.db_type == "supabase":
                cursor.execute(
                    "SELECT onboarding_completed FROM users WHERE id = %s",
                    (user_id,)
                )
            else:
                cursor.execute(
                    "SELECT onboarding_completed FROM users WHERE id = ?",
                    (user_id,)
                )
            result = cursor.fetchone()
            if result:
                if isinstance(result, dict):
                    return result.get('onboarding_completed', False)
                return bool(result[0] if result else False)
            return False
    except Exception:
        # If column doesn't exist yet, return False
        return False


def mark_onboarding_complete(user_id: int, db_manager):
    """Marcar onboarding como completado en la base de datos"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            if db_manager.db_type == "supabase":
                cursor.execute(
                    "UPDATE users SET onboarding_completed = TRUE WHERE id = %s",
                    (user_id,)
                )
            else:
                cursor.execute(
                    "UPDATE users SET onboarding_completed = 1 WHERE id = ?",
                    (user_id,)
                )
            conn.commit()
        
        # Invalidate cache to ensure fresh data on next call
        check_onboarding_status.clear()
    except Exception as e:
        # If column doesn't exist, that's okay - we'll handle it gracefully
        st.warning(f"Could not save onboarding status: {e}")


def show_onboarding_modal(
    step: int,
    title: str,
    content: str,
    position: str = "center",
    show_back: bool = True,
    show_skip: bool = True
) -> str:
    """
    Show an onboarding modal/step
    
    Returns: 'next', 'back', 'skip', or 'close'
    """
    # Create modal overlay
    back_button = f'<button id="onboarding-back" style="padding: 0.5rem 1.5rem; background: #f0f0f0; border: none; border-radius: 5px; cursor: pointer;">⬅️ Atrás</button>' if show_back else ''
    skip_button = f'<button id="onboarding-skip" style="padding: 0.5rem 1.5rem; background: #f0f0f0; border: none; border-radius: 5px; cursor: pointer;">Saltar Tour</button>' if show_skip else ''
    next_text = 'Siguiente ➡️' if show_back or show_skip else 'Entendido ✓'
    back_script = f'document.getElementById("onboarding-back").addEventListener("click", function() {{ window.parent.postMessage({{type: "onboarding-action", action: "back"}}, "*"); }});' if show_back else ''
    skip_script = f'document.getElementById("onboarding-skip").addEventListener("click", function() {{ window.parent.postMessage({{type: "onboarding-action", action: "skip"}}, "*"); }});' if show_skip else ''
    modal_html = f'<div id="onboarding-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); z-index: 9999; display: flex; align-items: center; justify-content: center;"><div style="background: white; padding: 2rem; border-radius: 15px; max-width: 600px; width: 90%; box-shadow: 0 10px 40px rgba(0,0,0,0.3); position: relative;"><h2 style="color: #1f77b4; margin-bottom: 1rem;">{title}</h2><div style="color: #333; line-height: 1.6; margin-bottom: 2rem;">{content}</div><div style="display: flex; gap: 1rem; justify-content: flex-end;">{back_button}{skip_button}<button id="onboarding-next" style="padding: 0.5rem 1.5rem; background: #1f77b4; color: white; border: none; border-radius: 5px; cursor: pointer;">{next_text}</button></div></div></div><script>document.getElementById("onboarding-next").addEventListener("click", function() {{ window.parent.postMessage({{type: "onboarding-action", action: "next"}}, "*"); }});{back_script}{skip_script}</script>'
    
    st.components.v1.html(modal_html, height=600)
    
    # Use buttons as fallback if JS doesn't work
    col1, col2, col3 = st.columns([1, 1, 1])
    action = None
    
    with col1:
        if show_back:
            if st.button("⬅️ Atrás", key=f"onboarding_back_{step}"):
                action = "back"
    
    with col2:
        if show_skip:
            if st.button("Saltar Tour", key=f"onboarding_skip_{step}"):
                action = "skip"
    
    with col3:
        if st.button("Siguiente ➡️" if (show_back or show_skip) else "Entendido ✓", 
                    key=f"onboarding_next_{step}", type="primary"):
            action = "next"
    
    return action or ""


def create_simple_onboarding_step(
    step_number: int,
    title: str,
    description: str,
    highlight_element: Optional[str] = None
):
    """
    Create a simple onboarding step using Streamlit components
    This version doesn't require JavaScript and works purely with Streamlit
    """
    st.markdown("---")
    st.markdown(f"### Paso {step_number}: {title}")
    st.info(replace_emojis(description))
    
    return st.button(f"Continuar al Paso {step_number + 1}", key=f"onboarding_step_{step_number}")


# Configuracion - Pasos de onboarding predefinidos para la plataforma
ONBOARDING_STEPS = [
    {
        "title": replace_emojis("👋 ¡Bienvenido a la Plataforma!"),
        "content": "<p>Te damos la bienvenida a nuestra plataforma de análisis de datos. Este tour rápido te mostrará las funcionalidades principales en menos de 2 minutos.</p><p><strong>¿Qué aprenderás?</strong></p><ul><li>📚 Cómo navegar por los niveles de aprendizaje</li><li>📊 Cómo cargar y analizar tus datos</li><li>🎯 Cómo crear dashboards profesionales</li></ul>",
    },
    {
        "title": replace_emojis("📚 Niveles de Aprendizaje"),
        "content": "<p>La plataforma tiene <strong>5 niveles progresivos</strong> que te enseñarán análisis de datos paso a paso:</p><ul><li><strong>Nivel 0:</strong> Conceptos básicos de datos</li><li><strong>Nivel 1:</strong> Preparación y carga de datos</li><li><strong>Nivel 2:</strong> Filtros y organización</li><li><strong>Nivel 3:</strong> Métricas y KPIs</li><li><strong>Nivel 4:</strong> Visualizaciones avanzadas</li></ul><p>Cada nivel incluye ejercicios prácticos y un quiz al final.</p>",
    },
    {
        "title": replace_emojis("📤 Carga de Datos"),
        "content": "<p>Puedes trabajar con tus propios datos subiendo archivos CSV o Excel.</p><p><strong>Formatos soportados:</strong></p><ul><li>CSV (.csv)</li><li>Excel (.xlsx, .xls)</li></ul><p>También puedes usar nuestros datasets de ejemplo para practicar.</p>",
    },
    {
        "title": replace_emojis("📊 Dashboard Blanco"),
        "content": "<p>Una vez que tengas datos, puedes crear dashboards personalizados con:</p><ul><li>Métricas clave (KPIs)</li><li>Gráficos interactivos</li><li>Filtros personalizados</li><li>Visualizaciones profesionales</li></ul>",
    },
    {
        "title": replace_emojis("✅ ¡Listo para Comenzar!"),
        "content": "<p>Ya conoces lo básico de la plataforma. ¡Es hora de empezar a aprender!</p><p><strong>Sugerencia:</strong> Comienza por el <strong>Nivel 0</strong> si es tu primera vez con análisis de datos.</p><p>¡Éxito en tu aprendizaje! 🚀</p>",
        "show_back": False,
        "show_skip": False,
    },
]


def show_onboarding_tour(user_id: Optional[int] = None, db_manager=None):
    """
    Función principal para mostrar el tour de onboarding
    Gestiona el flujo paso a paso usando el estado de sesión
    """
    # Initialize onboarding state
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 0
    if 'onboarding_active' not in st.session_state:
        st.session_state.onboarding_active = True
    
    if not st.session_state.onboarding_active:
        return False
    
    current_step = st.session_state.onboarding_step
    
    # Check if we've completed all steps
    if current_step >= len(ONBOARDING_STEPS):
        st.session_state.onboarding_active = False
        if user_id and db_manager:
            mark_onboarding_complete(user_id, db_manager)
        return False
    
    # Get current step configuration
    step_config = ONBOARDING_STEPS[current_step]
    
    # Show the step using simple Streamlit components (no JS required)
    st.markdown("---")
    st.markdown(f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2); color: white;"><h2 style="color: white; margin-bottom: 1rem;">{step_config["title"]}</h2><div style="line-height: 1.8;">{step_config["content"]}</div><div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);"><small>Paso {current_step + 1} de {len(ONBOARDING_STEPS)}</small></div></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_step > 0:
            if st.button("⬅️ Atrás", key="onboarding_back", use_container_width=True):
                st.session_state.onboarding_step -= 1
                st.rerun()
    
    with col2:
        if st.button("Saltar Tour", key="onboarding_skip", use_container_width=True):
            st.session_state.onboarding_active = False
            if user_id and db_manager:
                mark_onboarding_complete(user_id, db_manager)
            st.rerun()
    
    with col3:
        button_text = "Finalizar ✓" if current_step == len(ONBOARDING_STEPS) - 1 else "Siguiente ➡️"
        if st.button(button_text, key="onboarding_next", use_container_width=True, type="primary"):
            if current_step < len(ONBOARDING_STEPS) - 1:
                st.session_state.onboarding_step += 1
                st.rerun()
            else:
                # Completed!
                st.session_state.onboarding_active = False
                if user_id and db_manager:
                    mark_onboarding_complete(user_id, db_manager)
                st.success(replace_emojis("✅ ¡Tour completado! Ya conoces las funcionalidades principales."))
                st.rerun()
    
    return True

