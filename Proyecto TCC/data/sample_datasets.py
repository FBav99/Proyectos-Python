import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_ecommerce_dataset():
    """Create sample e-commerce dataset"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = 1000
    
    data = {
        'Fecha': np.random.choice(dates, n_records),
        'Producto': np.random.choice(['Laptop', 'Smartphone', 'Tablet', 'Auriculares', 'Cámara'], n_records),
        'Categoria': np.random.choice(['Electrónica', 'Tecnología', 'Accesorios'], n_records),
        'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Centro'], n_records),
        'Precio': np.random.normal(500, 200, n_records).round(2),
        'Cantidad': np.random.poisson(2, n_records),
        'Calificacion': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.05, 0.1, 0.15, 0.4, 0.3]),
        'Metodo_Pago': np.random.choice(['Tarjeta', 'Efectivo', 'Transferencia'], n_records)
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Ingresos'] = df['Precio'] * df['Cantidad']
    
    return df.sort_values('Fecha').reset_index(drop=True)

def create_healthcare_dataset():
    """Create sample healthcare dataset with some data quality issues"""
    np.random.seed(123)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = 800
    
    # Create data with intentional issues
    data = {
        'Fecha_Consulta': np.random.choice(dates, n_records),
        'Paciente_ID': [f'P{i:04d}' for i in range(1, n_records + 1)],
        'Edad': np.random.normal(45, 15, n_records).round(0),
        'Genero': np.random.choice(['M', 'F', 'Masculino', 'Femenino', ''], n_records, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
        'Diagnostico': np.random.choice(['Hipertensión', 'Diabetes', 'Gripe', 'Dolor de espalda', 'Migraña', ''], n_records),
        'Presion_Sistolica': np.random.normal(120, 20, n_records).round(0),
        'Presion_Diastolica': np.random.normal(80, 10, n_records).round(0),
        'Peso_kg': np.random.normal(70, 15, n_records).round(1),
        'Altura_cm': np.random.normal(170, 10, n_records).round(0)
    }
    
    df = pd.DataFrame(data)
    df['Fecha_Consulta'] = pd.to_datetime(df['Fecha_Consulta'])
    
    # Add some data quality issues
    df.loc[np.random.choice(df.index, 50), 'Edad'] = np.nan  # Missing values
    df.loc[np.random.choice(df.index, 30), 'Peso_kg'] = -5  # Invalid values
    df.loc[np.random.choice(df.index, 20), 'Altura_cm'] = 300  # Outliers
    
    return df.sort_values('Fecha_Consulta').reset_index(drop=True)

def create_finance_dataset():
    """Create sample financial dataset"""
    np.random.seed(456)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = 1200
    
    data = {
        'Fecha': np.random.choice(dates, n_records),
        'Tipo_Transaccion': np.random.choice(['Depósito', 'Retiro', 'Transferencia', 'Pago'], n_records),
        'Categoria': np.random.choice(['Alimentación', 'Transporte', 'Entretenimiento', 'Servicios', 'Compras'], n_records),
        'Monto': np.random.normal(100, 50, n_records).round(2),
        'Cuenta': np.random.choice(['Cuenta Corriente', 'Cuenta de Ahorros', 'Tarjeta de Crédito'], n_records),
        'Descripcion': ['Transacción ' + str(i) for i in range(1, n_records + 1)],
        'Balance': np.cumsum(np.random.normal(0, 100, n_records)).round(2)
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    return df.sort_values('Fecha').reset_index(drop=True)

def create_education_dataset():
    """Create sample education dataset"""
    np.random.seed(789)
    n_students = 500
    
    data = {
        'Estudiante_ID': [f'E{i:04d}' for i in range(1, n_students + 1)],
        'Nombre': [f'Estudiante {i}' for i in range(1, n_students + 1)],
        'Edad': np.random.normal(20, 3, n_students).round(0),
        'Carrera': np.random.choice(['Ingeniería', 'Medicina', 'Derecho', 'Administración', 'Arquitectura'], n_students),
        'Semestre': np.random.choice(range(1, 11), n_students),
        'Promedio_General': np.random.normal(3.5, 0.5, n_students).round(2),
        'Asignaturas_Aprobadas': np.random.poisson(15, n_students),
        'Horas_Estudio_Semana': np.random.normal(20, 5, n_students).round(1),
        'Actividades_Extracurriculares': np.random.choice([0, 1, 2, 3], n_students)
    }
    
    df = pd.DataFrame(data)
    
    # Add some realistic constraints
    df.loc[df['Promedio_General'] > 4.0, 'Promedio_General'] = 4.0
    df.loc[df['Promedio_General'] < 1.0, 'Promedio_General'] = 1.0
    
    return df.reset_index(drop=True)

def create_sales_dataset():
    """Create sample sales dataset with seasonal patterns"""
    np.random.seed(321)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = 1500
    
    # Create seasonal patterns
    seasonal_factor = np.sin(2 * np.pi * np.arange(len(dates)) / 365) * 0.3 + 1
    
    data = {
        'Fecha': np.random.choice(dates, n_records),
        'Vendedor': np.random.choice(['Ana', 'Carlos', 'María', 'Juan', 'Laura'], n_records),
        'Producto': np.random.choice(['Producto A', 'Producto B', 'Producto C', 'Producto D'], n_records),
        'Cantidad': np.random.poisson(5, n_records),
        'Precio_Unitario': np.random.normal(100, 30, n_records).round(2),
        'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n_records),
        'Cliente_Tipo': np.random.choice(['Nuevo', 'Recurrente', 'VIP'], n_records)
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Ingresos'] = df['Cantidad'] * df['Precio_Unitario']
    
    # Apply seasonal factor
    df['Ingresos'] = df['Ingresos'] * np.random.choice(seasonal_factor, len(df))
    
    return df.sort_values('Fecha').reset_index(drop=True)

def get_sample_datasets():
    """Return all available sample datasets"""
    return {
        'E-commerce': {
            'data': create_ecommerce_dataset(),
            'description': 'Datos de ventas online con productos, regiones y calificaciones',
            'difficulty': 'Básico',
            'data_quality_issues': 'Mínimas'
        },
        'Healthcare': {
            'data': create_healthcare_dataset(),
            'description': 'Datos médicos con problemas de calidad para práctica de limpieza',
            'difficulty': 'Intermedio',
            'data_quality_issues': 'Valores faltantes, outliers, inconsistencias'
        },
        'Finance': {
            'data': create_finance_dataset(),
            'description': 'Transacciones financieras con categorías y balances',
            'difficulty': 'Básico',
            'data_quality_issues': 'Mínimas'
        },
        'Education': {
            'data': create_education_dataset(),
            'description': 'Datos de estudiantes universitarios con rendimiento académico',
            'difficulty': 'Básico',
            'data_quality_issues': 'Mínimas'
        },
        'Sales': {
            'data': create_sales_dataset(),
            'description': 'Ventas con patrones estacionales y múltiples dimensiones',
            'difficulty': 'Intermedio',
            'data_quality_issues': 'Mínimas'
        }
    }
