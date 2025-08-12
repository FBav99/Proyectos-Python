import streamlit as st

# Page config
st.set_page_config(page_title="Guía Paso a Paso", layout="centered")

# Title
st.title("👣 Guía Paso a Paso")
st.markdown("""
Bienvenido a la guía interactiva para aprender a usar esta herramienta paso a paso.  
Ideal si es tu primera vez usando una herramienta de análisis de datos.  
""")

st.divider()

# Step 1: Upload a file
with st.expander("1️⃣ Subir un archivo"):
    st.markdown("""
    - Ve al menú lateral y selecciona **'Cargar archivo'**
    - Sube un archivo `.csv` o `.xlsx` con tus datos
    - Asegúrate de que tenga una fila de cabecera con los nombres de columnas

    💡 *Tip:* Intenta usar archivos con menos de 10 mil filas para empezar.
    """)

# Step 2: Apply filters
with st.expander("2️⃣ Aplicar filtros"):
    st.markdown("""
    - Después de subir tu archivo, ve a la sección de filtros
    - Elige columnas como "Categoría", "Año", "Producto", etc.
    - Esto te permite reducir los datos y enfocarte

    💡 *Tip:* Empieza aplicando un solo filtro para ver cómo cambia la tabla.
    """)

# Step 3: View data table
with st.expander("3️⃣ Explorar la tabla de datos"):
    st.markdown("""
    - La tabla muestra los datos que has cargado y filtrado
    - Puedes ordenar las columnas o usar scroll para explorarlos

    💡 *Tip:* Si la tabla aparece vacía, intenta quitar filtros.
    """)

# Step 4: View metrics
with st.expander("4️⃣ Ver métricas (KPIs)"):
    st.markdown("""
    - Esta sección te muestra números clave como totales, promedios o máximos
    - Se actualizan automáticamente con tus filtros

    💡 *Tip:* Selecciona columnas numéricas para ver más métricas útiles.
    """)

# Step 5: Create visualizations
with st.expander("5️⃣ Crear visualizaciones"):
    st.markdown("""
    - Elige el tipo de gráfico: barras, líneas, áreas, mapas, etc.
    - Luego selecciona las columnas de datos que quieres graficar

    💡 *Tip:* Usa gráficos de barras para comparar categorías, y líneas para ver evolución en el tiempo.
    """)

# Optional: Add a glossary/help for chart types
with st.expander("ℹ️ ¿Qué gráfico usar?"):
    st.markdown("""
    - **Barras**: Comparar cantidades entre categorías (ideal para productos, zonas, etc.)
    - **Líneas**: Ver cambios a lo largo del tiempo (ideal para fechas, evolución mensual)
    - **Torta (Pie)**: Solo si hay pocas categorías (máx. 5–6), para ver proporciones
    - **Mapas**: Si tus datos tienen coordenadas o regiones

    ❌ *Evita usar tortas con muchas categorías, se vuelven difíciles de leer.*
    """)

st.divider()

# Final section: Let user try it themselves
st.success("¡Ahora te toca a ti!")

st.markdown("""
Sigue estos pasos ahora en la app:

✅ Sube un archivo  
✅ Aplica al menos un filtro  
✅ Explora la tabla  
✅ Revisa una métrica  
✅ Crea una visualización

¿Listo para comenzar?
""")

# Simulated navigation button
if st.button("🚀 Ir a la app principal"):
    st.info("(Simulación) Aquí irías a la página principal de la app.")

st.caption("Esta guía está disponible en todo momento desde la sección 'Ayuda'.")

