import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.auth_config import init_authentication, get_user_progress, update_user_progress
from core.data_loader import get_data
from core.data_quality_analyzer import data_quality_page
from data.sample_datasets import get_sample_datasets
from utils.metrics import calculate_metrics, calculate_growth_metrics, calculate_performance_insights
from utils.visualizations import (
    create_time_series_chart, 
    create_category_analysis, 
    create_regional_analysis,
    create_correlation_matrix,
    create_custom_calculation_charts
)
from utils.calculations import apply_custom_calculations
from utils.filters import apply_all_filters
from utils.ui_components import (
    create_sidebar_controls,
    create_custom_calculations_ui,
    display_metrics_dashboard,
    display_custom_calculations_metrics,
    display_export_section
)

def get_level_progress():
    """Get current progress across all levels"""
    progress = {
        'nivel1': st.session_state.get('nivel1_completed', False),
        'nivel2': st.session_state.get('nivel2_completed', False),
        'nivel3': st.session_state.get('nivel3_completed', False),
        'nivel4': st.session_state.get('nivel4_completed', False)
    }
    
    completed_count = sum(progress.values())
    total_progress = (completed_count / 4) * 100
    
    return total_progress, completed_count, progress

def main():
    """Función principal de la aplicación"""
    # Configurar página específica para Inicio
    st.set_page_config(
        page_title="Inicio - Dashboard Principal",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Initialize authentication
    authenticator = init_authentication()
    
    # Login using the correct method from the official documentation
    authenticator.login()
    
    # Check authentication status using session state
    if st.session_state.get('authentication_status'):
        # User is authenticated
        username = st.session_state.get('username')
        name = st.session_state.get('name')
        
        # Add logout button
        authenticator.logout('Cerrar Sesión', 'main')
    elif st.session_state.get('authentication_status') == False:
        st.error('Usuario/contraseña incorrectos')
        return
    elif st.session_state.get('authentication_status') is None:
        st.warning('Por favor ingresa tu usuario y contraseña')
        return
    
    # User is authenticated
    st.markdown(f'<h1 class="main-header">📊 Panel de Análisis de Datos - Dashboard Principal</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666;">Bienvenido, <strong>{name}</strong>! 👋</p>', unsafe_allow_html=True)
    
    # Get user progress
    user_progress = get_user_progress(username)
    
    # Learning levels navigation with improved design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.5rem;">🎓 Sistema de Aprendizaje por Niveles</h2>
        <p style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.1rem;">
            ¿Eres nuevo en análisis de datos? Completa nuestros niveles paso a paso para dominar todas las funcionalidades
        </p>
    """, unsafe_allow_html=True)
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
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
    
    # Navigation buttons inside the card
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📚 Nivel 1: Básico", type="primary", use_container_width=True, key="inicio_nivel1_header"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col2:
        if st.button("🔍 Nivel 2: Filtros", use_container_width=True, key="inicio_nivel2_header"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col3:
        if st.button("📊 Nivel 3: Métricas", use_container_width=True, key="inicio_nivel3_header"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col4:
        if st.button("🚀 Nivel 4: Avanzado", use_container_width=True, key="inicio_nivel4_header"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col5:
        if st.button("❓ Ayuda", use_container_width=True, key="inicio_ayuda_header"):
            st.switch_page("pages/00_Ayuda.py")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <div style="background: rgba(0, 0, 0, 0.6); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <p style="color: #ffffff; font-size: 0.9rem; margin: 0; font-weight: 500;">
                💡 <strong>Consejo:</strong> Si ya completaste los niveles, ¡este es tu dashboard principal para análisis avanzado!
            </p>
            </div>
            <div style="background: rgba(0, 0, 0, 0.6); padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem;">
                <p style="color: #ffffff; font-size: 0.8rem; margin: 0; font-weight: 500;">
                📖 <strong>Ayuda:</strong> Información detallada, guías paso a paso y solución de problemas
            </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Templates Section
    st.markdown("""
    <div style="background: rgba(40, 167, 69, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #28a745;">
        <h3 style="color: #28a745; margin-bottom: 1rem;">🎯 Crear tu Dashboard</h3>
        <p style="color: #666; margin-bottom: 1rem;"><strong>Elige cómo quieres empezar tu análisis:</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard creation options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Dashboard en Blanco")
        st.markdown("""
        - Crea tu dashboard desde cero
        - Elige tus propias visualizaciones
        - Máxima flexibilidad
        """)
        if st.button("🚀 Crear Dashboard en Blanco", use_container_width=True):
            st.session_state.dashboard_mode = "blank"
            st.session_state.show_dashboard = True
            st.rerun()
        
        with col2:
            st.markdown("### 📋 Plantillas Predefinidas")
            st.markdown("""
            - Dashboard con visualizaciones predefinidas
            - Ideal para principiantes
            - Estructura profesional
            """)
            if st.button("📋 Usar Plantilla", use_container_width=True):
                st.session_state.dashboard_mode = "template"
                st.session_state.show_dashboard = True
                st.rerun()
    
    with col3:
        st.markdown("### 🎨 Constructor Personalizado")
        st.markdown("""
        - Selecciona visualizaciones específicas
        - Personaliza tu dashboard
        - Control total del diseño
        """)
        if st.button("🎨 Constructor", use_container_width=True):
            st.session_state.dashboard_mode = "custom"
            st.session_state.show_dashboard = True
            st.rerun()
    
    # Sample Datasets Section
    st.markdown("### 📁 Datasets de Ejemplo")
    st.markdown("¿No tienes datos? Usa nuestros datasets de ejemplo para practicar:")
    
    sample_datasets = get_sample_datasets()
    
    # Display sample datasets in a grid
    cols = st.columns(2)
    for i, (name, info) in enumerate(sample_datasets.items()):
        with cols[i % 2]:
            with st.expander(f"📊 {name} - {info['difficulty']}"):
                st.markdown(f"**Descripción:** {info['description']}")
                st.markdown(f"**Problemas de calidad:** {info['data_quality_issues']}")
                
                if st.button(f"📥 Usar {name}", key=f"sample_{name}"):
                    st.session_state.sample_data = info['data']
                    st.session_state.data_quality_completed = True
                    st.success(f"¡Dataset {name} cargado exitosamente!")
                    st.rerun()
    
    # Data Upload Section
    st.markdown("### 📤 Subir tus Propios Datos")
    
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para comenzar tu análisis"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Archivo cargado exitosamente: {uploaded_file.name}")
            st.info(f"📊 {len(df)} filas, {len(df.columns)} columnas")
            
            # Show data preview
            with st.expander("👀 Vista previa de datos"):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Data quality analysis option
            if st.button("🧹 Analizar Calidad de Datos", type="primary"):
                st.session_state.uploaded_data = df
                st.session_state.show_data_quality = True
                st.rerun()
            
            # Skip to dashboard option
            if st.button("🚀 Ir Directo al Dashboard"):
                st.session_state.cleaned_data = df
                st.session_state.data_quality_completed = True
                st.session_state.show_dashboard = True
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
    
    # Show data quality analysis if requested
    if st.session_state.get('show_data_quality', False) and 'uploaded_data' in st.session_state:
        st.divider()
        data_quality_page(st.session_state.uploaded_data)
    
    # Show dashboard if data is ready
    if st.session_state.get('show_dashboard', False) and st.session_state.get('data_quality_completed', False):
        st.divider()
        show_dashboard(username)
    
    # User Profile Section
    st.divider()
    st.markdown("### 👤 Perfil de Usuario")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Usuario:** {username}")
        st.markdown(f"**Niveles completados:** {completed_count}/4")
        st.markdown(f"**Progreso total:** {total_progress:.1f}%")
    
    with col2:
        # Logout button
        if st.button("🚪 Cerrar Sesión"):
            authenticator.logout('Cerrar Sesión', 'main')
            st.rerun()
    
    # Help section
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(0, 0, 0, 0.6); padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;">
        <p style="color: #ffffff; margin-bottom: 0.5rem; font-weight: 500;"><strong>💡 ¿Necesitas ayuda?</strong></p>
        <p style="color: #ffffff; margin-bottom: 1rem;">Si no estás familiarizado con estas funcionalidades, te recomendamos completar nuestros niveles de aprendizaje primero.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add spacing before navigation buttons
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Inicio", use_container_width=True, key="inicio_inicio_footer"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("📚 Nivel 1", use_container_width=True, key="inicio_nivel1_footer"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col3:
        if st.button("🔍 Nivel 2", use_container_width=True, key="inicio_nivel2_footer"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col4:
        if st.button("📊 Nivel 3", use_container_width=True, key="inicio_nivel3_footer"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col5:
        if st.button("🚀 Nivel 4", use_container_width=True, key="inicio_nivel4_footer"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col6:
        if st.button("❓ Ayuda", use_container_width=True, key="inicio_ayuda_footer"):
            st.switch_page("pages/00_Ayuda.py")

def show_dashboard(username):
    """Show the main dashboard based on selected mode"""
    
    # Get data
    if 'cleaned_data' in st.session_state:
        df = st.session_state.cleaned_data
    elif 'sample_data' in st.session_state:
        df = st.session_state.sample_data
    else:
        st.error("No hay datos disponibles para el dashboard.")
        return
    
    dashboard_mode = st.session_state.get('dashboard_mode', 'blank')
    
    st.markdown("# 📊 Dashboard de Análisis")
    
    if dashboard_mode == "blank":
        show_blank_dashboard(df, username)
    elif dashboard_mode == "template":
        show_template_dashboard(df, username)
    elif dashboard_mode == "custom":
        show_custom_dashboard(df, username)

def show_blank_dashboard(df, username):
    """Show blank dashboard with basic controls"""
    
    st.markdown("### 🎨 Dashboard en Blanco")
    st.markdown("Crea tu análisis personalizado:")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Filas", f"{len(df):,}")
    with col2:
        st.metric("📋 Columnas", len(df.columns))
    with col3:
        st.metric("📊 Memoria", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    with col4:
        st.metric("🔢 Numéricas", len(df.select_dtypes(include=[np.number]).columns))
    
    # Data preview
    st.markdown("### 📋 Vista Previa de Datos")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_template_dashboard(df, username):
    """Show template dashboard with predefined visualizations"""
    
    st.markdown("### 📋 Dashboard con Plantilla")
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Display metrics
    display_metrics_dashboard(metrics, df)
    
    # Predefined visualizations
    st.markdown("### 📊 Visualizaciones Predefinidas")
    
    # Time series if date column exists
    if 'Date' in df.columns or 'Fecha' in df.columns:
        date_col = 'Date' if 'Date' in df.columns else 'Fecha'
        st.plotly_chart(create_time_series_chart(df, 'Revenue' if 'Revenue' in df.columns else df.select_dtypes(include=[np.number]).columns[0]), use_container_width=True)
    
    # Category and regional analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Category' in df.columns or 'Categoria' in df.columns:
            cat_col = 'Category' if 'Category' in df.columns else 'Categoria'
            st.plotly_chart(create_category_analysis(df), use_container_width=True)
    
    with col2:
        if 'Region' in df.columns or 'Region' in df.columns:
            reg_col = 'Region' if 'Region' in df.columns else 'Region'
            st.plotly_chart(create_regional_analysis(df), use_container_width=True)
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_custom_dashboard(df, username):
    """Show custom dashboard builder"""
    
    st.markdown("### 🎨 Constructor de Dashboard Personalizado")
    
    # Available visualizations
    available_viz = []
    
    if 'Date' in df.columns or 'Fecha' in df.columns:
        available_viz.append("📈 Series Temporales")
    
    if len(df.select_dtypes(include=[np.number]).columns) > 0:
        available_viz.append("📊 Gráficos de Barras")
        available_viz.append("🥧 Gráficos de Pastel")
    
    if len(df.select_dtypes(include=['object']).columns) > 0:
        available_viz.append("📋 Análisis por Categorías")
    
    # Let user select visualizations
    selected_viz = st.multiselect(
        "Selecciona las visualizaciones que quieres incluir:",
        available_viz,
        default=available_viz[:2] if len(available_viz) >= 2 else available_viz
    )
    
    if selected_viz:
        st.markdown("### 📊 Tu Dashboard Personalizado")
        
        # Display selected visualizations
        for viz in selected_viz:
            if viz == "📈 Series Temporales":
                st.plotly_chart(create_time_series_chart(df, 'Revenue' if 'Revenue' in df.columns else df.select_dtypes(include=[np.number]).columns[0]), use_container_width=True)
            elif viz == "📊 Gráficos de Barras":
                # Create bar chart
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    import plotly.express as px
                    fig = px.bar(df, x=df.index[:20], y=numeric_cols[0], title=f"Gráfico de Barras - {numeric_cols[0]}")
                    st.plotly_chart(fig, use_container_width=True)
            elif viz == "🥧 Gráficos de Pastel":
                # Create pie chart
                categorical_cols = df.select_dtypes(include=['object']).columns
                if len(categorical_cols) > 0:
                    import plotly.express as px
                    fig = px.pie(df, names=categorical_cols[0], title=f"Distribución - {categorical_cols[0]}")
                    st.plotly_chart(fig, use_container_width=True)
            elif viz == "📋 Análisis por Categorías":
                st.plotly_chart(create_category_analysis(df), use_container_width=True)
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

if __name__ == "__main__":
    main() 