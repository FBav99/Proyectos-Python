import streamlit as st
import pandas as pd
from datetime import datetime

# Importar el gestor de niveles mejorados
from core.levels_manager import get_levels_ui, get_levels_manager

# Page config
st.set_page_config(
    page_title="Niveles Mejorados - Recursos Online Validados",
    page_icon="🌟",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
    }
    .metric-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .resource-link {
        background: #007bff;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        text-decoration: none;
        display: inline-block;
        margin: 5px;
        font-size: 0.9rem;
    }
    .certification-badge {
        background: #28a745;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌟 Niveles Mejorados</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Recursos Online Validados y Certificaciones Profesionales</p>', unsafe_allow_html=True)
    
    # Información sobre la mejora
    st.markdown("""
    <div class="info-box">
        <h2>🚀 Transformación de la Plataforma</h2>
        <p>Esta propuesta transforma el proyecto de una herramienta educativa básica a una plataforma de formación profesional reconocida en la industria de datos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obtener instancias
    levels_manager = get_levels_manager()
    levels_ui = get_levels_ui()
    
    # Simular progreso del usuario (en una implementación real, esto vendría de la base de datos)
    user_progress = {
        'nivel_1': st.session_state.get('nivel1_completed', False),
        'nivel_2': st.session_state.get('nivel2_completed', False),
        'nivel_3': st.session_state.get('nivel3_completed', False),
        'nivel_4': st.session_state.get('nivel4_completed', False)
    }
    
    # Tabs para diferentes secciones
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Ruta de Aprendizaje", 
        "📚 Recursos Online", 
        "🏆 Certificaciones", 
        "📊 Comparación"
    ])
    
    with tab1:
        st.markdown("## 🗺️ Tu Ruta de Aprendizaje Personalizada")
        
        # Mostrar progreso actual
        progress_summary = levels_manager.get_user_progress_summary(user_progress)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Niveles Completados", f"{progress_summary['completed_count']}/{progress_summary['total_levels']}")
        with col2:
            st.metric("Progreso Total", f"{progress_summary['progress_percentage']:.1f}%")
        with col3:
            st.metric("Tiempo Estimado", f"{progress_summary['total_estimated_time']}h")
        with col4:
            next_level = progress_summary.get('next_level')
            if next_level:
                next_info = levels_manager.get_level_info(next_level)
                st.metric("Próximo Nivel", next_info.get('title', '')[:20] + "...")
            else:
                st.metric("Próximo Nivel", "¡Completado!")
        
        # Mostrar siguiente nivel recomendado
        if next_level:
            next_level_info = levels_manager.get_level_info(next_level)
            st.info(f"""
            🎯 **Próximo Nivel Recomendado**: {next_level_info.get('title', '')}
            
            {next_level_info.get('subtitle', '')}
            
            ⏱️ Duración estimada: {next_level_info.get('duration', '')}
            """)
        
        # Mostrar todos los niveles con la nueva interfaz
        st.markdown("## 📚 Todos los Niveles Mejorados")
        levels = levels_manager.get_all_levels()
        
        for level_key in levels.keys():
            levels_ui.display_level_card(level_key, user_progress)
    
    with tab2:
        st.markdown("## 📚 Recursos Online Validados")
        
        # Mostrar recursos por nivel
        for level_key, level_info in levels.items():
            st.markdown(f"### {level_info.get('icon', '📚')} {level_info.get('title', '')}")
            
            resources = levels_manager.get_level_resources(level_key)
            if resources:
                cols = st.columns(min(3, len(resources)))
                for i, resource in enumerate(resources):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{resource.get('name', '')}</h4>
                            <p style="color: #666; font-size: 0.9rem;">{resource.get('description', '')}</p>
                            <a href="{resource.get('url', '#')}" target="_blank" class="resource-link">
                                🔗 Ver Recurso
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No hay recursos externos configurados para este nivel.")
            
            st.divider()
    
    with tab3:
        st.markdown("## 🏆 Roadmap de Certificaciones")
        
        # Mostrar todas las certificaciones disponibles
        all_certifications = []
        for level_key, level_info in levels.items():
            certifications = level_info.get('certifications', [])
            for cert in certifications:
                all_certifications.append({
                    'name': cert.get('name', ''),
                    'level': cert.get('level', ''),
                    'description': cert.get('description', ''),
                    'url': cert.get('url', ''),
                    'prerequisite_level': level_key,
                    'level_title': level_info.get('title', '')
                })
        
        if all_certifications:
            st.markdown("### Certificaciones Disponibles por Nivel:")
            
            for cert in all_certifications:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{cert['name']}</h3>
                    <p><strong>Nivel:</strong> {cert['level']}</p>
                    <p><strong>Descripción:</strong> {cert['description']}</p>
                    <p><strong>Prerrequisito:</strong> {cert['level_title']}</p>
                    <a href="{cert['url']}" target="_blank" class="certification-badge">
                        🏆 Obtener Certificación
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay certificaciones configuradas.")
    
    with tab4:
        st.markdown("## 📊 Comparación: Antes vs Después")
        
        # Crear tabla comparativa
        comparison_data = {
            'Aspecto': [
                'Fundamentación Teórica',
                'Recursos de Referencia',
                'Certificaciones',
                'Estándares de la Industria',
                'Aplicación Práctica',
                'Carrera Profesional',
                'Credibilidad',
                'Escalabilidad'
            ],
            'Antes': [
                '❌ Básica',
                '❌ Limitados',
                '❌ No disponibles',
                '❌ No alineados',
                '❌ Ejemplos simples',
                '❌ No definida',
                '❌ Baja',
                '❌ Limitada'
            ],
            'Después': [
                '✅ DAMA-DMBOK, CRISP-DM',
                '✅ Recursos oficiales',
                '✅ Google, Microsoft, AWS',
                '✅ Estándares internacionales',
                '✅ Casos reales',
                '✅ Ruta clara',
                '✅ Alta',
                '✅ Ilimitada'
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Métricas de mejora
        st.markdown("### 📈 Métricas de Mejora")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Recursos Online", "20+", "+400%")
        with col2:
            st.metric("Certificaciones", "12+", "+∞")
        with col3:
            st.metric("Estándares", "5+", "+∞")
        
        # Beneficios
        st.markdown("### 🎯 Beneficios Clave")
        
        benefits = [
            "**Aprendizaje Validado**: Contenido basado en estándares de la industria",
            "**Certificaciones Reconocidas**: Preparación para certificaciones profesionales",
            "**Aplicación Práctica**: Casos de estudio reales",
            "**Carrera Profesional**: Ruta clara de desarrollo profesional",
            "**Credibilidad**: Contenido respaldado por organizaciones reconocidas",
            "**Escalabilidad**: Estructura que permite crecimiento",
            "**Diferencia**: Propuesta única en el mercado",
            "**Sostenibilidad**: Modelo de negocio basado en certificaciones"
        ]
        
        for benefit in benefits:
            st.markdown(f"✅ {benefit}")
    
    # Sección de implementación
    st.markdown("---")
    st.markdown("## 🚀 Próximos Pasos para la Implementación")
    
    steps = [
        "**Validación de Contenido**: Revisión por expertos en la industria",
        "**Desarrollo de Recursos**: Creación de materiales de aprendizaje",
        "**Integración de Herramientas**: Conexión con plataformas externas",
        "**Piloto**: Prueba con un grupo reducido de usuarios",
        "**Lanzamiento**: Implementación gradual de mejoras"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"{i}. {step}")
    
    # Call to action
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h2>🌟 ¿Listo para Transformar tu Plataforma?</h2>
        <p>Esta propuesta no solo mejora el contenido educativo, sino que posiciona tu proyecto como una plataforma de formación profesional reconocida en la industria de datos.</p>
        <p><strong>¡El futuro del aprendizaje de datos está aquí!</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
