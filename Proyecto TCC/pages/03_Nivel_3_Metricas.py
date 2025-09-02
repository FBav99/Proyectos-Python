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
    
    .metric-demo {
        background: #e8f5e8;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
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
    st.markdown('<h1 class="level-header">📊 Nivel 3: Entender Métricas</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">KPIs y Análisis de Rendimiento</h2>', unsafe_allow_html=True)
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/4 niveles)")
    
    # Verificar que los niveles anteriores estén completados
    if not progress['nivel1'] or not progress['nivel2']:
        st.warning("⚠️ Primero debes completar los Niveles 1 y 2 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # Información introductoria
    st.markdown("""
    <div class="info-box">
        <h3>🎯 ¿Qué aprenderás en este nivel?</h3>
        <p>En este nivel aprenderás a entender qué son las métricas y KPIs, cómo interpretarlas y 
        cómo usarlas para tomar mejores decisiones basadas en datos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasos del nivel
    st.markdown("## 📋 Pasos para Entender Métricas y KPIs")
    
    # Paso 1
    st.markdown("""
    <div class="step-box">
        <h3>1️⃣ Entender qué son las métricas y KPIs</h3>
        <p><strong>¿Qué son las métricas?</strong> Las métricas son números que te dicen algo importante 
        sobre tu negocio o actividad. Son como "termómetros" que miden el estado de las cosas.</p>
        
        <h4>📊 Tipos de métricas:</h4>
        <ul>
            <li><strong>Métricas de cantidad:</strong> Cuántos productos vendiste, cuántos clientes tienes</li>
            <li><strong>Métricas de dinero:</strong> Cuánto dinero ganaste, cuánto gastaste</li>
            <li><strong>Métricas de tiempo:</strong> Cuánto tiempo tardas en hacer algo</li>
            <li><strong>Métricas de calidad:</strong> Qué tan bien funciona algo, qué tan satisfechos están los clientes</li>
        </ul>
        
        <h4>🎯 ¿Qué son los KPIs?</h4>
        <p><strong>KPI</strong> significa "Indicador Clave de Rendimiento". Son las métricas más importantes 
        que te ayudan a saber si tu negocio va bien o mal.</p>
        
        <h4>✅ Ejemplos de KPIs comunes:</h4>
        <ul>
            <li><strong>Ventas totales:</strong> Cuánto dinero generaste en total</li>
            <li><strong>Número de clientes:</strong> Cuántas personas compran de ti</li>
            <li><strong>Satisfacción del cliente:</strong> Qué tan contentos están con tu servicio</li>
            <li><strong>Tiempo de entrega:</strong> Cuánto tardas en entregar un producto</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 2
    st.markdown("""
    <div class="step-box">
        <h3>2️⃣ Interpretar métricas clave de negocio</h3>
        <p><strong>¿Por qué es importante interpretar?</strong> Los números por sí solos no te dicen mucho. 
        Necesitas entender qué significan y cómo usarlos para tomar decisiones.</p>
        
        <h4>🔍 Cómo interpretar métricas:</h4>
        <ul>
            <li><strong>Compara con el pasado:</strong> ¿Son mejores o peores que antes?</li>
            <li><strong>Compara con metas:</strong> ¿Estás alcanzando tus objetivos?</li>
            <li><strong>Busca patrones:</strong> ¿Hay tendencias que se repiten?</li>
            <li><strong>Identifica problemas:</strong> ¿Qué números te preocupan?</li>
        </ul>
        
        <h4>📈 Ejemplos de interpretación:</h4>
        <ul>
            <li><strong>Ventas bajas:</strong> Podría ser temporada baja, problema de precios, o competencia</li>
            <li><strong>Clientes insatisfechos:</strong> Podría ser problema de calidad, servicio, o comunicación</li>
            <li><strong>Gastos altos:</strong> Podría ser inversión necesaria o desperdicio</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 3
    st.markdown("""
    <div class="step-box">
        <h3>3️⃣ Analizar tendencias y patrones</h3>
        <p><strong>¿Qué son las tendencias?</strong> Son cambios que ocurren con el tiempo. 
        Pueden ser hacia arriba (mejorando), hacia abajo (empeorando), o estables.</p>
        
        <h4>📊 Tipos de tendencias:</h4>
        <ul>
            <li><strong>Tendencia ascendente:</strong> Los números van subiendo (ej: más ventas cada mes)</li>
            <li><strong>Tendencia descendente:</strong> Los números van bajando (ej: menos clientes)</li>
            <li><strong>Tendencia estable:</strong> Los números se mantienen igual</li>
            <li><strong>Tendencia estacional:</strong> Los números suben y bajan en ciertos períodos</li>
        </ul>
        
        <h4>🔍 Cómo identificar patrones:</h4>
        <ul>
            <li><strong>Observa gráficos:</strong> Las líneas y barras te muestran patrones visualmente</li>
            <li><strong>Compara períodos:</strong> Este mes vs. el mes pasado, este año vs. el año pasado</li>
            <li><strong>Busca repeticiones:</strong> ¿Se repite algo cada semana, mes, o temporada?</li>
            <li><strong>Analiza causas:</strong> ¿Qué eventos causan los cambios?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 4
    st.markdown("""
    <div class="step-box">
        <h3>4️⃣ Usar métricas para tomar decisiones</h3>
        <p><strong>¿Cómo ayudan las métricas?</strong> Las métricas te dan información objetiva 
        para tomar decisiones más inteligentes en lugar de adivinar.</p>
        
        <h4>🎯 Decisiones basadas en métricas:</h4>
        <ul>
            <li><strong>Invertir más:</strong> Si las métricas muestran que algo funciona bien</li>
            <li><strong>Cambiar estrategia:</strong> Si las métricas muestran que algo no funciona</li>
            <li><strong>Establecer metas:</strong> Basándote en lo que has logrado antes</li>
            <li><strong>Identificar problemas:</strong> Antes de que se vuelvan graves</li>
        </ul>
        
        <h4>💡 Ejemplos prácticos:</h4>
        <ul>
            <li><strong>Si las ventas bajan:</strong> Podrías revisar precios, promociones, o calidad</li>
            <li><strong>Si los clientes están insatisfechos:</strong> Podrías mejorar el servicio o productos</li>
            <li><strong>Si los gastos suben mucho:</strong> Podrías revisar dónde se va el dinero</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 5
    st.markdown("""
    <div class="step-box">
        <h3>5️⃣ Crear dashboards de rendimiento</h3>
        <p><strong>¿Qué es un dashboard?</strong> Es una pantalla que muestra las métricas más importantes 
        de tu negocio en un solo lugar, como un "tablero de control".</p>
        
        <h4>📱 Elementos de un dashboard:</h4>
        <ul>
            <li><strong>Números grandes:</strong> Las métricas más importantes (ventas, clientes, etc.)</li>
            <li><strong>Gráficos:</strong> Para mostrar tendencias y comparaciones</li>
            <li><strong>Tablas:</strong> Para mostrar datos detallados</li>
            <li><strong>Alertas:</strong> Para avisarte cuando algo necesita atención</li>
        </ul>
        
        <h4>✅ Beneficios de un dashboard:</h4>
        <ul>
            <li><strong>Vista rápida:</strong> Ves todo lo importante en un vistazo</li>
            <li><strong>Detección temprana:</strong> Identificas problemas antes de que empeoren</li>
            <li><strong>Comunicación:</strong> Puedes mostrar a otros cómo va el negocio</li>
            <li><strong>Enfoque:</strong> Te concentras en lo que realmente importa</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Ejemplo práctico
    st.markdown("## 🎯 Ejemplo Práctico")
    
    st.markdown("""
    <div class="info-box">
        <h3>📊 Vamos a analizar métricas usando datos de ventas</h3>
        <p>Te mostraré cómo interpretar diferentes métricas y qué decisiones podrías tomar basándote en ellas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear datos de ejemplo
    df = create_sample_data()
    
    st.markdown("### 📁 Datos de ejemplo (Ventas de una tienda)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Análisis de métricas
    st.markdown("### 📊 Análisis de Métricas Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 Métricas de Ventas:**")
        
        # Calcular métricas
        ventas_totales = df['Ventas'].sum()
        ventas_promedio = df['Ventas'].mean()
        ventas_max = df['Ventas'].max()
        ventas_min = df['Ventas'].min()
        
        st.metric("Ventas totales", f"${ventas_totales:,.0f}")
        st.metric("Ventas promedio", f"${ventas_promedio:,.0f}")
        st.metric("Venta más alta", f"${ventas_max:,.0f}")
        st.metric("Venta más baja", f"${ventas_min:,.0f}")
        
        st.markdown("**📈 Análisis:**")
        if ventas_promedio > 1000:
            st.success("✅ Las ventas están por encima del promedio esperado")
        else:
            st.warning("⚠️ Las ventas están por debajo del promedio esperado")
    
    with col2:
        st.markdown("**👥 Métricas de Clientes:**")
        
        # Calcular métricas de clientes
        total_registros = len(df)
        categorias_unicas = df['Categoria'].nunique()
        regiones_unicas = df['Region'].nunique()
        calificacion_promedio = df['Calificacion'].mean()
        
        st.metric("Total de transacciones", total_registros)
        st.metric("Categorías de productos", categorias_unicas)
        st.metric("Regiones atendidas", regiones_unicas)
        st.metric("Calificación promedio", f"{calificacion_promedio:.1f}/5")
        
        st.markdown("**📊 Análisis:**")
        if calificacion_promedio >= 4:
            st.success("✅ Los clientes están muy satisfechos")
        elif calificacion_promedio >= 3:
            st.info("ℹ️ Los clientes están moderadamente satisfechos")
        else:
            st.warning("⚠️ Los clientes no están satisfechos")
    
    # Análisis de tendencias
    st.markdown("### 📈 Análisis de Tendencias")
    
    # Agrupar por mes para ver tendencias
    df['Mes'] = df['Fecha'].dt.to_period('M')
    ventas_mensuales = df.groupby('Mes')['Ventas'].sum().reset_index()
    ventas_mensuales['Mes'] = ventas_mensuales['Mes'].astype(str)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Ventas por Mes:**")
        st.dataframe(ventas_mensuales, use_container_width=True)
        
        # Calcular tendencia
        if len(ventas_mensuales) > 1:
            primer_mes = ventas_mensuales.iloc[0]['Ventas']
            ultimo_mes = ventas_mensuales.iloc[-1]['Ventas']
            cambio = ((ultimo_mes - primer_mes) / primer_mes) * 100
            
            st.markdown(f"**📊 Cambio total:** {cambio:+.1f}%")
            
            if cambio > 0:
                st.success("✅ Tendencia positiva - las ventas están subiendo")
            elif cambio < 0:
                st.warning("⚠️ Tendencia negativa - las ventas están bajando")
            else:
                st.info("ℹ️ Tendencia estable - las ventas se mantienen igual")
    
    with col2:
        st.markdown("**🏷️ Ventas por Categoría:**")
        ventas_categoria = df.groupby('Categoria')['Ventas'].sum().sort_values(ascending=False)
        
        # Mostrar top categorías
        st.markdown("**Top 3 categorías:**")
        for i, (cat, venta) in enumerate(ventas_categoria.head(3).items(), 1):
            st.markdown(f"{i}. **{cat}**: ${venta:,.0f}")
        
        # Análisis de la mejor categoría
        mejor_categoria = ventas_categoria.index[0]
        mejor_venta = ventas_categoria.iloc[0]
        st.markdown(f"**🎯 Mejor categoría:** {mejor_categoria}")
        st.markdown(f"**💰 Ventas:** ${mejor_venta:,.0f}")
    
    # Dashboard simple
    st.markdown("### 📱 Dashboard de Rendimiento")
    
    st.markdown("""
    <div class="metric-demo">
        <h3>🎯 KPIs Principales</h3>
        <p>Estos son los indicadores más importantes para monitorear el rendimiento de tu negocio:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs en tarjetas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>💰 Ventas Totales</h4>
            <h2>${ventas_totales:,.0f}</h2>
            <p>Ingresos generados</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>📊 Transacciones</h4>
            <h2>{total_registros}</h2>
            <p>Total de ventas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>⭐ Satisfacción</h4>
            <h2>{calificacion_promedio:.1f}/5</h2>
            <p>Calificación clientes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>🏷️ Categorías</h4>
            <h2>{categorias_unicas}</h2>
            <p>Productos ofrecidos</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Consejos importantes
    st.markdown("## 💡 Consejos Importantes")
    
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Errores comunes a evitar:</h3>
        <ul>
            <li><strong>Enfocarse solo en una métrica:</strong> Mira varias métricas juntas para tener una visión completa</li>
            <li><strong>Ignorar el contexto:</strong> Los números pueden cambiar por razones temporales o estacionales</li>
            <li><strong>No establecer metas:</strong> Sin metas, no sabes si los números son buenos o malos</li>
            <li><strong>Reaccionar demasiado rápido:</strong> Espera a ver si los cambios son temporales o permanentes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>✅ Buenas prácticas:</h3>
        <ul>
            <li><strong>Revisa métricas regularmente:</strong> Establece un horario para revisar tus números</li>
            <li><strong>Establece metas realistas:</strong> Basadas en tu historial y capacidades</li>
            <li><strong>Documenta cambios:</strong> Anota qué acciones causaron mejoras o problemas</li>
            <li><strong>Comparte con tu equipo:</strong> Todos deben entender cómo va el negocio</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Actividad práctica
    st.markdown("## 🎯 Actividad Práctica")
    
    st.markdown("""
    <div class="step-box">
        <h3>📝 Ejercicio para practicar:</h3>
        <p>1. <strong>Identifica tus KPIs:</strong> Piensa en 3-5 métricas más importantes para tu negocio</p>
        <p>2. <strong>Establece metas:</strong> Define números objetivo para cada KPI</p>
        <p>3. <strong>Revisa regularmente:</strong> Establece un horario para revisar tus métricas</p>
        <p>4. <strong>Analiza tendencias:</strong> Compara este mes con meses anteriores</p>
        <p>5. <strong>Toma decisiones:</strong> Basándote en lo que te dicen los números</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificación de completado
    st.markdown("## ✅ Verificación del Nivel")
    
    nivel3_completed = st.checkbox(
        "He completado todos los pasos del Nivel 3",
        value=st.session_state.get('nivel3_completed', False),
        key='nivel3_checkbox'
    )
    
    if nivel3_completed:
        st.session_state['nivel3_completed'] = True
        st.markdown("""
        <div class="completion-checkbox">
            <h3>🎉 ¡Felicidades! Has completado el Nivel 3</h3>
            <p>Ahora sabes cómo entender e interpretar métricas y KPIs para tomar mejores decisiones. 
            Estás listo para continuar con el siguiente nivel.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar siguiente nivel
        st.markdown("### 🚀 ¿Qué sigue?")
        st.markdown("En el **Nivel 4** aprenderás a crear cálculos personalizados y visualizaciones avanzadas.")
        
        if st.button("Continuar al Nivel 4", type="primary"):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>📚 ¿Quieres saber más?</h3>
        <p>Este nivel está basado en frameworks de métricas empresariales y mejores prácticas de análisis de rendimiento. 
        Si quieres profundizar en los fundamentos teóricos, consulta la documentación del proyecto.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
