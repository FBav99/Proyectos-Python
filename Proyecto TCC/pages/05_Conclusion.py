# Nombre del Archivo: 05_Conclusion.py
# Descripción: Página de Conclusión - Resumen de la jornada de aprendizaje del usuario
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
from utils.learning import load_level_styles, get_level_progress
from utils.learning.learning_progress import save_level_progress
from utils.ui import auth_ui
from utils.ui.icon_system import get_icon, replace_emojis
from utils.learning.level_components import create_info_box, create_step_card
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configuracion - Configurar manejo de errores
configure_streamlit_error_handling()

# Configuracion - Configurar página
st.set_page_config(
    page_title="Conclusión - Tu Jornada de Aprendizaje",
    page_icon=get_icon("🎓", 20),
    layout="wide"
)

# Estilo - Cargar estilos CSS para páginas de nivel
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Configuracion - Recomendaciones de Herramientas BI basadas en preferencias
BI_TOOLS = {
    'tableau': {
        'name': 'Tableau',
        'icon': '📊',
        'description': 'Herramienta de visualización líder para análisis exploratorio y dashboards interactivos',
        'best_for': ['Visualizaciones avanzadas', 'Análisis exploratorio', 'Dashboards empresariales'],
        'learning_curve': 'Intermedia',
        'price': 'Desde $70/mes',
        'website': 'https://www.tableau.com'
    },
    'powerbi': {
        'name': 'Power BI',
        'icon': '⚡',
        'description': 'Solución completa de Microsoft para análisis de datos y business intelligence',
        'best_for': ['Integración con Microsoft', 'Análisis empresarial', 'Reportes automatizados'],
        'learning_curve': 'Baja a Intermedia',
        'price': 'Desde $10/mes',
        'website': 'https://powerbi.microsoft.com'
    },
    'python': {
        'name': 'Python + Pandas',
        'icon': '🐍',
        'description': 'Lenguaje de programación con librerías poderosas para análisis de datos y machine learning',
        'best_for': ['Análisis personalizado', 'Automatización', 'Machine Learning'],
        'learning_curve': 'Alta',
        'price': 'Gratis',
        'website': 'https://www.python.org'
    },
    'excel': {
        'name': 'Excel Avanzado',
        'icon': '📈',
        'description': 'Herramienta familiar con capacidades avanzadas de análisis y visualización',
        'best_for': ['Análisis básico a intermedio', 'Equipos que ya usan Excel', 'Reportes rápidos'],
        'learning_curve': 'Baja',
        'price': 'Incluido en Microsoft 365',
        'website': 'https://www.microsoft.com/excel'
    },
    'google_data_studio': {
        'name': 'Looker Studio (Google)',
        'icon': '📱',
        'description': 'Herramienta gratuita de Google para crear dashboards y reportes interactivos',
        'best_for': ['Dashboards básicos', 'Integración con Google Workspace', 'Costo cero'],
        'learning_curve': 'Baja',
        'price': 'Gratis',
        'website': 'https://lookerstudio.google.com'
    },
    'qlik': {
        'name': 'Qlik Sense',
        'icon': '🔍',
        'description': 'Plataforma de BI con capacidades de descubrimiento de datos y visualización',
        'best_for': ['Análisis asociativo', 'Dashboards interactivos', 'Self-service BI'],
        'learning_curve': 'Intermedia',
        'price': 'Desde $30/mes',
        'website': 'https://www.qlik.com'
    }
}

def get_bi_recommendation(preferences):
    """Generate BI tool recommendations based on user preferences"""
    scores = {
        'tableau': 0,
        'powerbi': 0,
        'python': 0,
        'excel': 0,
        'google_data_studio': 0,
        'qlik': 0
    }
    
    # Scoring based on preferences
    if 'visualizaciones' in preferences or 'dashboards' in preferences:
        scores['tableau'] += 3
        scores['powerbi'] += 2
        scores['google_data_studio'] += 2
        scores['qlik'] += 2
    
    if 'automatizacion' in preferences or 'personalizado' in preferences:
        scores['python'] += 3
        scores['excel'] += 1
    
    if 'empresarial' in preferences or 'reportes' in preferences:
        scores['powerbi'] += 3
        scores['tableau'] += 2
        scores['qlik'] += 2
    
    if 'gratis' in preferences or 'bajo_costo' in preferences:
        scores['python'] += 3
        scores['google_data_studio'] += 3
        scores['excel'] += 2
    
    if 'facil' in preferences or 'rapido' in preferences:
        scores['excel'] += 3
        scores['google_data_studio'] += 3
        scores['powerbi'] += 2
    
    if 'microsoft' in preferences:
        scores['powerbi'] += 3
        scores['excel'] += 2
    
    if 'exploratorio' in preferences:
        scores['tableau'] += 3
        scores['qlik'] += 2
    
    # Get top 3 recommendations
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = [tool_id for tool_id, score in sorted_scores[:3] if score > 0]
    
    return top_3 if top_3 else ['tableau', 'powerbi', 'excel']

# Principal - Página de Conclusión
@safe_main
def main():
    # UI - Inicializar Sidebar con Info de Usuario
    current_user = init_sidebar()
    
    # Validacion - Verificar Autenticacion de Usuario
    if not current_user:
        st.markdown(replace_emojis("🔐 Por favor inicia sesión para acceder a esta sección."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Usuario - Obtener Usuario Actual
    user = current_user
    if not user or 'id' not in user:
        st.markdown(replace_emojis("❌ Error: No se pudo obtener la información del usuario."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Title
    st.title(replace_emojis("🎓 Conclusión: Tu Jornada de Aprendizaje"))
    st.subheader("Resumen, Aplicación y Próximos Pasos")
    
    # 2. Progress Bar
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(1.0)
        st.caption(f"Progreso general: 100% (5/5 niveles completados)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Validacion - Verificar que Todos los Niveles Estén Completados
    all_completed = all([progress['nivel0'], progress['nivel1'], progress['nivel2'], 
                        progress['nivel3'], progress['nivel4']])
    
    if not all_completed:
        missing_levels = []
        if not progress['nivel0']: missing_levels.append("Nivel 0: Introducción")
        if not progress['nivel1']: missing_levels.append("Nivel 1: Básico")
        if not progress['nivel2']: missing_levels.append("Nivel 2: Filtros")
        if not progress['nivel3']: missing_levels.append("Nivel 3: Métricas")
        if not progress['nivel4']: missing_levels.append("Nivel 4: Avanzado")
        
        st.warning(f"⚠️ Para acceder a la conclusión, primero debes completar todos los niveles. Te faltan: {', '.join(missing_levels)}")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("Ver Mis Niveles", type="primary", use_container_width=True):
                st.switch_page("Inicio.py")
        return
    
    # 3. Celebration Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2.5rem; border-radius: 15px; margin: 2rem 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: white; margin-bottom: 1rem; font-size: 2.5rem;">🏆 ¡Felicidades!</h1>
        <p style="color: white; font-size: 1.3rem; margin-bottom: 0.5rem;">Has completado todos los niveles de aprendizaje</p>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">Estás listo para aplicar tus conocimientos en el mundo real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Resumen de Conceptos Aprendidos
    st.header(replace_emojis("📚 Resumen de lo que Aprendiste"))
    st.markdown("A lo largo de tu jornada, has adquirido conocimientos fundamentales en análisis de datos. Aquí tienes un resumen de los conceptos clave por nivel:")
    
    # Resumen por Nivel
    level_summaries = [
        {
            'level': 'Nivel 0',
            'title': 'Introducción',
            'icon': '🧭',
            'concepts': [
                'Qué son los datos y su importancia',
                'Tipos de datos (numéricos, texto, fecha, booleanos)',
                'Estructura de datos en tablas (filas y columnas)',
                'Diferencia entre datos limpios y datos con problemas',
                'Capacidades del análisis de datos'
            ]
        },
        {
            'level': 'Nivel 1',
            'title': 'Básico',
            'icon': '📚',
            'concepts': [
                'Preparación y carga de datos',
                'Identificación de problemas de calidad',
                'Limpieza de datos (valores faltantes, duplicados)',
                'Verificación de integridad de datos',
                'Transformación básica de datos'
            ]
        },
        {
            'level': 'Nivel 2',
            'title': 'Filtros',
            'icon': '🔍',
            'concepts': [
                'Aplicación de filtros a datos',
                'Segmentación por múltiples criterios',
                'Análisis por categorías y períodos',
                'Organización de información',
                'Extracción de insights específicos'
            ]
        },
        {
            'level': 'Nivel 3',
            'title': 'Métricas',
            'icon': '📊',
            'concepts': [
                'Cálculo de métricas clave (KPIs)',
                'Interpretación de resultados numéricos',
                'Análisis de tendencias',
                'Comparación de métricas entre categorías',
                'Uso de métricas para toma de decisiones'
            ]
        },
        {
            'level': 'Nivel 4',
            'title': 'Avanzado',
            'icon': '🚀',
            'concepts': [
                'Creación de visualizaciones interactivas',
                'Diseño de dashboards profesionales',
                'Cálculos personalizados y avanzados',
                'Integración de múltiples tipos de gráficos',
                'Presentación efectiva de datos'
            ]
        }
    ]
    
    for summary in level_summaries:
        with st.expander(f"{summary['icon']} {summary['level']}: {summary['title']}", expanded=False):
            st.markdown("**Conceptos clave que dominas:**")
            for concept in summary['concepts']:
                st.markdown(f"• {concept}")
    
    st.divider()
    
    # 5. Qué Esperar al Aplicar lo Aprendido
    st.header(replace_emojis("🌟 ¿Qué Puedes Esperar al Aplicar lo Aprendido?"))
    
    st.markdown("""
    Ahora que has completado todos los niveles, tienes las bases para:
    """)
    
    application_areas = [
        {
            'title': 'En tu Trabajo o Negocio',
            'icon': '💼',
            'content': [
                'Crear reportes de ventas y rendimiento',
                'Analizar tendencias de negocio',
                'Identificar oportunidades de mejora',
                'Presentar datos de manera profesional a tu equipo'
            ]
        },
        {
            'title': 'En Proyectos Personales',
            'icon': '📊',
            'content': [
                'Analizar tus finanzas personales',
                'Evaluar hábitos y productividad',
                'Tomar decisiones basadas en datos',
                'Compartir insights con visualizaciones claras'
            ]
        },
        {
            'title': 'En tu Desarrollo Profesional',
            'icon': '🚀',
            'content': [
                'Mejorar tu capacidad de análisis crítico',
                'Aumentar tu valor en el mercado laboral',
                'Desarrollar proyectos de análisis de datos',
                'Continuar aprendiendo herramientas más avanzadas'
            ]
        }
    ]
    
    cols = st.columns(3)
    for i, area in enumerate(application_areas):
        with cols[i]:
            create_info_box(
                "info-box",
                f"{area['icon']} {area['title']}",
                "<ul>" + "".join([f"<li>{item}</li>" for item in area['content']]) + "</ul>"
            )
    
    st.markdown("""
    **💡 Recuerda:** El análisis de datos es una habilidad que se mejora con la práctica. 
    Comienza aplicando lo aprendido en proyectos pequeños y ve aumentando la complejidad gradualmente.
    """)
    
    st.divider()
    
    # 6. Recomendaciones de Herramientas BI
    st.header(replace_emojis("🛠️ Encuentra la Herramienta BI Ideal para Ti"))
    st.markdown("""
    Basándote en tus preferencias y lo que más te llamó la atención durante el aprendizaje, 
    te recomendamos herramientas profesionales de Business Intelligence que pueden ayudarte a llevar tus análisis al siguiente nivel.
    """)
    
    # Formulario de preferencias
    with st.form("bi_preferences_form"):
        st.markdown("### 📝 Cuéntanos tus Preferencias")
        st.markdown("Selecciona las opciones que más te interesan para recibir recomendaciones personalizadas:")
        
        preferences = st.multiselect(
            "¿Qué es lo que más te interesa?",
            options=[
                'Visualizaciones avanzadas y dashboards interactivos',
                'Automatización y análisis personalizado',
                'Reportes empresariales y análisis de negocio',
                'Herramientas gratuitas o de bajo costo',
                'Facilidad de uso y aprendizaje rápido',
                'Integración con herramientas de Microsoft',
                'Análisis exploratorio y descubrimiento de datos',
                'Machine Learning y análisis avanzado'
            ],
            key="bi_preferences"
        )
        
        submitted = st.form_submit_button("🔍 Obtener Recomendaciones", type="primary", use_container_width=True)
    
    # Mostrar recomendaciones
    if submitted and preferences:
        # Normalizar preferencias para el algoritmo
        normalized_prefs = []
        pref_mapping = {
            'Visualizaciones avanzadas y dashboards interactivos': ['visualizaciones', 'dashboards'],
            'Automatización y análisis personalizado': ['automatizacion', 'personalizado'],
            'Reportes empresariales y análisis de negocio': ['empresarial', 'reportes'],
            'Herramientas gratuitas o de bajo costo': ['gratis', 'bajo_costo'],
            'Facilidad de uso y aprendizaje rápido': ['facil', 'rapido'],
            'Integración con herramientas de Microsoft': ['microsoft'],
            'Análisis exploratorio y descubrimiento de datos': ['exploratorio'],
            'Machine Learning y análisis avanzado': ['personalizado', 'automatizacion']
        }
        
        for pref in preferences:
            if pref in pref_mapping:
                normalized_prefs.extend(pref_mapping[pref])
        
        recommendations = get_bi_recommendation(normalized_prefs)
        
        st.markdown("### 🎯 Tus Recomendaciones Personalizadas")
        st.markdown("Basándote en tus preferencias, estas son las herramientas que mejor se adaptan a ti:")
        
        for i, tool_id in enumerate(recommendations, 1):
            tool = BI_TOOLS[tool_id]
            with st.expander(f"{i}. {tool['icon']} **{tool['name']}** - Recomendación #{i}", expanded=(i == 1)):
                st.markdown(f"**{tool['description']}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Ideal para:**")
                    for item in tool['best_for']:
                        st.markdown(f"• {item}")
                
                with col2:
                    st.markdown(f"**Curva de aprendizaje:** {tool['learning_curve']}")
                    st.markdown(f"**Precio:** {tool['price']}")
                
                st.markdown(f"**Sitio web:** [{tool['website']}]({tool['website']})")
        
        # Mostrar otras opciones
        other_tools = [tid for tid in BI_TOOLS.keys() if tid not in recommendations]
        if other_tools:
            with st.expander("💡 Otras Herramientas que Podrían Interesarte"):
                cols = st.columns(min(3, len(other_tools)))
                for i, tool_id in enumerate(other_tools):
                    tool = BI_TOOLS[tool_id]
                    with cols[i % 3]:
                        st.markdown(f"**{tool['icon']} {tool['name']}**")
                        st.caption(tool['description'])
    elif submitted:
        st.info("Por favor selecciona al menos una preferencia para obtener recomendaciones personalizadas.")
    else:
        # Mostrar información general sobre herramientas BI
        st.info("💡 Completa el formulario de arriba para recibir recomendaciones personalizadas basadas en tus intereses.")
        
        st.markdown("### 📋 Herramientas BI Principales")
        cols = st.columns(3)
        tools_list = list(BI_TOOLS.items())
        for i, (tool_id, tool) in enumerate(tools_list):
            with cols[i % 3]:
                st.markdown(f"**{tool['icon']} {tool['name']}**")
                st.caption(tool['description'])
    
    st.divider()
    
    # 7. Próximos Pasos
    st.header(replace_emojis("🎯 Próximos Pasos Recomendados"))
    
    next_steps = [
        {
            'step': '1',
            'title': 'Practica con tus Propios Datos',
            'description': 'Aplica lo aprendido analizando datos reales de tu trabajo, negocio o proyectos personales',
            'action': 'Crea tu primer análisis personal'
        },
        {
            'step': '2',
            'title': 'Explora Herramientas BI',
            'description': 'Prueba alguna de las herramientas recomendadas para llevar tus análisis al siguiente nivel',
            'action': 'Investiga las herramientas recomendadas'
        },
        {
            'step': '3',
            'title': 'Continúa Aprendiendo',
            'description': 'Profundiza en temas específicos como estadística, machine learning o visualización avanzada',
            'action': 'Busca cursos o recursos adicionales'
        },
        {
            'step': '4',
            'title': 'Comparte tus Proyectos',
            'description': 'Crea dashboards y visualizaciones para compartir insights con tu equipo o comunidad',
            'action': 'Comparte tus análisis'
        }
    ]
    
    for next_step in next_steps:
        create_step_card(
            step_number=next_step['step'],
            title=next_step['title'],
            description=next_step['description']
        )
    
    st.divider()
    
    # 8. Navegación Final
    st.header(replace_emojis("🔗 ¿Qué Quieres Hacer Ahora?"))
    
    nav_cols = st.columns(4)
    
    with nav_cols[0]:
        if st.button("📊 Crear Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/08_Dashboard_Blanco.py")
    
    with nav_cols[1]:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with nav_cols[2]:
        if st.button("📚 Revisar Niveles", use_container_width=True):
            st.switch_page("pages/00_Nivel_0_Introduccion.py")
    
    with nav_cols[3]:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
        <h3 style="color: #667eea;">🎓 ¡Gracias por Completar tu Jornada de Aprendizaje!</h3>
        <p style="color: #666;">Has adquirido las habilidades fundamentales para el análisis de datos. ¡Sigue practicando y explorando!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

