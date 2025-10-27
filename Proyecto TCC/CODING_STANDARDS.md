# Estándares de Código - Proyecto TCC

## Principios Generales

1. **Código limpio y legible**: El código debe ser fácil de leer y entender
2. **Comentarios útiles**: Los comentarios deben explicar el "por qué", no el "qué"
3. **Nombres descriptivos**: Variables y funciones deben tener nombres que describan su propósito
4. **Sin emojis en comentarios**: Los comentarios deben ser profesionales y sin emojis

## Estructura de Archivos

### Encabezado del Archivo
```python
"""
Nombre del Archivo: nombre_archivo.py
Descripción: Descripción breve del propósito del archivo
Autor: Fernando Bavera Villalba
Fecha: DD/MM/YYYY
"""
```

### Imports
```python
# Imports estándar
import streamlit as st
import pandas as pd

# Imports locales del proyecto
from utils.ui import handle_authentication
from core.config import setup_page_config
```

## Comentarios

### Formato de Comentarios

**Linea única:**
```python
# Verificar autenticación del usuario
if 'user' not in st.session_state:
    return
```

**Múltiples líneas para explicar secciones:**
```python
# ============================================================================
# AUTHENTICATION SECTION - Verify user login and permissions
# ============================================================================
```

**Comentarios de funciones:**
```python
def calculate_total_sales(df):
    """
    Calcula el total de ventas de un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'Ventas'
    
    Returns:
        float: Suma total de ventas
    """
    return df['Ventas'].sum()
```

### Comentarios DO's y DON'Ts

**DO:**
```python
# Verificar que el usuario tiene permisos de administrador
# Calcular el promedio de las últimas 30 días
# Inicializar la base de datos con valores por defecto
```

**DON'T:**
```python
# Asignar x a y
# Loop
# Variable
# 🔐 Seguridad
```

## Nombres de Variables y Funciones

### Variables
```python
# Bueno
user_id = 123
total_sales = calculate_sales()
is_authenticated = True

# Malo
id = 123
x = calculate_sales()
auth = True
```

### Funciones
```python
# Bueno
def get_user_profile(user_id):
    pass

def save_level_progress(user_id, level, completed):
    pass

# Malo
def get():
    pass

def save():
    pass
```

## Estructura de Código

### Secciones Principales
```python
# ============================================================================
# IMPORTS AND CONFIGURATION
# ============================================================================

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# ============================================================================
# MAIN FUNCTION
# ============================================================================
```

### Organización Lógica
1. Imports
2. Configuración de página
3. Funciones auxiliares
4. Función principal
5. Ejecución principal

## Manejo de Errores

```python
try:
    result = process_data(df)
except ValueError as e:
    st.error(f"Error en los datos: {e}")
except Exception as e:
    st.error(f"Error inesperado: {e}")
    logger.error(f"Error en process_data: {e}")
```

## Strings y UI

```python
# Usar f-strings para interpolación
st.markdown(f'Bienvenido, {user_name}!')

# Evitar emojis en variables de texto
# No: title = "📊 Dashboard"
# Si: title = "Dashboard"
```

## Ejemplo Completo

```python
"""
Nombre del Archivo: calculate_metrics.py
Descripción: Calcula métricas de ventas del dashboard
Autor: Fernando Bavera Villalba
Fecha: 25/10/2025
"""

import streamlit as st
import pandas as pd

def calculate_total_revenue(df):
    """
    Calcula el ingreso total del DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas
    
    Returns:
        float: Ingreso total
    """
    if 'Ventas' not in df.columns:
        raise ValueError("DataFrame debe contener columna 'Ventas'")
    
    return df['Ventas'].sum()

def calculate_average_order_value(df):
    """
    Calcula el valor promedio de orden.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de ventas
    
    Returns:
        float: Valor promedio de orden
    """
    if len(df) == 0:
        return 0
    
    return df['Ventas'].mean()

def main():
    """Función principal de la aplicación"""
    
    # Configurar página
    st.set_page_config(page_title="Métricas de Ventas")
    
    # Verificar que hay datos en la sesión
    if 'data' not in st.session_state:
        st.error("No hay datos disponibles. Por favor, sube un archivo.")
        return
    
    # Obtener datos
    df = st.session_state['data']
    
    # Calcular métricas
    try:
        total_revenue = calculate_total_revenue(df)
        avg_order_value = calculate_average_order_value(df)
        
        # Mostrar métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ingreso Total", f"${total_revenue:,.2f}")
        with col2:
            st.metric("Promedio de Orden", f"${avg_order_value:,.2f}")
    
    except ValueError as e:
        st.error(f"Error en los datos: {e}")

if __name__ == "__main__":
    main()
```
