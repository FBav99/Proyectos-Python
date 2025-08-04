import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(
    page_title="Panel de Análisis de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejor estilo
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Generar conjunto de datos de muestra para demostración"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    n_records = len(dates)
    
    data = {
        'Date': np.random.choice(dates, n_records//2),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], n_records//2),
        'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_records//2),
        'Sales': np.random.normal(1000, 300, n_records//2).round(2),
        'Quantity': np.random.poisson(5, n_records//2),
        'Customer_Age': np.random.normal(35, 12, n_records//2).round(0),
        'Rating': np.random.choice([1, 2, 3, 4, 5], n_records//2, p=[0.05, 0.1, 0.15, 0.4, 0.3])
    }
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Sales'] * df['Quantity']
    df['Profit_Margin'] = np.random.uniform(0.1, 0.4, len(df))
    df['Profit'] = df['Revenue'] * df['Profit_Margin']
    
    return df.sort_values('Date').reset_index(drop=True)

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

def create_time_series_chart(df, metric='Revenue'):
    """Crear visualización de series temporales"""
    daily_data = df.groupby('Date')[metric].sum().reset_index()
    
    fig = px.line(daily_data, x='Date', y=metric, 
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

def create_category_analysis(df):
    """Crear gráficos de análisis por categoría"""
    category_metrics = df.groupby('Category').agg({
        'Revenue': 'sum',
        'Quantity': 'sum',
        'Rating': 'mean'
    }).reset_index()
    
    # Crear subgráficos
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Ingresos por Categoría', 'Calificación Promedio por Categoría'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Gráfico de barras de ingresos
    fig.add_trace(
        go.Bar(x=category_metrics['Category'], 
               y=category_metrics['Revenue'],
               name='Ingresos',
               marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Gráfico de barras de calificación
    fig.add_trace(
        go.Bar(x=category_metrics['Category'], 
               y=category_metrics['Rating'],
               name='Calificación Prom.',
               marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    return fig

def create_regional_analysis(df):
    """Crear visualización de rendimiento regional"""
    regional_data = df.groupby('Region').agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    fig = px.bar(regional_data, x='Region', y='Revenue',
                 title='Ingresos por Región',
                 template='plotly_white',
                 color='Revenue',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400)
    return fig

def export_data(df, filters_applied):
    """Crear funcionalidad de exportación"""
    buffer = io.BytesIO()
    
    # Crear archivo Excel con múltiples hojas
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos_Filtrados', index=False)
        
        # Agregar hoja de resumen
        metrics = calculate_metrics(df)
        summary_df = pd.DataFrame([metrics])
        summary_df.to_excel(writer, sheet_name='Metricas_Resumen', index=False)
        
        # Agregar información de filtros
        filter_info = pd.DataFrame([filters_applied])
        filter_info.to_excel(writer, sheet_name='Filtros_Aplicados', index=False)
    
    buffer.seek(0)
    return buffer

# Aplicación Principal
def main():
    st.markdown('<h1 class="main-header">📊 Panel de Análisis de Datos</h1>', unsafe_allow_html=True)
    
    # Barra lateral para carga de archivos y filtros
    st.sidebar.title("🔧 Controles")
    
    # Carga de archivos
    uploaded_file = st.sidebar.file_uploader(
        "Sube tu archivo de datos",
        type=['csv', 'xlsx', 'xls'],
        help="Sube un archivo CSV o Excel para analizar tus datos"
    )
    
    # Cargar datos
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Intentar convertir columnas de fecha
            for col in df.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except:
                        pass
                        
            st.sidebar.success(f"✅ Cargadas {len(df)} filas de datos")
        except Exception as e:
            st.sidebar.error(f"Error al cargar archivo: {str(e)}")
            df = load_sample_data()
    else:
        st.sidebar.info("Usando datos de muestra para demostración")
        df = load_sample_data()
    
    # Vista previa de datos
    st.subheader("📋 Vista Previa de Datos")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Filtros de la barra lateral
    st.sidebar.subheader("🎛️ Filtros")
    
    # Almacenar df original para referencia
    original_df = df.copy()
    filters_applied = {}
    
    # Filtro de fecha
    if 'Date' in df.columns:
        date_range = st.sidebar.date_input(
            "Seleccionar Rango de Fechas",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
        if len(date_range) == 2:
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & 
                   (df['Date'] <= pd.to_datetime(date_range[1]))]
            filters_applied['Rango de Fechas'] = f"{date_range[0]} hasta {date_range[1]}"
    
    # Filtro de categoría
    if 'Category' in df.columns:
        categories = st.sidebar.multiselect(
            "Seleccionar Categorías",
            options=original_df['Category'].unique(),
            default=original_df['Category'].unique()
        )
        if categories:
            df = df[df['Category'].isin(categories)]
            filters_applied['Categorías'] = categories
    
    # Filtro de región
    if 'Region' in df.columns:
        regions = st.sidebar.multiselect(
            "Seleccionar Regiones",
            options=original_df['Region'].unique(),
            default=original_df['Region'].unique()
        )
        if regions:
            df = df[df['Region'].isin(regions)]
            filters_applied['Regiones'] = regions
    
    # Constructor de Cálculos Personalizados
    st.sidebar.subheader("🧮 Cálculos Personalizados")
    
    # Obtener columnas numéricas para cálculos
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    if len(numeric_cols) >= 1:
        # Selector de tipo de cálculo
        calc_type = st.sidebar.selectbox(
            "Tipo de Cálculo",
            ["Matemáticas Básicas", "Comparaciones Temporales", "Agregaciones"]
        )
        
        num_calculations = st.sidebar.number_input("Número de cálculos personalizados", min_value=0, max_value=5, value=0)
        
        custom_calculations = []
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
            
            # Aplicar cálculos
            for calc_info in custom_calculations:
                try:
                    if calc_info['type'] == 'basic':
                        # Operaciones matemáticas básicas (código existente)
                        col1_calc, col2_calc, operation = calc_info['col1'], calc_info['col2'], calc_info['operation']
                        calc_name = calc_info['name']
                        
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
                            
                    elif calc_info['type'] == 'time':
                        # Cálculos basados en tiempo
                        target_col = calc_info['target_col']
                        date_col = calc_info['date_col']
                        time_op = calc_info['time_operation']
                        calc_name = calc_info['name']
                        
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
                            
                    elif calc_info['type'] == 'aggregation':
                        # Cálculos de agregación
                        target_col = calc_info['target_col']
                        group_col = calc_info['group_col']
                        agg_op = calc_info['agg_operation']
                        calc_name = calc_info['name']
                        
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
                    
                    # Rastrear cálculos aplicados
                    filters_applied[f'Cálculo Personalizado {calc_info["name"]}'] = f"{calc_info}"
                    
                except Exception as e:
                    st.sidebar.error(f"Error en el cálculo '{calc_info['name']}': {str(e)}")
            
            st.sidebar.markdown("---")
    
    # Filtros numéricos (actualizado para incluir cálculos personalizados)
    all_numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in ['Sales', 'Revenue', 'Rating']:
        if col in all_numeric_cols:
            col_min, col_max = float(original_df[col].min() if col in original_df.columns else df[col].min()), float(original_df[col].max() if col in original_df.columns else df[col].max())
            if col_min != col_max:  # Solo mostrar deslizador si hay un rango
                range_values = st.sidebar.slider(
                    f"Rango de {col}",
                    min_value=col_min,
                    max_value=col_max,
                    value=(col_min, col_max),
                    step=(col_max - col_min) / 100 if col_max != col_min else 1.0
                )
                df = df[(df[col] >= range_values[0]) & (df[col] <= range_values[1])]
                if range_values != (col_min, col_max):
                    filters_applied[f'Rango de {col}'] = range_values
    
    # Mostrar información de datos filtrados
    if len(filters_applied) > 0:
        st.info(f"📊 Mostrando {len(df):,} filas después de aplicar filtros (originalmente {len(original_df):,} filas)")
    
    # Panel de Métricas Clave
    st.subheader("🎯 Métricas Clave de Rendimiento")
    
    if len(df) > 0:
        metrics = calculate_metrics(df)
        
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
        if num_calculations > 0:
            st.subheader("🧮 Tus Cálculos Personalizados")
            
            calc_cols = st.columns(min(3, num_calculations))
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
                        formula = f"{calc_info['col1']} {calc_info['operation']} {calc_info['col2']}"
                        st.caption(f"Fórmula: {formula}")
            
            # Gráficos de cálculos personalizados
            st.subheader("📈 Tendencias de Cálculos Personalizados")
            
            # Crear gráficos para cálculos personalizados a lo largo del tiempo
            if 'Date' in df.columns:
                for calc_info in custom_calculations:
                    calc_name = calc_info['name']
                    if calc_name in df.columns:
                        custom_fig = create_time_series_chart(df, calc_name)
                        st.plotly_chart(custom_fig, use_container_width=True)
            
            # Análisis de correlación para cálculos personalizados
            custom_calc_names = [calc['name'] for calc in custom_calculations if calc['name'] in df.columns]
            if len(custom_calc_names) >= 2:
                st.subheader("🔗 Correlación de Cálculos Personalizados")
                
                corr_data = df[custom_calc_names].corr()
                
                fig_corr = px.imshow(
                    corr_data,
                    title="Matriz de Correlación de Cálculos Personalizados",
                    color_continuous_scale="RdBu",
                    aspect="auto"
                )
                fig_corr.update_layout(height=400)
                st.plotly_chart(fig_corr, use_container_width=True)

        # Análisis Avanzado
        st.subheader("🔍 Perspectivas Avanzadas")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("### 📈 Análisis de Crecimiento")
            if 'Date' in df.columns and len(df) > 30:
                # Calcular crecimiento mes a mes
                monthly_data = df.set_index('Date').resample('M')['Revenue'].sum()
                if len(monthly_data) > 1:
                    mom_growth = ((monthly_data.iloc[-1] - monthly_data.iloc[-2]) / monthly_data.iloc[-2] * 100)
                    st.metric("Crecimiento Mes a Mes", f"{mom_growth:.1f}%")
                
                # Período de mejor rendimiento
                daily_revenue = df.groupby('Date')['Revenue'].sum()
                best_day = daily_revenue.idxmax()
                st.success(f"🏆 Mejor día: {best_day.strftime('%Y-%m-%d')} (${daily_revenue.max():,.2f})")
        
        with insight_col2:
            st.markdown("### 🎯 Perspectivas de Rendimiento")
            
            if 'Category' in df.columns:
                top_category = df.groupby('Category')['Revenue'].sum().idxmax()
                st.success(f"🥇 Mejor Categoría: {top_category}")
            
            if 'Region' in df.columns:
                top_region = df.groupby('Region')['Revenue'].sum().idxmax()
                st.success(f"📍 Mejor Región: {top_region}")
            
            # Perspectiva de satisfacción del cliente
            high_rated = len(df[df['Rating'] >= 4]) / len(df) * 100
            st.info(f"😊 {high_rated:.1f}% clientes califican 4+ estrellas")
        
        # Funcionalidad de exportación
        st.subheader("📤 Exportar Datos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Descargar Datos Filtrados (Excel)", type="primary"):
                excel_buffer = export_data(df, filters_applied)
                st.download_button(
                    label="💾 Descargar Archivo Excel",
                    data=excel_buffer,
                    file_name=f"analisis_datos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📄 Descargar como CSV",
                data=csv_data,
                file_name=f"datos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col3:
            # Crear reporte de resumen
            summary_text = f"""
# Reporte Resumen de Análisis de Datos
Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Filtros Aplicados
{filters_applied if filters_applied else 'No se aplicaron filtros'}

## Métricas Clave
- Ingresos Totales: ${metrics['total_revenue']:,.2f}
- Pedidos Totales: {metrics['total_orders']:,}
- Valor Promedio de Pedido: ${metrics['avg_order_value']:.2f}
- Ganancia Total: ${metrics['total_profit']:,.2f}
- Margen de Ganancia: {metrics['profit_margin']:.1f}%
- Calificación Promedio: {metrics['avg_rating']:.2f}/5.0

## Resumen de Datos
- Total de Registros: {len(df):,}
- Rango de Fechas: {df['Date'].min().strftime('%Y-%m-%d')} hasta {df['Date'].max().strftime('%Y-%m-%d')}
"""
            st.download_button(
                label="📋 Descargar Reporte Resumen",
                data=summary_text,
                file_name=f"reporte_resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    else:
        st.warning("⚠️ Ningún dato coincide con tus filtros actuales. Por favor ajusta la configuración de filtros.")
    
    # Pie de página
    st.markdown("---")
    st.markdown("💡 **Consejo**: ¡Sube tu propio archivo CSV o Excel usando la barra lateral, o ajusta los filtros para explorar diferentes segmentos de datos!")

if __name__ == "__main__":
    main()