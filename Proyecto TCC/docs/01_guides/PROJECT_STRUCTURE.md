# 📁 Estructura del Proyecto TCC

## 🏗️ Organización de Carpetas

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
│   └── 📁 PROJECT_STRUCTURE.md    # Esta documentación
│
└── 📁 assets/                      # Recursos multimedia
    └── 📁 gifs/                    # GIFs de demostración
        ├── 📁 nivel1/
        ├── 📁 nivel2/
        ├── 📁 nivel3/
        └── 📁 nivel4/
```

## 🔧 Módulos Principales

### 📁 Core (Funcionalidades Principales)

#### 🔐 `auth_config.py`
- **Propósito**: Sistema de autenticación completo
- **Funciones principales**:
  - `init_authentication()`: Inicializa el sistema de autenticación
  - `get_user_progress()`: Obtiene el progreso del usuario
  - `update_user_progress()`: Actualiza el progreso del usuario
  - `check_achievement()`: Verifica y otorga logros

#### ⚙️ `config.py`
- **Propósito**: Configuración general de la aplicación
- **Funciones principales**:
  - `setup_page_config()`: Configuración de páginas Streamlit
  - `apply_custom_css()`: Estilos CSS personalizados

#### 📊 `data_loader.py`
- **Propósito**: Carga y procesamiento de datos
- **Funciones principales**:
  - `get_data()`: Carga datos desde archivos o datasets de ejemplo

#### 🔍 `data_quality_analyzer.py`
- **Propósito**: Análisis de calidad de datos
- **Funciones principales**:
  - `data_quality_page()`: Página completa de análisis de calidad

#### 🎯 `quiz_system.py`
- **Propósito**: Sistema de cuestionarios y evaluación
- **Funciones principales**:
  - Gestión de preguntas y respuestas
  - Evaluación automática
  - Seguimiento de puntuaciones

### 📁 Utils (Utilidades)

#### 🧮 `calculations.py`
- **Propósito**: Cálculos personalizados y fórmulas
- **Funciones principales**:
  - `apply_custom_calculations()`: Aplica cálculos personalizados

#### 🔧 `filters.py`
- **Propósito**: Filtros de datos avanzados
- **Funciones principales**:
  - `apply_all_filters()`: Aplica todos los filtros configurados

#### 📈 `metrics.py`
- **Propósito**: Cálculo de métricas y KPIs
- **Funciones principales**:
  - `calculate_metrics()`: Métricas básicas
  - `calculate_growth_metrics()`: Métricas de crecimiento
  - `calculate_performance_insights()`: Perspectivas de rendimiento

#### 📊 `visualizations.py`
- **Propósito**: Creación de visualizaciones
- **Funciones principales**:
  - `create_time_series_chart()`: Gráficos de series temporales
  - `create_category_analysis()`: Análisis por categorías
  - `create_regional_analysis()`: Análisis regional
  - `create_correlation_matrix()`: Matriz de correlación

#### 📤 `export.py`
- **Propósito**: Exportación de datos y reportes
- **Funciones principales**:
  - Exportación a Excel, CSV, PDF

#### 🎨 `ui_components.py`
- **Propósito**: Componentes de interfaz reutilizables
- **Funciones principales**:
  - `create_sidebar_controls()`: Controles de barra lateral
  - `display_metrics_dashboard()`: Dashboard de métricas
  - `display_export_section()`: Sección de exportación

#### 🎬 `gif_utils.py`
- **Propósito**: Utilidades para GIFs de demostración
- **Funciones principales**:
  - `display_level_gif()`: Muestra GIFs por nivel

### 📁 Pages (Páginas de Niveles)

#### 📚 `01_Nivel_1_Basico.py`
- **Propósito**: Nivel básico de preparación de datos
- **Contenido**: Carga de datos, limpieza básica, visualizaciones simples

#### 🔍 `02_Nivel_2_Filtros.py`
- **Propósito**: Nivel intermedio de filtros
- **Contenido**: Filtros avanzados, segmentación de datos

#### 📊 `03_Nivel_3_Metricas.py`
- **Propósito**: Nivel avanzado de métricas
- **Contenido**: KPIs, métricas de rendimiento, análisis estadístico

#### 🚀 `04_Nivel_4_Avanzado.py`
- **Propósito**: Nivel experto de análisis avanzado
- **Contenido**: Machine Learning, análisis predictivo, reportes avanzados

## 🔄 Flujo de Datos

```
Usuario → Autenticación → Selección de Nivel → Carga de Datos → 
Análisis → Visualización → Exportación → Progreso
```

## 🚀 Cómo Ejecutar

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar aplicación principal**:
   ```bash
   streamlit run Inicio.py
   ```

3. **Ejecutar dashboard sin autenticación**:
   ```bash
   streamlit run main.py
   ```

## 🔐 Credenciales de Acceso

- **Usuario**: `demo_user`
- **Contraseña**: `demo123`

## 📝 Notas de Desarrollo

- Todos los módulos están organizados por funcionalidad
- Las importaciones han sido actualizadas para reflejar la nueva estructura
- La documentación está centralizada en la carpeta `docs/`
- Los recursos multimedia están en `assets/`
- La configuración está separada en `config/`
