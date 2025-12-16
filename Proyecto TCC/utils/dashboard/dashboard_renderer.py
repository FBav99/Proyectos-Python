# Nombre del Archivo: dashboard_renderer.py
# Descripción: Renderizador de dashboard - Funciones para mostrar componentes de dashboard (métricas, gráficos, etc.)
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui import display_error

from utils.ui.icon_system import get_icon, replace_emojis
# UI - Mostrar Metrica
def display_metric(config, df):
    """Mostrar un componente de métrica"""
    metric_type = config.get('metric_type', 'count')
    column = config.get('column')
    
    try:
        if metric_type == 'count':
            value = len(df)
            label = "Total de Registros"
        elif metric_type in ['sum', 'mean', 'median', 'min', 'max']:
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
        else:
            st.error(f"Tipo de métrica no válido: {metric_type}")
            return
        
        # Formato - Formatear el Valor Según el Tipo
        if isinstance(value, (int, np.integer)):
            formatted_value = f"{value:,}"
        elif isinstance(value, (float, np.floating)):
            formatted_value = f"{value:,.2f}"
        else:
            formatted_value = str(value)
        
        st.metric(label, formatted_value)
        
    except Exception as e:
        display_error(e, "Calculando métrica")

# UI - Mostrar Grafico de Lineas
def display_line_chart(config, df):
    """Mostrar un gráfico de líneas"""
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

# UI - Mostrar Grafico de Barras
def display_bar_chart(config, df):
    """Mostrar un gráfico de barras"""
    x_col = config.get('x_column')
    y_col = config.get('y_column')
    orientation = config.get('orientation', 'vertical')
    
    if not x_col or not y_col:
        st.error("Selecciona columnas X e Y para el gráfico")
        return
    
    try:
        if orientation == 'horizontal':
            fig = px.bar(df, y=x_col, x=y_col, title=config.get('title', 'Gráfico de Barras'))
        else:
            fig = px.bar(df, x=x_col, y=y_col, title=config.get('title', 'Gráfico de Barras'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico de barras")

# UI - Mostrar Grafico Circular
def display_pie_chart(config, df):
    """Mostrar un gráfico circular"""
    values_col = config.get('values_column')
    names_col = config.get('names_column')
    
    if not values_col or not names_col:
        st.error("Selecciona columnas de valores y nombres para el gráfico")
        return
    
    try:
        # Procesamiento - Agregar Datos para Gráfico Circular
        pie_data = df.groupby(names_col)[values_col].sum().reset_index()
        fig = px.pie(pie_data, values=values_col, names=names_col, title=config.get('title', 'Gráfico Circular'))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        display_error(e, "Creando gráfico circular")

# UI - Mostrar Grafico de Area
def display_area_chart(config, df):
    """Mostrar un gráfico de área"""
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

# UI - Mostrar Grafico de Dispersión
def display_scatter_plot(config, df):
    """Mostrar un gráfico de dispersión"""
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

# UI - Mostrar Histograma
def display_histogram(config, df):
    """Mostrar un histograma"""
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

# UI - Mostrar Box Plot
def display_box_plot(config, df):
    """Mostrar un gráfico de caja (box plot)"""
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

# UI - Mostrar Grafico de Violin
def display_violin_plot(config, df):
    """Mostrar un gráfico de violín"""
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

# UI - Mostrar Matriz de Correlacion
def display_correlation_matrix(config, df):
    """Mostrar matriz de correlación"""
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

# UI - Mostrar Tabla de Datos
def display_data_table(config, df):
    """Mostrar una tabla de datos"""
    columns = config.get('columns', df.columns.tolist())
    rows = config.get('rows', min(20, len(df)))
    
    if not columns:
        st.error("Selecciona columnas para la tabla")
        return
    
    try:
        # Procesamiento - Filtrar Columnas y Filas
        table_df = df[columns].head(rows)
        st.dataframe(table_df, use_container_width=True)
        
        # UI - Mostrar Resumen
        st.caption(f"Mostrando {len(table_df)} de {len(df)} filas")
    except Exception as e:
        display_error(e, "Mostrando tabla de datos")

# Renderizado - Renderizar Componente
def render_component(component, df):
    """Renderizar un componente de dashboard según su tipo"""
    component_type = component['type']
    config = component['config']
    
    # UI - Agregar Encabezado de Componente
    st.markdown(f"### {component.get('title', component_type)}")
    
    # Renderizado - Renderizar Basado en Tipo de Componente
    if component_type == replace_emojis("📈 Métricas"):
        display_metric(config, df)
    
    elif component_type == replace_emojis("📊 Gráfico de Líneas"):
        display_line_chart(config, df)
    
    elif component_type == replace_emojis("📋 Gráfico de Barras"):
        display_bar_chart(config, df)
    
    elif component_type == "🥧 Gráfico Circular":
        display_pie_chart(config, df)
    
    elif component_type == replace_emojis("📈 Gráfico de Área"):
        display_area_chart(config, df)
    
    elif component_type == replace_emojis("📈 Gráfico de Dispersión"):
        display_scatter_plot(config, df)
    
    elif component_type == replace_emojis("📊 Histograma"):
        display_histogram(config, df)
    
    elif component_type == replace_emojis("📊 Box Plot"):
        display_box_plot(config, df)
    
    elif component_type == replace_emojis("📈 Gráfico de Violín"):
        display_violin_plot(config, df)
    
    elif component_type == replace_emojis("📊 Matriz de Correlación"):
        display_correlation_matrix(config, df)
    
    elif component_type == replace_emojis("📋 Tabla de Datos"):
        display_data_table(config, df)
    
    else:
        st.warning(f"Tipo de componente no reconocido: {component_type}")
    
    # UI - Agregar Controles de Componente
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚙️ Configurar", key=f"config_{component['id']}", use_container_width=True):
            st.session_state.editing_component = component['id']
            st.rerun()
    
    with col2:
        if st.button("🗑️ Eliminar", key=f"delete_{component['id']}", use_container_width=True):
            st.session_state.dashboard_components = [
                c for c in st.session_state.dashboard_components if c['id'] != component['id']
            ]
            st.rerun()


# Renderizado - Renderizar Dashboard Completo
def render_dashboard(df):
    """Render the complete dashboard"""
    components = st.session_state.get('dashboard_components', [])
    if not components:
        st.markdown(replace_emojis("🎨 No hay componentes en tu dashboard. Usa la barra lateral para agregar componentes."), unsafe_allow_html=True)
        return

    layout_rows = {}
    fallback_row_base = 1000

    for idx, component in enumerate(components):
        layout = component.get('layout') or {}
        row_key = layout.get('row')
        if row_key is None:
            row_key = fallback_row_base + idx
        order = layout.get('order', idx)
        col_span = layout.get('col_span', layout.get('width', 12))
        col_span = max(1, col_span)
        layout_rows.setdefault(row_key, []).append({
            'order': order,
            'col_span': col_span,
            'component': component
        })

    for row_key in sorted(layout_rows.keys()):
        row_components = sorted(layout_rows[row_key], key=lambda item: item['order'])
        column_spans = [item['col_span'] for item in row_components]
        columns = st.columns(column_spans)

        for col, item in zip(columns, row_components):
            with col:
                render_component(item['component'], df)
