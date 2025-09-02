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
        background: linear-gradient(90deg, #f8f9fa, #ffffff);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .advanced-demo {
        background: #f3e5f5;
        border: 1px solid #e1bee7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .formula-box {
        background: #e8f5e8;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .completion-checkbox {
        background: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    st.markdown('<h1 class="level-header">🚀 Nivel 4: Cálculos y Visualizaciones</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Crear Análisis Personalizados y Gráficos</h2>', unsafe_allow_html=True)
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/4 niveles)")
    
    # Verificar que los niveles anteriores estén completados
    if not all([progress['nivel1'], progress['nivel2'], progress['nivel3']]):
        st.warning("⚠️ Primero debes completar los Niveles 1, 2 y 3 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # Información introductoria
    st.markdown("""
    <div class="info-box">
        <h3>🎯 ¿Qué aprenderás en este nivel?</h3>
        <p>En este nivel aprenderás a crear cálculos personalizados, generar visualizaciones interactivas 
        y crear dashboards completos para presentar tu información de manera profesional.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasos del nivel
    st.markdown("## 📋 Pasos para Crear Análisis Avanzados")
    
    # Paso 1
    st.markdown("""
    <div class="step-box">
        <h3>1️⃣ Crear cálculos personalizados avanzados</h3>
        <p><strong>¿Qué son los cálculos personalizados?</strong> Son fórmulas que creas tú mismo para 
        obtener información específica que no está disponible directamente en tus datos.</p>
        
        <h4>🔢 Tipos de cálculos que puedes crear:</h4>
        <ul>
            <li><strong>Porcentajes:</strong> Qué parte del total representa algo</li>
            <li><strong>Promedios ponderados:</strong> Promedios que dan más importancia a ciertos valores</li>
            <li><strong>Cambios porcentuales:</strong> Cuánto aumentó o disminuyó algo</li>
            <li><strong>Ratios y proporciones:</strong> Comparaciones entre diferentes valores</li>
        </ul>
        
        <h4>📝 Ejemplos de fórmulas:</h4>
        <ul>
            <li><strong>Margen de ganancia:</strong> (Precio de venta - Costo) / Precio de venta × 100</li>
            <li><strong>Porcentaje de crecimiento:</strong> (Valor actual - Valor anterior) / Valor anterior × 100</li>
            <li><strong>Promedio ponderado:</strong> Suma de (Valor × Peso) / Suma de pesos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 2
    st.markdown("""
    <div class="step-box">
        <h3>2️⃣ Generar visualizaciones interactivas</h3>
        <p><strong>¿Qué son las visualizaciones?</strong> Son gráficos y diagramas que convierten 
        números y datos en imágenes fáciles de entender.</p>
        
        <h4>📊 Tipos de gráficos útiles:</h4>
        <ul>
            <li><strong>Gráficos de línea:</strong> Para mostrar tendencias a lo largo del tiempo</li>
            <li><strong>Gráficos de barras:</strong> Para comparar diferentes categorías</li>
            <li><strong>Gráficos circulares:</strong> Para mostrar partes de un todo</li>
            <li><strong>Gráficos de dispersión:</strong> Para ver relaciones entre dos variables</li>
        </ul>
        
        <h4>🎨 Características de gráficos interactivos:</h4>
        <ul>
            <li><strong>Zoom:</strong> Puedes acercarte a partes específicas del gráfico</li>
            <li><strong>Hover:</strong> Al pasar el mouse ves información detallada</li>
            <li><strong>Filtros:</strong> Puedes mostrar u ocultar ciertos datos</li>
            <li><strong>Animaciones:</strong> Los gráficos se actualizan cuando cambias los datos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 3
    st.markdown("""
    <div class="step-box">
        <h3>3️⃣ Analizar tendencias temporales</h3>
        <p><strong>¿Qué son las tendencias temporales?</strong> Son patrones que se repiten 
        en el tiempo, como ventas que suben en diciembre o visitas que bajan los fines de semana.</p>
        
        <h4>⏰ Tipos de patrones temporales:</h4>
        <ul>
            <li><strong>Patrones diarios:</strong> Cambios que ocurren cada día (ej: más ventas por la tarde)</li>
            <li><strong>Patrones semanales:</strong> Cambios que ocurren cada semana (ej: menos actividad los domingos)</li>
            <li><strong>Patrones mensuales:</strong> Cambios que ocurren cada mes (ej: facturación al inicio del mes)</li>
            <li><strong>Patrones estacionales:</strong> Cambios que ocurren cada temporada (ej: más ventas en verano)</li>
        </ul>
        
        <h4>🔍 Cómo identificar tendencias:</h4>
        <ul>
            <li><strong>Observa gráficos de línea:</strong> Las líneas te muestran patrones visualmente</li>
            <li><strong>Compara períodos:</strong> Este mes vs. el mismo mes del año pasado</li>
            <li><strong>Busca repeticiones:</strong> ¿Se repite algo cada cierto tiempo?</li>
            <li><strong>Analiza causas:</strong> ¿Qué eventos causan los cambios?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 4
    st.markdown("""
    <div class="step-box">
        <h3>4️⃣ Crear dashboards completos</h3>
        <p><strong>¿Qué es un dashboard completo?</strong> Es una página o pantalla que muestra 
        todas las métricas importantes de tu negocio en un solo lugar, organizadas de manera clara.</p>
        
        <h4>📱 Elementos de un dashboard completo:</h4>
        <ul>
            <li><strong>Resumen ejecutivo:</strong> Los números más importantes en la parte superior</li>
            <li><strong>Métricas detalladas:</strong> Desglose de cada área del negocio</li>
            <li><strong>Gráficos interactivos:</strong> Para explorar los datos en detalle</li>
            <li><strong>Alertas y notificaciones:</strong> Para avisarte cuando algo necesita atención</li>
            <li><strong>Navegación fácil:</strong> Para moverse entre diferentes secciones</li>
        </ul>
        
        <h4>🎯 Beneficios de un dashboard completo:</h4>
        <ul>
            <li><strong>Vista completa:</strong> Ves todo lo importante en un solo lugar</li>
            <li><strong>Toma de decisiones:</strong> Tienes toda la información necesaria</li>
            <li><strong>Comunicación:</strong> Puedes mostrar a otros el estado del negocio</li>
            <li><strong>Identificación de problemas:</strong> Ves rápidamente qué necesita atención</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 5
    st.markdown("""
    <div class="step-box">
        <h3>5️⃣ Exportar resultados y reportes</h3>
        <p><strong>¿Por qué exportar?</strong> Los reportes te permiten compartir información 
        con otras personas, guardar análisis para el futuro, y presentar resultados profesionalmente.</p>
        
        <h4>📄 Formatos de exportación:</h4>
        <ul>
            <li><strong>PDF:</strong> Para reportes formales y presentaciones</li>
            <li><strong>Excel:</strong> Para análisis detallados y cálculos</li>
            <li><strong>Imágenes:</strong> Para usar en presentaciones o documentos</li>
            <li><strong>Enlaces web:</strong> Para compartir dashboards interactivos</li>
        </ul>
        
        <h4>📋 Elementos de un reporte profesional:</h4>
        <ul>
            <li><strong>Título y fecha:</strong> Identificación clara del reporte</li>
            <li><strong>Resumen ejecutivo:</strong> Conclusiones principales</li>
            <li><strong>Métricas clave:</strong> Los números más importantes</li>
            <li><strong>Gráficos y tablas:</strong> Visualización de los datos</li>
            <li><strong>Conclusiones y recomendaciones:</strong> Qué hacer con la información</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Ejemplo práctico
    st.markdown("## 🎯 Ejemplo Práctico")
    
    st.markdown("""
    <div class="info-box">
        <h3>📊 Vamos a crear cálculos personalizados y visualizaciones</h3>
        <p>Te mostraré cómo crear fórmulas personalizadas y diferentes tipos de gráficos para analizar tus datos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear datos de ejemplo
    df = create_sample_data()
    
    st.markdown("### 📁 Datos de ejemplo (Ventas de una tienda)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Cálculos personalizados
    st.markdown("### 🔢 Cálculos Personalizados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 Cálculos de Rentabilidad:**")
        
        # Calcular métricas personalizadas
        df['Margen_Ganancia'] = ((df['Ventas'] - (df['Ventas'] * 0.6)) / df['Ventas'] * 100).round(2)
        df['ROI'] = (df['Ingresos'] / (df['Ventas'] * 0.6) * 100).round(2)
        
        st.markdown("**📊 Margen de Ganancia:**")
        st.markdown("""
        <div class="formula-box">
        Margen = (Precio de Venta - Costo) / Precio de Venta × 100
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Margen promedio", f"{df['Margen_Ganancia'].mean():.1f}%")
        st.metric("Margen máximo", f"{df['Margen_Ganancia'].max():.1f}%")
        st.metric("Margen mínimo", f"{df['Margen_Ganancia'].min():.1f}%")
    
    with col2:
        st.markdown("**📈 Cálculos de Rendimiento:**")
        
        st.markdown("**📊 ROI (Retorno de Inversión):**")
        st.markdown("""
        <div class="formula-box">
        ROI = (Ingresos - Costos) / Costos × 100
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("ROI promedio", f"{df['ROI'].mean():.1f}%")
        st.metric("ROI máximo", f"{df['ROI'].max():.1f}%")
        st.metric("ROI mínimo", f"{df['ROI'].min():.1f}%")
        
        st.markdown("**🎯 Análisis:**")
        if df['ROI'].mean() > 100:
            st.success("✅ Excelente retorno de inversión")
        elif df['ROI'].mean() > 50:
            st.info("ℹ️ Buen retorno de inversión")
        else:
            st.warning("⚠️ Bajo retorno de inversión")
    
    # Visualizaciones
    st.markdown("### 📊 Visualizaciones Interactivas")
    
    # Gráfico de tendencias temporales
    st.markdown("**📈 Tendencia de Ventas por Mes:**")
    
    df['Mes'] = df['Fecha'].dt.to_period('M')
    ventas_mensuales = df.groupby('Mes')['Ventas'].sum().reset_index()
    ventas_mensuales['Mes'] = ventas_mensuales['Mes'].astype(str)
    
    fig_line = px.line(
        ventas_mensuales, 
        x='Mes', 
        y='Ventas',
        title='Tendencia de Ventas Mensuales',
        labels={'Ventas': 'Ventas ($)', 'Mes': 'Mes'},
        markers=True
    )
    fig_line.update_layout(height=400)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Gráfico de barras por categoría
    st.markdown("**🏷️ Ventas por Categoría:**")
    
    ventas_categoria = df.groupby('Categoria')['Ventas'].sum().sort_values(ascending=False)
    
    fig_bar = px.bar(
        x=ventas_categoria.index,
        y=ventas_categoria.values,
        title='Ventas Totales por Categoría',
        labels={'x': 'Categoría', 'y': 'Ventas ($)'},
        color=ventas_categoria.values,
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Gráfico de dispersión
    st.markdown("**🔍 Relación entre Ventas y Calificación:**")
    
    fig_scatter = px.scatter(
        df,
        x='Ventas',
        y='Calificacion',
        color='Categoria',
        title='Relación: Ventas vs Calificación del Cliente',
        labels={'Ventas': 'Ventas ($)', 'Calificacion': 'Calificación (1-5)'},
        size='Cantidad',
        hover_data=['Region', 'Fecha']
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Dashboard completo
    st.markdown("### 📱 Dashboard Completo")
    
    st.markdown("""
    <div class="advanced-demo">
        <h3>🎯 Resumen Ejecutivo</h3>
        <p>Vista completa de las métricas más importantes de tu negocio:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Ventas Totales", 
            f"${df['Ventas'].sum():,.0f}",
            f"{((df['Ventas'].sum() - df['Ventas'].mean() * len(df)) / (df['Ventas'].mean() * len(df)) * 100):+.1f}%"
        )
    
    with col2:
        st.metric(
            "📊 Transacciones", 
            len(df),
            f"{len(df) - len(df) // 2:+d}"
        )
    
    with col3:
        st.metric(
            "⭐ Satisfacción", 
            f"{df['Calificacion'].mean():.1f}/5",
            f"{df['Calificacion'].mean() - 3:+.1f}"
        )
    
    with col4:
        st.metric(
            "🎯 Margen Promedio", 
            f"{df['Margen_Ganancia'].mean():.1f}%",
            f"{df['Margen_Ganancia'].mean() - 40:+.1f}%"
        )
    
    # Análisis por región
    st.markdown("**🌍 Análisis por Región:**")
    
    analisis_region = df.groupby('Region').agg({
        'Ventas': ['sum', 'mean', 'count'],
        'Calificacion': 'mean',
        'Margen_Ganancia': 'mean'
    }).round(2)
    
    analisis_region.columns = ['Ventas_Total', 'Ventas_Promedio', 'Transacciones', 'Calificacion_Promedio', 'Margen_Promedio']
    analisis_region = analisis_region.sort_values('Ventas_Total', ascending=False)
    
    st.dataframe(analisis_region, use_container_width=True)
    
    # Consejos importantes
    st.markdown("## 💡 Consejos Importantes")
    
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Errores comunes a evitar:</h3>
        <ul>
            <li><strong>Gráficos muy complejos:</strong> Mantén las visualizaciones simples y claras</li>
            <li><strong>Ignorar el contexto:</strong> Siempre explica qué significan los números</li>
            <li><strong>No validar fórmulas:</strong> Verifica que tus cálculos sean correctos</li>
            <li><strong>Exceso de información:</strong> No sobrecargues los dashboards con demasiados datos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>✅ Buenas prácticas:</h3>
        <ul>
            <li><strong>Usa colores consistentes:</strong> Mantén la misma paleta de colores en todos los gráficos</li>
            <li><strong>Incluye títulos claros:</strong> Cada gráfico debe tener un título que explique qué muestra</li>
            <li><strong>Agrega contexto:</strong> Incluye notas que expliquen qué significan los números</li>
            <li><strong>Prueba con usuarios:</strong> Asegúrate de que otros entiendan tus visualizaciones</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Actividad práctica
    st.markdown("## 🎯 Actividad Práctica")
    
    st.markdown("""
    <div class="step-box">
        <h3>📝 Ejercicio para practicar:</h3>
        <p>1. <strong>Crea cálculos personalizados:</strong> Calcula el margen de ganancia y ROI de tus productos</p>
        <p>2. <strong>Genera visualizaciones:</strong> Crea gráficos de línea, barras y dispersión</p>
        <p>3. <strong>Analiza tendencias:</strong> Identifica patrones temporales en tus datos</p>
        <p>4. <strong>Construye un dashboard:</strong> Organiza todas las métricas en una sola vista</p>
        <p>5. <strong>Exporta tu reporte:</strong> Guarda tu análisis en PDF o Excel</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificación de completado
    st.markdown("## ✅ Verificación del Nivel")
    
    nivel4_completed = st.checkbox(
        "He completado todos los pasos del Nivel 4",
        value=st.session_state.get('nivel4_completed', False),
        key='nivel4_checkbox'
    )
    
    if nivel4_completed:
        st.session_state['nivel4_completed'] = True
        st.markdown("""
        <div class="completion-checkbox">
            <h3>🎉 ¡Felicidades! Has completado el Nivel 4</h3>
            <p>Ahora sabes cómo crear cálculos personalizados, visualizaciones interactivas y dashboards completos. 
            ¡Has completado todos los niveles del curso!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar mensaje de finalización
        st.markdown("### 🏆 ¡Has Completado el Curso!")
        st.markdown("""
        <div class="success-box">
            <h3>🌟 Resumen de lo que has aprendido:</h3>
            <ul>
                <li><strong>Nivel 1:</strong> Preparar y cargar datos correctamente</li>
                <li><strong>Nivel 2:</strong> Organizar y filtrar información</li>
                <li><strong>Nivel 3:</strong> Entender métricas y KPIs</li>
                <li><strong>Nivel 4:</strong> Crear análisis personalizados y visualizaciones</li>
            </ul>
            <p><strong>¡Ahora tienes las habilidades básicas para analizar datos y tomar decisiones informadas!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Volver al Inicio", type="primary"):
            st.switch_page("Inicio.py")
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>📚 ¿Quieres saber más?</h3>
        <p>Este nivel está basado en principios de visualización de datos y mejores prácticas de análisis estadístico básico. 
        Si quieres profundizar en los fundamentos teóricos, consulta la documentación del proyecto.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
