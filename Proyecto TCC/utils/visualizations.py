import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_time_series_chart(df, metric='Revenue'):
    """Crear visualización de series temporales"""
    daily_data = df.groupby('Date')[metric].sum().reset_index()
    
    fig = px.line(daily_data, x='Date', y=metric, 
                  title=f'{metric} a lo Largo del Tiempo',
                  template='plotly_white')
    
    fig.update_traces(line=dict(width=3, color='#1f77b4'))
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title=metric,
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_category_analysis(df):
    """Crear gráficos de análisis por categoría"""
    category_metrics = df.groupby('Category').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'Rating': 'mean'
    }).reset_index()
    
    # Crear subgráficos
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Ingresos por Categoría', 'Calificación Promedio por Categoría'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Gráfico de barras de ingresos
    fig.add_trace(
        go.Bar(x=category_metrics['Category'], 
               y=category_metrics['Revenue'],
               name='Ingresos',
               marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Gráfico de barras de calificación
    fig.add_trace(
        go.Bar(x=category_metrics['Category'], 
               y=category_metrics['Rating'],
               name='Calificación Prom.',
               marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    return fig

def create_regional_analysis(df):
    """Crear visualización de rendimiento regional"""
    regional_data = df.groupby('Region').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    fig = px.bar(regional_data, x='Region', y='Revenue',
                 title='Ingresos por Región',
                 template='plotly_white',
                 color='Revenue',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400)
    return fig

def create_correlation_matrix(df, columns):
    """Crear matriz de correlación"""
    if len(columns) < 2:
        return None
    
    corr_data = df[columns].corr()
    
    fig = px.imshow(
        corr_data,
        title="Matriz de Correlación",
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    fig.update_layout(height=400)
    return fig

def create_custom_calculation_charts(df, custom_calculations):
    """Crear gráficos para cálculos personalizados"""
    charts = []
    
    for calc_info in custom_calculations:
        calc_name = calc_info['name']
        if calc_name in df.columns:
            # Gráfico de línea temporal si hay columna de fecha
            if 'Date' in df.columns:
                daily_calc = df.groupby('Date')[calc_name].mean().reset_index()
                fig = px.line(daily_calc, x='Date', y=calc_name,
                             title=f'{calc_name} a lo Largo del Tiempo',
                             template='plotly_white')
                fig.update_traces(line=dict(width=2, color='#2ca02c'))
                fig.update_layout(height=300)
                charts.append(fig)
    
    return charts 