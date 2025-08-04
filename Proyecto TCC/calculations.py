import pandas as pd
import numpy as np
import streamlit as st

def apply_basic_calculation(df, calc_info):
    """Aplicar operaciones matemáticas básicas"""
    col1_calc, col2_calc, operation = calc_info['col1'], calc_info['col2'], calc_info['operation']
    calc_name = calc_info['name']
    
    try:
        if operation == "Sumar (+)":
            df[calc_name] = df[col1_calc] + df[col2_calc]
        elif operation == "Restar (-)":
            df[calc_name] = df[col1_calc] - df[col2_calc]
        elif operation == "Multiplicar (×)":
            df[calc_name] = df[col1_calc] * df[col2_calc]
        elif operation == "Dividir (÷)":
            df[calc_name] = df[col1_calc] / df[col2_calc].replace(0, np.nan)
        elif operation == "Potencia (^)":
            df[calc_name] = df[col1_calc] ** df[col2_calc]
        elif operation == "Porcentaje (%)":
            df[calc_name] = (df[col1_calc] / df[col2_calc] * 100).replace([np.inf, -np.inf], np.nan)
        
        return True
    except Exception as e:
        st.sidebar.error(f"Error en cálculo básico '{calc_name}': {str(e)}")
        return False

def apply_time_calculation(df, calc_info):
    """Aplicar cálculos basados en tiempo"""
    target_col = calc_info['target_col']
    date_col = calc_info['date_col']
    time_op = calc_info['time_operation']
    calc_name = calc_info['name']
    
    try:
        df_sorted = df.sort_values(date_col)
        
        if time_op == "Año hasta la Fecha (YTD)":
            df[calc_name] = df_sorted.groupby(df_sorted[date_col].dt.year)[target_col].cumsum().values
            
        elif time_op == "Mismo Período Año Anterior (SPLY)":
            df[calc_name] = df_sorted.groupby([df_sorted[date_col].dt.month, df_sorted[date_col].dt.day])[target_col].shift(1).values
            
        elif time_op == "Mes a Mes (MoM)":
            monthly_data = df_sorted.groupby(df_sorted[date_col].dt.to_period('M'))[target_col].sum()
            mom_change = monthly_data.pct_change() * 100
            df[calc_name] = df_sorted[date_col].dt.to_period('M').map(mom_change).values
            
        elif time_op == "Trimestre a Trimestre (QoQ)":
            quarterly_data = df_sorted.groupby(df_sorted[date_col].dt.to_period('Q'))[target_col].sum()
            qoq_change = quarterly_data.pct_change() * 100
            df[calc_name] = df_sorted[date_col].dt.to_period('Q').map(qoq_change).values
            
        elif time_op == "Año a Año (YoY)":
            yearly_data = df_sorted.groupby(df_sorted[date_col].dt.to_period('Y'))[target_col].sum()
            yoy_change = yearly_data.pct_change() * 100
            df[calc_name] = df_sorted[date_col].dt.to_period('Y').map(yoy_change).values
            
        elif time_op == "Promedio Móvil 30 días":
            df[calc_name] = df_sorted.set_index(date_col)[target_col].rolling('30D').mean().values
            
        elif time_op == "Suma Móvil 90 días":
            df[calc_name] = df_sorted.set_index(date_col)[target_col].rolling('90D').sum().values
            
        elif time_op == "Suma Acumulada":
            df[calc_name] = df_sorted[target_col].cumsum().values
        
        return True
    except Exception as e:
        st.sidebar.error(f"Error en cálculo temporal '{calc_name}': {str(e)}")
        return False

def apply_aggregation_calculation(df, calc_info):
    """Aplicar cálculos de agregación"""
    target_col = calc_info['target_col']
    group_col = calc_info['group_col']
    agg_op = calc_info['agg_operation']
    calc_name = calc_info['name']
    
    try:
        if agg_op == "Suma":
            agg_result = df.groupby(group_col)[target_col].sum()
        elif agg_op == "Promedio":
            agg_result = df.groupby(group_col)[target_col].mean()
        elif agg_op == "Contar":
            agg_result = df.groupby(group_col)[target_col].count()
        elif agg_op == "Máximo":
            agg_result = df.groupby(group_col)[target_col].max()
        elif agg_op == "Mínimo":
            agg_result = df.groupby(group_col)[target_col].min()
        elif agg_op == "Desv. Estándar":
            agg_result = df.groupby(group_col)[target_col].std()
        elif agg_op == "Mediana":
            agg_result = df.groupby(group_col)[target_col].median()
        
        # Mapear de vuelta al dataframe original
        df[calc_name] = df[group_col].map(agg_result)
        
        return True
    except Exception as e:
        st.sidebar.error(f"Error en cálculo de agregación '{calc_name}': {str(e)}")
        return False

def apply_custom_calculations(df, custom_calculations):
    """Aplicar todos los cálculos personalizados"""
    filters_applied = {}
    
    for calc_info in custom_calculations:
        success = False
        
        if calc_info['type'] == 'basic':
            success = apply_basic_calculation(df, calc_info)
        elif calc_info['type'] == 'time':
            success = apply_time_calculation(df, calc_info)
        elif calc_info['type'] == 'aggregation':
            success = apply_aggregation_calculation(df, calc_info)
        
        if success:
            filters_applied[f'Cálculo Personalizado {calc_info["name"]}'] = f"{calc_info}"
    
    return filters_applied 