import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Nivel 4: Avanzado - Cálculos y Visualizaciones",
    page_icon="🚀",
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
    .advanced-demo {
        background: #f3e5f5;
        border: 1px solid #e1bee7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .formula-box {
        background: #e8f5e8;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
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

def create_time_series_chart(df, metric='Ingresos'):
    """Create time series visualization"""
    daily_data = df.groupby('Fecha')[metric].sum().reset_index()
    
    fig = px.line(daily_data, x='Fecha', y=metric, 
                  title=f'{metric} a lo Largo del Tiempo',
                  template='plotly_white')
    
    fig.update_traces(line=dict(width=3, color='#1f77b4'))
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title=metric,
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_category_chart(df):
    """Create category analysis chart"""
    category_data = df.groupby('Categoria').agg({
        'Ingresos': 'sum',
        'Ganancia': 'sum',
        'Calificacion': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Ingresos por Categoría', 'Ganancia por Categoría'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Bar(x=category_data['Categoria'], 
               y=category_data['Ingresos'],
               name='Ingresos',
               marker_color='#1f77b4'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=category_data['Categoria'], 
               y=category_data['Ganancia'],
               name='Ganancia',
               marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    return fig

def main():
    # Header
    st.markdown('<h1 class="level-header">🚀 Nivel 4: Avanzado</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Cálculos Personalizados y Visualizaciones</h2>', unsafe_allow_html=True)
    
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
    was_completed = st.session_state.get('nivel4_completed', False)
    
    if st.checkbox("✅ Click aquí para marcar este nivel como Completado", 
                  value=was_completed,
                  key='nivel4_completion_checkbox'):
        # Only show balloons if this is the first time completing
        if not was_completed:
            st.balloons()
            st.success("🎉 ¡Felicidades! Has completado el Nivel 4. ¡Has terminado todos los niveles!")
        st.session_state['nivel4_completed'] = True
    else:
        st.session_state['nivel4_completed'] = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Introduction
    st.markdown("""
    ## 🎯 Objetivo de este Nivel
    
    En este nivel aprenderás a:
    - Crear cálculos personalizados avanzados
    - Generar visualizaciones interactivas
    - Analizar tendencias temporales
    - Crear dashboards completos
    - Exportar resultados y reportes
    """)
    
    # Load sample data
    df = create_sample_data()
    
    # Step 1: Custom Calculations
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🧮 Paso 1: Cálculos Personalizados")
    
    st.markdown("""
    ### 🎯 ¿Qué son los Cálculos Personalizados?
    
    Los cálculos personalizados te permiten:
    - **Crear nuevas métricas** basadas en tus datos existentes
    - **Realizar análisis específicos** para tu negocio
    - **Comparar diferentes indicadores** de rendimiento
    - **Identificar patrones** que no son evidentes a simple vista
    """)
    
    st.markdown("### 🔧 Tipos de Cálculos Disponibles:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔢 Matemáticas Básicas**
        - Suma, resta, multiplicación
        - División y porcentajes
        - Potencias y raíces
        - Operaciones combinadas
        """)
    
    with col2:
        st.markdown("""
        **📅 Análisis Temporal**
        - Crecimiento mes a mes
        - Comparación año anterior
        - Promedios móviles
        - Acumulados
        """)
    
    with col3:
        st.markdown("""
        **📊 Agregaciones**
        - Totales por grupo
        - Promedios por categoría
        - Máximos y mínimos
        - Desviaciones estándar
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Interactive Custom Calculations
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎮 Paso 2: Demostración de Cálculos")
    
    st.markdown("""
    ### 📊 Explora Cálculos Personalizados:
    """)
    
    st.markdown('<div class="advanced-demo">', unsafe_allow_html=True)
    
    # Calculation type selector
    calc_type = st.selectbox(
        "🔧 Tipo de Cálculo:",
        ["Matemáticas Básicas", "Análisis Temporal", "Agregaciones"]
    )
    
    if calc_type == "Matemáticas Básicas":
        st.markdown("#### 🔢 Cálculos Matemáticos:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic math operations
            operation = st.selectbox(
                "Operación:",
                ["Sumar (+)", "Restar (-)", "Multiplicar (×)", "Dividir (÷)", "Porcentaje (%)"]
            )
            
            col1_calc = st.selectbox("Columna 1:", options=['Ingresos', 'Ventas', 'Cantidad', 'Ganancia'])
            col2_calc = st.selectbox("Columna 2:", options=['Ventas', 'Cantidad', 'Ingresos', 'Ganancia'])
        
        with col2:
            calc_name = st.text_input("Nombre del cálculo:", value="Calculo_Personalizado")
            
            # Apply calculation
            if st.button("🧮 Aplicar Cálculo"):
                if operation == "Sumar (+)":
                    df[calc_name] = df[col1_calc] + df[col2_calc]
                elif operation == "Restar (-)":
                    df[calc_name] = df[col1_calc] - df[col2_calc]
                elif operation == "Multiplicar (×)":
                    df[calc_name] = df[col1_calc] * df[col2_calc]
                elif operation == "Dividir (÷)":
                    df[calc_name] = df[col1_calc] / df[col2_calc].replace(0, np.nan)
                elif operation == "Porcentaje (%)":
                    df[calc_name] = (df[col1_calc] / df[col2_calc] * 100).replace([np.inf, -np.inf], np.nan)
                
                st.success(f"✅ Cálculo '{calc_name}' aplicado exitosamente!")
                
                # Show formula
                st.markdown('<div class="formula-box">', unsafe_allow_html=True)
                st.markdown(f"**Fórmula aplicada:** `{col1_calc} {operation.split()[1]} {col2_calc}`")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"📊 {calc_name} - Total", f"{df[calc_name].sum():,.2f}")
                with col2:
                    st.metric(f"📊 {calc_name} - Promedio", f"{df[calc_name].mean():,.2f}")
                with col3:
                    st.metric(f"📊 {calc_name} - Máximo", f"{df[calc_name].max():,.2f}")
    
    elif calc_type == "Análisis Temporal":
        st.markdown("#### 📅 Análisis Temporal:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_col = st.selectbox("Columna objetivo:", options=['Ingresos', 'Ventas', 'Cantidad', 'Ganancia'])
            
            time_operation = st.selectbox(
                "Operación temporal:",
                ["Promedio Móvil 7 días", "Promedio Móvil 30 días", "Suma Acumulada", "Crecimiento Diario"]
            )
        
        with col2:
            calc_name = st.text_input("Nombre del cálculo:", value=f"{target_col}_Temporal")
            
            if st.button("📅 Aplicar Análisis Temporal"):
                df_sorted = df.sort_values('Fecha')
                
                if time_operation == "Promedio Móvil 7 días":
                    df[calc_name] = df_sorted.set_index('Fecha')[target_col].rolling('7D').mean().values
                elif time_operation == "Promedio Móvil 30 días":
                    df[calc_name] = df_sorted.set_index('Fecha')[target_col].rolling('30D').mean().values
                elif time_operation == "Suma Acumulada":
                    df[calc_name] = df_sorted[target_col].cumsum().values
                elif time_operation == "Crecimiento Diario":
                    df[calc_name] = df_sorted[target_col].pct_change() * 100
                
                st.success(f"✅ Análisis temporal '{calc_name}' aplicado exitosamente!")
                
                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"📊 {calc_name} - Último valor", f"{df[calc_name].iloc[-1]:,.2f}")
                with col2:
                    st.metric(f"📊 {calc_name} - Promedio", f"{df[calc_name].mean():,.2f}")
                with col3:
                    st.metric(f"📊 {calc_name} - Máximo", f"{df[calc_name].max():,.2f}")
    
    elif calc_type == "Agregaciones":
        st.markdown("#### 📊 Agregaciones:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_col = st.selectbox("Columna objetivo:", options=['Ingresos', 'Ventas', 'Cantidad', 'Ganancia'])
            group_col = st.selectbox("Agrupar por:", options=['Categoria', 'Region'])
            
            agg_operation = st.selectbox(
                "Operación de agregación:",
                ["Suma", "Promedio", "Máximo", "Mínimo", "Contar"]
            )
        
        with col2:
            calc_name = st.text_input("Nombre del cálculo:", value=f"{target_col}_{agg_operation}_{group_col}")
            
            if st.button("📊 Aplicar Agregación"):
                if agg_operation == "Suma":
                    agg_result = df.groupby(group_col)[target_col].sum()
                elif agg_operation == "Promedio":
                    agg_result = df.groupby(group_col)[target_col].mean()
                elif agg_operation == "Máximo":
                    agg_result = df.groupby(group_col)[target_col].max()
                elif agg_operation == "Mínimo":
                    agg_result = df.groupby(group_col)[target_col].min()
                elif agg_operation == "Contar":
                    agg_result = df.groupby(group_col)[target_col].count()
                
                # Map back to original dataframe
                df[calc_name] = df[group_col].map(agg_result)
                
                st.success(f"✅ Agregación '{calc_name}' aplicada exitosamente!")
                
                # Show results
                st.markdown("#### 📋 Resultados por Grupo:")
                result_df = df.groupby(group_col)[calc_name].first().reset_index()
                st.dataframe(result_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Visualizations
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📊 Paso 3: Visualizaciones Avanzadas")
    
    st.markdown("""
    ### 🎨 Tipos de Visualizaciones:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Gráficos de Línea**
        - Tendencias temporales
        - Evolución de métricas
        - Comparación de períodos
        """)
        
        st.markdown("""
        **📊 Gráficos de Barras**
        - Comparación entre categorías
        - Análisis por regiones
        - Ranking de elementos
        """)
    
    with col2:
        st.markdown("""
        **🔄 Gráficos de Dispersión**
        - Correlaciones entre variables
        - Identificación de outliers
        - Análisis de patrones
        """)
        
        st.markdown("""
        **📋 Tablas Interactivas**
        - Resúmenes detallados
        - Filtros dinámicos
        - Exportación de datos
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Interactive Visualizations
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎮 Paso 4: Demostración de Visualizaciones")
    
    st.markdown('<div class="advanced-demo">', unsafe_allow_html=True)
    
    # Visualization selector
    viz_type = st.selectbox(
        "📊 Tipo de Visualización:",
        ["Series Temporales", "Análisis por Categoría", "Comparación de Métricas"]
    )
    
    if viz_type == "Series Temporales":
        st.markdown("#### 📈 Series Temporales:")
        
        metric_viz = st.selectbox("Métrica a visualizar:", options=['Ingresos', 'Ventas', 'Cantidad', 'Ganancia'])
        
        # Create time series chart
        fig = create_time_series_chart(df, metric_viz)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights
        st.markdown("#### 💡 Insights de la Tendencias:")
        
        # Calculate trend
        daily_data = df.groupby('Fecha')[metric_viz].sum()
        if len(daily_data) > 1:
            trend = (daily_data.iloc[-1] - daily_data.iloc[0]) / daily_data.iloc[0] * 100
            st.info(f"📈 **Tendencia general**: {trend:.1f}% de cambio desde el inicio")
        
        # Best and worst days
        best_day = daily_data.idxmax()
        worst_day = daily_data.idxmin()
        st.success(f"🏆 **Mejor día**: {best_day.strftime('%Y-%m-%d')} (${daily_data.max():,.2f})")
        st.warning(f"📉 **Peor día**: {worst_day.strftime('%Y-%m-%d')} (${daily_data.min():,.2f})")
    
    elif viz_type == "Análisis por Categoría":
        st.markdown("#### 📊 Análisis por Categoría:")
        
        # Create category chart
        fig = create_category_chart(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights
        st.markdown("#### 💡 Insights por Categoría:")
        
        category_analysis = df.groupby('Categoria').agg({
            'Ingresos': 'sum',
            'Ganancia': 'sum',
            'Calificacion': 'mean'
        }).round(2)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_cat_revenue = category_analysis['Ingresos'].idxmax()
            st.success(f"💰 **Mayor Ingreso**: {best_cat_revenue}")
        
        with col2:
            best_cat_profit = category_analysis['Ganancia'].idxmax()
            st.success(f"💵 **Mayor Ganancia**: {best_cat_profit}")
        
        with col3:
            best_cat_rating = category_analysis['Calificacion'].idxmax()
            st.success(f"⭐ **Mejor Calificación**: {best_cat_rating}")
    
    elif viz_type == "Comparación de Métricas":
        st.markdown("#### 🔄 Comparación de Métricas:")
        
        # Create correlation matrix
        numeric_cols = ['Ingresos', 'Ventas', 'Cantidad', 'Ganancia', 'Calificacion']
        corr_data = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_data,
            title="Matriz de Correlación entre Métricas",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add insights
        st.markdown("#### 💡 Insights de Correlación:")
        
        # Find strongest correlations
        corr_pairs = []
        for i in range(len(corr_data.columns)):
            for j in range(i+1, len(corr_data.columns)):
                corr_pairs.append((
                    corr_data.columns[i],
                    corr_data.columns[j],
                    corr_data.iloc[i, j]
                ))
        
        # Sort by absolute correlation
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            strongest_pos = corr_pairs[0]
            st.success(f"🔗 **Correlación más fuerte**: {strongest_pos[0]} ↔ {strongest_pos[1]} ({strongest_pos[2]:.3f})")
        
        with col2:
            if len(corr_pairs) > 1:
                strongest_neg = [p for p in corr_pairs if p[2] < 0][0] if any(p[2] < 0 for p in corr_pairs) else corr_pairs[1]
                st.warning(f"📉 **Correlación negativa**: {strongest_neg[0]} ↔ {strongest_neg[1]} ({strongest_neg[2]:.3f})")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 5: Practice Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎯 Paso 5: Práctica Final - ¡Tu Turno!")
    
    st.markdown("""
    ### 📝 Ejercicio Final:
    
    **Objetivo**: Crear un análisis completo con cálculos personalizados y visualizaciones
    
    **Pasos**:
    1. Carga tu archivo de datos
    2. Crea al menos 2 cálculos personalizados
    3. Genera visualizaciones relevantes
    4. Identifica insights clave
    5. Exporta tus resultados
    """)
    
    # File upload for practice
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo para la práctica final:",
        type=['csv', 'xlsx', 'xls'],
        help="Sube tu archivo para crear análisis avanzados"
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
            
            # Show data overview
            st.markdown("### 📊 Resumen de tus Datos:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 Total de Filas", len(practice_df))
                st.metric("📋 Total de Columnas", len(practice_df.columns))
            
            with col2:
                numeric_cols = practice_df.select_dtypes(include=[np.number]).columns
                st.metric("🔢 Columnas Numéricas", len(numeric_cols))
                st.metric("📅 Columnas de Fecha", len(practice_df.select_dtypes(include=['datetime64']).columns))
            
            with col3:
                object_cols = practice_df.select_dtypes(include=['object']).columns
                st.metric("🏷️ Columnas de Texto", len(object_cols))
                if len(numeric_cols) > 0:
                    st.metric("💰 Suma Total", f"{practice_df[numeric_cols].sum().sum():,.0f}")
            
            # Show sample data
            st.markdown("### 📋 Vista Previa:")
            st.dataframe(practice_df.head(10), use_container_width=True)
            
            # Suggestions for custom calculations
            st.markdown("### 💡 Sugerencias de Cálculos:")
            
            if len(numeric_cols) >= 2:
                st.info(f"🔢 Puedes crear cálculos entre: {', '.join(numeric_cols[:3])}")
            
            date_cols = practice_df.select_dtypes(include=['datetime64']).columns
            if len(date_cols) > 0 and len(numeric_cols) > 0:
                st.info(f"📅 Puedes crear análisis temporales usando '{date_cols[0]}' y '{numeric_cols[0]}'")
            
            if len(object_cols) > 0 and len(numeric_cols) > 0:
                st.info(f"📊 Puedes crear agregaciones agrupando por '{object_cols[0]}' y calculando '{numeric_cols[0]}'")
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")
            st.info("📊 Usando datos de ejemplo para la práctica")
    else:
        st.info("📤 Sube un archivo para comenzar la práctica final")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Final congratulations
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("## 🎉 ¡Felicitaciones!")
    
    st.markdown("""
    ### 🏆 Has Completado Todos los Niveles
    
    Ahora eres capaz de:
    - ✅ Preparar y cargar datos correctamente
    - ✅ Aplicar filtros para análisis específicos
    - ✅ Interpretar métricas y KPIs
    - ✅ Crear cálculos personalizados
    - ✅ Generar visualizaciones informativas
    - ✅ Realizar análisis completos de datos
    
    ### 🚀 Próximos Pasos:
    - Practica con tus propios datos
    - Explora funcionalidades avanzadas
    - Comparte insights con tu equipo
    - Continúa aprendiendo nuevas técnicas
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Dashboard Principal"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("⬅️ Nivel Anterior"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col3:
        if st.button("📚 Repasar Niveles"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col4:
        if st.button("❓ Ayuda"):
            st.switch_page("pages/00_Ayuda.py")
    
    # Tips section
    st.markdown("""
    ---
    ### 💡 Consejos Avanzados:
    - **Iteración**: No tengas miedo de experimentar con diferentes cálculos
    - **Validación**: Siempre verifica que tus cálculos tengan sentido
    - **Documentación**: Documenta las fórmulas y lógica de tus cálculos
    - **Visualización**: Usa diferentes tipos de gráficos para diferentes insights
    - **Storytelling**: Cuenta una historia con tus datos y visualizaciones
    - **Colaboración**: Comparte tus análisis con otros para obtener perspectivas
    """)

if __name__ == "__main__":
    main()
