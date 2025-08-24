import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.export import export_data, get_csv_data, create_summary_report

def create_sidebar_controls():
    """Crear controles de la barra lateral"""
    st.sidebar.title("🔧 Controles")
    
    # Carga de archivos
    uploaded_file = st.sidebar.file_uploader(
        "Sube tu archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para analizar tus datos"
    )
    
    return uploaded_file

def create_custom_calculations_ui(df):
    """Crear interfaz para cálculos personalizados"""
    st.sidebar.subheader("🧮 Cálculos Personalizados")
    
    # Obtener columnas numéricas para cálculos
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    custom_calculations = []
    
    if len(numeric_cols) >= 1:
        # Selector de tipo de cálculo
        calc_type = st.sidebar.selectbox(
            "Tipo de Cálculo",
            ["Matemáticas Básicas", "Comparaciones Temporales", "Agregaciones"]
        )
        
        num_calculations = st.sidebar.number_input("Número de cálculos personalizados", min_value=0, max_value=5, value=0)
        
        for i in range(num_calculations):
            st.sidebar.markdown(f"**Cálculo {i+1}:**")
            
            if calc_type == "Matemáticas Básicas":
                # Operaciones matemáticas originales
                col1_calc = st.sidebar.selectbox(f"Columna 1", options=numeric_cols, key=f"col1_{i}")
                operation = st.sidebar.selectbox(
                    f"Operación", 
                    options=["Sumar (+)", "Restar (-)", "Multiplicar (×)", "Dividir (÷)", "Potencia (^)", "Porcentaje (%)"],
                    key=f"op_{i}"
                )
                col2_calc = st.sidebar.selectbox(f"Columna 2", options=numeric_cols, key=f"col2_{i}")
                calc_name = st.sidebar.text_input(f"Nombra este cálculo", value=f"Personalizado_{i+1}", key=f"name_{i}")
                
                custom_calculations.append({
                    'type': 'basic',
                    'name': calc_name,
                    'col1': col1_calc,
                    'operation': operation,
                    'col2': col2_calc
                })
                
            elif calc_type == "Comparaciones Temporales" and len(date_cols) > 0:
                # Cálculos basados en tiempo
                target_col = st.sidebar.selectbox(f"Columna Objetivo", options=numeric_cols, key=f"target_{i}")
                date_col = st.sidebar.selectbox(f"Columna de Fecha", options=date_cols, key=f"date_{i}")
                
                time_operation = st.sidebar.selectbox(
                    f"Comparación Temporal",
                    options=[
                        "Año hasta la Fecha (YTD)",
                        "Mismo Período Año Anterior (SPLY)", 
                        "Mes a Mes (MoM)",
                        "Trimestre a Trimestre (QoQ)",
                        "Año a Año (YoY)",
                        "Promedio Móvil 30 días",
                        "Suma Móvil 90 días",
                        "Suma Acumulada"
                    ],
                    key=f"time_op_{i}"
                )
                
                calc_name = st.sidebar.text_input(f"Nombra este cálculo", value=f"{target_col}_{time_operation.split()[0]}", key=f"time_name_{i}")
                
                custom_calculations.append({
                    'type': 'time',
                    'name': calc_name,
                    'target_col': target_col,
                    'date_col': date_col,
                    'time_operation': time_operation
                })
                
            elif calc_type == "Agregaciones":
                # Cálculos de agregación
                target_col = st.sidebar.selectbox(f"Columna Objetivo", options=numeric_cols, key=f"agg_target_{i}")
                group_by_cols = [col for col in df.columns if df[col].dtype == 'object' or col in date_cols]
                
                if group_by_cols:
                    group_col = st.sidebar.selectbox(f"Agrupar Por", options=group_by_cols, key=f"group_{i}")
                    agg_operation = st.sidebar.selectbox(
                        f"Agregación",
                        options=["Suma", "Promedio", "Contar", "Máximo", "Mínimo", "Desv. Estándar", "Mediana"],
                        key=f"agg_op_{i}"
                    )
                    
                    calc_name = st.sidebar.text_input(f"Nombra este cálculo", value=f"{target_col}_{agg_operation}_por_{group_col}", key=f"agg_name_{i}")
                    
                    custom_calculations.append({
                        'type': 'aggregation',
                        'name': calc_name,
                        'target_col': target_col,
                        'group_col': group_col,
                        'agg_operation': agg_operation
                    })
            
            st.sidebar.markdown("---")
    
    return custom_calculations

def display_metrics_dashboard(metrics, df):
    """Mostrar panel de métricas clave"""
    st.subheader("🎯 Métricas Clave de Rendimiento")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Ingresos Totales",
            f"${metrics['total_revenue']:,.2f}",
            delta=f"{metrics['profit_margin']:.1f}% margen"
        )
    
    with col2:
        st.metric(
            "📈 Pedidos Totales",
            f"{metrics['total_orders']:,}",
            delta=f"${metrics['avg_order_value']:.2f} promedio"
        )
    
    with col3:
        st.metric(
            "💵 Ganancia Total",
            f"${metrics['total_profit']:,.2f}",
            delta=f"{metrics['profit_margin']:.1f}% margen"
        )
    
    with col4:
        st.metric(
            "⭐ Calificación Promedio",
            f"{metrics['avg_rating']:.2f}/5.0",
            delta=f"{len(df[df['Rating'] >= 4])} clientes satisfechos"
        )

def display_custom_calculations_metrics(df, custom_calculations):
    """Mostrar métricas de cálculos personalizados"""
    if not custom_calculations:
        return
    
    st.subheader("🧮 Tus Cálculos Personalizados")
    
    calc_cols = st.columns(min(3, len(custom_calculations)))
    for i, calc_info in enumerate(custom_calculations):
        with calc_cols[i % 3]:
            calc_name = calc_info['name']
            if calc_name in df.columns:
                avg_value = df[calc_name].mean()
                total_value = df[calc_name].sum()
                
                st.metric(
                    f"📊 {calc_name}",
                    f"{avg_value:.2f}" if not np.isnan(avg_value) else "N/A",
                    delta=f"Total: {total_value:.2f}" if not np.isnan(total_value) else "N/A"
                )
                
                # Mostrar fórmula
                if calc_info['type'] == 'basic':
                    formula = f"{calc_info['col1']} {calc_info['operation']} {calc_info['col2']}"
                    st.caption(f"Fórmula: {formula}")

def display_export_section(df, filters_applied, metrics):
    """Mostrar sección de exportación"""
    st.subheader("📤 Exportar Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Descargar Datos Filtrados (Excel)", type="primary"):
            excel_buffer = export_data(df, filters_applied, metrics)
            st.download_button(
                label="💾 Descargar Archivo Excel",
                data=excel_buffer,
                file_name=f"analisis_datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        csv_data = get_csv_data(df)
        st.download_button(
            label="📄 Descargar como CSV",
            data=csv_data,
            file_name=f"datos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col3:
        # Crear reporte de resumen
        summary_text = create_summary_report(df, filters_applied, metrics)
        st.download_button(
            label="📋 Descargar Reporte Resumen",
            data=summary_text,
            file_name=f"reporte_resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        ) 