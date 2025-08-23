import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Nivel 2: Filtros - Análisis de Datos",
    page_icon="🔍",
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
    .filter-demo {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
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
    
    return df.sort_values('Fecha').reset_index(drop=True)

def main():
    # Header
    st.markdown('<h1 class="level-header">🔍 Nivel 2: Filtros</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Análisis y Filtrado de Datos</h2>', unsafe_allow_html=True)
    
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
    was_completed = st.session_state.get('nivel2_completed', False)
    
    if st.checkbox("✅ Click aquí para marcar este nivel como Completado", 
                  value=was_completed,
                  key='nivel2_completion_checkbox'):
        # Only show balloons if this is the first time completing
        if not was_completed:
            st.balloons()
            st.success("🎉 ¡Felicidades! Has completado el Nivel 2. ¡Continúa con el siguiente nivel!")
        st.session_state['nivel2_completed'] = True
    else:
        st.session_state['nivel2_completed'] = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Introduction
    st.markdown("""
    ## 🎯 Objetivo de este Nivel
    
    En este nivel aprenderás a:
    - Usar filtros de fecha para analizar períodos específicos
    - Filtrar por categorías y regiones
    - Aplicar filtros numéricos con deslizadores
    - Combinar múltiples filtros para análisis detallado
    - Entender cómo los filtros afectan tus métricas
    """)
    
    # Load sample data for demonstration
    df = create_sample_data()
    
    # Step 1: Understanding Filters
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎛️ Paso 1: Entender los Filtros")
    
    st.markdown("""
    ### 📊 ¿Qué son los Filtros?
    
    Los filtros te permiten:
    - **Reducir** la cantidad de datos que analizas
    - **Enfocarte** en información específica
    - **Comparar** diferentes segmentos
    - **Identificar** patrones y tendencias
    
    ### 🔧 Tipos de Filtros Disponibles:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📅 Filtros de Fecha**
        - Rango de fechas
        - Períodos específicos
        - Comparaciones temporales
        """)
    
    with col2:
        st.markdown("""
        **🏷️ Filtros de Categoría**
        - Selección múltiple
        - Análisis por grupos
        - Comparación entre categorías
        """)
    
    with col3:
        st.markdown("""
        **📊 Filtros Numéricos**
        - Rangos con deslizadores
        - Valores mínimos y máximos
        - Filtros dinámicos
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Date Filters Demo
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📅 Paso 2: Filtros de Fecha")
    
    st.markdown("""
    ### 🎯 Cómo Usar Filtros de Fecha:
    1. Ve a la barra lateral
    2. Busca "Seleccionar Rango de Fechas"
    3. Elige fechas de inicio y fin
    4. Observa cómo cambian los datos
    """)
    
    # Interactive date filter demo
    st.markdown('<div class="filter-demo">', unsafe_allow_html=True)
    st.markdown("### 🎮 Demostración Interactiva:")
    
    # Date range selector
    date_range = st.date_input(
        "📅 Selecciona un rango de fechas para ver el efecto:",
        value=(df['Fecha'].min(), df['Fecha'].max()),
        min_value=df['Fecha'].min(),
        max_value=df['Fecha'].max()
    )
    
    if len(date_range) == 2:
        # Filter data based on selection
        filtered_df = df[(df['Fecha'] >= pd.to_datetime(date_range[0])) & 
                        (df['Fecha'] <= pd.to_datetime(date_range[1]))]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📊 Datos Originales", len(df))
            st.metric("💰 Ingresos Totales", f"${df['Ingresos'].sum():,.2f}")
        
        with col2:
            st.metric("📊 Datos Filtrados", len(filtered_df))
            st.metric("💰 Ingresos Filtrados", f"${filtered_df['Ingresos'].sum():,.2f}")
        
        # Show filtered data
        st.markdown("### 📋 Datos Filtrados:")
        st.dataframe(filtered_df.head(10), use_container_width=True)
        
        # Show the effect
        reduction = ((len(df) - len(filtered_df)) / len(df)) * 100
        st.info(f"📉 El filtro redujo los datos en un {reduction:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Category Filters Demo
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🏷️ Paso 3: Filtros de Categoría")
    
    st.markdown("""
    ### 🎯 Cómo Usar Filtros de Categoría:
    1. Busca "Seleccionar Categorías" en la barra lateral
    2. Marca/desmarca las categorías que quieres analizar
    3. Observa cómo cambian las métricas
    """)
    
    # Interactive category filter demo
    st.markdown('<div class="filter-demo">', unsafe_allow_html=True)
    st.markdown("### 🎮 Demostración Interactiva:")
    
    # Category selector
    categories = st.multiselect(
        "🏷️ Selecciona categorías para filtrar:",
        options=df['Categoria'].unique(),
        default=df['Categoria'].unique()
    )
    
    if categories:
        # Filter data based on selection
        cat_filtered_df = df[df['Categoria'].isin(categories)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📊 Datos Originales", len(df))
            st.metric("🏷️ Categorías Totales", len(df['Categoria'].unique()))
        
        with col2:
            st.metric("📊 Datos Filtrados", len(cat_filtered_df))
            st.metric("🏷️ Categorías Seleccionadas", len(categories))
        
        # Show category breakdown
        st.markdown("### 📊 Desglose por Categoría:")
        cat_summary = cat_filtered_df.groupby('Categoria').agg({
            'Ingresos': 'sum',
            'Cantidad': 'sum'
        }).round(2)
        st.dataframe(cat_summary, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Numeric Filters Demo
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 📊 Paso 4: Filtros Numéricos")
    
    st.markdown("""
    ### 🎯 Cómo Usar Filtros Numéricos:
    1. Busca los deslizadores en la barra lateral
    2. Ajusta los valores mínimos y máximos
    3. Observa cómo se filtran los datos automáticamente
    """)
    
    # Interactive numeric filter demo
    st.markdown('<div class="filter-demo">', unsafe_allow_html=True)
    st.markdown("### 🎮 Demostración Interactiva:")
    
    # Sales range slider
    sales_range = st.slider(
        "💰 Rango de Ventas:",
        min_value=float(df['Ventas'].min()),
        max_value=float(df['Ventas'].max()),
        value=(float(df['Ventas'].min()), float(df['Ventas'].max())),
        step=10.0
    )
    
    # Rating range slider
    rating_range = st.slider(
        "⭐ Rango de Calificación:",
        min_value=int(df['Calificacion'].min()),
        max_value=int(df['Calificacion'].max()),
        value=(int(df['Calificacion'].min()), int(df['Calificacion'].max())),
        step=1
    )
    
    # Filter data based on selections
    num_filtered_df = df[
        (df['Ventas'] >= sales_range[0]) & 
        (df['Ventas'] <= sales_range[1]) &
        (df['Calificacion'] >= rating_range[0]) & 
        (df['Calificacion'] <= rating_range[1])
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📊 Datos Originales", len(df))
        st.metric("💰 Ventas Promedio", f"${df['Ventas'].mean():.2f}")
    
    with col2:
        st.metric("📊 Datos Filtrados", len(num_filtered_df))
        st.metric("💰 Ventas Promedio Filtradas", f"${num_filtered_df['Ventas'].mean():.2f}")
    
    # Show filtered data
    st.markdown("### 📋 Datos Filtrados por Rangos:")
    st.dataframe(num_filtered_df.head(10), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 5: Practice Section
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("## 🎯 Paso 5: Práctica - ¡Tu Turno!")
    
    st.markdown("""
    ### 📝 Ejercicio Práctico:
    
    **Objetivo**: Analizar las ventas de "Electronica" en el primer trimestre de 2023
    
    **Pasos**:
    1. Aplica un filtro de fecha para Q1 2023 (Enero-Marzo)
    2. Aplica un filtro de categoría para "Electronica"
    3. Observa cómo cambian las métricas
    4. Compara con otros períodos o categorías
    """)
    
    # Interactive practice area
    st.markdown("### 🎮 Área de Práctica:")
    
    # Load user's data if available
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo para practicar (opcional):",
        type=['csv', 'xlsx', 'xls'],
        help="Si no tienes archivo, usa los datos de ejemplo"
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
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")
            practice_df = df  # Use sample data as fallback
    else:
        practice_df = df
        st.info("📊 Usando datos de ejemplo para la práctica")
    
    # Practice filters
    st.markdown("#### 🔧 Aplica Filtros:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date filter for practice
        if any('fecha' in col.lower() or 'date' in col.lower() for col in practice_df.columns):
            date_col = [col for col in practice_df.columns if 'fecha' in col.lower() or 'date' in col.lower()][0]
            practice_date_range = st.date_input(
                "📅 Rango de fechas:",
                value=(practice_df[date_col].min(), practice_df[date_col].max()),
                min_value=practice_df[date_col].min(),
                max_value=practice_df[date_col].max()
            )
        else:
            practice_date_range = None
    
    with col2:
        # Category filter for practice
        if any('categoria' in col.lower() or 'category' in col.lower() for col in practice_df.columns):
            cat_col = [col for col in practice_df.columns if 'categoria' in col.lower() or 'category' in col.lower()][0]
            practice_categories = st.multiselect(
                "🏷️ Categorías:",
                options=practice_df[cat_col].unique(),
                default=practice_df[cat_col].unique()
            )
        else:
            practice_categories = None
    
    # Apply filters and show results
    filtered_practice_df = practice_df.copy()
    
    if practice_date_range and len(practice_date_range) == 2:
        filtered_practice_df = filtered_practice_df[
            (filtered_practice_df[date_col] >= pd.to_datetime(practice_date_range[0])) & 
            (filtered_practice_df[date_col] <= pd.to_datetime(practice_date_range[1]))
        ]
    
    if practice_categories:
        filtered_practice_df = filtered_practice_df[filtered_practice_df[cat_col].isin(practice_categories)]
    
    # Show results
    st.markdown("#### 📊 Resultados:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Filas Originales", len(practice_df))
        st.metric("📉 Filas Filtradas", len(filtered_practice_df))
    
    with col2:
        # Show numeric metrics if available
        numeric_cols = filtered_practice_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            main_numeric = numeric_cols[0]
            st.metric(f"💰 Total {main_numeric}", f"{filtered_practice_df[main_numeric].sum():,.2f}")
    
    with col3:
        if len(filtered_practice_df) > 0:
            reduction = ((len(practice_df) - len(filtered_practice_df)) / len(practice_df)) * 100
            st.metric("📊 Reducción", f"{reduction:.1f}%")
    
    # Show filtered data
    st.markdown("#### 📋 Datos Filtrados:")
    st.dataframe(filtered_practice_df.head(10), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Success Criteria
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("## ✅ Criterios de Éxito")
    
    st.markdown("""
    Has completado este nivel cuando:
    - ✅ Puedes aplicar filtros de fecha correctamente
    - ✅ Sabes usar filtros de categoría y región
    - ✅ Entiendes cómo funcionan los filtros numéricos
    - ✅ Puedes combinar múltiples filtros
    - ✅ Observas cómo los filtros afectan las métricas
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.divider()
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Dashboard Principal", key="nivel2_dashboard"):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("⬅️ Nivel Anterior", key="nivel2_anterior"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
    
    with col4:
        if st.button("➡️ Siguiente Nivel", key="nivel2_siguiente"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    # Tips section
    st.markdown("""
    ---
    ### 💡 Consejos para Filtros:
    - **Combinar filtros**: Usa múltiples filtros para análisis más específicos
    - **Comparar períodos**: Aplica filtros de fecha para comparar diferentes períodos
    - **Segmentar datos**: Usa filtros de categoría para analizar segmentos específicos
    - **Rangos numéricos**: Los deslizadores son ideales para encontrar valores atípicos
    - **Resetear filtros**: Puedes quitar filtros seleccionando "Todos" o el rango completo
    """)

if __name__ == "__main__":
    main()
