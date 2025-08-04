# Panel de Análisis de Datos - Versión Modular

Este proyecto es una aplicación de análisis de datos construida con Streamlit, organizada en módulos para facilitar el mantenimiento y la extensión.

## 📁 Estructura del Proyecto

```
Proyecto TCC/
├── main.py                 # Archivo principal de la aplicación
├── config.py              # Configuración de página y estilos CSS
├── data_loader.py         # Carga y generación de datos
├── metrics.py             # Cálculo de métricas de negocio
├── visualizations.py      # Creación de gráficos y visualizaciones
├── calculations.py        # Cálculos personalizados
├── filters.py             # Filtros de datos
├── export.py              # Funcionalidad de exportación
├── ui_components.py       # Componentes de interfaz de usuario
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
└── prueba1.py            # Archivo original (monolítico)
```

## 🚀 Instalación y Uso

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación:**
   ```bash
   streamlit run main.py
   ```

## 📋 Módulos

### `config.py`
- Configuración de la página de Streamlit
- Estilos CSS personalizados
- Funciones de configuración

### `data_loader.py`
- Carga de archivos CSV/Excel
- Generación de datos de muestra
- Manejo de errores de carga

### `metrics.py`
- Cálculo de métricas clave de negocio
- Análisis de crecimiento
- Perspectivas de rendimiento

### `visualizations.py`
- Creación de gráficos con Plotly
- Series temporales
- Análisis por categorías y regiones
- Matrices de correlación

### `calculations.py`
- Operaciones matemáticas básicas
- Cálculos temporales (YTD, MoM, etc.)
- Agregaciones por grupos

### `filters.py`
- Filtros de fecha
- Filtros por categoría y región
- Filtros numéricos

### `export.py`
- Exportación a Excel
- Exportación a CSV
- Generación de reportes

### `ui_components.py`
- Controles de la barra lateral
- Interfaz de cálculos personalizados
- Dashboard de métricas
- Sección de exportación

## 🔧 Características

- **Carga de datos:** Soporte para CSV y Excel
- **Filtros dinámicos:** Por fecha, categoría, región y valores numéricos
- **Cálculos personalizados:** Matemáticas básicas, temporales y agregaciones
- **Visualizaciones interactivas:** Gráficos con Plotly
- **Exportación:** Múltiples formatos (Excel, CSV, Markdown)
- **Métricas en tiempo real:** Actualización automática con filtros

## 🎯 Ventajas de la Estructura Modular

1. **Mantenibilidad:** Cada módulo tiene una responsabilidad específica
2. **Reutilización:** Los módulos pueden ser reutilizados en otros proyectos
3. **Testabilidad:** Fácil de escribir pruebas unitarias para cada módulo
4. **Escalabilidad:** Fácil agregar nuevas funcionalidades
5. **Colaboración:** Múltiples desarrolladores pueden trabajar en diferentes módulos

## 📝 Ejemplo de Uso

```python
# Importar módulos específicos
from data_loader import get_data
from metrics import calculate_metrics
from visualizations import create_time_series_chart

# Usar funcionalidades específicas
df = get_data(uploaded_file)
metrics = calculate_metrics(df)
chart = create_time_series_chart(df, 'Revenue')
```

## 🔄 Migración desde la Versión Monolítica

La versión original (`prueba1.py`) contenía todo el código en un solo archivo. La nueva estructura modular:

- Separa las responsabilidades en archivos específicos
- Mantiene la misma funcionalidad
- Mejora la organización del código
- Facilita futuras modificaciones

## 📊 Funcionalidades Principales

- **Análisis de datos:** Métricas de negocio, tendencias, correlaciones
- **Filtros avanzados:** Múltiples criterios de filtrado
- **Cálculos personalizados:** Flexibilidad para análisis específicos
- **Visualizaciones:** Gráficos interactivos y informativos
- **Exportación:** Reportes en múltiples formatos

## 🤝 Contribución

Para contribuir al proyecto:

1. Trabaja en el módulo específico que necesites modificar
2. Mantén la separación de responsabilidades
3. Actualiza la documentación según sea necesario
4. Prueba que todos los módulos funcionen correctamente juntos 