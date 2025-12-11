import pandas as pd
import numpy as np
import streamlit as st

from utils.ui.icon_system import get_icon, replace_emojis
from utils.data.data_handling import load_excel_with_sheet_selection, load_csv_with_delimiter_selection
# Datos - Cargar Datos de Muestra
@st.cache_data(show_spinner=False, ttl=3600)
def load_sample_data():
    """Generar conjunto de datos de muestra para demostración"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    n_records = len(dates)
    
    data = {
        'Date': np.random.choice(dates, n_records//2),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], n_records//2),
        'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_records//2),
        'Sales': np.random.normal(1000, 300, n_records//2).round(2),
        'Quantity': np.random.poisson(5, n_records//2),
        'Customer_Age': np.random.normal(35, 12, n_records//2).round(0),
        'Rating': np.random.choice([1, 2, 3, 4, 5], n_records//2, p=[0.05, 0.1, 0.15, 0.4, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Sales'] * df['Quantity']
    df['Profit_Margin'] = np.random.uniform(0.1, 0.4, len(df))
    df['Profit'] = df['Revenue'] * df['Profit_Margin']
    
    return df.sort_values('Date').reset_index(drop=True)

# Archivo - Cargar Archivo Subido
def load_uploaded_file(uploaded_file):
    """Cargar archivo subido por el usuario"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = load_csv_with_delimiter_selection(uploaded_file, key_prefix="sidebar_loader")
            if df is None:
                return None
        else:
            df = load_excel_with_sheet_selection(uploaded_file, key_prefix="sidebar_loader")
            if df is None:
                return None
        
        # Intentar convertir columnas de fecha
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
                    
        st.sidebar.success(f"{get_icon("✅", 20)} Cargadas {len(df)} filas de datos")
        return df
    except Exception as e:
        st.sidebar.error(f"Error al cargar archivo: {str(e)}")
        return None

# Datos - Obtener Datos de Archivo o Muestra
def get_data(uploaded_file):
    """Obtener datos del archivo subido o usar datos de muestra"""
    if uploaded_file is not None:
        df = load_uploaded_file(uploaded_file)
        if df is not None:
            return df
    
    st.sidebar.info("Usando datos de muestra para demostración")
    return load_sample_data() 