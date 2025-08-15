# Panel de Análisis de Datos - Aprendizaje por Niveles

Este proyecto es una aplicación de análisis de datos construida con Streamlit que incluye un sistema de aprendizaje progresivo por niveles. Está diseñado para enseñar a los usuarios cómo usar herramientas de análisis de datos de manera gradual y efectiva.

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
├── prueba1.py            # Archivo original (monolítico)
└── pages/                 # Páginas de aprendizaje por niveles
    ├── 00_Ayuda.py       # Centro de ayuda y guía de usuario
    ├── 01_Nivel_1_Basico.py      # Nivel 1: Preparación de datos
    ├── 02_Nivel_2_Filtros.py     # Nivel 2: Filtros y análisis
    ├── 03_Nivel_3_Metricas.py    # Nivel 3: Métricas y KPIs
    └── 04_Nivel_4_Avanzado.py    # Nivel 4: Cálculos y visualizaciones
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

## 📚 Sistema de Aprendizaje por Niveles

La aplicación incluye un sistema de aprendizaje progresivo con 4 niveles:

### 🎯 Nivel 1: Básico - Preparación de Datos
- **Objetivo**: Aprender a preparar y cargar datos correctamente
- **Contenido**: Formato de archivos, carga de datos, verificación
- **Duración**: 15-20 minutos
- **Archivo**: `pages/01_Nivel_1_Basico.py`

### 🔍 Nivel 2: Filtros - Análisis de Datos
- **Objetivo**: Dominar el uso de filtros para análisis específicos
- **Contenido**: Filtros de fecha, categorías, rangos numéricos
- **Duración**: 20-25 minutos
- **Archivo**: `pages/02_Nivel_2_Filtros.py`

### 📊 Nivel 3: Métricas - KPIs y Análisis
- **Objetivo**: Entender e interpretar métricas de negocio
- **Contenido**: KPIs, métricas clave, interpretación de tendencias
- **Duración**: 25-30 minutos
- **Archivo**: `pages/03_Nivel_3_Metricas.py`

### 🚀 Nivel 4: Avanzado - Cálculos y Visualizaciones
- **Objetivo**: Crear análisis personalizados y visualizaciones
- **Contenido**: Cálculos personalizados, visualizaciones, exportación
- **Duración**: 30-35 minutos
- **Archivo**: `pages/04_Nivel_4_Avanzado.py`

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

- **Sistema de aprendizaje por niveles:** 4 niveles progresivos de dificultad
- **Carga de datos:** Soporte para CSV y Excel
- **Filtros dinámicos:** Por fecha, categoría, región y valores numéricos
- **Cálculos personalizados:** Matemáticas básicas, temporales y agregaciones
- **Visualizaciones interactivas:** Gráficos con Plotly
- **Exportación:** Múltiples formatos (Excel, CSV, Markdown)
- **Métricas en tiempo real:** Actualización automática con filtros
- **Ejercicios prácticos:** Cada nivel incluye actividades interactivas
- **Centro de ayuda:** Guía completa de usuario y solución de problemas

## 🎯 Ventajas del Sistema de Aprendizaje

1. **Aprendizaje progresivo:** Los usuarios avanzan gradualmente en complejidad
2. **Práctica interactiva:** Cada nivel incluye ejercicios prácticos
3. **Flexibilidad:** Los usuarios pueden saltar a niveles avanzados si ya tienen experiencia
4. **Retroalimentación inmediata:** Los ejercicios proporcionan feedback instantáneo
5. **Aplicación real:** Los usuarios aprenden con datos reales y casos de uso prácticos

## 🏗️ Ventajas de la Estructura Modular

1. **Mantenibilidad:** Cada módulo tiene una responsabilidad específica
2. **Reutilización:** Los módulos pueden ser reutilizados en otros proyectos
3. **Testabilidad:** Fácil de escribir pruebas unitarias para cada módulo
4. **Escalabilidad:** Fácil agregar nuevas funcionalidades
5. **Colaboración:** Múltiples desarrolladores pueden trabajar en diferentes módulos

## 📝 Ejemplo de Uso

### Uso Básico
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

### Navegación por Niveles
1. **Inicio**: Ejecuta `streamlit run main.py`
2. **Nivel 1**: Haz clic en "📚 Nivel 1: Básico" para comenzar
3. **Progreso**: Completa cada nivel en orden o salta según tu experiencia
4. **Práctica**: Usa los ejercicios interactivos en cada nivel
5. **Ayuda**: Consulta el centro de ayuda si tienes dudas

## 🔄 Migración desde la Versión Monolítica

La versión original (`prueba1.py`) contenía todo el código en un solo archivo. La nueva estructura incluye:

### Mejoras en Organización
- Separa las responsabilidades en archivos específicos
- Mantiene la misma funcionalidad
- Mejora la organización del código
- Facilita futuras modificaciones

### Nuevas Funcionalidades Educativas
- Sistema de aprendizaje por niveles
- Ejercicios prácticos interactivos
- Centro de ayuda completo
- Navegación progresiva
- Retroalimentación inmediata

## 📊 Funcionalidades Principales

### Análisis de Datos
- **Métricas de negocio:** KPIs automáticos y personalizados
- **Tendencias temporales:** Análisis de evolución en el tiempo
- **Correlaciones:** Identificación de relaciones entre variables
- **Segmentación:** Análisis por categorías y grupos

### Herramientas de Filtrado
- **Filtros avanzados:** Múltiples criterios de filtrado
- **Filtros temporales:** Rangos de fechas específicos
- **Filtros numéricos:** Deslizadores interactivos
- **Combinación de filtros:** Análisis multidimensional

### Funcionalidades Avanzadas
- **Cálculos personalizados:** Flexibilidad para análisis específicos
- **Visualizaciones:** Gráficos interactivos y informativos
- **Exportación:** Reportes en múltiples formatos
- **Dashboard completo:** Vista integral de métricas y tendencias

## 🤝 Contribución

Para contribuir al proyecto:

### Desarrollo de Funcionalidades
1. Trabaja en el módulo específico que necesites modificar
2. Mantén la separación de responsabilidades
3. Actualiza la documentación según sea necesario
4. Prueba que todos los módulos funcionen correctamente juntos

### Mejoras Educativas
1. Revisa los niveles de aprendizaje existentes
2. Propón nuevos ejercicios o explicaciones
3. Mejora la claridad de las instrucciones
4. Agrega ejemplos prácticos adicionales

### Reporte de Problemas
1. Describe el problema específico
2. Incluye pasos para reproducir el error
3. Especifica el nivel donde ocurre el problema
4. Proporciona información del entorno (sistema operativo, versiones) 