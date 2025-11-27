import pandas as pd
import streamlit as st

# Filtro - Aplicar Filtro de Fecha
def apply_date_filter(df, original_df):
    """Aplicar filtro de fecha"""
    filters_applied = {}
    
    if 'Date' in df.columns:
        date_range = st.sidebar.date_input(
            "Seleccionar Rango de Fechas",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
        if len(date_range) == 2:
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & 
                   (df['Date'] <= pd.to_datetime(date_range[1]))]
            filters_applied['Rango de Fechas'] = f"{date_range[0]} hasta {date_range[1]}"
    
    return df, filters_applied

# Filtro - Aplicar Filtro de Categoria
def apply_category_filter(df, original_df):
    """Aplicar filtro de categoría"""
    filters_applied = {}
    
    if 'Category' in df.columns:
        categories = st.sidebar.multiselect(
            "Seleccionar Categorías",
            options=original_df['Category'].unique(),
            default=original_df['Category'].unique()
        )
        if categories:
            df = df[df['Category'].isin(categories)]
            filters_applied['Categorías'] = categories
    
    return df, filters_applied

# Filtro - Aplicar Filtro de Region
def apply_region_filter(df, original_df):
    """Aplicar filtro de región"""
    filters_applied = {}
    
    if 'Region' in df.columns:
        regions = st.sidebar.multiselect(
            "Seleccionar Regiones",
            options=original_df['Region'].unique(),
            default=original_df['Region'].unique()
        )
        if regions:
            df = df[df['Region'].isin(regions)]
            filters_applied['Regiones'] = regions
    
    return df, filters_applied

# Filtro - Aplicar Filtros Numericos
def apply_numeric_filters(df, original_df):
    """Aplicar filtros numéricos"""
    filters_applied = {}
    
    all_numeric_cols = df.select_dtypes(include=['number']).columns
    for col in ['Sales', 'Revenue', 'Rating']:
        if col in all_numeric_cols:
            col_min, col_max = float(original_df[col].min() if col in original_df.columns else df[col].min()), float(original_df[col].max() if col in original_df.columns else df[col].max())
            if col_min != col_max:  # Solo mostrar deslizador si hay un rango
                range_values = st.sidebar.slider(
                    f"Rango de {col}",
                    min_value=col_min,
                    max_value=col_max,
                    value=(col_min, col_max),
                    step=(col_max - col_min) / 100 if col_max != col_min else 1.0
                )
                df = df[(df[col] >= range_values[0]) & (df[col] <= range_values[1])]
                if range_values != (col_min, col_max):
                    filters_applied[f'Rango de {col}'] = range_values
    
    return df, filters_applied

# Filtro - Aplicar Todos los Filtros
def apply_all_filters(df, original_df):
    """Aplicar todos los filtros"""
    filters_applied = {}
    
    # Aplicar filtros en secuencia
    df, date_filters = apply_date_filter(df, original_df)
    filters_applied.update(date_filters)
    
    df, category_filters = apply_category_filter(df, original_df)
    filters_applied.update(category_filters)
    
    df, region_filters = apply_region_filter(df, original_df)
    filters_applied.update(region_filters)
    
    df, numeric_filters = apply_numeric_filters(df, original_df)
    filters_applied.update(numeric_filters)
    
    return df, filters_applied 