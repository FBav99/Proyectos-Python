import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Importar módulos personalizados
from config import setup_page_config, apply_custom_css
from data_loader import get_data
from metrics import calculate_metrics, calculate_growth_metrics, calculate_performance_insights
from visualizations import (
    create_time_series_chart, 
    create_category_analysis, 
    create_regional_analysis,
    create_correlation_matrix,
    create_custom_calculation_charts
)
from calculations import apply_custom_calculations
from filters import apply_all_filters
from ui_components import (
    create_sidebar_controls,
    create_custom_calculations_ui,
    display_metrics_dashboard,
    display_custom_calculations_metrics,
    display_export_section
)

def main():
    """Función principal de la aplicación"""
    # Configurar página
    setup_page_config()
    apply_custom_css()
    
    # Título principal
    st.markdown('<h1 class="main-header">📊 Panel de Análisis de Datos - Dashboard Principal</h1>', unsafe_allow_html=True)
    
    # Learning levels navigation with improved design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem; font-size: 1.5rem;">🎓 Sistema de Aprendizaje por Niveles</h2>
        <p style="color: white; text-align: center; margin-bottom: 1.5rem; font-size: 1.1rem;">
            ¿Eres nuevo en análisis de datos? Completa nuestros niveles paso a paso para dominar todas las funcionalidades
        </p>
    """, unsafe_allow_html=True)
    
    # Navigation buttons inside the card
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📚 Nivel 1: Básico", type="primary", use_container_width=True):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col2:
        if st.button("🔍 Nivel 2: Filtros", use_container_width=True):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col3:
        if st.button("📊 Nivel 3: Métricas", use_container_width=True):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col4:
        if st.button("🚀 Nivel 4: Avanzado", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col5:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;">
                💡 <strong>Consejo:</strong> Si ya completaste los niveles, ¡este es tu dashboard principal para análisis avanzado!
            </p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0.5rem 0 0 0;">
                📖 <strong>Ayuda:</strong> Información detallada, guías paso a paso y solución de problemas
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard description for advanced users
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745; margin-bottom: 2rem;">
        <h3 style="color: #28a745; margin-bottom: 0.5rem;">🎯 Dashboard Principal - Funcionalidades Avanzadas</h3>
        <p style="margin-bottom: 0.5rem;"><strong>Este dashboard incluye:</strong></p>
        <ul style="margin-bottom: 0;">
            <li>📊 <strong>Análisis completo de métricas y KPIs</strong></li>
            <li>🔍 <strong>Filtros avanzados y cálculos personalizados</strong></li>
            <li>📈 <strong>Visualizaciones interactivas y análisis de tendencias</strong></li>
            <li>📋 <strong>Exportación de datos y reportes</strong></li>
            <li>🎯 <strong>Perspectivas avanzadas y análisis de rendimiento</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear controles de la barra lateral
    uploaded_file = create_sidebar_controls()
    
    # Cargar datos
    df = get_data(uploaded_file)
    
    # Vista previa de datos
    st.subheader("📋 Vista Previa de Datos")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Almacenar df original para referencia
    original_df = df.copy()
    
    # Aplicar filtros
    st.sidebar.subheader("🎛️ Filtros")
    df, filters_applied = apply_all_filters(df, original_df)
    
    # Crear interfaz para cálculos personalizados
    custom_calculations = create_custom_calculations_ui(df)
    
    # Aplicar cálculos personalizados
    if custom_calculations:
        calc_filters = apply_custom_calculations(df, custom_calculations)
        filters_applied.update(calc_filters)
    
    # Mostrar información de datos filtrados
    if len(filters_applied) > 0:
        st.info(f"📊 Mostrando {len(df):,} filas después de aplicar filtros (originalmente {len(original_df):,} filas)")
    
    # Calcular y mostrar métricas
    if len(df) > 0:
        metrics = calculate_metrics(df)
        display_metrics_dashboard(metrics, df)
        
        # Sección de Gráficos
        st.subheader("📊 Análisis Visual")
        
        # Series temporales
        if 'Date' in df.columns:
            st.plotly_chart(create_time_series_chart(df, 'Revenue'), use_container_width=True)
        
        # Análisis por Categoría y Regional
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Category' in df.columns:
                st.plotly_chart(create_category_analysis(df), use_container_width=True)
        
        with col2:
            if 'Region' in df.columns:
                st.plotly_chart(create_regional_analysis(df), use_container_width=True)
        
        # Visualización de Cálculos Personalizados
        if custom_calculations:
            display_custom_calculations_metrics(df, custom_calculations)
            
            # Gráficos de cálculos personalizados
            st.subheader("📈 Tendencias de Cálculos Personalizados")
            
            # Crear gráficos para cálculos personalizados a lo largo del tiempo
            if 'Date' in df.columns:
                custom_charts = create_custom_calculation_charts(df, custom_calculations)
                for chart in custom_charts:
                    st.plotly_chart(chart, use_container_width=True)
            
            # Análisis de correlación para cálculos personalizados
            custom_calc_names = [calc['name'] for calc in custom_calculations if calc['name'] in df.columns]
            if len(custom_calc_names) >= 2:
                st.subheader("🔗 Correlación de Cálculos Personalizados")
                
                corr_fig = create_correlation_matrix(df, custom_calc_names)
                if corr_fig:
                    st.plotly_chart(corr_fig, use_container_width=True)
        
        # Análisis Avanzado
        st.subheader("🔍 Perspectivas Avanzadas")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("### 📈 Análisis de Crecimiento")
            growth_metrics = calculate_growth_metrics(df)
            if growth_metrics:
                st.metric("Crecimiento Mes a Mes", f"{growth_metrics['mom_growth']:.1f}%")
                st.success(f"🏆 Mejor día: {growth_metrics['best_day'].strftime('%Y-%m-%d')} (${growth_metrics['best_day_revenue']:,.2f})")
        
        with insight_col2:
            st.markdown("### 🎯 Perspectivas de Rendimiento")
            
            performance_insights = calculate_performance_insights(df)
            if 'top_category' in performance_insights:
                st.success(f"🥇 Mejor Categoría: {performance_insights['top_category']}")
            
            if 'top_region' in performance_insights:
                st.success(f"📍 Mejor Región: {performance_insights['top_region']}")
            
            if 'high_rated_percentage' in performance_insights:
                st.info(f"😊 {performance_insights['high_rated_percentage']:.1f}% clientes califican 4+ estrellas")
        
        # Funcionalidad de exportación
        display_export_section(df, filters_applied, metrics)
    
    else:
        st.warning("⚠️ Ningún dato coincide con tus filtros actuales. Por favor ajusta la configuración de filtros.")
    
    # Pie de página con enlaces a niveles
    st.markdown("---")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center;">
        <p style="margin-bottom: 0.5rem;"><strong>💡 ¿Necesitas ayuda?</strong></p>
        <p style="margin-bottom: 1rem;">Si no estás familiarizado con estas funcionalidades, te recomendamos completar nuestros niveles de aprendizaje primero.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📚 Nivel 1", use_container_width=True):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col2:
        if st.button("🔍 Nivel 2", use_container_width=True):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col3:
        if st.button("📊 Nivel 3", use_container_width=True):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col4:
        if st.button("🚀 Nivel 4", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col5:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

if __name__ == "__main__":
    main() 