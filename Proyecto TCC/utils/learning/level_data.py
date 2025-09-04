import pandas as pd
import numpy as np

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = len(dates)
    
    data = {
        'Fecha': np.random.choice(dates, n_records//2),
        'Categoria': np.random.choice(['Electronica', 'Ropa', 'Libros', 'Hogar'], n_records//2),
        'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n_records//2),
        'Ventas': np.random.normal(1000, 300, n_records//2).round(2),
        'Cantidad': np.random.poisson(5, n_records//2),
        'Calificacion': np.random.choice([1, 2, 3, 4, 5], n_records//2, p=[0.05, 0.1, 0.15, 0.4, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Ingresos'] = df['Ventas'] * df['Cantidad']
    
    return df.sort_values('Fecha').reset_index(drop=True)

def analyze_uploaded_data(df_uploaded):
    """Analyze uploaded data and return analysis results"""
    # Calculate data types
    numeric_cols = df_uploaded.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df_uploaded.select_dtypes(include=['object']).columns.tolist()
    date_cols = df_uploaded.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Check for missing values
    missing_data = df_uploaded.isnull().sum()
    total_missing = missing_data.sum()
    missing_percentage = (total_missing / (len(df_uploaded) * len(df_uploaded.columns))) * 100
    
    # Check for duplicate rows
    duplicates = df_uploaded.duplicated().sum()
    
    return {
        'numeric_cols': numeric_cols,
        'text_cols': text_cols,
        'date_cols': date_cols,
        'total_missing': total_missing,
        'missing_percentage': missing_percentage,
        'duplicates': duplicates
    }
