import pandas as pd
import numpy as np

# Calculo - Calcular Metricas Clave
def calculate_metrics(df):
    """Calcular métricas clave del negocio de forma flexible"""
    metrics = {}
    
    # Métricas básicas que siempre están disponibles
    metrics['total_records'] = len(df)
    metrics['total_columns'] = len(df.columns)
    
    # Métricas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Usar la primera columna numérica como principal
        main_numeric = numeric_cols[0]
        metrics['total_value'] = df[main_numeric].sum()
        metrics['avg_value'] = df[main_numeric].mean()
        metrics['max_value'] = df[main_numeric].max()
        metrics['min_value'] = df[main_numeric].min()
        
        # Si hay más de una columna numérica, calcular métricas adicionales
        if len(numeric_cols) > 1:
            second_numeric = numeric_cols[1]
            metrics['total_value_2'] = df[second_numeric].sum()
            metrics['avg_value_2'] = df[second_numeric].mean()
    
    # Métricas categóricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        metrics['unique_categories'] = df[categorical_cols[0]].nunique()
        metrics['most_common_category'] = df[categorical_cols[0]].mode().iloc[0] if not df[categorical_cols[0]].mode().empty else "N/A"
    
    # Métricas de fechas si existen
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        metrics['date_range_days'] = (df[date_cols[0]].max() - df[date_cols[0]].min()).days
    
    return metrics

# Calculo - Calcular Metricas de Crecimiento
def calculate_growth_metrics(df):
    """Calcular métricas de crecimiento de forma flexible"""
    metrics = {}
    
    # Buscar columnas de fecha
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
    
    if len(date_cols) > 0 and len(df) >= 10:
        date_col = date_cols[0]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            main_numeric = numeric_cols[0]
            
            # Calcular crecimiento mes a mes
            try:
                monthly_data = df.set_index(date_col).resample('ME')[main_numeric].sum()
                if len(monthly_data) > 1:
                    mom_growth = ((monthly_data.iloc[-1] - monthly_data.iloc[-2]) / monthly_data.iloc[-2] * 100)
                    metrics['monthly_growth'] = mom_growth
            except:
                pass
            
            # Período de mejor rendimiento
            try:
                daily_data = df.groupby(date_col)[main_numeric].sum()
                best_day = daily_data.idxmax()
                best_day_value = daily_data.max()
                metrics['best_day'] = best_day
                metrics['best_day_value'] = best_day_value
            except:
                pass
    
    return metrics

# Calculo - Calcular Perspectivas de Rendimiento
def calculate_performance_insights(df):
    """Calcular perspectivas de rendimiento de forma flexible"""
    insights = []
    
    # Buscar columnas categóricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        # Análisis por categorías
        for cat_col in categorical_cols[:2]:  # Máximo 2 categorías
            try:
                top_category = df.groupby(cat_col)[numeric_cols[0]].sum().idxmax()
                insights.append(f"La categoría '{top_category}' tiene el mayor valor total en {numeric_cols[0]}")
            except:
                pass
    
    # Análisis de distribución
    if len(numeric_cols) > 0:
        main_numeric = numeric_cols[0]
        mean_val = df[main_numeric].mean()
        median_val = df[main_numeric].median()
        
        if mean_val > median_val * 1.2:
            insights.append(f"La distribución de {main_numeric} está sesgada hacia valores altos")
        elif mean_val < median_val * 0.8:
            insights.append(f"La distribución de {main_numeric} está sesgada hacia valores bajos")
        else:
            insights.append(f"La distribución de {main_numeric} es relativamente simétrica")
    
    # Análisis de completitud
    missing_data = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = ((total_cells - missing_data) / total_cells) * 100
    
    if completeness < 90:
        insights.append(f"El dataset tiene {100-completeness:.1f}% de datos faltantes")
    else:
        insights.append("El dataset tiene buena completitud de datos")
    
    # Análisis de outliers
    if len(numeric_cols) > 0:
        main_numeric = numeric_cols[0]
        Q1 = df[main_numeric].quantile(0.25)
        Q3 = df[main_numeric].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[main_numeric] < Q1 - 1.5*IQR) | (df[main_numeric] > Q3 + 1.5*IQR)]
        
        if len(outliers) > 0:
            outlier_percentage = (len(outliers) / len(df)) * 100
            insights.append(f"Se detectaron {len(outliers)} outliers ({outlier_percentage:.1f}% del total)")
    
    return insights 