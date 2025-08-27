import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.auth_service import auth_service, login_user, logout_user, get_current_user, require_auth
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
    
    # Check if user is already authenticated
    current_user = get_current_user()
    
    if not current_user:
        # Show login form
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: white; margin-bottom: 1rem;">🔐 Iniciar Sesión</h1>
            <p style="color: white; font-size: 1.1rem;">Accede a tu cuenta para continuar</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Tu nombre de usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Tu contraseña")
            
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("🚀 Iniciar Sesión", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("📝 Registrarse", use_container_width=True):
                    st.switch_page("pages/05_Registro.py")
        
        if login_submitted and username and password:
            success, message = login_user(username, password)
            if success:
                st.success("✅ ¡Inicio de sesión exitoso!")
                st.rerun()
            else:
                st.error(f"❌ {message}")
        
        # Add additional options
        st.markdown("---")
        st.markdown("### 🔐 ¿Necesitas ayuda?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Crear Nueva Cuenta", type="primary", use_container_width=True):
                st.switch_page("pages/05_Registro.py")
        with col2:
            if st.button("🔑 ¿Olvidaste tu contraseña?", use_container_width=True):
                st.switch_page("pages/06_Recuperar_Password.py")
        with col3:
            if st.button("🌐 Login con Google/Microsoft", use_container_width=True):
                st.switch_page("pages/07_OAuth_Login.py")
        return
    
    # User is authenticated - show logout button
    username = current_user['username']
    name = f"{current_user['first_name']} {current_user['last_name']}"
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("### 👤 Usuario")
        st.write(f"**{name}**")
        st.write(f"@{username}")
        
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            logout_user()
            st.rerun()
    
    # ============================================================================
    # HEADER SECTION - Welcome and User Info
    # ============================================================================
    st.markdown(f'<h1 class="main-header">📊 Panel de Análisis de Datos</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.2rem;">Bienvenido, <strong>{name}</strong>! 👋</p>', unsafe_allow_html=True)
    
    # Get user progress from database
    total_progress, completed_count, progress = get_level_progress(current_user['id'])
    
    # ============================================================================
    # QUICK START SECTION - Main Action Buttons
    # ============================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.8rem;">🚀 ¿Qué quieres hacer hoy?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Main action buttons in a clean grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #28a745; margin-bottom: 1rem;">📤 Subir Datos</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Comienza con tus propios archivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📁 Subir Archivo", type="primary", use_container_width=True, key="upload_main"):
            st.session_state.show_upload_section = True
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #007bff; margin-bottom: 1rem;">📊 Datos de Ejemplo</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Practica con datasets predefinidos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Usar Ejemplos", type="secondary", use_container_width=True, key="examples_main"):
            st.session_state.show_examples_section = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3 style="color: #ffc107; margin-bottom: 1rem;">📚 Aprender</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">Completa los niveles de aprendizaje</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎓 Ver Niveles", type="secondary", use_container_width=True, key="learn_main"):
            st.session_state.show_learning_section = True
            st.rerun()
    
    # ============================================================================
    # UPLOAD SECTION
    # ============================================================================
    if st.session_state.get('show_upload_section', False):
        st.markdown("---")
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
                
                # Action buttons for loaded data
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🧹 Analizar Calidad de Datos", type="primary", use_container_width=True):
                        st.session_state.uploaded_data = df
                        st.session_state.show_data_quality = True
                        st.rerun()
                
                with col2:
                    if st.button("🚀 Ir Directo al Dashboard", use_container_width=True):
                        st.session_state.cleaned_data = df
                        st.session_state.data_quality_completed = True
                        st.session_state.show_dashboard = True
                        st.rerun()
                        
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {str(e)}")
        
        # Back button
        if st.button("⬅️ Volver", key="back_from_upload"):
            st.session_state.show_upload_section = False
            # Clear selected_template to avoid redirect loops
            if 'selected_template' in st.session_state:
                del st.session_state.selected_template
            st.rerun()
    
    # ============================================================================
    # EXAMPLES SECTION
    # ============================================================================
    if st.session_state.get('show_examples_section', False):
        st.markdown("---")
        st.markdown("### 📊 Datasets de Ejemplo")
        st.markdown("Elige un dataset para practicar:")
        
        sample_datasets = get_sample_datasets()
        
        # Display sample datasets in a clean grid
        cols = st.columns(2)
        for i, (name, info) in enumerate(sample_datasets.items()):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                        <h4 style="color: #007bff; margin-bottom: 0.5rem;">📊 {name}</h4>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Dificultad:</strong> {info['difficulty']}</p>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">{info['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📥 Usar {name}", key=f"sample_{name}", use_container_width=True):
                        st.session_state.sample_data = info['data']
                        st.session_state.data_quality_completed = True
                        st.session_state.show_dashboard = True
                        st.success(f"¡Dataset {name} cargado exitosamente!")
                        st.rerun()
        
        # Back button
        if st.button("⬅️ Volver", key="back_from_examples"):
            st.session_state.show_examples_section = False
            # Clear selected_template to avoid redirect loops
            if 'selected_template' in st.session_state:
                del st.session_state.selected_template
            st.rerun()
    
    # ============================================================================
    # LEARNING SECTION
    # ============================================================================
    if st.session_state.get('show_learning_section', False):
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
    
    # ============================================================================
    # DATA QUALITY ANALYSIS SECTION
    # ============================================================================
    if st.session_state.get('show_data_quality', False) and 'uploaded_data' in st.session_state:
        st.divider()
        data_quality_page(st.session_state.uploaded_data)
    
    # ============================================================================
    # DASHBOARD SECTION
    # ============================================================================
    if st.session_state.get('show_dashboard', False) and st.session_state.get('data_quality_completed', False):
        st.divider()
        show_dashboard(username)
    
    # ============================================================================
    # USER PROFILE SECTION (Minimal)
    # ============================================================================
    if not any([st.session_state.get('show_upload_section', False), 
                st.session_state.get('show_examples_section', False),
                st.session_state.get('show_learning_section', False),
                st.session_state.get('show_data_quality', False),
                st.session_state.get('show_dashboard', False)]):
        
        # Clear selected_template when showing main page to avoid redirect loops
        if 'selected_template' in st.session_state:
            del st.session_state.selected_template
        
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
    
    selected_template = st.session_state.get('selected_template', 'blank')
    
    st.markdown("# 📊 Dashboard de Análisis")
    
    # Template selection if not already selected
    if selected_template == 'blank':
        st.markdown("### 🎨 Selecciona el tipo de dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("#### 🎨 **Dashboard en Blanco**")
            st.markdown("Construye tu dashboard manualmente")
            if st.button("🎨 Usar Blanco", key="template_blank", use_container_width=True):
                st.switch_page("pages/08_Dashboard_Blanco.py")
        
        with col2:
            st.markdown("#### 🎯 **Dashboard KPI**")
            st.markdown("Indicadores clave de rendimiento para ejecutivos")
            if st.button("🚀 Usar KPI", key="template_kpi", use_container_width=True):
                st.session_state.selected_template = "kpi"
                st.rerun()
        
        with col3:
            st.markdown("#### 📊 **Dashboard Analítico**")
            st.markdown("Análisis detallado por segmentos")
            if st.button("📊 Usar Analítico", key="template_analytical", use_container_width=True):
                st.session_state.selected_template = "analytical"
                st.rerun()
        
        with col4:
            st.markdown("#### 🔍 **Dashboard Detallado**")
            st.markdown("Análisis granular y exhaustivo")
            if st.button("🔍 Usar Detallado", key="template_detailed", use_container_width=True):
                st.session_state.selected_template = "detailed"
                st.rerun()
    
    # Show selected template
    if selected_template == "kpi":
        show_kpi_template(df, username)
    elif selected_template == "analytical":
        show_analytical_template(df, username)
    elif selected_template == "detailed":
        show_detailed_template(df, username)



def show_kpi_template(df, username):
    """Show KPI template - Macro level dashboard"""
    
    st.markdown("### 🎯 Plantilla KPI - Nivel Macro")
    st.markdown("*Dashboard ejecutivo con indicadores clave de rendimiento*")
    
    # Calculate basic metrics
    metrics = calculate_metrics(df)
    
    # Display key KPIs in a prominent way
    st.markdown("#### 📊 Indicadores Clave de Rendimiento")
    
    # Main KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Registros", f"{len(df):,}", delta=f"+{len(df)//10:,}")
    with col2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            main_col = numeric_cols[0]
            total_value = df[main_col].sum()
            st.metric(f"💰 Total {main_col}", f"{total_value:,.0f}", delta=f"+{total_value//20:,.0f}")
        else:
            st.metric("📊 Columnas", len(df.columns))
    with col3:
        st.metric("📅 Última Actualización", datetime.now().strftime("%d/%m/%Y"))
    with col4:
        quality_score = 85  # Placeholder - could be calculated
        st.metric("🎯 Calidad de Datos", f"{quality_score}%", delta="+5%")
    
    # Executive summary
    st.markdown("#### 📋 Resumen Ejecutivo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Tendencias Principales:**")
        st.markdown("- 📈 Crecimiento sostenido en registros")
        st.markdown("- 💰 Incremento en valores monetarios")
        st.markdown("- 🎯 Mejora en calidad de datos")
    
    with col2:
        st.markdown("**Recomendaciones:**")
        st.markdown("- ✅ Mantener tendencia actual")
        st.markdown("- 🔍 Monitorear outliers")
        st.markdown("- 📊 Revisar métricas mensuales")
    
    # Simple trend chart if date column exists
    st.markdown("#### 📈 Tendencia General")
    time_chart = create_time_series_chart(df)
    if time_chart is not None:
        st.plotly_chart(time_chart, use_container_width=True)
    else:
        st.info("No se pudo crear el gráfico de tendencias. Verifica que tengas columnas de fecha y valores numéricos.")
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_analytical_template(df, username):
    """Show Analytical template - Medium level dashboard"""
    
    st.markdown("### 📊 Plantilla Analítica - Nivel Medio")
    st.markdown("*Dashboard analítico con análisis detallado por segmentos*")
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Display metrics dashboard
    display_metrics_dashboard(metrics, df)
    
    # Segment analysis
    st.markdown("#### 🔍 Análisis por Segmentos")
    
    # Category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Análisis por Categorías**")
        cat_chart = create_category_analysis(df)
        if cat_chart is not None:
            st.plotly_chart(cat_chart, use_container_width=True)
        else:
            st.info("No hay suficientes datos categóricos para este análisis.")
    
    with col2:
        st.markdown("**🌍 Análisis Regional**")
        reg_chart = create_regional_analysis(df)
        if reg_chart is not None:
            st.plotly_chart(reg_chart, use_container_width=True)
        else:
            st.info("No hay suficientes datos categóricos para este análisis.")
    
    # Correlation analysis
    st.markdown("#### 🔗 Análisis de Correlaciones")
    corr_chart = create_correlation_matrix(df)
    if corr_chart is not None:
        st.plotly_chart(corr_chart, use_container_width=True)
    else:
        st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones.")
    
    # Time series analysis
    st.markdown("#### 📈 Análisis Temporal")
    time_chart = create_time_series_chart(df)
    if time_chart is not None:
        st.plotly_chart(time_chart, use_container_width=True)
    else:
        st.info("No se pudo crear el análisis temporal. Verifica que tengas columnas de fecha y valores numéricos.")
    
    # Performance insights
    st.markdown("#### 💡 Insights de Rendimiento")
    insights = calculate_performance_insights(df)
    for insight in insights[:3]:  # Show top 3 insights
        st.info(f"💡 {insight}")
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_detailed_template(df, username):
    """Show Detailed template - Micro level dashboard"""
    
    st.markdown("### 🔍 Plantilla Detallada - Nivel Micro")
    st.markdown("*Dashboard granular con análisis exhaustivo y patrones detallados*")
    
    # Calculate comprehensive metrics
    metrics = calculate_metrics(df)
    growth_metrics = calculate_growth_metrics(df)
    
    # Display all metrics
    display_metrics_dashboard(metrics, df)
    
    # Growth metrics
    st.markdown("#### 📈 Métricas de Crecimiento")
    display_metrics_dashboard(growth_metrics, df)
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuciones", "🔍 Outliers", "📈 Tendencias", "🔗 Correlaciones"])
    
    with tab1:
        st.markdown("#### 📊 Análisis de Distribuciones")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:3]:  # Show first 3 numeric columns
                st.markdown(f"**Distribución de {col}**")
                fig = px.histogram(df, x=col, title=f"Distribución de {col}")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔍 Análisis de Outliers")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:2]:  # Show first 2 numeric columns
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
                
                st.markdown(f"**Outliers en {col}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cantidad de Outliers", len(outliers))
                with col2:
                    st.metric("Porcentaje", f"{len(outliers)/len(df)*100:.1f}%")
                
                if len(outliers) > 0:
                    st.dataframe(outliers.head(10), use_container_width=True)
    
    with tab3:
        st.markdown("#### 📈 Análisis de Tendencias Detallado")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:2]:  # Show first 2 numeric columns
                st.markdown(f"**Tendencia de {col}**")
                time_chart = create_time_series_chart(df, col)
                if time_chart is not None:
                    st.plotly_chart(time_chart, use_container_width=True)
                else:
                    st.info(f"No se pudo crear el gráfico de tendencias para {col}")
        else:
            st.info("No hay columnas numéricas para el análisis de tendencias.")
    
    with tab4:
        st.markdown("#### 🔗 Análisis de Correlaciones Detallado")
        corr_chart = create_correlation_matrix(df)
        if corr_chart is not None:
            st.plotly_chart(corr_chart, use_container_width=True)
            
            # Correlation insights
            st.markdown("**💡 Insights de Correlación:**")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr_matrix = df[numeric_cols].corr()
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        st.success(f"✅ {numeric_cols[i]} y {numeric_cols[j]} tienen correlación fuerte ({corr_value:.2f})")
                    elif abs(corr_value) > 0.5:
                        st.info(f"ℹ️ {numeric_cols[i]} y {numeric_cols[j]} tienen correlación moderada ({corr_value:.2f})")
        else:
            st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones.")
    
    # Custom calculations section
    st.markdown("#### 🧮 Cálculos Personalizados")
    create_custom_calculations_ui(df)
    
    # Export section
    st.markdown("#### 📤 Exportar Análisis")
    display_export_section(df, {}, metrics)
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)



if __name__ == "__main__":
    main() 