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
    
    .filter-demo {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
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
    
    /* Ensure all text elements have proper contrast */
    .step-box h3, .step-box h4, .step-box p, .step-box ul, .step-box li,
    .warning-box h3, .warning-box ul, .warning-box li,
    .success-box h3, .success-box ul, .success-box li,
    .filter-demo h3, .filter-demo p,
    .completion-checkbox h3, .completion-checkbox p,
    .info-box h3, .info-box p {
        color: inherit !important;
    }
    
    /* Force light backgrounds for all elements */
    .step-box, .warning-box, .success-box, .filter-demo, .completion-checkbox, .info-box {
        background-color: inherit !important;
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
    st.markdown('<h1 class="level-header">🔍 Nivel 2: Organizar Información</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">Encontrar y Organizar los Datos que Necesitas</h2>', unsafe_allow_html=True)
    
    # Dynamic Progress indicator
    total_progress, completed_count, progress = get_level_progress()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(total_progress / 100)
        st.caption(f"Progreso general: {total_progress:.1f}% ({completed_count}/4 niveles)")
    
    # Verificar que el nivel anterior esté completado
    if not progress['nivel1']:
        st.warning("⚠️ Primero debes completar el Nivel 1 antes de continuar con este nivel.")
        if st.button("Ir al Nivel 1", type="primary"):
            st.switch_page("pages/01_Nivel_1_Basico.py")
        return
    
    # Información introductoria
    st.markdown("""
    <div class="info-box">
        <h3>🎯 ¿Qué aprenderás en este nivel?</h3>
        <p>En este nivel aprenderás a usar filtros para encontrar exactamente la información que necesitas. 
        Los filtros te ayudan a organizar y analizar datos de manera más efectiva.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasos del nivel
    st.markdown("## 📋 Pasos para Organizar y Filtrar Datos")
    
    # Paso 1
    st.markdown("""
    <div class="step-box">
        <h3>1️⃣ Usar filtros de fecha para analizar períodos específicos</h3>
        <p><strong>¿Por qué es útil?</strong> Los filtros de fecha te permiten ver información de un período específico, 
        como las ventas del último mes o de un trimestre particular.</p>
        
        <h4>📅 Tipos de filtros de fecha:</h4>
        <ul>
            <li><strong>Rango de fechas:</strong> Desde una fecha hasta otra</li>
            <li><strong>Período específico:</strong> Último mes, este año, etc.</li>
            <li><strong>Fecha única:</strong> Un día específico</li>
        </ul>
        
        <h4>✅ Ejemplos de uso:</h4>
        <ul>
            <li>Ver ventas del último trimestre</li>
            <li>Comparar resultados entre dos meses</li>
            <li>Analizar tendencias por estación</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 2
    st.markdown("""
    <div class="step-box">
        <h3>2️⃣ Filtrar por categorías y regiones</h3>
        <p><strong>¿Qué significa?</strong> Los filtros por categoría te permiten ver solo los productos o servicios 
        que te interesan, y los filtros por región te muestran resultados de áreas geográficas específicas.</p>
        
        <h4>🏷️ Filtros por categoría:</h4>
        <ul>
            <li><strong>Productos:</strong> Solo electrónicos, solo ropa, etc.</li>
            <li><strong>Servicios:</strong> Solo consultoría, solo mantenimiento, etc.</li>
            <li><strong>Tipos de cliente:</strong> Solo empresas, solo particulares, etc.</li>
        </ul>
        
        <h4>🌍 Filtros por región:</h4>
        <ul>
            <li><strong>Países o estados:</strong> Solo México, solo California, etc.</li>
            <li><strong>Ciudades:</strong> Solo Ciudad de México, solo Los Ángeles, etc.</li>
            <li><strong>Zonas:</strong> Solo norte, solo sur, solo este, solo oeste</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 3
    st.markdown("""
    <div class="step-box">
        <h3>3️⃣ Aplicar filtros numéricos con deslizadores</h3>
        <p><strong>¿Cómo funcionan?</strong> Los filtros numéricos te permiten establecer rangos de valores, 
        como ver solo productos entre ciertos precios o ventas por encima de un monto mínimo.</p>
        
        <h4>🔢 Tipos de filtros numéricos:</h4>
        <ul>
            <li><strong>Rango de precios:</strong> Desde $100 hasta $500</li>
            <li><strong>Ventas mínimas:</strong> Solo productos que vendieron más de 50 unidades</li>
            <li><strong>Calificaciones:</strong> Solo productos con 4 estrellas o más</li>
            <li><strong>Edad o antigüedad:</strong> Solo clientes entre 25 y 45 años</li>
        </ul>
        
        <h4>🎛️ Cómo usar deslizadores:</h4>
        <ol>
            <li>Mueve el deslizador izquierdo para establecer el valor mínimo</li>
            <li>Mueve el deslizador derecho para establecer el valor máximo</li>
            <li>Los resultados se actualizan automáticamente</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Paso 4
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 4️⃣ Combinar múltiples filtros para análisis detallado")
    st.markdown("**¿Por qué combinar filtros?** Al usar varios filtros juntos, puedes obtener información muy específica y relevante para tu análisis.")
    
    st.markdown("#### 🔗 Ejemplos de combinaciones:")
    st.markdown("""
    - **Fecha + Categoría:** Ventas de electrónicos en diciembre
    - **Región + Precio:** Productos caros en el norte
    - **Categoría + Calificación:** Ropa con 5 estrellas
    - **Fecha + Región + Precio:** Ventas altas en el sur este mes
    """)
    
    st.markdown("#### 💡 Consejos para combinar filtros:")
    st.markdown("""
    - Empieza con un filtro y ve agregando más gradualmente
    - Verifica que no estés filtrando demasiado (pocos resultados)
    - Usa filtros que tengan sentido juntos
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Paso 5
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 5️⃣ Entender cómo los filtros afectan las métricas")
    st.markdown("**¿Qué significa?** Cuando aplicas filtros, los totales, promedios y otras métricas cambian para mostrar solo la información filtrada.")
    
    st.markdown("#### 📊 Métricas que cambian con filtros:")
    st.markdown("""
    - **Total de ventas:** Solo suma los productos filtrados
    - **Promedio de precios:** Solo considera los productos visibles
    - **Número de registros:** Solo cuenta los resultados filtrados
    - **Porcentajes:** Se recalculan con la nueva base de datos
    """)
    
    st.markdown("#### ⚠️ Importante recordar:")
    st.markdown("""
    - Los filtros no cambian tus datos originales
    - Siempre puedes quitar filtros para ver todo nuevamente
    - Los filtros se aplican en tiempo real
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ejemplo práctico
    st.markdown("## 🎯 Ejemplo Práctico")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Vamos a practicar con filtros usando datos de ventas")
    st.markdown("Te mostraré cómo aplicar diferentes tipos de filtros y ver cómo cambian los resultados.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Crear datos de ejemplo
    df = create_sample_data()
    
    st.markdown("### 📁 Datos de ejemplo (Ventas de una tienda)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Filtros interactivos
    st.markdown("### 🔍 Aplicar Filtros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Filtro por fecha:**")
        fecha_inicio = st.date_input(
            "Fecha de inicio",
            value=df['Fecha'].min().date(),
            min_value=df['Fecha'].min().date(),
            max_value=df['Fecha'].max().date()
        )
        fecha_fin = st.date_input(
            "Fecha de fin",
            value=df['Fecha'].max().date(),
            min_value=df['Fecha'].min().date(),
            max_value=df['Fecha'].max().date()
        )
        
        st.markdown("**🏷️ Filtro por categoría:**")
        categorias = ['Todas'] + list(df['Categoria'].unique())
        categoria_seleccionada = st.selectbox("Seleccionar categoría", categorias)
        
        st.markdown("**🌍 Filtro por región:**")
        regiones = ['Todas'] + list(df['Region'].unique())
        region_seleccionada = st.selectbox("Seleccionar región", regiones)
    
    with col2:
        st.markdown("**🔢 Filtros numéricos:**")
        
        st.markdown("**💰 Rango de ventas:**")
        ventas_min = st.slider(
            "Ventas mínimas",
            min_value=float(df['Ventas'].min()),
            max_value=float(df['Ventas'].max()),
            value=float(df['Ventas'].min()),
            step=50.0
        )
        ventas_max = st.slider(
            "Ventas máximas",
            min_value=float(df['Ventas'].min()),
            max_value=float(df['Ventas'].max()),
            value=float(df['Ventas'].max()),
            step=50.0
        )
        
        st.markdown("**⭐ Calificación mínima:**")
        calificacion_min = st.slider(
            "Calificación mínima",
            min_value=1,
            max_value=5,
            value=1
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    # Filtro de fechas
    df_filtrado = df_filtrado[
        (df_filtrado['Fecha'].dt.date >= fecha_inicio) &
        (df_filtrado['Fecha'].dt.date <= fecha_fin)
    ]
    
    # Filtro de categoría
    if categoria_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_seleccionada]
    
    # Filtro de región
    if region_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Region'] == region_seleccionada]
    
    # Filtros numéricos
    df_filtrado = df_filtrado[
        (df_filtrado['Ventas'] >= ventas_min) &
        (df_filtrado['Ventas'] <= ventas_max) &
        (df_filtrado['Calificacion'] >= calificacion_min)
    ]
    
    # Mostrar resultados filtrados
    st.markdown("### 📊 Resultados Filtrados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Registros originales", len(df))
        st.metric("Registros filtrados", len(df_filtrado))
    
    with col2:
        st.metric("Ventas totales", f"${df_filtrado['Ventas'].sum():,.0f}")
        st.metric("Promedio ventas", f"${df_filtrado['Ventas'].mean():,.0f}")
    
    with col3:
        st.metric("Ingresos totales", f"${df_filtrado['Ingresos'].sum():,.0f}")
        st.metric("Promedio ingresos", f"${df_filtrado['Ingresos'].mean():,.0f}")
    
    with col4:
        st.metric("Calificación promedio", f"{df_filtrado['Calificacion'].mean():.1f}")
        st.metric("Productos únicos", df_filtrado['Categoria'].nunique())
    
    # Mostrar datos filtrados
    if len(df_filtrado) > 0:
        st.markdown("**📋 Datos filtrados:**")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados. Intenta ajustar los filtros.")
    
    # Consejos importantes
    st.markdown("## 💡 Consejos Importantes")
    
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ Errores comunes a evitar:</h3>
        <ul>
            <li><strong>Filtros muy restrictivos:</strong> Si filtras demasiado, podrías no obtener resultados</li>
            <li><strong>Olvidar quitar filtros:</strong> Asegúrate de limpiar filtros cuando cambies de análisis</li>
            <li><strong>Filtros contradictorios:</strong> No uses filtros que se contradigan entre sí</li>
            <li><strong>Ignorar el contexto:</strong> Usa filtros que tengan sentido para tu análisis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h3>✅ Buenas prácticas:</h3>
        <ul>
            <li><strong>Planifica tu análisis:</strong> Piensa qué información necesitas antes de filtrar</li>
            <li><strong>Usa filtros gradualmente:</strong> Empieza con uno y ve agregando más</li>
            <li><strong>Verifica los resultados:</strong> Siempre revisa que los filtros den los resultados esperados</li>
            <li><strong>Documenta tus filtros:</strong> Anota qué filtros usaste para poder repetir el análisis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Actividad práctica
    st.markdown("## 🎯 Actividad Práctica")
    
    st.markdown("""
    <div class="step-box">
        <h3>📝 Ejercicio para practicar:</h3>
        <p>1. <strong>Analiza ventas por período:</strong> Usa filtros de fecha para ver ventas del último trimestre</p>
        <p>2. <strong>Filtra por categoría:</strong> Ve solo los productos de una categoría específica</p>
        <p>3. <strong>Aplica filtros numéricos:</strong> Establece un rango de precios o ventas</p>
        <p>4. <strong>Combina filtros:</strong> Usa fecha + categoría + región juntos</p>
        <p>5. <strong>Observa los cambios:</strong> Nota cómo cambian las métricas con cada filtro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificación de completado
    st.markdown("## ✅ Verificación del Nivel")
    
    nivel2_completed = st.checkbox(
        "He completado todos los pasos del Nivel 2",
        value=st.session_state.get('nivel2_completed', False),
        key='nivel2_checkbox'
    )
    
    if nivel2_completed:
        st.session_state['nivel2_completed'] = True
        st.markdown("""
        <div class="completion-checkbox">
            <h3>🎉 ¡Felicidades! Has completado el Nivel 2</h3>
            <p>Ahora sabes cómo organizar y filtrar datos para encontrar exactamente lo que necesitas. 
            Estás listo para continuar con el siguiente nivel.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar siguiente nivel
        st.markdown("### 🚀 ¿Qué sigue?")
        st.markdown("En el **Nivel 3** aprenderás a entender e interpretar métricas y KPIs para tomar mejores decisiones.")
        
        if st.button("Continuar al Nivel 3", type="primary"):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>📚 ¿Quieres saber más?</h3>
        <p>Este nivel está basado en metodologías de análisis exploratorio de datos y mejores prácticas de la industria. 
        Si quieres profundizar en los fundamentos teóricos, consulta la documentación del proyecto.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
