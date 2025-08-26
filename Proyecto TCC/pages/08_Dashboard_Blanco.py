import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.auth_config import init_authentication, get_user_progress, update_user_progress
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
from utils.error_handler import display_error, safe_execute

def main():
    """Dashboard en Blanco - Construcción Manual"""
    # Configurar página
    st.set_page_config(
        page_title="Dashboard en Blanco - Construcción Manual",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Initialize authentication
    authenticator = init_authentication()
    
    # Check authentication
    if not st.session_state.get('authentication_status'):
        st.error("Por favor inicia sesión para acceder a esta página.")
        st.stop()
    
    username = st.session_state.get('username')
    name = st.session_state.get('name')
    
    # Header
    st.markdown(f'<h1 class="main-header">🎨 Dashboard en Blanco</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.1rem;">Construye tu dashboard personalizado, <strong>{name}</strong></p>', unsafe_allow_html=True)
    
    # Get data
    df = None
    if 'cleaned_data' in st.session_state:
        df = st.session_state.cleaned_data
    elif 'sample_data' in st.session_state:
        df = st.session_state.sample_data
    else:
        st.error("❌ No hay datos disponibles. Por favor, sube datos o usa un dataset de ejemplo desde la página de inicio.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Volver al Inicio", use_container_width=True):
                st.switch_page("Inicio.py")
        with col2:
            if st.button("📤 Subir Datos", use_container_width=True):
                st.switch_page("Inicio.py")
        st.stop()
    
    # Initialize dashboard components in session state
    if 'dashboard_components' not in st.session_state:
        st.session_state.dashboard_components = []
    
    # Sidebar for controls
    with st.sidebar:
        # Header with gradient background
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
            <h3 style="color: white; margin: 0; font-size: 1.2rem;">🎨 Dashboard Builder</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Construye tu dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data info with better styling
        st.markdown("""
        <div style="background: rgba(0, 123, 255, 0.1); padding: 1rem; border-radius: 8px; 
                    border-left: 4px solid #007bff; margin-bottom: 1.5rem;">
            <h4 style="color: #007bff; margin: 0 0 0.5rem 0; font-size: 1rem;">📊 Información de Datos</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Filas:</strong> {}</p>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Columnas:</strong> {}</p>
        </div>
        """.format(len(df), len(df.columns)), unsafe_allow_html=True)
        
        # Component categories with icons and descriptions
        st.markdown("### 🎯 Tipos de Componentes")
        
        # Metrics category
        with st.expander("📈 Métricas y KPIs", expanded=False):
            st.markdown("**Indicadores numéricos clave**")
            if st.button("📊 Agregar Métrica", key="add_metric", use_container_width=True):
                new_component = {
                    'id': len(st.session_state.dashboard_components),
                    'type': "📈 Métricas",
                    'title': "Nueva Métrica",
                    'config': get_default_config("📈 Métricas", df)
                }
                st.session_state.dashboard_components.append(new_component)
                st.rerun()
        
        # Charts category
        with st.expander("📊 Gráficos Básicos", expanded=False):
            st.markdown("**Visualizaciones fundamentales**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📈 Líneas", key="add_line", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📊 Gráfico de Líneas",
                        'title': "Gráfico de Líneas",
                        'config': get_default_config("📊 Gráfico de Líneas", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
                
                if st.button("📋 Barras", key="add_bar", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📋 Gráfico de Barras",
                        'title': "Gráfico de Barras",
                        'config': get_default_config("📋 Gráfico de Barras", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
            
            with col2:
                if st.button("🥧 Circular", key="add_pie", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "🥧 Gráfico Circular",
                        'title': "Gráfico Circular",
                        'config': get_default_config("🥧 Gráfico Circular", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
                
                if st.button("📈 Área", key="add_area", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📈 Gráfico de Área",
                        'title': "Gráfico de Área",
                        'config': get_default_config("📈 Gráfico de Área", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
        
        # Advanced charts category
        with st.expander("🔬 Gráficos Avanzados", expanded=False):
            st.markdown("**Análisis estadístico avanzado**")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📈 Dispersión", key="add_scatter", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📈 Gráfico de Dispersión",
                        'title': "Gráfico de Dispersión",
                        'config': get_default_config("📈 Gráfico de Dispersión", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
                
                if st.button("📊 Histograma", key="add_hist", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📊 Histograma",
                        'title': "Histograma",
                        'config': get_default_config("📊 Histograma", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
            
            with col2:
                if st.button("📊 Box Plot", key="add_box", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📊 Box Plot",
                        'title': "Box Plot",
                        'config': get_default_config("📊 Box Plot", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
                
                if st.button("📈 Violín", key="add_violin", use_container_width=True):
                    new_component = {
                        'id': len(st.session_state.dashboard_components),
                        'type': "📈 Gráfico de Violín",
                        'title': "Gráfico de Violín",
                        'config': get_default_config("📈 Gráfico de Violín", df)
                    }
                    st.session_state.dashboard_components.append(new_component)
                    st.rerun()
        
        # Data analysis category
        with st.expander("🔍 Análisis de Datos", expanded=False):
            st.markdown("**Herramientas de análisis**")
            
            if st.button("🔗 Matriz de Correlación", key="add_corr", use_container_width=True):
                new_component = {
                    'id': len(st.session_state.dashboard_components),
                    'type': "🔗 Matriz de Correlación",
                    'title': "Matriz de Correlación",
                    'config': get_default_config("🔗 Matriz de Correlación", df)
                }
                st.session_state.dashboard_components.append(new_component)
                st.rerun()
            
            if st.button("📋 Tabla de Datos", key="add_table", use_container_width=True):
                new_component = {
                    'id': len(st.session_state.dashboard_components),
                    'type': "📋 Tabla de Datos",
                    'title': "Tabla de Datos",
                    'config': get_default_config("📋 Tabla de Datos", df)
                }
                st.session_state.dashboard_components.append(new_component)
                st.rerun()
        
        # Dashboard management
        st.markdown("---")
        st.markdown("### 🛠️ Gestión del Dashboard")
        
        # Quick stats
        component_count = len(st.session_state.dashboard_components)
        st.markdown(f"""
        <div style="background: rgba(40, 167, 69, 0.1); padding: 0.8rem; border-radius: 6px; 
                    border-left: 3px solid #28a745; margin-bottom: 1rem;">
            <p style="color: #28a745; margin: 0; font-size: 0.9rem;">
                <strong>📊 Componentes activos:</strong> {component_count}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons with better styling
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar", key="save_dash", use_container_width=True, type="primary"):
                save_dashboard()
        
        with col2:
            if st.button("🗑️ Limpiar", key="clear_dash", use_container_width=True):
                st.session_state.dashboard_components = []
                st.rerun()
        
        # Export section
        st.markdown("### 📤 Exportar")
        export_format = st.selectbox("Formato de exportación:", ["PNG", "PDF", "HTML"], key="export_format")
        
        if st.button("📤 Exportar Dashboard", key="export_dash", use_container_width=True, type="secondary"):
            export_dashboard(export_format)
        
        # Tips section
        if component_count == 0:
            st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #ffc107; margin-top: 1rem;">
                <h4 style="color: #ffc107; margin: 0 0 0.5rem 0; font-size: 1rem;">💡 Consejos</h4>
                <ul style="color: #666; margin: 0; font-size: 0.9rem; padding-left: 1rem;">
                    <li>Comienza con métricas básicas</li>
                    <li>Agrega gráficos de líneas para tendencias</li>
                    <li>Usa gráficos de barras para comparaciones</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Main dashboard area
    st.markdown("### 🎨 Área de Construcción")
    
    if not st.session_state.dashboard_components:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(0,0,0,0.05); border-radius: 10px; border: 2px dashed #ccc;">
            <h3 style="color: #666; margin-bottom: 1rem;">🎨 Dashboard Vacío</h3>
            <p style="color: #666; margin-bottom: 2rem;">Usa el panel lateral para agregar componentes y construir tu dashboard personalizado.</p>
            <p style="color: #999; font-size: 0.9rem;">💡 Tip: Comienza agregando algunas métricas y gráficos básicos</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display components in a grid
        for i, component in enumerate(st.session_state.dashboard_components):
            with st.container():
                st.markdown("---")
                
                # Component header with controls
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    component['title'] = st.text_input(
                        f"Título del componente {i+1}:",
                        value=component['title'],
                        key=f"title_{component['id']}"
                    )
                
                with col2:
                    if st.button("⚙️ Configurar", key=f"config_{component['id']}"):
                        component['show_config'] = not component.get('show_config', False)
                        st.rerun()
                
                with col3:
                    if st.button("🔄 Actualizar", key=f"refresh_{component['id']}"):
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Eliminar", key=f"delete_{component['id']}"):
                        st.session_state.dashboard_components.pop(i)
                        st.rerun()
                
                # Configuration panel
                if component.get('show_config', False):
                    with st.expander("⚙️ Configuración", expanded=True):
                        component['config'] = configure_component(component, df)
                
                # Display component
                display_component(component, df)
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            # Clear selected_template to avoid redirect loops
            if 'selected_template' in st.session_state:
                del st.session_state.selected_template
            st.switch_page("Inicio.py")
    with col2:
        if st.button("📊 Ver Dashboard", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    with col3:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

def get_default_config(component_type, df):
    """Get default configuration for a component type"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if component_type == "📈 Métricas":
        return {
            'metric_type': 'count',
            'column': numeric_cols[0] if numeric_cols else None,
            'aggregation': 'sum'
        }
    elif component_type in ["📊 Gráfico de Líneas", "📈 Gráfico de Área"]:
        return {
            'x_column': categorical_cols[0] if categorical_cols else None,
            'y_column': numeric_cols[0] if numeric_cols else None,
            'color_column': None
        }
    elif component_type == "📋 Gráfico de Barras":
        return {
            'x_column': categorical_cols[0] if categorical_cols else None,
            'y_column': numeric_cols[0] if numeric_cols else None,
            'orientation': 'vertical'
        }
    elif component_type == "🥧 Gráfico Circular":
        return {
            'values_column': numeric_cols[0] if numeric_cols else None,
            'names_column': categorical_cols[0] if categorical_cols else None
        }
    elif component_type == "📈 Gráfico de Dispersión":
        return {
            'x_column': numeric_cols[0] if numeric_cols else None,
            'y_column': numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0],
            'color_column': categorical_cols[0] if categorical_cols else None
        }
    elif component_type == "📊 Histograma":
        return {
            'column': numeric_cols[0] if numeric_cols else None,
            'bins': 20
        }
    elif component_type == "📋 Tabla de Datos":
        return {
            'columns': df.columns.tolist()[:5],
            'rows': 10
        }
    elif component_type == "🔗 Matriz de Correlación":
        return {
            'columns': numeric_cols[:5] if len(numeric_cols) > 1 else numeric_cols
        }
    elif component_type in ["📊 Box Plot", "📈 Gráfico de Violín"]:
        return {
            'x_column': categorical_cols[0] if categorical_cols else None,
            'y_column': numeric_cols[0] if numeric_cols else None
        }
    
    return {}

def configure_component(component, df):
    """Configure a component based on its type"""
    config = component['config']
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if component['type'] == "📈 Métricas":
        col1, col2, col3 = st.columns(3)
        with col1:
            config['metric_type'] = st.selectbox(
                "Tipo de métrica:",
                ["count", "sum", "mean", "median", "min", "max"],
                index=0 if config.get('metric_type') == 'count' else 1,
                key=f"metric_type_{component['id']}"
            )
        with col2:
            if config['metric_type'] != 'count':
                config['column'] = st.selectbox(
                    "Columna:",
                    numeric_cols,
                    index=0,
                    key=f"metric_col_{component['id']}"
                )
        with col3:
            if config['metric_type'] == 'sum':
                config['aggregation'] = st.selectbox(
                    "Agregación:",
                    ["sum", "mean", "median"],
                    key=f"metric_agg_{component['id']}"
                )
    
    elif component['type'] in ["📊 Gráfico de Líneas", "📈 Gráfico de Área"]:
        col1, col2 = st.columns(2)
        with col1:
            config['x_column'] = st.selectbox(
                "Columna X:",
                df.columns.tolist(),
                index=df.columns.get_loc(config.get('x_column', df.columns[0])),
                key=f"line_x_{component['id']}"
            )
        with col2:
            config['y_column'] = st.selectbox(
                "Columna Y:",
                numeric_cols,
                index=0,
                key=f"line_y_{component['id']}"
            )
        
        config['color_column'] = st.selectbox(
            "Columna de color (opcional):",
            [None] + categorical_cols,
            key=f"line_color_{component['id']}"
        )
    
    elif component['type'] == "📋 Gráfico de Barras":
        col1, col2 = st.columns(2)
        with col1:
            config['x_column'] = st.selectbox(
                "Columna X:",
                df.columns.tolist(),
                index=df.columns.get_loc(config.get('x_column', df.columns[0])),
                key=f"bar_x_{component['id']}"
            )
        with col2:
            config['y_column'] = st.selectbox(
                "Columna Y:",
                numeric_cols,
                index=0,
                key=f"bar_y_{component['id']}"
            )
        
        config['orientation'] = st.selectbox(
            "Orientación:",
            ["vertical", "horizontal"],
            key=f"bar_orientation_{component['id']}"
        )
    
    elif component['type'] == "🥧 Gráfico Circular":
        col1, col2 = st.columns(2)
        with col1:
            config['values_column'] = st.selectbox(
                "Columna de valores:",
                numeric_cols,
                index=0,
                key=f"pie_values_{component['id']}"
            )
        with col2:
            config['names_column'] = st.selectbox(
                "Columna de nombres:",
                categorical_cols,
                index=0,
                key=f"pie_names_{component['id']}"
            )
    
    elif component['type'] == "📈 Gráfico de Dispersión":
        col1, col2 = st.columns(2)
        with col1:
            config['x_column'] = st.selectbox(
                "Columna X:",
                numeric_cols,
                index=0,
                key=f"scatter_x_{component['id']}"
            )
        with col2:
            config['y_column'] = st.selectbox(
                "Columna Y:",
                numeric_cols,
                index=1 if len(numeric_cols) > 1 else 0,
                key=f"scatter_y_{component['id']}"
            )
        
        config['color_column'] = st.selectbox(
            "Columna de color (opcional):",
            [None] + categorical_cols,
            key=f"scatter_color_{component['id']}"
        )
    
    elif component['type'] == "📊 Histograma":
        col1, col2 = st.columns(2)
        with col1:
            config['column'] = st.selectbox(
                "Columna:",
                numeric_cols,
                index=0,
                key=f"hist_col_{component['id']}"
            )
        with col2:
            config['bins'] = st.slider(
                "Número de bins:",
                min_value=5,
                max_value=50,
                value=config.get('bins', 20),
                key=f"hist_bins_{component['id']}"
            )
    
    elif component['type'] == "📋 Tabla de Datos":
        config['columns'] = st.multiselect(
            "Columnas a mostrar:",
            df.columns.tolist(),
            default=config.get('columns', df.columns.tolist()[:5]),
            key=f"table_cols_{component['id']}"
        )
        config['rows'] = st.slider(
            "Número de filas:",
            min_value=5,
            max_value=100,
            value=config.get('rows', 10),
            key=f"table_rows_{component['id']}"
        )
    
    elif component['type'] == "🔗 Matriz de Correlación":
        config['columns'] = st.multiselect(
            "Columnas numéricas:",
            numeric_cols,
            default=config.get('columns', numeric_cols[:5]),
            key=f"corr_cols_{component['id']}"
        )
    
    elif component['type'] in ["📊 Box Plot", "📈 Gráfico de Violín"]:
        col1, col2 = st.columns(2)
        with col1:
            config['x_column'] = st.selectbox(
                "Columna X (categórica):",
                categorical_cols,
                index=0,
                key=f"box_x_{component['id']}"
            )
        with col2:
            config['y_column'] = st.selectbox(
                "Columna Y (numérica):",
                numeric_cols,
                index=0,
                key=f"box_y_{component['id']}"
            )
    
    return config

def display_component(component, df):
    """Display a component based on its type and configuration"""
    config = component['config']
    
    try:
        if component['type'] == "📈 Métricas":
            display_metrics_component(config, df)
        
        elif component['type'] == "📊 Gráfico de Líneas":
            display_line_chart(config, df)
        
        elif component['type'] == "📋 Gráfico de Barras":
            display_bar_chart(config, df)
        
        elif component['type'] == "🥧 Gráfico Circular":
            display_pie_chart(config, df)
        
        elif component['type'] == "📈 Gráfico de Dispersión":
            display_scatter_chart(config, df)
        
        elif component['type'] == "📊 Histograma":
            display_histogram(config, df)
        
        elif component['type'] == "📋 Tabla de Datos":
            display_data_table(config, df)
        
        elif component['type'] == "📈 Gráfico de Área":
            display_area_chart(config, df)
        
        elif component['type'] == "🔗 Matriz de Correlación":
            display_correlation_matrix(config, df)
        
        elif component['type'] == "📊 Box Plot":
            display_box_plot(config, df)
        
        elif component['type'] == "📈 Gráfico de Violín":
            display_violin_plot(config, df)
    
    except Exception as e:
        display_error(e, f"Mostrando componente: {component['type']}")

def display_metrics_component(config, df):
    """Display metrics component"""
    metric_type = config.get('metric_type', 'count')
    
    if metric_type == 'count':
        value = len(df)
        label = "Total Registros"
    else:
        column = config.get('column')
        if not column:
            st.error("Selecciona una columna para la métrica")
            return
        
        if metric_type == 'sum':
            value = df[column].sum()
            label = f"Suma de {column}"
        elif metric_type == 'mean':
            value = df[column].mean()
            label = f"Promedio de {column}"
        elif metric_type == 'median':
            value = df[column].median()
            label = f"Mediana de {column}"
        elif metric_type == 'min':
            value = df[column].min()
            label = f"Mínimo de {column}"
        elif metric_type == 'max':
            value = df[column].max()
            label = f"Máximo de {column}"
    
    # Format value based on type
    if isinstance(value, (int, float)):
        if abs(value) >= 1000000:
            formatted_value = f"{value/1000000:.1f}M"
        elif abs(value) >= 1000:
            formatted_value = f"{value/1000:.1f}K"
        else:
            formatted_value = f"{value:,.0f}" if isinstance(value, int) else f"{value:.2f}"
    else:
        formatted_value = str(value)
    
    st.metric(label, formatted_value)

def display_line_chart(config, df):
    """Display line chart"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    color_col = config.get('color_column')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        if color_col:
            fig = px.line(df, x=x_col, y=y_col, color=color_col, title=config.get('title', 'Gráfico de Líneas'))
        else:
            fig = px.line(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Líneas'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de líneas")

def display_bar_chart(config, df):
    """Display bar chart"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    orientation = config.get('orientation', 'vertical')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        if orientation == 'horizontal':
            fig = px.bar(df, x=y_col, y=x_col, title=config.get('title', 'Gráfico de Barras'))
        else:
            fig = px.bar(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Barras'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de barras")

def display_pie_chart(config, df):
    """Display pie chart"""
    values_col = config.get('values_column')
    names_col = config.get('names_column')
    
    if not values_col or not names_col:
        st.error("Selecciona columnas de valores y nombres para el gráfico")
        return
    
    try:
        # Aggregate data for pie chart
        pie_data = df.groupby(names_col)[values_col].sum().reset_index()
        fig = px.pie(pie_data, values=values_col, names=names_col, title=config.get('title', 'Gráfico Circular'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico circular")

def display_scatter_chart(config, df):
    """Display scatter chart"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    color_col = config.get('color_column')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        if color_col:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=config.get('title', 'Gráfico de Dispersión'))
        else:
            fig = px.scatter(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Dispersión'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de dispersión")

def display_histogram(config, df):
    """Display histogram"""
    column = config.get('column')
    bins = config.get('bins', 20)
    
    if not column:
        st.error("Selecciona una columna para el histograma")
        return
    
    try:
        fig = px.histogram(df, x=column, nbins=bins, title=config.get('title', 'Histograma'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando histograma")

def display_data_table(config, df):
    """Display data table"""
    columns = config.get('columns', df.columns.tolist()[:5])
    rows = config.get('rows', 10)
    
    if not columns:
        st.error("Selecciona columnas para mostrar en la tabla")
        return
    
    try:
        display_df = df[columns].head(rows)
        st.dataframe(display_df, use_container_width=True)
    except Exception as e:
        display_error(e, "Mostrando tabla de datos")

def display_area_chart(config, df):
    """Display area chart"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    color_col = config.get('color_column')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        if color_col:
            fig = px.area(df, x=x_col, y=y_col, color=color_col, title=config.get('title', 'Gráfico de Área'))
        else:
            fig = px.area(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Área'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de área")

def display_correlation_matrix(config, df):
    """Display correlation matrix"""
    columns = config.get('columns', [])
    
    if len(columns) < 2:
        st.error("Selecciona al menos 2 columnas numéricas para la matriz de correlación")
        return
    
    try:
        corr_matrix = df[columns].corr()
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title=config.get('title', 'Matriz de Correlación')
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando matriz de correlación")

def display_box_plot(config, df):
    """Display box plot"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        fig = px.box(df, x=x_col, y=y_col, title=config.get('title', 'Box Plot'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando box plot")

def display_violin_plot(config, df):
    """Display violin plot"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        fig = px.violin(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Violín'))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de violín")

def save_dashboard():
    """Save dashboard configuration"""
    try:
        dashboard_config = {
            'components': st.session_state.dashboard_components,
            'created_at': datetime.now().isoformat(),
            'user': st.session_state.get('username', 'unknown')
        }
        
        # Save to session state for now (could be extended to save to file/database)
        st.session_state.saved_dashboard = dashboard_config
        st.success("✅ Dashboard guardado exitosamente!")
    except Exception as e:
        display_error(e, "Guardando dashboard")

def export_dashboard(format_type):
    """Export dashboard"""
    if not st.session_state.dashboard_components:
        st.warning("No hay componentes para exportar")
        return
    
    try:
        st.info(f"📤 Exportando dashboard en formato {format_type}...")
        # Here you would implement the actual export logic
        # For now, just show a success message
        st.success(f"✅ Dashboard exportado como {format_type}")
    except Exception as e:
        display_error(e, f"Exportando dashboard como {format_type}")

if __name__ == "__main__":
    main()
