import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.ui.icon_system import get_icon, replace_emojis
# Analisis - Analizar Calidad de Datos
@st.cache_data(show_spinner=False, ttl=600)
def analyze_data_quality(df):
    """Comprehensive data quality analysis"""
    
    analysis = {
        'basic_info': {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
            'duplicates': df.duplicated().sum()
        },
        'missing_data': {
            'missing_counts': df.isnull().sum().to_dict(),
            'missing_percentages': (df.isnull().sum() / len(df) * 100).to_dict(),
            'columns_with_missing': df.columns[df.isnull().any()].tolist()
        },
        'data_types': df.dtypes.astype(str).to_dict(),
        'numeric_analysis': {},
        'categorical_analysis': {},
        'date_analysis': {},
        'outliers': {},
        'inconsistencies': {}
    }
    
    # Analisis - Analizar Columnas Numericas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        analysis['numeric_analysis'][col] = {
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'zeros': int((df[col] == 0).sum()),
            'negatives': int((df[col] < 0).sum())
        }
        
        # Detect outliers using IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        
        analysis['outliers'][col] = {
            'count': len(outliers),
            'percentage': len(outliers) / len(df) * 100,
            'values': outliers.astype(str).tolist()
        }
    
    # Analisis - Analizar Columnas Categoricas
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_values = df[col].nunique()
        analysis['categorical_analysis'][col] = {
            'unique_values': unique_values,
            'most_common': str(df[col].mode().iloc[0]) if not df[col].mode().empty else None,
            'most_common_count': df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0,
            'empty_strings': (df[col] == '').sum(),
            'whitespace_only': (df[col].str.strip() == '').sum() if df[col].dtype == 'object' else 0
        }
    
    # Analisis - Analizar Columnas de Fecha
    date_cols = df.select_dtypes(include=['datetime64']).columns
    for col in date_cols:
        analysis['date_analysis'][col] = {
            'min_date': str(df[col].min()),
            'max_date': str(df[col].max()),
            'date_range': (df[col].max() - df[col].min()).days,
            'future_dates': (df[col] > pd.Timestamp.now()).sum()
        }
    
    return analysis

# Reporte - Crear Reporte de Calidad
def create_quality_report(df, analysis):
    """Create comprehensive quality report"""
    
    st.markdown(replace_emojis("## 📊 Reporte de Calidad de Datos"), unsafe_allow_html=True)
    
    # UI - Mostrar Informacion Basica
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(replace_emojis("📈 Filas"), f"{analysis['basic_info']['rows']:,}")
    with col2:
        st.metric(replace_emojis("📋 Columnas"), analysis['basic_info']['columns'])
    with col3:
        st.metric("💾 Memoria", f"{analysis['basic_info']['memory_usage']:.2f} MB")
    with col4:
        st.metric(replace_emojis("🔄 Duplicados"), analysis['basic_info']['duplicates'])
    
    # UI - Mostrar Puntuacion de Calidad de Datos
    quality_score = calculate_quality_score(analysis)
    st.markdown(f"### {get_icon("🎯", 20)} Puntuación de Calidad: {quality_score:.1f}/100", unsafe_allow_html=True)
    
    # UI - Mostrar Barra de Progreso de Calidad
    st.progress(quality_score / 100)
    
    # UI - Mostrar Tabs de Analisis Detallado
    tab1, tab2, tab3, tab4, tab5 = st.tabs([replace_emojis("📋 General"), "❌ Valores Faltantes", "🔢 Numéricas", "📝 Categóricas", "📅 Fechas"])
    
    with tab1:
        show_general_analysis(df, analysis)
    
    with tab2:
        show_missing_data_analysis(analysis)
    
    with tab3:
        show_numeric_analysis(analysis)
    
    with tab4:
        show_categorical_analysis(analysis)
    
    with tab5:
        show_date_analysis(analysis)

# Calculo - Calcular Puntuacion de Calidad
def calculate_quality_score(analysis):
    """Calculate overall data quality score"""
    score = 100
    
    # Calculo - Penalizar Datos Faltantes
    missing_percentages = analysis['missing_data']['missing_percentages']
    for col, percentage in missing_percentages.items():
        if percentage > 50:
            score -= 20
        elif percentage > 20:
            score -= 10
        elif percentage > 5:
            score -= 5
    
    # Calculo - Penalizar Duplicados
    duplicate_percentage = analysis['basic_info']['duplicates'] / analysis['basic_info']['rows'] * 100
    if duplicate_percentage > 10:
        score -= 15
    elif duplicate_percentage > 5:
        score -= 10
    elif duplicate_percentage > 1:
        score -= 5
    
    # Calculo - Penalizar Outliers
    for col, outlier_info in analysis['outliers'].items():
        if outlier_info['percentage'] > 10:
            score -= 10
        elif outlier_info['percentage'] > 5:
            score -= 5
    
    return max(0, score)

# UI - Mostrar Analisis General
def show_general_analysis(df, analysis):
    """Show general data analysis"""
    st.markdown(replace_emojis("### 📊 Información General"), unsafe_allow_html=True)
    
    # UI - Mostrar Resumen de Tipos de Datos
    st.markdown("#### Tipos de Datos:")
    type_counts = pd.Series(analysis['data_types']).value_counts()
    fig = px.pie(values=type_counts.values, names=type_counts.index, title="Distribución de Tipos de Datos")
    st.plotly_chart(fig, use_container_width=True)
    
    # UI - Mostrar Tabla de Informacion de Columnas
    st.markdown("#### Información de Columnas:")
    column_info = pd.DataFrame({
        'Columna': df.columns,
        'Tipo': df.dtypes.astype(str),
        'Valores Únicos': [df[col].nunique() for col in df.columns],
        'Valores Faltantes': [df[col].isnull().sum() for col in df.columns],
        '% Faltantes': [(df[col].isnull().sum() / len(df) * 100) for col in df.columns]
    })
    st.dataframe(column_info, use_container_width=True)

# UI - Mostrar Analisis de Datos Faltantes
def show_missing_data_analysis(analysis):
    """Show missing data analysis"""
    st.markdown(replace_emojis("### ❌ Análisis de Valores Faltantes"), unsafe_allow_html=True)
    
    if analysis['missing_data']['columns_with_missing']:
        # Missing data chart
        missing_df = pd.DataFrame({
            'Columna': list(analysis['missing_data']['missing_percentages'].keys()),
            'Porcentaje': list(analysis['missing_data']['missing_percentages'].values())
        }).sort_values('Porcentaje', ascending=False)
        
        fig = px.bar(missing_df, x='Columna', y='Porcentaje', 
                    title="Porcentaje de Valores Faltantes por Columna")
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown(replace_emojis("#### 💡 Recomendaciones:"), unsafe_allow_html=True)
        for col, percentage in analysis['missing_data']['missing_percentages'].items():
            if percentage > 50:
                st.warning(f"⚠️ **{col}**: {percentage:.1f}% faltantes - Considera eliminar esta columna")
            elif percentage > 20:
                st.info(f"ℹ️ **{col}**: {percentage:.1f}% faltantes - Considera imputación")
            elif percentage > 5:
                st.markdown(f"{get_icon("✅", 20)} **{col}**: {percentage:.1f}% faltantes - Manejo estándar", unsafe_allow_html=True)
    else:
        st.markdown(replace_emojis("🎉 ¡No hay valores faltantes en tu dataset!"), unsafe_allow_html=True)

# UI - Mostrar Analisis de Columnas Numericas
def show_numeric_analysis(analysis):
    """Show numeric columns analysis"""
    st.markdown(replace_emojis("### 🔢 Análisis de Columnas Numéricas"), unsafe_allow_html=True)
    
    if analysis['numeric_analysis']:
        # Summary statistics
        numeric_summary = pd.DataFrame(analysis['numeric_analysis']).T
        st.dataframe(numeric_summary, use_container_width=True)
        
        # Outliers analysis
        st.markdown(replace_emojis("#### 📊 Análisis de Outliers:"), unsafe_allow_html=True)
        outliers_df = pd.DataFrame({
            'Columna': list(analysis['outliers'].keys()),
            'Cantidad': [info['count'] for info in analysis['outliers'].values()],
            'Porcentaje': [info['percentage'] for info in analysis['outliers'].values()]
        })
        
        if not outliers_df.empty:
            fig = px.bar(outliers_df, x='Columna', y='Porcentaje',
                        title="Porcentaje de Outliers por Columna")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ No hay columnas numéricas en tu dataset")

# UI - Mostrar Analisis de Columnas Categoricas
def show_categorical_analysis(analysis):
    """Show categorical columns analysis"""
    st.markdown(replace_emojis("### 📝 Análisis de Columnas Categóricas"), unsafe_allow_html=True)
    
    if analysis['categorical_analysis']:
        # Categorical summary
        cat_summary = pd.DataFrame(analysis['categorical_analysis']).T
        st.dataframe(cat_summary, use_container_width=True)
        
        # Inconsistencies
        st.markdown(replace_emojis("#### 🔍 Posibles Inconsistencias:"), unsafe_allow_html=True)
        for col, info in analysis['categorical_analysis'].items():
            if info['empty_strings'] > 0:
                st.warning(f"⚠️ **{col}**: {info['empty_strings']} cadenas vacías")
            if info['whitespace_only'] > 0:
                st.info(f"ℹ️ **{col}**: {info['whitespace_only']} valores solo con espacios")
    else:
        st.info("ℹ️ No hay columnas categóricas en tu dataset")

# UI - Mostrar Analisis de Columnas de Fecha
def show_date_analysis(analysis):
    """Show date columns analysis"""
    st.markdown(replace_emojis("### 📅 Análisis de Columnas de Fecha"), unsafe_allow_html=True)
    
    if analysis['date_analysis']:
        # Date summary
        date_summary = pd.DataFrame(analysis['date_analysis']).T
        st.dataframe(date_summary, use_container_width=True)
        
        # Future dates warning
        for col, info in analysis['date_analysis'].items():
            if info['future_dates'] > 0:
                st.warning(f"⚠️ **{col}**: {info['future_dates']} fechas futuras detectadas")
    else:
        st.info("ℹ️ No hay columnas de fecha en tu dataset")

# UI - Crear Opciones de Limpieza
def create_data_cleaning_options(df, analysis):
    """Create data cleaning options"""
    st.markdown("## 🧹 Opciones de Limpieza de Datos")
    
    cleaned_df = df.copy()
    
    # UI - Mostrar Manejo de Datos Faltantes
    st.markdown(replace_emojis("### ❌ Manejo de Valores Faltantes"), unsafe_allow_html=True)
    
    for col in analysis['missing_data']['columns_with_missing']:
        missing_pct = analysis['missing_data']['missing_percentages'][col]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{col}** ({missing_pct:.1f}% faltantes)")
        with col2:
            if missing_pct > 50:
                action = st.selectbox(
                    f"Acción para {col}",
                    ["Eliminar columna", "Mantener"],
                    key=f"missing_{col}"
                )
                if action == "Eliminar columna":
                    cleaned_df = cleaned_df.drop(columns=[col])
            else:
                action = st.selectbox(
                    f"Acción para {col}",
                    ["Eliminar filas", "Imputar con media/mediana", "Imputar con valor más común", "Mantener"],
                    key=f"missing_{col}"
                )
                
                if action == "Eliminar filas":
                    cleaned_df = cleaned_df.dropna(subset=[col])
                elif action == "Imputar con media/mediana":
                    if col in analysis['numeric_analysis']:
                        value = cleaned_df[col].median()
                        cleaned_df[col] = cleaned_df[col].fillna(value)
                elif action == "Imputar con valor más común":
                    value = cleaned_df[col].mode().iloc[0] if not cleaned_df[col].mode().empty else "Desconocido"
                    cleaned_df[col] = cleaned_df[col].fillna(value)
    
    # UI - Mostrar Manejo de Duplicados
    st.markdown(replace_emojis("### 🔄 Manejo de Duplicados"), unsafe_allow_html=True)
    if analysis['basic_info']['duplicates'] > 0:
        duplicate_action = st.selectbox(
            "Acción para duplicados",
            ["Eliminar duplicados", "Mantener"],
            key="duplicates"
        )
        if duplicate_action == "Eliminar duplicados":
            cleaned_df = cleaned_df.drop_duplicates()
    
    # UI - Mostrar Manejo de Outliers
    st.markdown(replace_emojis("### 📊 Manejo de Outliers"), unsafe_allow_html=True)
    for col in analysis['outliers']:
        outlier_pct = analysis['outliers'][col]['percentage']
        if outlier_pct > 5:
            outlier_action = st.selectbox(
                f"Acción para outliers en {col}",
                ["Eliminar outliers", "Capar outliers", "Mantener"],
                key=f"outlier_{col}"
            )
            
            if outlier_action in ["Eliminar outliers", "Capar outliers"]:
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                if outlier_action == "Eliminar outliers":
                    cleaned_df = cleaned_df[(cleaned_df[col] >= lower_bound) & (cleaned_df[col] <= upper_bound)]
                else:  # Cap outliers
                    cleaned_df[col] = cleaned_df[col].clip(lower=lower_bound, upper=upper_bound)
    
    return cleaned_df

# Principal - Pagina de Calidad de Datos
def data_quality_page(df):
    """Main data quality analysis page"""
    st.markdown("# 🧹 Análisis y Limpieza de Datos")
    st.markdown("### Paso 2: Revisa la calidad de tus datos antes de continuar")
    
    # Analisis - Analizar Calidad de Datos
    analysis = analyze_data_quality(df)
    
    # UI - Mostrar Reporte de Calidad
    create_quality_report(df, analysis)
    
    st.divider()
    
    # UI - Mostrar Opciones de Limpieza de Datos
    cleaned_df = create_data_cleaning_options(df, analysis)
    
    # UI - Mostrar Comparacion de Datos
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(replace_emojis("### 📊 Datos Originales"), unsafe_allow_html=True)
        st.metric("Filas", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    with col2:
        st.markdown("### 🧹 Datos Limpiados")
        st.metric("Filas", len(cleaned_df))
        st.metric("Columnas", len(cleaned_df.columns))
        st.metric("Memoria", f"{cleaned_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # UI - Mostrar Botones de Accion
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Usar Datos Limpiados", type="primary"):
            st.session_state.cleaned_data = cleaned_df
            st.session_state.data_quality_completed = True
            st.success("¡Datos limpiados cargados exitosamente!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Usar Datos Originales"):
            st.session_state.cleaned_data = df
            st.session_state.data_quality_completed = True
            st.success("¡Datos originales cargados exitosamente!")
            st.rerun()
    
    with col3:
        if st.button("📤 Subir Nuevo Archivo"):
            st.session_state.data_quality_completed = False
            st.rerun()
    
    return cleaned_df
