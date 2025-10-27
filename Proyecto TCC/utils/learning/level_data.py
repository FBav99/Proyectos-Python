import pandas as pd
import numpy as np

def create_sample_data(version='clean'):
    """
    Create sample data for demonstration with dirty and clean versions
    
    Args:
        version (str): 'dirty' for raw data with issues, 'clean' for processed data
    """
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = len(dates)
    
    if version == 'dirty':
        # Create dirty data with common data quality issues
        data = {
            'Fecha': np.random.choice(dates, n_records//2),
            'Categoria': np.random.choice(['Electronica', 'Ropa', 'Libros', 'Hogar', 'ELECTRONICA', 'ropa', 'libros', 'HOGAR', ''], n_records//2, p=[0.19, 0.19, 0.19, 0.19, 0.05, 0.05, 0.05, 0.05, 0.04]),
            'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'norte', 'SUR', 'este', 'OESTE', 'Centro'], n_records//2, p=[0.19, 0.19, 0.19, 0.19, 0.05, 0.05, 0.05, 0.05, 0.04]),
            'Ventas': np.random.normal(1000, 300, n_records//2).round(2),
            'Cantidad': np.random.poisson(5, n_records//2),
            'Calificacion': np.random.choice([1, 2, 3, 4, 5, 6, 0, -1], n_records//2, p=[0.05, 0.10, 0.15, 0.40, 0.25, 0.02, 0.02, 0.01])
        }
        
        df = pd.DataFrame(data)
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Ingresos'] = df['Ventas'] * df['Cantidad']
        
        # Add some data quality issues
        # Missing values
        missing_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
        df.loc[missing_indices, 'Categoria'] = np.nan
        
        # Duplicate rows
        duplicate_indices = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
        df = pd.concat([df, df.loc[duplicate_indices]], ignore_index=True)
        
        # Outliers
        outlier_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
        df.loc[outlier_indices, 'Ventas'] = df.loc[outlier_indices, 'Ventas'] * 10
        
        # Inconsistent date formats (simulate)
        date_inconsistent = np.random.choice(df.index, size=int(len(df) * 0.1), replace=False)
        df.loc[date_inconsistent, 'Fecha'] = df.loc[date_inconsistent, 'Fecha'].dt.strftime('%m/%d/%Y')
        
    else:  # clean version
        # Create clean, processed data
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
        
        # Clean the data
        df = df.dropna()  # Remove missing values
        df = df.drop_duplicates()  # Remove duplicates
        df = df[df['Calificacion'].between(1, 5)]  # Remove invalid ratings
        df = df[df['Ventas'] > 0]  # Remove negative sales
        df = df[df['Cantidad'] > 0]  # Remove zero quantities
    
    return df.sort_values('Fecha').reset_index(drop=True)

def get_data_progression_info():
    """Get information about data progression across levels"""
    return {
        'nivel0': {
            'title': 'Conceptos de Datos',
            'data_type': 'clean',
            'description': 'Datos organizados para entender conceptos básicos',
            'achievement': 'Entender qué son los datos y cómo se organizan'
        },
        'nivel1': {
            'title': 'Preparación de Datos',
            'data_type': 'dirty',
            'description': 'Datos sin procesar que necesitan preparación',
            'achievement': 'Aprender a cargar y verificar datos correctamente'
        },
        'nivel2': {
            'title': 'Filtros y Organización',
            'data_type': 'clean',
            'description': 'Datos preparados listos para filtrar',
            'achievement': 'Dominar el uso de filtros para encontrar información específica'
        },
        'nivel3': {
            'title': 'Métricas y KPIs',
            'data_type': 'clean',
            'description': 'Datos limpios para calcular métricas',
            'achievement': 'Calcular e interpretar métricas de negocio'
        },
        'nivel4': {
            'title': 'Análisis Avanzado',
            'data_type': 'clean',
            'description': 'Datos optimizados para análisis complejos',
            'achievement': 'Crear dashboards profesionales y visualizaciones avanzadas'
        }
    }

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
