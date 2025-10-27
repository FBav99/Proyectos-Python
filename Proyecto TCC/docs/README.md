# Panel de Análisis de Datos - Aprendizaje por Niveles

Este proyecto es una aplicación de análisis de datos construida con Streamlit que incluye un sistema de aprendizaje progresivo por niveles. Está diseñado para enseñar a los usuarios cómo usar herramientas de análisis de datos de manera gradual y efectiva.

## 📁 Estructura del Proyecto

```
Proyecto TCC/
├── 📄 Inicio.py                    # Página principal con autenticación
├── 📄 main.py                      # Dashboard principal (sin autenticación)
├── 📄 requirements.txt             # Dependencias del proyecto
├── 📄 prueba1.py                   # Archivo de pruebas
│
├── 📁 core/                        # Módulos principales del sistema
│   ├── 🔐 auth_config.py          # Sistema de autenticación
│   ├── ⚙️ config.py               # Configuración de la aplicación
│   ├── 📊 data_loader.py          # Carga y procesamiento de datos
│   ├── 🔍 data_quality_analyzer.py # Análisis de calidad de datos
│   └── 🎯 quiz_system.py          # Sistema de cuestionarios
│
├── 📁 utils/                       # Utilidades y herramientas
│   ├── 🧮 calculations.py         # Cálculos personalizados
│   ├── 🔧 filters.py              # Filtros de datos
│   ├── 📈 metrics.py              # Métricas y KPIs
│   ├── 📊 visualizations.py       # Visualizaciones y gráficos
│   ├── 📤 export.py               # Exportación de datos
│   ├── 🎨 ui_components.py        # Componentes de interfaz
│   └── 🎬 gif_utils.py            # Utilidades para GIFs
│
├── 📁 pages/                       # Páginas de niveles de aprendizaje
│   ├── ❓ 00_Ayuda.py             # Página de ayuda
│   ├── 📚 01_Nivel_1_Basico.py    # Nivel 1: Básico
│   ├── 🔍 02_Nivel_2_Filtros.py   # Nivel 2: Filtros
│   ├── 📊 03_Nivel_3_Metricas.py  # Nivel 3: Métricas
│   └── 🚀 04_Nivel_4_Avanzado.py  # Nivel 4: Avanzado
│
├── 📁 data/                        # Datos y datasets
│   └── 📊 sample_datasets.py       # Datasets de ejemplo
│
├── 📁 config/                      # Archivos de configuración
│   └── ⚙️ config.yaml             # Configuración de autenticación
│
├── 📁 docs/                        # Documentación
│   ├── 📖 README.md               # Documentación principal
│   ├── 📋 INTEGRATION_SUMMARY.md  # Resumen de integración
│   ├── 🎬 IMPLEMENTACION_GIFS.md  # Implementación de GIFs
│   ├── 🎬 GIF_CREATION_GUIDE.md   # Guía de creación de GIFs
│   ├── 📁 PROJECT_STRUCTURE.md    # Estructura del proyecto
│   ├── 🗺️ USER_FLOW_INDEX.md      # Índice de documentación de flujo de usuario
│   ├── 📘 USER_FLOW_GUIDE.md      # Guía completa de flujo de usuario
│   ├── 📊 USER_FLOW_SUMMARY.md    # Resumen visual de flujos
│   └── ⚡ USER_FLOW_QUICK_REFERENCE.md # Referencia rápida de flujos
│
└── 📁 assets/                      # Recursos multimedia
    └── 📁 gifs/                    # GIFs de demostración
        ├── 📁 nivel1/
        ├── 📁 nivel2/
        ├── 📁 nivel3/
        └── 📁 nivel4/
```

> 📋 **Nota**: Para más detalles sobre la estructura del proyecto, consulta [`docs/PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md)

## 🚀 Instalación y Uso

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación principal (con autenticación):**
   ```bash
   streamlit run Inicio.py
   ```

3. **Ejecutar dashboard sin autenticación:**
   ```bash
   streamlit run main.py
   ```

## 🔐 Credenciales de Acceso

- **Usuario**: `demo_user`
- **Contraseña**: `demo123`

## 🗺️ Documentación de Flujo de Usuario

**¿Quieres entender el viaje completo de un usuario?** Consulta nuestra documentación de flujo de usuario:

- **[📖 Índice de Flujo de Usuario](USER_FLOW_INDEX.md)** - Comienza aquí para navegar toda la documentación de flujos
- **[📘 Guía Completa de Flujo](USER_FLOW_GUIDE.md)** - Walkthrough detallado completo del viaje del usuario (15k palabras)
- **[📊 Resumen Visual de Flujos](USER_FLOW_SUMMARY.md)** - Diagramas y visualizaciones del flujo (5k palabras)
- **[⚡ Referencia Rápida](USER_FLOW_QUICK_REFERENCE.md)** - Hoja de referencia de una página para consulta rápida

### 🎯 Qué Documento Usar

| Necesitas | Usa Este Documento |
|-----------|-------------------|
| Entender el sistema rápidamente | ⚡ Referencia Rápida |
| Ver flujos visuales | 📊 Resumen Visual |
| Detalles completos del viaje | 📘 Guía Completa |
| Navegar toda la documentación | 📖 Índice |

> 💡 **Ejemplo de Usuario**: Todos los documentos siguen el viaje de **María González**, una usuaria sin experiencia previa en análisis de datos, desde su registro hasta la creación de su primer dashboard profesional con el dataset de **TechStore (E-commerce)**.

## 📚 Sistema de Aprendizaje por Niveles

La aplicación incluye un sistema de aprendizaje progresivo con 5 niveles:

### 🌟 Nivel 0: Introducción - Conceptos de Datos
- **Objetivo**: Entender los conceptos fundamentales sobre qué son los datos
- **Contenido**: Tipos de datos, qué puedes hacer con ellos, estructura de datos
- **Duración**: 10-15 minutos
- **Archivo**: `pages/00_Nivel_0_Introduccion.py`

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

## 📋 Módulos Principales

### 🔐 `core/auth_config.py`
- Sistema de autenticación completo
- Gestión de usuarios y sesiones
- Seguimiento de progreso y logros

### ⚙️ `core/config.py`
- Configuración de la página de Streamlit
- Estilos CSS personalizados
- Funciones de configuración

### 📊 `core/data_loader.py`
- Carga de archivos CSV/Excel
- Generación de datos de muestra
- Manejo de errores de carga

### 🔍 `core/data_quality_analyzer.py`
- Análisis completo de calidad de datos
- Detección de valores faltantes
- Validación de formatos

### 🎯 `core/quiz_system.py`
- Sistema de cuestionarios interactivos
- Evaluación automática
- Seguimiento de puntuaciones

### 📈 `utils/metrics.py`
- Cálculo de métricas clave de negocio
- Análisis de crecimiento
- Perspectivas de rendimiento

### 📊 `utils/visualizations.py`
- Creación de gráficos con Plotly
- Series temporales
- Análisis por categorías y regiones
- Matrices de correlación

### 🧮 `utils/calculations.py`
- Operaciones matemáticas básicas
- Cálculos temporales (YTD, MoM, etc.)
- Agregaciones por grupos

### 🔧 `utils/filters.py`
- Filtros de fecha
- Filtros por categoría y región
- Filtros numéricos

### 🎨 `utils/ui_components.py`
- Componentes de interfaz reutilizables
- Controles de barra lateral
- Dashboards de métricas

### 📤 `utils/export.py`
- Exportación a múltiples formatos
- Generación de reportes
- Funcionalidad de descarga
- Exportación a Excel
- Exportación a CSV
- Generación de reportes

### `ui_components.py`
- Controles de la barra lateral
- Interfaz de cálculos personalizados
- Dashboard de métricas
- Sección de exportación

## 🔧 Características

- **Sistema de aprendizaje por niveles:** 5 niveles progresivos de dificultad
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