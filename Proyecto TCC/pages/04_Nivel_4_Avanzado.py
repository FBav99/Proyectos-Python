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
from utils.learning.level_components import create_progression_summary, create_level_preview, create_data_quality_insight, create_achievement_display
from utils.learning.level_data import get_data_progression_info
from utils.ui import auth_ui
from utils.ui.icon_system import get_icon, replace_emojis
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

# Page config
st.set_page_config(
    page_title="Nivel 4: Avanzado - Análisis de Datos",
    page_icon=get_icon("🚀", 20),
    layout="wide"
)

# Load CSS styling for level pages
st.markdown(load_level_styles(), unsafe_allow_html=True)

# Helper functions are now imported from utils.level_components and utils.level_data

@safe_main
def main():
    # Initialize sidebar with user info (always visible)
    current_user = init_sidebar()
    
    # Check if user is authenticated
    if not current_user:
        st.markdown(replace_emojis("🔐 Por favor inicia sesión para acceder a este nivel."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # Get current user
    user = current_user
    if not user or 'id' not in user:
        st.markdown(replace_emojis("❌ Error: No se pudo obtener la información del usuario."), unsafe_allow_html=True)
        if st.button("Ir al Inicio", type="primary"):
            st.switch_page("Inicio.py")
        return
    
    # 1. Title (level name and description)
    st.title(replace_emojis("🚀 Nivel 4: Avanzado"))
    st.subheader("Cálculos y Visualizaciones Avanzadas")
    
    # 2. Progress Bar (showing progress across levels)
    total_progress, completed_count, progress = get_level_progress(user['id'])
    
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/5 niveles)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Verificar que los niveles anteriores estén completados
    if not all([progress['nivel1'], progress['nivel2'], progress['nivel3']]):
        st.warning("⚠️ Primero debes completar los Niveles 1, 2 y 3 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # 3. Progression Summary
    create_progression_summary(progress)
    
    # 4. Show achievement for previous level if completed
    if progress.get('nivel3', False):
        create_achievement_display('nivel3', progress)
    
    # 5. Level Preview
    create_level_preview('nivel4')
    
    # 6. Introduction Section (what the user will learn)
    st.header(replace_emojis("🎯 ¿Qué aprenderás en este nivel?"))
    st.markdown("¡Felicidades! Has llegado al nivel más avanzado. Ahora que dominas **conceptos básicos** (Nivel 0), **preparación de datos** (Nivel 1), **filtros** (Nivel 2) y **métricas** (Nivel 3), en este nivel aprenderás a crear cálculos personalizados, generar visualizaciones interactivas y crear dashboards completos para presentar tu información de manera profesional.")
    
    # Add connection to all previous levels
    create_info_box(
        "success-box",
        replace_emojis("🎓 Resumen de tu Jornada de Aprendizaje"),
        "<p><strong>Nivel 0:</strong> Aprendiste qué son los datos y cómo se organizan<br/><strong>Nivel 1:</strong> Aprendiste a preparar y cargar datos correctamente<br/><strong>Nivel 2:</strong> Aprendiste a filtrar y organizar información<br/><strong>Nivel 3:</strong> Aprendiste a calcular métricas y KPIs<br/><strong>Nivel 4:</strong> ¡Ahora crearás dashboards profesionales!</p>"
    )
    
    # 7. Steps Section (clear, actionable instructions)
    st.header(replace_emojis("📋 Pasos para Crear Análisis Avanzados"))
    
    # Step 1
    create_step_card(
        step_number="4.1",
        title="Crear cálculos personalizados avanzados",
        description="<strong>¿Qué son los cálculos personalizados?</strong> Son fórmulas que creas tú mismo para obtener información específica que no está disponible directamente en tus datos.",
        sections={
            replace_emojis("🔢 Tipos de cálculos que puedes crear:"): [
                "<strong>Porcentajes:</strong> Qué parte del total representa algo",
                "<strong>Promedios ponderados:</strong> Promedios que dan más importancia a ciertos valores",
                "<strong>Cambios porcentuales:</strong> Cuánto aumentó o disminuyó algo",
                "<strong>Ratios y proporciones:</strong> Comparaciones entre diferentes valores"
            ],
            replace_emojis("📝 Ejemplos de fórmulas:"): [
                "<strong>Margen de ganancia:</strong> (Precio de venta - Costo) / Precio de venta × 100",
                "<strong>Porcentaje de crecimiento:</strong> (Valor actual - Valor anterior) / Valor anterior × 100",
                "<strong>Promedio ponderado:</strong> Suma de (Valor × Peso) / Suma de pesos"
            ]
        }
    )
    
    # Step 2
    create_step_card(
        step_number="4.2",
        title="Generar visualizaciones interactivas",
        description="<strong>¿Por qué visualizaciones interactivas?</strong> Los gráficos interactivos te permiten explorar los datos de manera más profunda y encontrar insights ocultos.",
        sections={
            replace_emojis("📊 Tipos de visualizaciones:"): [
                "<strong>Gráficos de línea:</strong> Para mostrar tendencias a lo largo del tiempo",
                "<strong>Gráficos de barras:</strong> Para comparar categorías",
                "<strong>Gráficos de dispersión:</strong> Para ver relaciones entre dos variables",
                "<strong>Mapas de calor:</strong> Para mostrar patrones en tablas de datos"
            ],
            replace_emojis("🎯 Características de visualizaciones interactivas:"): [
                "Zoom y panorámica para explorar detalles",
                "Tooltips que muestran información al pasar el mouse",
                "Filtros que permiten cambiar la vista de los datos",
                "Selección de elementos para análisis específicos"
            ]
        }
    )
    
    # Step 3
    create_step_card(
        step_number="4.3",
        title="Crear dashboards profesionales",
        description="<strong>¿Qué es un dashboard?</strong> Es una colección de visualizaciones y métricas organizadas de manera lógica para contar una historia con los datos.",
        sections={
            "🏗️ Elementos de un dashboard efectivo:": [
                "<strong>Métricas clave (KPIs):</strong> Los números más importantes en la parte superior",
                "<strong>Visualizaciones:</strong> Gráficos que explican las métricas",
                "<strong>Filtros:</strong> Controles para cambiar la vista de los datos",
                "<strong>Navegación:</strong> Forma de moverse entre diferentes vistas"
            ],
            replace_emojis("💡 Principios de diseño:"): [
                "Mantén el diseño limpio y sin distracciones",
                "Usa colores de manera consistente y significativa",
                "Organiza la información de más importante a menos importante",
                "Asegúrate de que sea fácil de entender para tu audiencia"
            ]
        }
    )
    
    # Step 4
    create_step_card(
        step_number="4.4",
        title="Interpretar y comunicar insights",
        description="<strong>¿Qué son los insights?</strong> Son descubrimientos importantes en los datos que pueden llevar a acciones o decisiones valiosas.",
        sections={
            replace_emojis("🔍 Cómo encontrar insights:"): [
                "Busca patrones inesperados en los datos",
                "Compara diferentes períodos o grupos",
                "Identifica valores atípicos o anomalías",
                "Conecta diferentes métricas para ver el panorama completo"
            ],
            replace_emojis("📢 Cómo comunicar insights:"): [
                "Cuenta una historia con los datos",
                "Explica qué significa cada insight para el negocio",
                "Sugiere acciones específicas basadas en los datos",
                "Usa visualizaciones para respaldar tus conclusiones"
            ]
        }
    )
    
    # 5. Practical Example Section
    st.header(replace_emojis("💡 Ejemplo Práctico: Dashboard Avanzado"))
    
    # Show data quality insight for this level
    create_data_quality_insight('nivel4', 'clean')
    
    # Create sample data
    df = create_sample_data('clean')  # Use clean data for Level 4
    
    # Show data overview
    st.subheader(replace_emojis("📊 Datos de Ejemplo"))
    
    # Show how all concepts come together
    create_info_box(
        "info-box",
        "🔗 Todos los Conceptos se Unen Aquí",
        "<p>En este nivel verás cómo todo lo que aprendiste se conecta:<br/>• <strong>Tipos de datos</strong> (Nivel 0) para entender qué columnas usar<br/>• <strong>Datos limpios</strong> (Nivel 1) para cálculos precisos<br/>• <strong>Filtros</strong> (Nivel 2) para análisis específicos<br/>• <strong>Métricas</strong> (Nivel 3) para crear KPIs avanzados<br/>• <strong>Visualizaciones</strong> (Nivel 4) para comunicar insights</p>"
    )
    
    st.dataframe(df.head(10), use_container_width=True)
    
    # Advanced calculations
    st.subheader(replace_emojis("🔢 Cálculos Avanzados"))
    
    # Calculate advanced metrics
    df['Margen_Ganancia'] = ((df['Ventas'] - (df['Ventas'] * 0.6)) / df['Ventas'] * 100).round(2)
    df['Ingresos_Totales'] = df['Ventas'] * df['Cantidad']
    df['Eficiencia_Ventas'] = (df['Ingresos_Totales'] / df['Cantidad']).round(2)
    
    # Show calculated metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Ingresos_Totales'].sum()
        st.metric(replace_emojis("💰 Ingresos Totales"), f"${total_revenue:,.2f}")
    
    with col2:
        avg_margin = df['Margen_Ganancia'].mean()
        st.metric(replace_emojis("📈 Margen Promedio"), f"{avg_margin:.1f}%")
    
    with col3:
        total_orders = len(df)
        st.metric(replace_emojis("📋 Total de Pedidos"), f"{total_orders:,}")
    
    with col4:
        avg_efficiency = df['Eficiencia_Ventas'].mean()
        st.metric("⚡ Eficiencia Promedio", f"${avg_efficiency:.2f}")
    
    # Interactive visualizations
    st.subheader(replace_emojis("📊 Visualizaciones Interactivas"))
    
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
        st.subheader(replace_emojis("📈 Análisis de Tendencias Temporales"))
        
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
        st.markdown(replace_emojis("**💡 Insights de Correlación:** - Los valores cercanos a 1 indican correlación positiva fuerte - Los valores cercanos a -1 indican correlación negativa fuerte - Los valores cercanos a 0 indican poca o ninguna correlación"), unsafe_allow_html=True)
    
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")
    
    # 6. Dashboard Creation Section
    st.header("🏗️ Crear tu Propio Dashboard")
    
    st.markdown("Ahora puedes crear tu propio dashboard personalizado. Selecciona las métricas y visualizaciones que quieras incluir.")
    
    # Dashboard configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(replace_emojis("📊 Métricas a Mostrar"))
        show_revenue = st.checkbox(replace_emojis("💰 Ingresos Totales"), value=True)
        show_margin = st.checkbox(replace_emojis("📈 Margen de Ganancia"), value=True)
        show_orders = st.checkbox(replace_emojis("📋 Número de Pedidos"), value=True)
        show_efficiency = st.checkbox("⚡ Eficiencia de Ventas", value=True)
    
    with col2:
        st.subheader(replace_emojis("📈 Visualizaciones a Incluir"))
        show_category_chart = st.checkbox("🏷️ Gráfico por Categoría", value=True)
        show_region_chart = st.checkbox("🌍 Gráfico por Región", value=True)
        show_trends = st.checkbox(replace_emojis("📈 Análisis de Tendencias"), value=True)
        show_correlation = st.checkbox("🔗 Matriz de Correlación", value=True)
    
    # Generate custom dashboard
    if st.button("🚀 Generar Dashboard Personalizado", type="primary"):
        st.subheader(replace_emojis("🎯 Tu Dashboard Personalizado"))
        
        # Show selected metrics
        if any([show_revenue, show_margin, show_orders, show_efficiency]):
            st.markdown(replace_emojis("### 📊 Métricas Clave"), unsafe_allow_html=True)
            
            metrics_cols = []
            if show_revenue:
                metrics_cols.append((f"{get_icon('💰', 20)} Ingresos Totales", f"${filtered_df['Ingresos_Totales'].sum():,.2f}"))
            if show_margin:
                metrics_cols.append((f"{get_icon('📈', 20)} Margen Promedio", f"{filtered_df['Margen_Ganancia'].mean():.1f}%"))
            if show_orders:
                metrics_cols.append((f"{get_icon('📋', 20)} Total de Pedidos", f"{len(filtered_df):,}"))
            if show_efficiency:
                metrics_cols.append(("⚡ Eficiencia Promedio", f"${filtered_df['Eficiencia_Ventas'].mean():.2f}"))
            
            # Create columns for metrics
            cols = st.columns(len(metrics_cols))
            for i, (label, value) in enumerate(metrics_cols):
                with cols[i]:
                    st.metric(label, value)
        
        # Show selected visualizations
        if any([show_category_chart, show_region_chart, show_trends, show_correlation]):
            st.markdown(replace_emojis("### 📈 Visualizaciones"), unsafe_allow_html=True)
            
            if show_category_chart:
                st.plotly_chart(fig_category, use_container_width=True)
            
            if show_region_chart:
                st.plotly_chart(fig_region, use_container_width=True)
            
            if show_trends and 'Fecha' in filtered_df.columns:
                st.plotly_chart(fig_trends, use_container_width=True)
            
            if show_correlation:
                st.plotly_chart(fig_corr, use_container_width=True)
    
    # 7. Quiz Section - Must complete quiz before marking level as complete
    st.header("🧠 Quiz del Nivel")
    st.markdown("### Pon a prueba tus conocimientos")
    st.info(replace_emojis("📝 **Importante:** Debes aprobar el quiz (al menos 3 de 5 preguntas correctas) antes de poder marcar el nivel como completado."))
    
    # Check if user passed the quiz
    quiz_passed = st.session_state.get(f'quiz_nivel4_passed', False)
    
    if quiz_passed:
        st.markdown(replace_emojis("✅ ¡Has aprobado el quiz! Ahora puedes marcar el nivel como completado."), unsafe_allow_html=True)
    else:
        # Show quiz using unified system
        from core.quiz_system import create_quiz
        create_quiz('nivel4', user['username'])
        
        # Check if quiz was just completed and passed
        if st.session_state.get(f'quiz_nivel4_completed', False):
            score = st.session_state.get(f'quiz_nivel4_score', 0)
            if score >= 3:
                st.session_state[f'quiz_nivel4_passed'] = True
                st.rerun()
    
    st.divider()
    
    # 8. Navigation or next steps
    st.header(replace_emojis("✅ Verificación del Nivel"))
    
    # Only allow marking as complete if quiz is passed
    if not quiz_passed:
        st.warning("⚠️ Debes aprobar el quiz antes de poder marcar el nivel como completado.")
        nivel4_completed = False
    else:
        nivel4_completed = st.checkbox(
            "He completado todos los pasos del Nivel 4 y aprobé el quiz",
            value=st.session_state.get('nivel4_completed', False),
            key='nivel4_checkbox'
        )
    
    if nivel4_completed:
        # Save progress to database
        user_id = user['id']
        if save_level_progress(user_id, 'nivel4', True):
            st.session_state['nivel4_completed'] = True
        else:
            st.markdown(replace_emojis("❌ Error al guardar el progreso. Intenta de nuevo."), unsafe_allow_html=True)
            return
        
        # Show final achievement
        create_achievement_display('nivel4', progress)
        
        # Show final progression summary
        create_progression_summary(progress)
        
        st.markdown(replace_emojis("🎉 ¡Felicidades! Has completado todos los niveles del curso. ¡Eres un experto en análisis de datos!"), unsafe_allow_html=True)
        
        st.markdown(replace_emojis("### 📝 Antes de continuar, nos gustaría conocer tu opinión sobre este nivel y la experiencia general."), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Encuesta del Nivel 4", type="primary"):
                st.session_state.survey_level = 'nivel4'
                st.switch_page("pages/99_Survey_Nivel.py")
        with col2:
            if st.button("🏆 Encuesta Final", type="primary"):
                st.switch_page("pages/99_Survey_Final.py")
        with col3:
            if st.button("📊 Crear Dashboard", type="secondary"):
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
