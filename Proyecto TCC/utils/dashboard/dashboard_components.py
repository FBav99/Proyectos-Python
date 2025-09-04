import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
            'x_column': df.columns[0] if len(df.columns) > 0 else None,
            'y_column': numeric_cols[0] if numeric_cols else None,
            'color_column': None
        }
    
    elif component_type == "📋 Gráfico de Barras":
        return {
            'x_column': df.columns[0] if len(df.columns) > 0 else None,
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
            'y_column': numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0] if numeric_cols else None,
            'color_column': categorical_cols[0] if categorical_cols else None
        }
    
    elif component_type == "📊 Histograma":
        return {
            'column': numeric_cols[0] if numeric_cols else None,
            'bins': 20
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
                max_value=100,
                value=config.get('bins', 20),
                key=f"hist_bins_{component['id']}"
            )
    
    elif component['type'] in ["📊 Box Plot", "📈 Gráfico de Violín"]:
        col1, col2 = st.columns(2)
        with col1:
            config['x_column'] = st.selectbox(
                "Columna X:",
                categorical_cols,
                index=0,
                key=f"box_x_{component['id']}"
            )
        with col2:
            config['y_column'] = st.selectbox(
                "Columna Y:",
                numeric_cols,
                index=0,
                key=f"box_y_{component['id']}"
            )
    
    elif component['type'] == "📊 Matriz de Correlación":
        config['columns'] = st.multiselect(
            "Seleccionar columnas numéricas:",
            numeric_cols,
            default=numeric_cols[:min(5, len(numeric_cols))],
            key=f"corr_cols_{component['id']}"
        )
    
    elif component['type'] == "📋 Tabla de Datos":
        config['columns'] = st.multiselect(
            "Seleccionar columnas:",
            df.columns.tolist(),
            default=df.columns.tolist()[:min(10, len(df.columns))],
            key=f"table_cols_{component['id']}"
        )
        config['rows'] = st.slider(
            "Número de filas:",
            min_value=5,
            max_value=100,
            value=min(20, len(df)),
            key=f"table_rows_{component['id']}"
        )
    
    # Title configuration for all components
    config['title'] = st.text_input(
        "Título del componente:",
        value=config.get('title', component['title']),
        key=f"title_{component['id']}"
    )

def create_component_buttons():
    """Create buttons for adding different component types"""
    st.markdown("### 🎯 Tipos de Componentes")
    
    # Metrics category
    with st.expander("📈 Métricas y KPIs", expanded=False):
        st.markdown("**Indicadores numéricos clave**")
        if st.button("📊 Agregar Métrica", key="add_metric", use_container_width=True):
            return "📈 Métricas"
    
    # Charts category
    with st.expander("📊 Gráficos Básicos", expanded=False):
        st.markdown("**Visualizaciones fundamentales**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Líneas", key="add_line", use_container_width=True):
                return "📊 Gráfico de Líneas"
            
            if st.button("📋 Barras", key="add_bar", use_container_width=True):
                return "📋 Gráfico de Barras"
        
        with col2:
            if st.button("🥧 Circular", key="add_pie", use_container_width=True):
                return "🥧 Gráfico Circular"
            
            if st.button("📈 Área", key="add_area", use_container_width=True):
                return "📈 Gráfico de Área"
    
    # Advanced charts category
    with st.expander("🔬 Gráficos Avanzados", expanded=False):
        st.markdown("**Análisis estadístico avanzado**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Dispersión", key="add_scatter", use_container_width=True):
                return "📈 Gráfico de Dispersión"
            
            if st.button("📊 Histograma", key="add_hist", use_container_width=True):
                return "📊 Histograma"
        
        with col2:
            if st.button("📊 Box Plot", key="add_box", use_container_width=True):
                return "📊 Box Plot"
            
            if st.button("📈 Violín", key="add_violin", use_container_width=True):
                return "📈 Gráfico de Violín"
    
    # Analysis category
    with st.expander("🔍 Análisis", expanded=False):
        st.markdown("**Herramientas de análisis**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Correlación", key="add_correlation", use_container_width=True):
                return "📊 Matriz de Correlación"
        
        with col2:
            if st.button("📋 Tabla", key="add_table", use_container_width=True):
                return "📋 Tabla de Datos"
    
    return None

def add_component_to_dashboard(component_type, df):
    """Add a new component to the dashboard"""
    if component_type:
        new_component = {
            'id': len(st.session_state.dashboard_components),
            'type': component_type,
            'title': f"Nuevo {component_type}",
            'config': get_default_config(component_type, df)
        }
        st.session_state.dashboard_components.append(new_component)
        return True
    return False
