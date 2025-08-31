import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Nivel 3: Métricas - KPIs y Análisis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .level-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .step-box {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-demo {
        background: #e8f5e8;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .completion-checkbox {
        background: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_level_progress():
    """Get current progress across all levels"""
    progress = {
        'nivel1': st.session_state.get('nivel1_completed', False),
        'nivel2': st.session_state.get('nivel2_completed', False),
        'nivel3': st.session_state.get('nivel3_completed', False),
        'nivel4': st.session_state.get('nivel4_completed', False)
    }
    
    completed_count = sum(progress.values())
    total_progress = (completed_count / 4) * 100
    
    return total_progress, completed_count, progress

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_records = len(dates)
    
    data = {
        'Fecha': np.random.choice(dates, n_records//2),
        'Categoria': np.random.choice(['Electronica', 'Ropa', 'Libros', 'Hogar', 'Deportes'], n_records//2),
        'Region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Central'], n_records//2),
        'Ventas': np.random.normal(1000, 300, n_records//2).round(2),
        'Cantidad': np.random.poisson(5, n_records//2),
        'Calificacion': np.random.choice([1, 2, 3, 4, 5], n_records//2, p=[0.05, 0.1, 0.15, 0.4, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Ingresos'] = df['Ventas'] * df['Cantidad']
    df['Margen_Ganancia'] = np.random.uniform(0.1, 0.4, len(df))
    df['Ganancia'] = df['Ingresos'] * df['Margen_Ganancia']
    
    return df.sort_values('Fecha').reset_index(drop=True)

def calculate_basic_metrics(df):
    """Calculate basic business metrics"""
    metrics = {
        'total_ingresos': df['Ingresos'].sum(),
        'total_ventas': df['Ventas'].sum(),
        'total_cantidad': df['Cantidad'].sum(),
        'total_ganancia': df['Ganancia'].sum(),
        'promedio_ingresos': df['Ingresos'].mean(),
        'promedio_ventas': df['Ventas'].mean(),
        'promedio_calificacion': df['Calificacion'].mean(),
        'total_transacciones': len(df),
        'margen_ganancia': (df['Ganancia'].sum() / df['Ingresos'].sum() * 100) if df['Ingresos'].sum() > 0 else 0
    }
    return metrics

def main():
    # Header
    st.markdown('<h1 class="level-header">📊 Nivel 3: Números Importantes</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Entender los Números Clave de tu Negocio</h2>', unsafe_allow_html=True)
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso: {total_progress:.0f}% - {completed_count} de 4 niveles completados")
        
        # Show completion status for each level
        st.markdown("**Estado de Niveles:**")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            status = "✅" if progress['nivel1'] else "⏳"
            st.markdown(f"{status} Nivel 1")
        with col_b:
            status = "✅" if progress['nivel2'] else "⏳"
            st.markdown(f"{status} Nivel 2")
        with col_c:
            status = "✅" if progress['nivel3'] else "⏳"
            st.markdown(f"{status} Nivel 3")
        with col_d:
            status = "✅" if progress['nivel4'] else "⏳"
            st.markdown(f"{status} Nivel 4")
    
    # Level Completion Checkbox - At the top
    st.markdown('<div class="completion-checkbox">', unsafe_allow_html=True)
    st.markdown("## 🎯 Marcar Nivel como Completado")
    
    # Check if this is the first time completing the level
    was_completed = st.session_state.get('nivel3_completed', False)
    
    if st.checkbox("✅ Click aquí para marcar este nivel como Completado", 
                  value=was_completed,
                  key='nivel3_completion_checkbox'):
        # Only show balloons if this is the first time completing
        if not was_completed:
            st.balloons()
            st.success("🎉 ¡Felicidades! Has completado el Nivel 3. ¡Ya entiendes los números importantes!")
        st.session_state['nivel3_completed'] = True
    else:
        st.session_state['nivel3_completed'] = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Introduction
    st.markdown("""
    ## 🎯 Objetivo de este Nivel
    
    En este nivel aprenderás a:
    - Entender qué son los números importantes (métricas y KPIs)
    - Interpretar números clave de tu negocio (ventas, ganancias, etc.)
    - Analizar tendencias y patrones en tus datos
    - Usar estos números para tomar mejores decisiones
    - Crear resúmenes visuales de tu información
    """)
    
    # Load sample data
    df = create_sample_data()
    
    # Step 1: Understanding Metrics
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📈 Paso 1: ¿Qué son las Métricas?")
    
    st.markdown("""
    ### 🎯 Definición:
    
    **Métricas** son medidas numéricas que te ayudan a:
    - **Evaluar** el rendimiento de tu negocio
    - **Comparar** diferentes períodos o segmentos
    - **Identificar** tendencias y patrones
    - **Tomar decisiones** basadas en datos
    
    ### 🔑 Tipos de Métricas:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **💰 Métricas Financieras**
        - Ingresos totales
        - Ganancia neta
        - Margen de ganancia
        - Valor promedio por transacción
        """)
        
        st.markdown("""
        **📊 Métricas Operacionales**
        - Número de transacciones
        - Cantidad vendida
        - Tasa de conversión
        - Eficiencia operativa
        """)
    
    with col2:
        st.markdown("""
        **⭐ Métricas de Satisfacción**
        - Calificación promedio
        - NPS (Net Promoter Score)
        - Tasa de retención
        - Satisfacción del cliente
        """)
        
        st.markdown("""
        **📈 Métricas de Crecimiento**
        - Crecimiento mes a mes
        - Crecimiento año a año
        - Tasa de expansión
        - Adquisición de clientes
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Key Business Metrics
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 💰 Paso 2: Métricas Clave de Negocio")
    
    st.markdown("""
    ### 🎯 Las 5 Métricas Más Importantes:
    """)
    
    # Calculate and display metrics
    metrics = calculate_basic_metrics(df)
    
    # Display metrics in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>💰 Ingresos</h3>
            <h2>${metrics['total_ingresos']:,.0f}</h2>
            <p>Total de ventas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>📈 Transacciones</h3>
            <h2>{metrics['total_transacciones']:,}</h2>
            <p>Número de ventas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>💵 Ganancia</h3>
            <h2>${metrics['total_ganancia']:,.0f}</h2>
            <p>Beneficio neto</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>📊 Margen</h3>
            <h2>{metrics['margen_ganancia']:.1f}%</h2>
            <p>Porcentaje de ganancia</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>⭐ Calificación</h3>
            <h2>{metrics['promedio_calificacion']:.1f}/5</h2>
            <p>Satisfacción promedio</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Interactive Metrics Demo
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎮 Paso 3: Demostración Interactiva")
    
    st.markdown("""
    ### 📊 Explora las Métricas:
    
    Usa los filtros para ver cómo cambian las métricas:
    """)
    
    # Interactive filters for metrics demo
    st.markdown('<div class="metric-demo">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date filter
        date_range = st.date_input(
            "📅 Rango de fechas:",
            value=(df['Fecha'].min(), df['Fecha'].max()),
            min_value=df['Fecha'].min(),
            max_value=df['Fecha'].max()
        )
        
        # Category filter
        categories = st.multiselect(
            "🏷️ Categorías:",
            options=df['Categoria'].unique(),
            default=df['Categoria'].unique()
        )
    
    with col2:
        # Region filter
        regions = st.multiselect(
            "🌍 Regiones:",
            options=df['Region'].unique(),
            default=df['Region'].unique()
        )
        
        # Rating filter
        rating_range = st.slider(
            "⭐ Rango de calificación:",
            min_value=int(df['Calificacion'].min()),
            max_value=int(df['Calificacion'].max()),
            value=(int(df['Calificacion'].min()), int(df['Calificacion'].max())),
            step=1
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Fecha'] >= pd.to_datetime(date_range[0])) & 
            (filtered_df['Fecha'] <= pd.to_datetime(date_range[1]))
        ]
    
    if categories:
        filtered_df = filtered_df[filtered_df['Categoria'].isin(categories)]
    
    if regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    
    filtered_df = filtered_df[
        (filtered_df['Calificacion'] >= rating_range[0]) & 
        (filtered_df['Calificacion'] <= rating_range[1])
    ]
    
    # Calculate filtered metrics
    filtered_metrics = calculate_basic_metrics(filtered_df)
    
    # Show comparison
    st.markdown("### 📊 Comparación de Métricas:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💰 Ingresos",
            f"${filtered_metrics['total_ingresos']:,.0f}",
            delta=f"{((filtered_metrics['total_ingresos'] - metrics['total_ingresos']) / metrics['total_ingresos'] * 100):.1f}%"
        )
        
        st.metric(
            "📈 Transacciones",
            f"{filtered_metrics['total_transacciones']:,}",
            delta=f"{((filtered_metrics['total_transacciones'] - metrics['total_transacciones']) / metrics['total_transacciones'] * 100):.1f}%"
        )
    
    with col2:
        st.metric(
            "💵 Ganancia",
            f"${filtered_metrics['total_ganancia']:,.0f}",
            delta=f"{((filtered_metrics['total_ganancia'] - metrics['total_ganancia']) / metrics['total_ganancia'] * 100):.1f}%"
        )
        
        st.metric(
            "📊 Margen",
            f"{filtered_metrics['margen_ganancia']:.1f}%",
            delta=f"{filtered_metrics['margen_ganancia'] - metrics['margen_ganancia']:.1f}%"
        )
    
    with col3:
        st.metric(
            "⭐ Calificación",
            f"{filtered_metrics['promedio_calificacion']:.1f}/5",
            delta=f"{filtered_metrics['promedio_calificacion'] - metrics['promedio_calificacion']:.1f}"
        )
        
        st.metric(
            "📊 Datos Filtrados",
            f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):,}"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Metrics Analysis
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🔍 Paso 4: Análisis de Métricas")
    
    st.markdown("""
    ### 📈 Interpretando las Métricas:
    """)
    
    # Show detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Análisis por Categoría:")
        cat_analysis = df.groupby('Categoria').agg({
            'Ingresos': 'sum',
            'Ganancia': 'sum',
            'Calificacion': 'mean',
            'Cantidad': 'sum'
        }).round(2)
        
        # Calculate margin for each category
        cat_analysis['Margen_%'] = (cat_analysis['Ganancia'] / cat_analysis['Ingresos'] * 100).round(1)
        
        st.dataframe(cat_analysis, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Análisis por Región:")
        region_analysis = df.groupby('Region').agg({
            'Ingresos': 'sum',
            'Ganancia': 'sum',
            'Calificacion': 'mean',
            'Cantidad': 'sum'
        }).round(2)
        
        # Calculate margin for each region
        region_analysis['Margen_%'] = (region_analysis['Ganancia'] / region_analysis['Ingresos'] * 100).round(1)
        
        st.dataframe(region_analysis, use_container_width=True)
    
    # Insights section
    st.markdown("#### 💡 Insights Clave:")
    
    # Find best performing category and region
    best_category = cat_analysis['Ingresos'].idxmax()
    best_region = region_analysis['Ingresos'].idxmax()
    best_rating_category = cat_analysis['Calificacion'].idxmax()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success(f"🥇 **Mejor Categoría**: {best_category}")
        st.caption(f"Ingresos: ${cat_analysis.loc[best_category, 'Ingresos']:,.0f}")
    
    with col2:
        st.success(f"🌍 **Mejor Región**: {best_region}")
        st.caption(f"Ingresos: ${region_analysis.loc[best_region, 'Ingresos']:,.0f}")
    
    with col3:
        st.success(f"⭐ **Mejor Calificación**: {best_rating_category}")
        st.caption(f"Calificación: {cat_analysis.loc[best_rating_category, 'Calificacion']:.1f}/5")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 5: Practice Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎯 Paso 5: Práctica - ¡Tu Turno!")
    
    st.markdown("""
    ### 📝 Ejercicio Práctico:
    
    **Objetivo**: Analizar las métricas de tu negocio
    
    **Pasos**:
    1. Carga tu archivo de datos
    2. Observa las métricas principales
    3. Aplica filtros y ve cómo cambian
    4. Identifica insights clave
    5. Compara diferentes segmentos
    """)
    
    # File upload for practice
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo para practicar:",
        type=['csv', 'xlsx', 'xls'],
        help="Sube tu archivo para analizar tus propias métricas"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                practice_df = pd.read_csv(uploaded_file)
            else:
                practice_df = pd.read_excel(uploaded_file)
            
            # Try to convert date columns
            for col in practice_df.columns:
                if 'fecha' in col.lower() or 'date' in col.lower():
                    try:
                        practice_df[col] = pd.to_datetime(practice_df[col])
                    except:
                        pass
            
            st.success(f"✅ Archivo cargado: {len(practice_df)} filas")
            
            # Show basic info about the data
            st.markdown("### 📊 Información de tus Datos:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 Total de Filas", len(practice_df))
                st.metric("📋 Total de Columnas", len(practice_df.columns))
            
            with col2:
                numeric_cols = practice_df.select_dtypes(include=[np.number]).columns
                st.metric("🔢 Columnas Numéricas", len(numeric_cols))
                st.metric("📅 Columnas de Fecha", len(practice_df.select_dtypes(include=['datetime64']).columns))
            
            with col3:
                if len(numeric_cols) > 0:
                    total_numeric = practice_df[numeric_cols].sum().sum()
                    st.metric("💰 Suma Total Numérica", f"{total_numeric:,.0f}")
                
                object_cols = practice_df.select_dtypes(include=['object']).columns
                st.metric("🏷️ Columnas de Texto", len(object_cols))
            
            # Show sample data
            st.markdown("### 📋 Vista Previa:")
            st.dataframe(practice_df.head(10), use_container_width=True)
            
            # Show column types
            st.markdown("### 📋 Tipos de Columnas:")
            column_info = pd.DataFrame({
                'Columna': practice_df.columns,
                'Tipo': practice_df.dtypes.astype(str),
                'Valores Únicos': [practice_df[col].nunique() for col in practice_df.columns],
                'Valores Vacíos': [practice_df[col].isnull().sum() for col in practice_df.columns]
            })
            st.dataframe(column_info, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")
            st.info("📊 Usando datos de ejemplo para la práctica")
    else:
        st.info("📤 Sube un archivo para comenzar la práctica")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Criteria
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("## ✅ Criterios de Éxito")
    
    st.markdown("""
    Has completado este nivel cuando:
    - ✅ Entiendes qué son las métricas y KPIs
    - ✅ Puedes interpretar métricas básicas de negocio
    - ✅ Sabes cómo los filtros afectan las métricas
    - ✅ Puedes identificar insights clave
    - ✅ Entiendes la importancia del análisis de datos
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Official Sources Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🏛️ Fuentes Oficiales")
    
    st.markdown("""
    ### 📚 Respaldos Oficiales para este Nivel:
    
    **Framework de Métricas Empresariales:**
    - **Balanced Scorecard Institute**: [Framework de métricas empresariales](https://balancedscorecard.org/)
    
    **Métricas de Analytics:**
    - **Google Analytics Academy**: [Métricas web y de negocio](https://analytics.google.com/analytics/academy/)
    
    **Visualización de Métricas:**
    - **Tableau Training**: [Creación de dashboards](https://www.tableau.com/learn/training)
    
    **Power BI Métricas:**
    - **Microsoft Power BI Learning Path**: [Métricas empresariales](https://docs.microsoft.com/en-us/learn/powerplatform/power-bi)
    
    ### 📖 Certificaciones Relacionadas:
    - **Google Analytics Individual Qualification (GAIQ)**: [Certificación de Google Analytics](https://analytics.google.com/analytics/academy/)
    - **Tableau Desktop Specialist**: [Certificación de Tableau](https://www.tableau.com/learn/certification)
    - **Microsoft Power BI Data Analyst**: [Certificación de Microsoft](https://docs.microsoft.com/en-us/certifications/power-bi-data-analyst-associate/)
    
    ### 🔗 Recursos Adicionales:
    - **Google Data Studio**: [Visualización gratuita](https://datastudio.google.com/)
    - **Tableau Public**: [Análisis avanzado](https://public.tableau.com/)
    - **Power BI**: [Integración empresarial](https://powerbi.microsoft.com/)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Dashboard Principal", key="nivel3_dashboard"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("⬅️ Nivel Anterior", key="nivel3_anterior"):
            st.switch_page("pages/02_Nivel_2_Filtros.py")
    
    with col4:
        if st.button("➡️ Siguiente Nivel", key="nivel3_siguiente"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    # Tips section
    st.markdown("""
    ---
    ### 💡 Consejos para Métricas:
    - **Contexto**: Siempre considera el contexto al interpretar métricas
    - **Comparación**: Compara métricas con períodos anteriores o benchmarks
    - **Tendencias**: Observa tendencias a lo largo del tiempo
    - **Segmentación**: Analiza métricas por diferentes segmentos
    - **Acción**: Usa las métricas para tomar decisiones informadas
    """)

if __name__ == "__main__":
    main()
