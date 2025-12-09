import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Visualizacion - Crear Grafico de Series Temporales
def create_time_series_chart(df, metric=None):
    """Crear visualización de series temporales de forma flexible"""
    # Consulta - Buscar Columnas de Fecha
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) == 0:
        # Intentar convertir columnas que parezcan fechas
        for col in df.columns:
            if 'date' in col.lower() or 'fecha' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols = [col]
                    break
                except:
                    continue
    
    if len(date_cols) == 0:
        # Si no hay fechas, crear un gráfico simple
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            fig = px.line(df, x=df.index, y=numeric_cols[0], 
                         title=f'{numeric_cols[0]} por Índice',
                         template='plotly_white')
            fig.update_layout(height=400)
            return fig
        return None
    
    date_col = date_cols[0]
    
    # Consulta - Buscar Metrica Numerica
    if metric is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return None
        metric = numeric_cols[0]
    
    try:
        daily_data = df.groupby(date_col)[metric].sum().reset_index()
        
        fig = px.line(daily_data, x=date_col, y=metric, 
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
    except:
        return None

# Visualizacion - Crear Analisis por Categoria
def create_category_analysis(df):
    """Crear gráficos de análisis por categoría de forma flexible"""
    # Consulta - Buscar Columnas Categoricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(categorical_cols) == 0 or len(numeric_cols) == 0:
        return None
    
    # Procesamiento - Usar Primera Categoria y Primera Metrica Numerica
    cat_col = categorical_cols[0]
    metric_col = numeric_cols[0]
    
    try:
        category_metrics = df.groupby(cat_col)[metric_col].sum().reset_index()
        
        fig = px.bar(category_metrics, x=cat_col, y=metric_col,
                    title=f'{metric_col} por {cat_col}',
                    template='plotly_white',
                    color=metric_col,
                    color_continuous_scale='Blues')
        
        fig.update_layout(height=400)
        return fig
    except:
        return None

# Visualizacion - Crear Analisis Regional
def create_regional_analysis(df):
    """Crear visualización de rendimiento regional de forma flexible"""
    # Consulta - Buscar Columnas Categoricas (Excluyendo Primera que Ya se Uso)
    categorical_cols = df.select_dtypes(include=['object']).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(categorical_cols) < 2 or len(numeric_cols) == 0:
        return None
    
    # Procesamiento - Usar Segunda Categoria y Primera Metrica Numerica
    cat_col = categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0]
    metric_col = numeric_cols[0]
    
    try:
        regional_data = df.groupby(cat_col)[metric_col].sum().reset_index()
        
        fig = px.bar(regional_data, x=cat_col, y=metric_col,
                    title=f'{metric_col} por {cat_col}',
                    template='plotly_white',
                    color=metric_col,
                    color_continuous_scale='Blues')
        
        fig.update_layout(height=400)
        return fig
    except:
        return None

# Visualizacion - Crear Matriz de Correlacion
def create_correlation_matrix(df, columns=None):
    """Crear matriz de correlación de forma flexible"""
    if columns is None:
        # Usar todas las columnas numéricas
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(columns) < 2:
        return None
    
    try:
        corr_data = df[columns].corr()
        
        fig = px.imshow(
            corr_data,
            title="Matriz de Correlación",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig.update_layout(height=400)
        return fig
    except:
        return None

# Visualizacion - Crear Graficos de Calculos Personalizados
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