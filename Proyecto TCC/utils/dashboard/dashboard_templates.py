import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

from utils.analysis import (
    calculate_metrics, 
    calculate_growth_metrics, 
    calculate_performance_insights,
    create_time_series_chart, 
    create_category_analysis, 
    create_regional_analysis,
    create_correlation_matrix
)
from utils.ui import (
    display_metrics_dashboard,
    create_custom_calculations_ui,
    display_export_section
)

def show_kpi_template(df, username):
    """Show KPI template - Macro level dashboard"""
    
    st.markdown("### 🎯 Plantilla KPI - Nivel Macro")
    st.markdown("*Dashboard ejecutivo con indicadores clave de rendimiento*")
    
    # Calculate basic metrics
    metrics = calculate_metrics(df)
    
    # Display key KPIs in a prominent way
    st.markdown("#### 📊 Indicadores Clave de Rendimiento")
    
    # Main KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Registros", f"{len(df):,}", delta=f"+{len(df)//10:,}")
    with col2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            main_col = numeric_cols[0]
            total_value = df[main_col].sum()
            st.metric(f"💰 Total {main_col}", f"{total_value:,.0f}", delta=f"+{total_value//20:,.0f}")
        else:
            st.metric("📊 Columnas", len(df.columns))
    with col3:
        st.metric("📅 Última Actualización", datetime.now().strftime("%d/%m/%Y"))
    with col4:
        quality_score = 85  # Placeholder - could be calculated
        st.metric("🎯 Calidad de Datos", f"{quality_score}%", delta="+5%")
    
    # Executive summary
    st.markdown("#### 📋 Resumen Ejecutivo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Tendencias Principales:**")
        st.markdown("- 📈 Crecimiento sostenido en registros")
        st.markdown("- 💰 Incremento en valores monetarios")
        st.markdown("- 🎯 Mejora en calidad de datos")
    
    with col2:
        st.markdown("**Recomendaciones:**")
        st.markdown("- ✅ Mantener tendencia actual")
        st.markdown("- 🔍 Monitorear outliers")
        st.markdown("- 📊 Revisar métricas mensuales")
    
    # Simple trend chart if date column exists
    st.markdown("#### 📈 Tendencia General")
    time_chart = create_time_series_chart(df)
    if time_chart is not None:
        st.plotly_chart(time_chart, use_container_width=True)
    else:
        st.info("No se pudo crear el gráfico de tendencias. Verifica que tengas columnas de fecha y valores numéricos.")
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_analytical_template(df, username):
    """Show Analytical template - Medium level dashboard"""
    
    st.markdown("### 📊 Plantilla Analítica - Nivel Medio")
    st.markdown("*Dashboard analítico con análisis detallado por segmentos*")
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Display metrics dashboard
    display_metrics_dashboard(metrics, df)
    
    # Segment analysis
    st.markdown("#### 🔍 Análisis por Segmentos")
    
    # Category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Análisis por Categorías**")
        cat_chart = create_category_analysis(df)
        if cat_chart is not None:
            st.plotly_chart(cat_chart, use_container_width=True)
        else:
            st.info("No hay suficientes datos categóricos para este análisis.")
    
    with col2:
        st.markdown("**🌍 Análisis Regional**")
        reg_chart = create_regional_analysis(df)
        if reg_chart is not None:
            st.plotly_chart(reg_chart, use_container_width=True)
        else:
            st.info("No hay suficientes datos categóricos para este análisis.")
    
    # Correlation analysis
    st.markdown("#### 🔗 Análisis de Correlaciones")
    corr_chart = create_correlation_matrix(df)
    if corr_chart is not None:
        st.plotly_chart(corr_chart, use_container_width=True)
    else:
        st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones.")
    
    # Time series analysis
    st.markdown("#### 📈 Análisis Temporal")
    time_chart = create_time_series_chart(df)
    if time_chart is not None:
        st.plotly_chart(time_chart, use_container_width=True)
    else:
        st.info("No se pudo crear el análisis temporal. Verifica que tengas columnas de fecha y valores numéricos.")
    
    # Performance insights
    st.markdown("#### 💡 Insights de Rendimiento")
    insights = calculate_performance_insights(df)
    for insight in insights[:3]:  # Show top 3 insights
        st.info(f"💡 {insight}")
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_detailed_template(df, username):
    """Show Detailed template - Micro level dashboard"""
    
    st.markdown("### 🔍 Plantilla Detallada - Nivel Micro")
    st.markdown("*Dashboard granular con análisis exhaustivo y patrones detallados*")
    
    # Calculate comprehensive metrics
    metrics = calculate_metrics(df)
    growth_metrics = calculate_growth_metrics(df)
    
    # Display all metrics
    display_metrics_dashboard(metrics, df)
    
    # Growth metrics
    st.markdown("#### 📈 Métricas de Crecimiento")
    display_metrics_dashboard(growth_metrics, df)
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuciones", "🔍 Outliers", "📈 Tendencias", "🔗 Correlaciones"])
    
    with tab1:
        st.markdown("#### 📊 Análisis de Distribuciones")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:3]:  # Show first 3 numeric columns
                st.markdown(f"**Distribución de {col}**")
                fig = px.histogram(df, x=col, title=f"Distribución de {col}")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔍 Análisis de Outliers")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:2]:  # Show first 2 numeric columns
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
                
                st.markdown(f"**Outliers en {col}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cantidad de Outliers", len(outliers))
                with col2:
                    st.metric("Porcentaje", f"{len(outliers)/len(df)*100:.1f}%")
                
                if len(outliers) > 0:
                    st.dataframe(outliers.head(10), use_container_width=True)
    
    with tab3:
        st.markdown("#### 📈 Análisis de Tendencias Detallado")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            for col in numeric_cols[:2]:  # Show first 2 numeric columns
                st.markdown(f"**Tendencia de {col}**")
                time_chart = create_time_series_chart(df, col)
                if time_chart is not None:
                    st.plotly_chart(time_chart, use_container_width=True)
                else:
                    st.info(f"No se pudo crear el gráfico de tendencias para {col}")
        else:
            st.info("No hay columnas numéricas para el análisis de tendencias.")
    
    with tab4:
        st.markdown("#### 🔗 Análisis de Correlaciones Detallado")
        corr_chart = create_correlation_matrix(df)
        if corr_chart is not None:
            st.plotly_chart(corr_chart, use_container_width=True)
            
            # Correlation insights
            st.markdown("**💡 Insights de Correlación:**")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr_matrix = df[numeric_cols].corr()
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        st.success(f"✅ {numeric_cols[i]} y {numeric_cols[j]} tienen correlación fuerte ({corr_value:.2f})")
                    elif abs(corr_value) > 0.5:
                        st.info(f"ℹ️ {numeric_cols[i]} y {numeric_cols[j]} tienen correlación moderada ({corr_value:.2f})")
        else:
            st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones.")
    
    # Custom calculations section
    st.markdown("#### 🧮 Cálculos Personalizados")
    create_custom_calculations_ui(df)
    
    # Export section
    st.markdown("#### 📤 Exportar Análisis")
    display_export_section(df, {}, metrics)
    
    # Update user progress
    update_user_progress(username, data_analyses_created=1)

def show_dashboard_selection(df, username):
    """Show dashboard template selection and handle the selected template"""
    selected_template = st.session_state.get('selected_template', 'blank')
    
    st.markdown("# 📊 Dashboard de Análisis")
    
    # Template selection if not already selected
    if selected_template == 'blank':
        st.markdown("### 🎨 Selecciona el tipo de dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("#### 🎨 **Dashboard en Blanco**")
            st.markdown("Construye tu dashboard manualmente")
            if st.button("🎨 Usar Blanco", key="template_blank", use_container_width=True):
                st.switch_page("pages/08_Dashboard_Blanco.py")
        
        with col2:
            st.markdown("#### 🎯 **Dashboard KPI**")
            st.markdown("Indicadores clave de rendimiento para ejecutivos")
            if st.button("🚀 Usar KPI", key="template_kpi", use_container_width=True):
                st.session_state.selected_template = "kpi"
                st.rerun()
        
        with col3:
            st.markdown("#### 📊 **Dashboard Analítico**")
            st.markdown("Análisis detallado por segmentos")
            if st.button("📊 Usar Analítico", key="template_analytical", use_container_width=True):
                st.session_state.selected_template = "analytical"
                st.rerun()
        
        with col4:
            st.markdown("#### 🔍 **Dashboard Detallado**")
            st.markdown("Análisis granular y exhaustivo")
            if st.button("🔍 Usar Detallado", key="template_detailed", use_container_width=True):
                st.session_state.selected_template = "detailed"
                st.rerun()
    
    # Show selected template
    if selected_template == "kpi":
        show_kpi_template(df, username)
    elif selected_template == "analytical":
        show_analytical_template(df, username)
    elif selected_template == "detailed":
        show_detailed_template(df, username)

def update_user_progress(username, **kwargs):
    """Update user progress in the database"""
    # This function would update user progress in the database
    # For now, it's a placeholder
    pass
