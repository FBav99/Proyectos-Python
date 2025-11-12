import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

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

def create_dirty_dataset():
    """Create a dataset with intentional data quality issues for testing cleaning functions"""
    np.random.seed(999)
    n_records = 200
    
    # Create base lists for consistent length
    nombres_base = [
        '  Juan Pérez  ', 'MARÍA GARCÍA', 'carlos lopez', 'Ana María Rodríguez',
        'JOSE MARTINEZ', 'lucia fernandez', '  Pedro Sánchez  ', 'ELENA MORALES',
        'miguel torres', 'Carmen Jiménez', '  ', 'null', 'N/A', '  Roberto Díaz  ',
        'Sofia Castro', 'ANTONIO RUIZ', '  isabel vega  ', 'Francisco Moreno',
        'laura herrera', '  DAVID GUTIERREZ  '
    ]
    
    emails_base = [
        'juan.perez@email.com', 'MARIA.GARCIA@EMAIL.COM', 'carlos.lopez@email.com',
        'ana.rodriguez@email.com', 'jose.martinez@email.com', 'lucia.fernandez@email.com',
        'pedro.sanchez@email.com', 'elena.morales@email.com', 'miguel.torres@email.com',
        'carmen.jimenez@email.com', 'roberto.diaz@email.com', 'sofia.castro@email.com',
        'antonio.ruiz@email.com', 'isabel.vega@email.com', 'francisco.moreno@email.com',
        'laura.herrera@email.com', 'david.gutierrez@email.com', '  ', 'null', 'N/A'
    ]
    
    telefonos_base = [
        '+1-555-123-4567', '(555) 123-4567', '555-123-4567', '5551234567',
        '+1-555-234-5678', '(555) 234-5678', '555-234-5678', '5552345678',
        '+1-555-345-6789', '(555) 345-6789', '555-345-6789', '5553456789',
        '+1-555-456-7890', '(555) 456-7890', '555-456-7890', '5554567890',
        '+1-555-567-8901', '(555) 567-8901', '555-567-8901', '5555678901'
    ]
    
    categorias_base = [
        'Electrónicos', 'ELECTRONICOS', 'electronicos', 'Electrónicos',
        'Ropa', 'ROPA', 'ropa', 'Ropa',
        'Hogar', 'HOGAR', 'hogar', 'Hogar',
        'Deportes', 'DEPORTES', 'deportes', 'Deportes',
        'Libros', 'LIBROS', 'libros', 'Libros',
        '  ', 'null', 'N/A', 'Otros'
    ]
    
    ciudades_base = [
        'México', 'Mexico', 'méxico', 'MEXICO',
        'Bogotá', 'Bogota', 'bogotá', 'BOGOTA',
        'Buenos Aires', 'Buenos aires', 'BUENOS AIRES', 'buenos aires',
        'Santiago', 'santiago', 'SANTIAGO', 'Santiago',
        'Lima', 'lima', 'LIMA', 'Lima',
        '  ', 'null', 'N/A', 'Otra'
    ]
    
    precios_base = [
        '$100.50', '100.50', '100,50', '100',
        '$250.75', '250.75', '250,75', '250',
        '$500.00', '500.00', '500,00', '500',
        '$750.25', '750.25', '750,25', '750',
        '$1000.00', '1000.00', '1000,00', '1000'
    ]
    
    estados_base = [
        'Activo', 'ACTIVO', 'activo', 'Activo',
        'Inactivo', 'INACTIVO', 'inactivo', 'Inactivo',
        'Pendiente', 'PENDIENTE', 'pendiente', 'Pendiente',
        'Cancelado', 'CANCELADO', 'cancelado', 'Cancelado',
        '  ', 'null', 'N/A', 'Otro'
    ]
    
    fechas_base = [
        '2023-01-15', '15/01/2023', '2023-01-15 10:30:00', '15-01-2023',
        '2023-02-20', '20/02/2023', '2023-02-20 14:45:00', '20-02-2023',
        '2023-03-10', '10/03/2023', '2023-03-10 09:15:00', '10-03-2023',
        '2023-04-05', '05/04/2023', '2023-04-05 16:20:00', '05-04-2023',
        '2023-05-12', '12/05/2023', '2023-05-12 11:00:00', '12-05-2023'
    ]
    
    comentarios_base = [
        '¡Excelente producto!', 'excelente producto', 'EXCELENTE PRODUCTO',
        'Muy bueno, lo recomiendo', 'muy bueno, lo recomiendo', 'MUY BUENO, LO RECOMIENDO',
        'Regular, podría mejorar', 'regular, podría mejorar', 'REGULAR, PODRÍA MEJORAR',
        'No me gustó mucho', 'no me gustó mucho', 'NO ME GUSTÓ MUCHO',
        'Pésimo servicio', 'pésimo servicio', 'PESIMO SERVICIO',
        '  ', 'null', 'N/A', 'Sin comentarios'
    ]
    
    # Create data with various issues - ensure all arrays have n_records length
    data = {
        # Names with inconsistent formatting
        'Nombre': (nombres_base * (n_records // len(nombres_base) + 1))[:n_records],
        
        # Emails with various formats
        'Email': (emails_base * (n_records // len(emails_base) + 1))[:n_records],
        
        # Phone numbers with different formats
        'Telefono': (telefonos_base * (n_records // len(telefonos_base) + 1))[:n_records],
        
        # Categories with inconsistencies
        'Categoria': (categorias_base * (n_records // len(categorias_base) + 1))[:n_records],
        
        # Cities with accents and special characters
        'Ciudad': (ciudades_base * (n_records // len(ciudades_base) + 1))[:n_records],
        
        # Prices with various formats
        'Precio': (precios_base * (n_records // len(precios_base) + 1))[:n_records],
        
        # Status with mixed formats
        'Estado': (estados_base * (n_records // len(estados_base) + 1))[:n_records],
        
        # Dates with different formats
        'Fecha_Registro': (fechas_base * (n_records // len(fechas_base) + 1))[:n_records],
        
        # Numeric values with issues
        'Edad': np.random.choice([25, 30, 35, 40, 45, 50, 55, 60, -5, 150, np.nan, ''], n_records),
        'Puntuacion': np.random.choice([1, 2, 3, 4, 5, 0, 6, 7, np.nan, ''], n_records),
        
        # Text with special characters and accents
        'Comentario': (comentarios_base * (n_records // len(comentarios_base) + 1))[:n_records]
    }
    
    df = pd.DataFrame(data)
    
    # Add some duplicates
    df = pd.concat([df, df.iloc[:20]], ignore_index=True)
    
    # Add some completely empty rows
    empty_rows = pd.DataFrame({
        'Nombre': [''] * 5,
        'Email': [''] * 5,
        'Telefono': [''] * 5,
        'Categoria': [''] * 5,
        'Ciudad': [''] * 5,
        'Precio': [''] * 5,
        'Estado': [''] * 5,
        'Fecha_Registro': [''] * 5,
        'Edad': [np.nan] * 5,
        'Puntuacion': [np.nan] * 5,
        'Comentario': [''] * 5
    })
    
    df = pd.concat([df, empty_rows], ignore_index=True)
    
    return df.reset_index(drop=True)

@st.cache_data(show_spinner=False, ttl=3600)
def get_sample_datasets():
    """Return all available sample datasets"""
    return {
        'Dataset Sucio (Limpieza)': {
            'data': create_dirty_dataset(),
            'description': 'Dataset con múltiples problemas de calidad para practicar limpieza automática',
            'difficulty': 'Avanzado',
            'data_quality_issues': 'Espacios, mayúsculas/minúsculas, acentos, teléfonos, emails, duplicados, valores faltantes'
        },
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
