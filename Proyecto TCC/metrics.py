import pandas as pd
import numpy as np

def calculate_metrics(df):
    """Calcular métricas clave del negocio"""
    total_revenue = df['Revenue'].sum()
    total_profit = df['Profit'].sum()
    avg_order_value = df['Revenue'].mean()
    total_orders = len(df)
    avg_rating = df['Rating'].mean()
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'avg_order_value': avg_order_value,
        'total_orders': total_orders,
        'avg_rating': avg_rating,
        'profit_margin': profit_margin
    }

def calculate_growth_metrics(df):
    """Calcular métricas de crecimiento"""
    if 'Date' not in df.columns or len(df) < 30:
        return {}
    
    # Calcular crecimiento mes a mes
    monthly_data = df.set_index('Date').resample('M')['Revenue'].sum()
    mom_growth = 0
    if len(monthly_data) > 1:
        mom_growth = ((monthly_data.iloc[-1] - monthly_data.iloc[-2]) / monthly_data.iloc[-2] * 100)
    
    # Período de mejor rendimiento
    daily_revenue = df.groupby('Date')['Revenue'].sum()
    best_day = daily_revenue.idxmax()
    best_day_revenue = daily_revenue.max()
    
    return {
        'mom_growth': mom_growth,
        'best_day': best_day,
        'best_day_revenue': best_day_revenue
    }

def calculate_performance_insights(df):
    """Calcular perspectivas de rendimiento"""
    insights = {}
    
    if 'Category' in df.columns:
        top_category = df.groupby('Category')['Revenue'].sum().idxmax()
        insights['top_category'] = top_category
    
    if 'Region' in df.columns:
        top_region = df.groupby('Region')['Revenue'].sum().idxmax()
        insights['top_region'] = top_region
    
    # Perspectiva de satisfacción del cliente
    if 'Rating' in df.columns:
        high_rated = len(df[df['Rating'] >= 4]) / len(df) * 100
        insights['high_rated_percentage'] = high_rated
    
    return insights 