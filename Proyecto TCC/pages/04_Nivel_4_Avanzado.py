import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from utils.system import display_level_gif
from utils.learning import load_level_styles, get_level_progress, create_step_card, create_info_box, create_sample_data
from utils.learning.learning_progress import save_level_progress

# Page config
st.set_page_config(
    page_title="Nivel 4: Avanzado - Análisis de Datos",
    page_icon="🚀",
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Helper functions are now imported from utils.level_components and utils.level_data

def main():
    # Check if user is authenticated
    if 'user' not in st.session_state or not st.session_state.get('authenticated'):
        st.error("🔐 Por favor inicia sesión para acceder a este nivel.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Get current user
    user = st.session_state.get('user')
    if not user or 'id' not in user:
        st.error("❌ Error: No se pudo obtener la información del usuario.")
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Title (level name and description)
    st.title("🚀 Nivel 4: Avanzado")
    st.subheader("Cálculos y Visualizaciones Avanzadas")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/4 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Verificar que los niveles anteriores estén completados
    if not all([progress['nivel1'], progress['nivel2'], progress['nivel3']]):
        st.warning("⚠️ Primero debes completar los Niveles 1, 2 y 3 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # 3. Introduction Section (what the user will learn)
    st.header("🎯 ¿Qué aprenderás en este nivel?")
    st.markdown("""
    En este nivel aprenderás a crear cálculos personalizados, generar visualizaciones interactivas 
    y crear dashboards completos para presentar tu información de manera profesional.
    """)
    
    # 4. Steps Section (clear, actionable instructions)
    st.header("📋 Pasos para Crear Análisis Avanzados")
    
    # Step 1
    create_step_card(
        step_number="1",
        title="Crear cálculos personalizados avanzados",
        description="<strong>¿Qué son los cálculos personalizados?</strong> Son fórmulas que creas tú mismo para obtener información específica que no está disponible directamente en tus datos.",
        sections={
            "🔢 Tipos de cálculos que puedes crear:": [
                "<strong>Porcentajes:</strong> Qué parte del total representa algo",
                "<strong>Promedios ponderados:</strong> Promedios que dan más importancia a ciertos valores",
                "<strong>Cambios porcentuales:</strong> Cuánto aumentó o disminuyó algo",
                "<strong>Ratios y proporciones:</strong> Comparaciones entre diferentes valores"
            ],
            "📝 Ejemplos de fórmulas:": [
                "<strong>Margen de ganancia:</strong> (Precio de venta - Costo) / Precio de venta × 100",
                "<strong>Porcentaje de crecimiento:</strong> (Valor actual - Valor anterior) / Valor anterior × 100",
                "<strong>Promedio ponderado:</strong> Suma de (Valor × Peso) / Suma de pesos"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="2",
        title="Generar visualizaciones interactivas",
        description="<strong>¿Por qué visualizaciones interactivas?</strong> Los gráficos interactivos te permiten explorar los datos de manera más profunda y encontrar insights ocultos.",
        sections={
            "📊 Tipos de visualizaciones:": [
                "<strong>Gráficos de línea:</strong> Para mostrar tendencias a lo largo del tiempo",
                "<strong>Gráficos de barras:</strong> Para comparar categorías",
                "<strong>Gráficos de dispersión:</strong> Para ver relaciones entre dos variables",
                "<strong>Mapas de calor:</strong> Para mostrar patrones en tablas de datos"
            ],
            "🎯 Características de visualizaciones interactivas:": [
                "Zoom y panorámica para explorar detalles",
                "Tooltips que muestran información al pasar el mouse",
                "Filtros que permiten cambiar la vista de los datos",
                "Selección de elementos para análisis específicos"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="3",
        title="Crear dashboards profesionales",
        description="<strong>¿Qué es un dashboard?</strong> Es una colección de visualizaciones y métricas organizadas de manera lógica para contar una historia con los datos.",
        sections={
            "🏗️ Elementos de un dashboard efectivo:": [
                "<strong>Métricas clave (KPIs):</strong> Los números más importantes en la parte superior",
                "<strong>Visualizaciones:</strong> Gráficos que explican las métricas",
                "<strong>Filtros:</strong> Controles para cambiar la vista de los datos",
                "<strong>Navegación:</strong> Forma de moverse entre diferentes vistas"
            ],
            "💡 Principios de diseño:": [
                "Mantén el diseño limpio y sin distracciones",
                "Usa colores de manera consistente y significativa",
                "Organiza la información de más importante a menos importante",
                "Asegúrate de que sea fácil de entender para tu audiencia"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="4",
        title="Interpretar y comunicar insights",
        description="<strong>¿Qué son los insights?</strong> Son descubrimientos importantes en los datos que pueden llevar a acciones o decisiones valiosas.",
        sections={
            "🔍 Cómo encontrar insights:": [
                "Busca patrones inesperados en los datos",
                "Compara diferentes períodos o grupos",
                "Identifica valores atípicos o anomalías",
                "Conecta diferentes métricas para ver el panorama completo"
            ],
            "📢 Cómo comunicar insights:": [
                "Cuenta una historia con los datos",
                "Explica qué significa cada insight para el negocio",
                "Sugiere acciones específicas basadas en los datos",
                "Usa visualizaciones para respaldar tus conclusiones"
            ]
        }
    )
    
    # 5. Practical Example Section
    st.header("💡 Ejemplo Práctico: Dashboard Avanzado")
    
    # Create sample data
    df = create_sample_data()
    
    # Show data overview
    st.subheader("📊 Datos de Ejemplo")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Advanced calculations
    st.subheader("🔢 Cálculos Avanzados")
    
    # Calculate advanced metrics
    df['Margen_Ganancia'] = ((df['Ventas'] - (df['Ventas'] * 0.6)) / df['Ventas'] * 100).round(2)
    df['Ingresos_Totales'] = df['Ventas'] * df['Cantidad']
    df['Eficiencia_Ventas'] = (df['Ingresos_Totales'] / df['Cantidad']).round(2)
    
    # Show calculated metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Ingresos_Totales'].sum()
        st.metric("💰 Ingresos Totales", f"${total_revenue:,.2f}")
    
    with col2:
        avg_margin = df['Margen_Ganancia'].mean()
        st.metric("📈 Margen Promedio", f"{avg_margin:.1f}%")
    
    with col3:
        total_orders = len(df)
        st.metric("📋 Total de Pedidos", f"{total_orders:,}")
    
    with col4:
        avg_efficiency = df['Eficiencia_Ventas'].mean()
        st.metric("⚡ Eficiencia Promedio", f"${avg_efficiency:.2f}")
    
    # Interactive visualizations
    st.subheader("📊 Visualizaciones Interactivas")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_sales = st.slider("Ventas Mínimas", float(df['Ventas'].min()), float(df['Ventas'].max()), float(df['Ventas'].min()))
    
    with col2:
        selected_categories = st.multiselect("Categorías", df['Categoria'].unique(), default=df['Categoria'].unique())
    
    with col3:
        selected_regions = st.multiselect("Regiones", df['Region'].unique(), default=df['Region'].unique())
    
    # Apply filters
    filtered_df = df[
        (df['Ventas'] >= min_sales) &
        (df['Categoria'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions))
    ]
    
    if not filtered_df.empty:
        # Create interactive charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by category with Plotly
            fig_category = px.bar(
                filtered_df.groupby('Categoria')['Ventas'].sum().reset_index(),
                x='Categoria',
                y='Ventas',
                title='Ventas por Categoría',
                color='Ventas',
                color_continuous_scale='viridis'
            )
            fig_category.update_layout(height=400)
            st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            # Sales by region with Plotly
            fig_region = px.pie(
                filtered_df.groupby('Region')['Ventas'].sum().reset_index(),
                values='Ventas',
                names='Region',
                title='Distribución de Ventas por Región'
            )
            fig_region.update_layout(height=400)
            st.plotly_chart(fig_region, use_container_width=True)
        
        # Time series analysis
        st.subheader("📈 Análisis de Tendencias Temporales")
        
        if 'Fecha' in filtered_df.columns:
            daily_sales = filtered_df.groupby(filtered_df['Fecha'].dt.date).agg({
                'Ventas': 'sum',
                'Ingresos_Totales': 'sum',
                'Margen_Ganancia': 'mean'
            }).reset_index()
            
            fig_trends = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Ventas Diarias', 'Margen de Ganancia Promedio'),
                vertical_spacing=0.1
            )
            
            fig_trends.add_trace(
                go.Scatter(x=daily_sales['Fecha'], y=daily_sales['Ventas'], name='Ventas'),
                row=1, col=1
            )
            
            fig_trends.add_trace(
                go.Scatter(x=daily_sales['Fecha'], y=daily_sales['Margen_Ganancia'], name='Margen'),
                row=2, col=1
            )
            
            fig_trends.update_layout(height=600, title_text="Análisis de Tendencias")
            st.plotly_chart(fig_trends, use_container_width=True)
        
        # Correlation analysis
        st.subheader("🔗 Análisis de Correlaciones")
        
        numeric_cols = ['Ventas', 'Cantidad', 'Calificacion', 'Margen_Ganancia']
        correlation_matrix = filtered_df[numeric_cols].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            title='Matriz de Correlación',
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Show correlation insights
        st.markdown("""
        **💡 Insights de Correlación:**
        - Los valores cercanos a 1 indican correlación positiva fuerte
        - Los valores cercanos a -1 indican correlación negativa fuerte
        - Los valores cercanos a 0 indican poca o ninguna correlación
        """)
    
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")
    
    # 6. Dashboard Creation Section
    st.header("🏗️ Crear tu Propio Dashboard")
    
    st.markdown("""
    Ahora puedes crear tu propio dashboard personalizado. Selecciona las métricas y visualizaciones que quieras incluir.
    """)
    
    # Dashboard configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Métricas a Mostrar")
        show_revenue = st.checkbox("💰 Ingresos Totales", value=True)
        show_margin = st.checkbox("📈 Margen de Ganancia", value=True)
        show_orders = st.checkbox("📋 Número de Pedidos", value=True)
        show_efficiency = st.checkbox("⚡ Eficiencia de Ventas", value=True)
    
    with col2:
        st.subheader("📈 Visualizaciones a Incluir")
        show_category_chart = st.checkbox("🏷️ Gráfico por Categoría", value=True)
        show_region_chart = st.checkbox("🌍 Gráfico por Región", value=True)
        show_trends = st.checkbox("📈 Análisis de Tendencias", value=True)
        show_correlation = st.checkbox("🔗 Matriz de Correlación", value=True)
    
    # Generate custom dashboard
    if st.button("🚀 Generar Dashboard Personalizado", type="primary"):
        st.subheader("🎯 Tu Dashboard Personalizado")
        
        # Show selected metrics
        if any([show_revenue, show_margin, show_orders, show_efficiency]):
            st.markdown("### 📊 Métricas Clave")
            
            metrics_cols = []
            if show_revenue:
                metrics_cols.append(("💰 Ingresos Totales", f"${filtered_df['Ingresos_Totales'].sum():,.2f}"))
            if show_margin:
                metrics_cols.append(("📈 Margen Promedio", f"{filtered_df['Margen_Ganancia'].mean():.1f}%"))
            if show_orders:
                metrics_cols.append(("📋 Total de Pedidos", f"{len(filtered_df):,}"))
            if show_efficiency:
                metrics_cols.append(("⚡ Eficiencia Promedio", f"${filtered_df['Eficiencia_Ventas'].mean():.2f}"))
            
            # Create columns for metrics
            cols = st.columns(len(metrics_cols))
            for i, (label, value) in enumerate(metrics_cols):
                with cols[i]:
                    st.metric(label, value)
        
        # Show selected visualizations
        if any([show_category_chart, show_region_chart, show_trends, show_correlation]):
            st.markdown("### 📈 Visualizaciones")
            
            if show_category_chart:
                st.plotly_chart(fig_category, use_container_width=True)
            
            if show_region_chart:
                st.plotly_chart(fig_region, use_container_width=True)
            
            if show_trends and 'Fecha' in filtered_df.columns:
                st.plotly_chart(fig_trends, use_container_width=True)
            
            if show_correlation:
                st.plotly_chart(fig_corr, use_container_width=True)
    
    # 7. Quiz Section
    st.header("🧠 Quiz de Comprensión")
    
    st.markdown("""
    Responde estas preguntas para verificar que entiendes los conceptos avanzados del nivel.
    """)
    
    # Quiz questions
    quiz_questions = [
        {
            "question": "¿Qué es un dashboard?",
            "options": [
                "Un gráfico individual",
                "Una colección de visualizaciones y métricas organizadas",
                "Una tabla de datos",
                "Un cálculo matemático"
            ],
            "correct": 1
        },
        {
            "question": "¿Por qué son importantes las visualizaciones interactivas?",
            "options": [
                "Porque se ven más bonitas",
                "Porque permiten explorar los datos de manera más profunda",
                "Porque son más fáciles de crear",
                "Porque ocupan menos espacio"
            ],
            "correct": 1
        },
        {
            "question": "¿Qué son los insights en análisis de datos?",
            "options": [
                "Solo los números",
                "Descubrimientos importantes que pueden llevar a acciones valiosas",
                "Los gráficos",
                "Las fórmulas matemáticas"
            ],
            "correct": 1
        }
    ]
    
    # Initialize quiz state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    
    # Display quiz
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**Pregunta {i+1}:** {q['question']}")
        
        answer = st.radio(
            f"Selecciona la respuesta correcta:",
            q['options'],
            key=f"quiz_{i}",
            label_visibility="collapsed"
        )
        
        st.session_state.quiz_answers[i] = q['options'].index(answer)
    
    # Quiz submission
    if st.button("📝 Enviar Respuestas", type="primary"):
        correct_answers = 0
        total_questions = len(quiz_questions)
        
        for i, q in enumerate(quiz_questions):
            if st.session_state.quiz_answers.get(i) == q['correct']:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100
        
        if score >= 80:
            st.success(f"🎉 ¡Excelente! Obtuviste {score:.0f}% - ¡Has completado todos los niveles exitosamente!")
            
            # Save progress
            if save_level_progress(user['id'], 'nivel4', True):
                st.session_state.quiz_completed = True
                st.balloons()
        else:
            st.warning(f"📚 Obtuviste {score:.0f}%. Necesitas al menos 80% para completar el nivel. ¡Sigue estudiando!")
    
    # Show completion status
    if st.session_state.get('quiz_completed', False):
        st.success("🎉 ¡Felicidades! Has completado todos los niveles del curso. ¡Eres un experto en análisis de datos!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Volver al Inicio", type="primary"):
                st.switch_page("Inicio.py")
        with col2:
            if st.button("📊 Crear Dashboard", type="primary"):
                st.switch_page("pages/08_Dashboard_Blanco.py")
    
    # 8. Navigation
    st.markdown("---")
    st.header("🧭 Navegación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬅️ Nivel 3", use_container_width=True):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col2:
        if st.button("🏠 Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col3:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")
    
    with col4:
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/08_Dashboard_Blanco.py")

if __name__ == "__main__":
    main()
