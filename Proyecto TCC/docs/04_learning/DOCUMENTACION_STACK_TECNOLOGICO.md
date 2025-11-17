# Documentación del Stack Tecnológico
## Plataforma de Análisis de Datos TCC

**Autor:** Fernando Bavera Villalba  
**Fecha:** 2025  
**Versión:** 1.0

---

## Resumen Ejecutivo

La Plataforma de Análisis de Datos TCC está construida sobre un stack tecnológico moderno centrado en Python, utilizando Streamlit como framework principal para la interfaz de usuario web. El sistema integra bibliotecas especializadas para manipulación de datos (Pandas, NumPy), visualización interactiva (Plotly, Matplotlib, Seaborn), análisis estadístico (SciPy, scikit-learn), gestión de bases de datos (SQLite como base de datos por defecto, con soporte para Supabase/PostgreSQL mediante psycopg2-binary), autenticación y seguridad (bcrypt, streamlit-authenticator), y utilidades de soporte (PyYAML, openpyxl, requests). Esta documentación proporciona una descripción técnica detallada de cada componente del stack, sus versiones, propósitos específicos en el proyecto, y su integración dentro de la arquitectura general del sistema.

---

## 1. Introducción

### 1.1 Contexto Tecnológico

La plataforma TCC ha sido desarrollada utilizando tecnologías de código abierto y estándares de la industria para análisis de datos y desarrollo web. La elección del stack tecnológico se basó en criterios de facilidad de uso, robustez, comunidad activa, y compatibilidad con los objetivos educativos del proyecto.

### 1.2 Objetivo del Documento

Este documento proporciona una descripción técnica exhaustiva de todas las dependencias y bibliotecas utilizadas en el proyecto, especificando versiones, propósitos, casos de uso específicos, y su rol dentro de la arquitectura del sistema.

### 1.3 Estructura del Stack

El stack tecnológico se organiza en las siguientes categorías:
- Framework web y UI
- Manipulación y análisis de datos
- Visualización de datos
- Análisis estadístico y machine learning
- Base de datos y persistencia
- Autenticación y seguridad
- Utilidades y soporte

---

## 2. Framework Web y Interfaz de Usuario

### 2.1 Streamlit

**Versión:** >= 1.28.0  
**Tipo:** Framework web para aplicaciones de datos  
**Documentación oficial:** https://streamlit.io

#### 2.1.1 Descripción

Streamlit es un framework de código abierto de Python diseñado específicamente para crear aplicaciones web interactivas para ciencia de datos y machine learning. Permite convertir scripts de Python en aplicaciones web compartibles sin necesidad de conocimientos de desarrollo frontend.

#### 2.1.2 Uso en el Proyecto

Streamlit constituye el núcleo de la interfaz de usuario de la plataforma TCC. Se utiliza para:

- **Páginas de Niveles de Aprendizaje:** Todas las páginas de niveles (00-04) están construidas con Streamlit, utilizando componentes como `st.title()`, `st.header()`, `st.markdown()`, `st.columns()`, y `st.dataframe()`.

- **Componentes Interactivos:** 
  - `st.file_uploader()` para carga de archivos en Nivel 1
  - `st.selectbox()`, `st.slider()`, `st.date_input()` para filtros interactivos en Niveles 2 y 3
  - `st.checkbox()` para configuraciones y verificaciones
  - `st.button()` para acciones del usuario

- **Visualización de Datos:**
  - `st.dataframe()` para mostrar tablas de datos
  - `st.metric()` para mostrar KPIs y métricas clave
  - `st.bar_chart()`, `st.line_chart()` para gráficos básicos
  - `st.plotly_chart()` para visualizaciones interactivas avanzadas

- **Gestión de Estado:**
  - `st.session_state` para mantener estado entre interacciones
  - Gestión de progreso del usuario
  - Estado de quizzes y evaluaciones

- **Navegación:**
  - `st.switch_page()` para navegación entre páginas
  - `st.set_page_config()` para configuración de páginas

- **Autenticación:**
  - Integración con sistema de autenticación mediante sidebar
  - Verificación de usuarios autenticados

#### 2.1.3 Características Utilizadas

- Layout responsivo con columnas (`st.columns()`)
- Caché de datos (`@st.cache_data`) para optimización
- Manejo de errores con decoradores personalizados
- Integración con Plotly para gráficos interactivos
- Soporte para HTML personalizado (`unsafe_allow_html=True`)

#### 2.1.4 Archivos Principales de Uso

- `Inicio.py` - Página principal
- `pages/00_Nivel_0_Introduccion.py` a `pages/04_Nivel_4_Avanzado.py` - Páginas de niveles
- `pages/08_Dashboard_Blanco.py` - Dashboard personalizable
- `pages/00_Ayuda.py` - Página de ayuda
- Todos los módulos en `utils/` que generan componentes UI

---

### 2.2 Streamlit-Authenticator

**Versión:** >= 0.4.2  
**Tipo:** Extensión de autenticación para Streamlit  
**Documentación oficial:** https://github.com/mkhorasani/Streamlit-Authenticator

#### 2.2.1 Descripción

Streamlit-Authenticator es una biblioteca que proporciona componentes de autenticación pre-construidos para aplicaciones Streamlit, incluyendo login, registro, recuperación de contraseña, y gestión de sesiones.

#### 2.2.2 Uso en el Proyecto

Aunque el proyecto utiliza un sistema de autenticación personalizado basado en Supabase/PostgreSQL, streamlit-authenticator puede estar presente como dependencia para funcionalidades de autenticación alternativas o futuras implementaciones.

#### 2.2.3 Integración

- Potencial uso en páginas de registro y login
- Gestión de sesiones de usuario
- Componentes de UI para autenticación

---

## 3. Manipulación y Análisis de Datos

### 3.1 Pandas

**Versión:** >= 2.0.0  
**Tipo:** Biblioteca de manipulación y análisis de datos  
**Documentación oficial:** https://pandas.pydata.org

#### 3.1.1 Descripción

Pandas es una biblioteca de código abierto de Python que proporciona estructuras de datos de alto rendimiento y herramientas de análisis de datos. Es fundamental para trabajar con datos tabulares en Python.

#### 3.1.2 Uso en el Proyecto

Pandas es la biblioteca principal para manipulación de datos en toda la plataforma:

- **Carga de Datos:**
  - `pd.read_csv()` para cargar archivos CSV en Nivel 1
  - `pd.read_excel()` para cargar archivos Excel
  - Generación de datos de muestra con DataFrames

- **Manipulación de Datos:**
  - Filtrado de datos (`df[df['columna'] == valor]`)
  - Agrupación (`df.groupby()`) para análisis por categorías y regiones
  - Agregaciones (`sum()`, `mean()`, `count()`, `nunique()`)
  - Operaciones de limpieza de datos

- **Análisis de Datos:**
  - `df.describe()` para estadísticas descriptivas
  - `df.info()` para información del DataFrame
  - `df.isnull()` para detección de valores faltantes
  - `df.duplicated()` para detección de duplicados
  - `df.corr()` para matrices de correlación

- **Transformaciones:**
  - Cálculo de columnas derivadas (margen de ganancia, ingresos totales)
  - Conversión de tipos de datos
  - Ordenamiento (`df.sort_values()`)
  - Reset de índices (`df.reset_index()`)

#### 3.1.3 Casos de Uso Específicos

- **Nivel 1:** Carga y análisis de archivos subidos por el usuario
- **Nivel 2:** Filtrado de datos con múltiples criterios
- **Nivel 3:** Cálculo de métricas y KPIs mediante agrupaciones
- **Nivel 4:** Cálculos avanzados y transformaciones complejas
- **Dashboard:** Manipulación de datos para visualizaciones

#### 3.1.4 Archivos Principales de Uso

- `utils/learning/level_data.py` - Generación de datos de muestra
- `utils/data/data_handling.py` - Operaciones de datos
- `utils/data/data_cleaner.py` - Limpieza de datos
- `utils/analysis/calculations.py` - Cálculos de métricas
- Todos los archivos de niveles que procesan datos

---

### 3.2 NumPy

**Versión:** >= 1.24.0  
**Tipo:** Biblioteca de computación numérica  
**Documentación oficial:** https://numpy.org

#### 3.2.1 Descripción

NumPy es la biblioteca fundamental para computación científica en Python. Proporciona un objeto de array multidimensional de alto rendimiento y herramientas para trabajar con estos arrays.

#### 3.2.2 Uso en el Proyecto

NumPy se utiliza principalmente como dependencia de otras bibliotecas (Pandas, SciPy, scikit-learn) y para operaciones numéricas:

- **Operaciones Numéricas:**
  - Cálculos matemáticos en arrays
  - Generación de datos aleatorios para datasets de ejemplo
  - Operaciones estadísticas básicas

- **Integración con Pandas:**
  - Pandas utiliza NumPy internamente para operaciones numéricas
  - Conversión entre arrays de NumPy y Series/DataFrames de Pandas

- **Análisis Estadístico:**
  - Funciones estadísticas básicas
  - Cálculos de percentiles y cuantiles
  - Operaciones de álgebra lineal (si se requieren)

#### 3.2.3 Casos de Uso Específicos

- Generación de datos de muestra numéricos
- Cálculos de métricas estadísticas
- Operaciones matemáticas en visualizaciones
- Soporte para bibliotecas de análisis estadístico

#### 3.2.4 Archivos Principales de Uso

- `utils/learning/level_data.py` - Generación de datos numéricos
- `utils/analysis/calculations.py` - Cálculos numéricos
- Dependencia implícita en todas las operaciones de Pandas

---

## 4. Visualización de Datos

### 4.1 Plotly

**Versión:** >= 5.15.0  
**Tipo:** Biblioteca de visualización interactiva  
**Documentación oficial:** https://plotly.com/python

#### 4.1.1 Descripción

Plotly es una biblioteca de visualización de código abierto que permite crear gráficos interactivos, dashboards y aplicaciones de datos. Los gráficos de Plotly son altamente interactivos y pueden ser incrustados en aplicaciones web.

#### 4.1.2 Uso en el Proyecto

Plotly es la biblioteca principal para visualizaciones interactivas avanzadas:

- **Visualizaciones en Nivel 4:**
  - `plotly.express` (px) para gráficos de alto nivel:
    - `px.bar()` para gráficos de barras interactivos
    - `px.pie()` para gráficos de pastel
    - `px.imshow()` para mapas de calor (matriz de correlación)
  - `plotly.graph_objects` (go) para gráficos de bajo nivel:
    - `go.Scatter()` para gráficos de línea
  - `plotly.subplots.make_subplots()` para gráficos con múltiples subplots

- **Características Interactivas:**
  - Zoom y panorámica
  - Tooltips al pasar el mouse
  - Selección de datos
  - Exportación de gráficos

- **Integración con Streamlit:**
  - `st.plotly_chart()` para renderizar gráficos Plotly en Streamlit
  - Configuración de layout y estilos

#### 4.1.3 Casos de Uso Específicos

- **Nivel 4:**
  - Gráficos de barras por categoría con escala de colores
  - Gráficos de pastel por región
  - Análisis de tendencias temporales con subplots
  - Matriz de correlación con mapa de calor

- **Dashboard:**
  - Visualizaciones interactivas personalizables
  - Gráficos dinámicos basados en filtros

#### 4.1.4 Archivos Principales de Uso

- `pages/04_Nivel_4_Avanzado.py` - Visualizaciones avanzadas
- `pages/08_Dashboard_Blanco.py` - Dashboard con gráficos interactivos
- `utils/dashboard/dashboard_components.py` - Componentes de visualización
- `utils/analysis/visualizations.py` - Funciones de visualización

---

### 4.2 Matplotlib

**Versión:** >= 3.7.0  
**Tipo:** Biblioteca de visualización 2D  
**Documentación oficial:** https://matplotlib.org

#### 4.2.1 Descripción

Matplotlib es una biblioteca de visualización 2D de Python que produce figuras de calidad de publicación en una variedad de formatos impresos y entornos interactivos.

#### 4.2.2 Uso en el Proyecto

Matplotlib se utiliza principalmente como dependencia de otras bibliotecas (Seaborn, algunas funciones de Pandas) y potencialmente para:

- **Visualizaciones Estáticas:**
  - Gráficos de respaldo si Plotly no está disponible
  - Exportación de gráficos a imágenes
  - Personalización avanzada de gráficos

- **Integración con Otras Bibliotecas:**
  - Seaborn utiliza Matplotlib como backend
  - Algunas funciones de Pandas generan gráficos con Matplotlib

#### 4.2.3 Casos de Uso Específicos

- Generación de gráficos estáticos para exportación
- Visualizaciones de respaldo
- Personalización de estilos de gráficos

---

### 4.3 Seaborn

**Versión:** >= 0.12.0  
**Tipo:** Biblioteca de visualización estadística  
**Documentación oficial:** https://seaborn.pydata.org

#### 4.3.1 Descripción

Seaborn es una biblioteca de visualización de datos estadísticos basada en Matplotlib. Proporciona una interfaz de alto nivel para dibujar gráficos estadísticos atractivos e informativos.

#### 4.3.2 Uso en el Proyecto

Seaborn puede utilizarse para:

- **Visualizaciones Estadísticas:**
  - Gráficos de distribución
  - Análisis de relaciones entre variables
  - Visualizaciones de datos categóricos

- **Estilos y Temas:**
  - Aplicación de temas visuales consistentes
  - Mejora de la estética de gráficos

#### 4.3.3 Casos de Uso Específicos

- Análisis exploratorio de datos avanzado
- Visualizaciones estadísticas en análisis de calidad de datos
- Gráficos de distribución y relaciones

---

## 5. Análisis Estadístico y Machine Learning

### 5.1 SciPy

**Versión:** >= 1.11.0  
**Tipo:** Biblioteca de algoritmos y herramientas matemáticas  
**Documentación oficial:** https://scipy.org

#### 5.1.1 Descripción

SciPy es una biblioteca de código abierto de Python utilizada para computación científica y técnica. Construida sobre NumPy, proporciona algoritmos y herramientas de alto nivel para matemáticas, ciencia e ingeniería.

#### 5.1.2 Uso en el Proyecto

SciPy puede utilizarse para:

- **Análisis Estadístico:**
  - Pruebas estadísticas
  - Análisis de distribuciones
  - Cálculos de correlación avanzados

- **Optimización:**
  - Algoritmos de optimización (si se requieren para análisis avanzados)

- **Procesamiento de Señales:**
  - Análisis de series temporales avanzado
  - Filtrado de datos

#### 5.1.3 Casos de Uso Específicos

- Análisis estadístico avanzado en Nivel 4
- Validación estadística de datos
- Análisis de series temporales

---

### 5.2 scikit-learn

**Versión:** >= 1.3.0  
**Tipo:** Biblioteca de machine learning  
**Documentación oficial:** https://scikit-learn.org

#### 5.2.1 Descripción

scikit-learn es una biblioteca de machine learning de código abierto que proporciona herramientas simples y eficientes para análisis predictivo de datos.

#### 5.2.2 Uso en el Proyecto

Aunque el proyecto se enfoca en análisis de datos básicos y no incluye machine learning en los niveles de aprendizaje (según las preferencias del usuario documentadas), scikit-learn puede estar presente para:

- **Funcionalidades Futuras:**
  - Análisis predictivo avanzado
  - Clustering de datos
  - Detección de anomalías

- **Utilidades Estadísticas:**
  - Algunas funciones de preprocesamiento de datos
  - Métricas de evaluación

#### 5.2.3 Nota Importante

Según la documentación del proyecto, el contenido está dirigido a un público general y no incluye temas avanzados como machine learning. Por lo tanto, scikit-learn puede estar presente como dependencia pero no se utiliza activamente en los niveles de aprendizaje actuales.

---

## 6. Base de Datos y Persistencia

### 6.1 psycopg2-binary

**Versión:** >= 2.9.0  
**Tipo:** Adaptador de base de datos PostgreSQL  
**Documentación oficial:** https://www.psycopg.org

#### 6.1.1 Descripción

psycopg2 es el adaptador de base de datos PostgreSQL más popular para Python. La versión "binary" incluye binarios precompilados, facilitando la instalación.

#### 6.1.2 Uso en el Proyecto

psycopg2-binary es esencial para la conexión con Supabase (que utiliza PostgreSQL):

- **Conexión a Base de Datos:**
  - Conexión a base de datos PostgreSQL/Supabase
  - Ejecución de consultas SQL
  - Gestión de transacciones

- **Operaciones de Datos:**
  - Almacenamiento de progreso de usuarios
  - Guardado de resultados de quizzes
  - Persistencia de configuraciones de dashboard
  - Almacenamiento de respuestas de encuestas

- **Gestión de Usuarios:**
  - Autenticación y autorización
  - Almacenamiento de credenciales (hasheadas)
  - Gestión de sesiones

#### 6.1.3 Casos de Uso Específicos

- **core/database.py:**
  - Gestión de conexiones a base de datos
  - Operaciones CRUD (Create, Read, Update, Delete)
  - Manejo de transacciones

- **core/progress_tracker.py:**
  - Guardado y recuperación de progreso de niveles
  - Actualización de estado de completación

- **core/quiz_system.py:**
  - Almacenamiento de resultados de quizzes
  - Historial de evaluaciones

- **core/survey_system.py:**
  - Persistencia de respuestas de encuestas

#### 6.1.4 Archivos Principales de Uso

- `core/database.py` - Gestión de base de datos
- `core/progress_tracker.py` - Seguimiento de progreso
- `core/auth_service.py` - Autenticación
- `core/quiz_system.py` - Sistema de evaluación
- `core/survey_system.py` - Sistema de encuestas

---

### 6.2 Supabase

**Versión:** Plataforma en la nube (sin versión específica)  
**Tipo:** Plataforma de base de datos backend-as-a-service  
**Documentación oficial:** https://supabase.com

#### 6.2.1 Descripción

Supabase es una plataforma de código abierto que proporciona una base de datos PostgreSQL gestionada en la nube, junto con servicios adicionales como autenticación, almacenamiento, y APIs REST y GraphQL automáticas. Es una alternativa de código abierto a Firebase, construida sobre PostgreSQL.

#### 6.2.2 Uso en el Proyecto

Supabase se utiliza como la plataforma de base de datos principal para la persistencia de datos:

- **Base de Datos PostgreSQL:**
  - Almacenamiento de datos de usuarios y autenticación
  - Persistencia de progreso de aprendizaje de usuarios
  - Almacenamiento de resultados de quizzes y evaluaciones
  - Guardado de configuraciones de dashboard
  - Persistencia de respuestas de encuestas

- **Gestión de Datos:**
  - Operaciones CRUD (Create, Read, Update, Delete) mediante SQL
  - Transacciones de base de datos
  - Consultas optimizadas para rendimiento
  - Gestión de conexiones y pooling

- **Autenticación y Seguridad:**
  - Almacenamiento seguro de credenciales de usuarios
  - Gestión de sesiones de usuario
  - Registro de actividades de seguridad
  - Validación de datos a nivel de base de datos

#### 6.2.3 Características Utilizadas

- **PostgreSQL como Base de Datos:**
  - Tablas relacionales para estructura de datos
  - Índices para optimización de consultas
  - Constraints para integridad de datos
  - Triggers y funciones almacenadas (si se requieren)

- **Conexión mediante psycopg2:**
  - Conexión directa a PostgreSQL de Supabase
  - Ejecución de consultas SQL parametrizadas
  - Gestión de transacciones
  - Manejo de errores de base de datos

- **Ventajas de Supabase:**
  - Base de datos gestionada sin necesidad de administración de servidor
  - Escalabilidad automática
  - Backups automáticos
  - Interfaz web para gestión de datos
  - APIs REST y GraphQL automáticas (si se requieren en el futuro)

#### 6.2.4 Casos de Uso Específicos

- **core/database.py:**
  - Gestión de conexiones a Supabase
  - Operaciones de base de datos mediante SQL
  - Inicialización de esquema de base de datos
  - Migraciones de esquema

- **core/auth_service.py:**
  - Almacenamiento de usuarios y credenciales
  - Gestión de sesiones de usuario
  - Registro de actividades de autenticación

- **core/progress_tracker.py:**
  - Persistencia de progreso de niveles de aprendizaje
  - Seguimiento de completación de niveles
  - Historial de actividades del usuario

- **core/quiz_system.py:**
  - Almacenamiento de resultados de evaluaciones
  - Historial de intentos de quizzes
  - Estadísticas de rendimiento

- **core/survey_system.py:**
  - Persistencia de respuestas de encuestas
  - Almacenamiento de datos de feedback

#### 6.2.5 Configuración

La conexión a Supabase se configura mediante:
- Variables de entorno para credenciales
- Archivo de configuración (`config/config.yaml`)
- Parámetros de conexión (host, puerto, base de datos, usuario, contraseña)

#### 6.2.6 Archivos Principales de Uso

- `core/database.py` - Gestión de conexiones y operaciones con Supabase
- `core/config.py` - Configuración de conexión a Supabase
- `config/config.yaml` - Parámetros de configuración de base de datos
- Todos los módulos que requieren persistencia de datos

---

### 6.3 SQLite

**Versión:** Incluida en Python estándar (sqlite3)  
**Tipo:** Base de datos SQL embebida  
**Documentación oficial:** https://docs.python.org/3/library/sqlite3.html

#### 6.3.1 Descripción

SQLite es una biblioteca de base de datos SQL embebida, ligera y sin servidor que está incluida en la biblioteca estándar de Python. SQLite almacena toda la base de datos en un solo archivo y no requiere un proceso de servidor separado, lo que la hace ideal para aplicaciones pequeñas a medianas, desarrollo local, y prototipado.

#### 6.3.2 Uso en el Proyecto

SQLite se utiliza como la base de datos por defecto y alternativa en la plataforma TCC:

- **Base de Datos por Defecto:**
  - Se utiliza cuando Supabase no está configurado o no está disponible
  - Base de datos local almacenada en el archivo `tcc_database.db`
  - No requiere configuración adicional ni servicios externos

- **Sistema Dual de Base de Datos:**
  - El proyecto soporta tanto SQLite como PostgreSQL/Supabase
  - La selección se realiza mediante configuración (`db_type` en secrets)
  - Si Supabase está configurado pero `psycopg2` no está instalado, automáticamente se usa SQLite como respaldo

- **Gestión de Datos:**
  - Almacenamiento de usuarios y autenticación
  - Persistencia de progreso de aprendizaje de usuarios
  - Almacenamiento de resultados de quizzes y evaluaciones
  - Guardado de configuraciones de dashboard
  - Persistencia de respuestas de encuestas
  - Gestión de archivos subidos y sesiones de análisis

#### 6.3.3 Características Utilizadas

- **Conexión y Configuración:**
  - `sqlite3.connect()` para establecer conexiones
  - Modo WAL (Write-Ahead Logging) para mejor acceso concurrente
  - Timeout de 5 segundos para manejar acceso concurrente
  - `row_factory = sqlite3.Row` para acceso tipo diccionario a filas
  - Habilitación de claves foráneas con `PRAGMA foreign_keys = ON`

- **Operaciones de Base de Datos:**
  - Creación de tablas con `CREATE TABLE IF NOT EXISTS`
  - Operaciones CRUD (Create, Read, Update, Delete)
  - Transacciones para garantizar integridad de datos
  - Consultas SQL estándar

- **Ventajas de SQLite:**
  - Sin necesidad de servidor de base de datos separado
  - Archivo único fácil de respaldar y migrar
  - Ideal para desarrollo local y pruebas
  - Sin dependencias externas (incluida en Python)
  - Rendimiento excelente para aplicaciones pequeñas a medianas

#### 6.3.4 Casos de Uso Específicos

- **core/database.py:**
  - Gestión de conexiones a SQLite
  - Creación e inicialización de esquema de base de datos
  - Operaciones de base de datos mediante SQL
  - Detección automática de tipo de base de datos
  - Fallback automático a SQLite si Supabase no está disponible

- **core/auth_service.py:**
  - Almacenamiento de usuarios y credenciales en SQLite
  - Gestión de sesiones de usuario
  - Registro de actividades de autenticación

- **core/progress_tracker.py:**
  - Persistencia de progreso de niveles de aprendizaje
  - Seguimiento de completación de niveles
  - Historial de actividades del usuario

- **core/quiz_system.py:**
  - Almacenamiento de resultados de evaluaciones
  - Historial de intentos de quizzes
  - Estadísticas de rendimiento

- **core/survey_system.py:**
  - Persistencia de respuestas de encuestas
  - Almacenamiento de datos de feedback

- **core/dashboard_repository.py:**
  - Guardado de configuraciones de dashboard
  - Persistencia de componentes de dashboard personalizados

#### 6.3.5 Configuración

La configuración de SQLite es automática y no requiere configuración adicional:

- **Ubicación del Archivo:**
  - Por defecto: `tcc_database.db` en el directorio raíz del proyecto
  - Configurable mediante `DB_PATH` en `core/database.py`

- **Inicialización Automática:**
  - La base de datos se crea automáticamente si no existe
  - Las tablas se crean automáticamente al inicializar la aplicación
  - No requiere migraciones manuales para el esquema inicial

- **Selección de Base de Datos:**
  - Se selecciona mediante `db_type` en configuración/secrets
  - Valor por defecto: `"sqlite"` si no se especifica
  - Se puede cambiar a `"supabase"` para usar PostgreSQL

#### 6.3.6 Limitaciones y Consideraciones

- **Escalabilidad:**
  - SQLite es ideal para aplicaciones pequeñas a medianas
  - Para aplicaciones con alto tráfico concurrente, se recomienda Supabase/PostgreSQL

- **Persistencia en Streamlit Cloud:**
  - En el tier gratuito de Streamlit Cloud, los archivos SQLite se reinician periódicamente
  - Para producción con persistencia garantizada, se recomienda usar Supabase

- **Acceso Concurrente:**
  - SQLite maneja acceso concurrente de lectura bien
  - Para escritura concurrente intensiva, PostgreSQL/Supabase es más adecuado

#### 6.3.7 Migración y Respaldo

- **Exportación de Datos:**
  - Scripts de migración disponibles para exportar datos de SQLite a JSON
  - `migrations/export_sqlite_data.py` - Exporta todos los datos a formato JSON
  - `migrations/migrate_sqlite_to_supabase.py` - Migra datos de SQLite a Supabase

- **Respaldo:**
  - Respaldo simple: copiar el archivo `tcc_database.db`
  - Exportación estructurada a JSON para migraciones

#### 6.3.8 Archivos Principales de Uso

- `core/database.py` - Gestión de conexiones y operaciones con SQLite
- `core/config.py` - Configuración de tipo de base de datos
- `migrations/export_sqlite_data.py` - Exportación de datos SQLite
- `migrations/migrate_sqlite_to_supabase.py` - Migración a Supabase
- Todos los módulos que requieren persistencia de datos

---

## 7. Autenticación y Seguridad

### 7.1 bcrypt

**Versión:** >= 4.0.0  
**Tipo:** Biblioteca de hashing de contraseñas  
**Documentación oficial:** https://github.com/pyca/bcrypt

#### 7.1.1 Descripción

bcrypt es una biblioteca de hashing de contraseñas diseñada para ser lenta y resistente a ataques de fuerza bruta. Es ampliamente utilizada para almacenar contraseñas de forma segura.

#### 7.1.2 Uso en el Proyecto

bcrypt se utiliza para:

- **Hashing de Contraseñas:**
  - Hash de contraseñas de usuarios durante el registro
  - Verificación de contraseñas durante el login
  - Almacenamiento seguro de credenciales

- **Seguridad:**
  - Prevención de almacenamiento de contraseñas en texto plano
  - Protección contra ataques de diccionario y fuerza bruta

#### 7.1.3 Casos de Uso Específicos

- **core/auth_service.py:**
  - Hash de contraseñas nuevas
  - Verificación de contraseñas en login
  - Actualización de contraseñas

- **core/database.py:**
  - Operaciones de seguridad relacionadas con usuarios

#### 7.1.4 Archivos Principales de Uso

- `core/auth_service.py` - Servicio de autenticación
- `core/database.py` - Operaciones de base de datos relacionadas con usuarios

---

## 8. Utilidades y Soporte

### 8.1 PyYAML

**Versión:** >= 6.0.0  
**Tipo:** Parser YAML para Python  
**Documentación oficial:** https://pyyaml.org

#### 8.1.1 Descripción

PyYAML es un parser completo de YAML para Python. YAML es un formato de serialización de datos legible por humanos.

#### 8.1.2 Uso en el Proyecto

PyYAML se utiliza para:

- **Configuración:**
  - Lectura de archivos de configuración (`config.yaml`)
  - Gestión de configuraciones de la aplicación
  - Configuración de autenticación (si se utiliza YAML)

- **Datos Estructurados:**
  - Carga de datos de configuración
  - Persistencia de configuraciones

#### 8.1.3 Casos de Uso Específicos

- **config/config.yaml:**
  - Configuración de la aplicación
  - Parámetros de conexión a base de datos
  - Configuraciones de autenticación

#### 8.1.4 Archivos Principales de Uso

- `core/config.py` - Gestión de configuración
- `config/config.yaml` - Archivo de configuración

---

### 8.2 openpyxl

**Versión:** >= 3.1.0  
**Tipo:** Biblioteca para leer y escribir archivos Excel  
**Documentación oficial:** https://openpyxl.readthedocs.io

#### 8.2.1 Descripción

openpyxl es una biblioteca de Python para leer y escribir archivos Excel 2010 xlsx/xlsm/xltx/xltm.

#### 8.2.2 Uso en el Proyecto

openpyxl se utiliza para:

- **Carga de Archivos Excel:**
  - Lectura de archivos `.xlsx` y `.xls` en Nivel 1
  - Procesamiento de datos de Excel subidos por usuarios
  - Soporte para múltiples hojas de cálculo

- **Exportación:**
  - Potencial exportación de resultados a Excel
  - Generación de reportes en formato Excel

#### 8.2.3 Casos de Uso Específicos

- **Nivel 1:**
  - Carga de archivos Excel subidos por usuarios
  - Conversión de datos de Excel a DataFrames de Pandas

- **Sistema de Exportación:**
  - Exportación de dashboards a Excel
  - Generación de reportes

#### 8.2.4 Archivos Principales de Uso

- `pages/01_Nivel_1_Basico.py` - Carga de archivos Excel
- `utils/data/data_handling.py` - Procesamiento de archivos
- `utils/system/export.py` - Funcionalidad de exportación

---

### 8.3 requests

**Versión:** >= 2.31.0  
**Tipo:** Biblioteca HTTP para Python  
**Documentación oficial:** https://requests.readthedocs.io

#### 8.3.1 Descripción

requests es una biblioteca HTTP elegante y simple para Python, construida para uso humano. Permite enviar solicitudes HTTP/1.1 de forma extremadamente simple.

#### 8.3.2 Uso en el Proyecto

requests se utiliza para:

- **Comunicación con APIs:**
  - Comunicación con Supabase REST API (si se requiere)
  - Llamadas a servicios externos
  - Integración con servicios web

- **Carga de Datos Remotos:**
  - Descarga de datasets desde URLs
  - Carga de recursos externos

#### 8.3.3 Casos de Uso Específicos

- Integración con Supabase
- Comunicación con servicios externos
- Carga de datos desde URLs

---

### 8.4 reportlab

**Versión:** Sin especificar (última versión)  
**Tipo:** Biblioteca para generación de PDFs  
**Documentación oficial:** https://www.reportlab.com

#### 8.4.1 Descripción

ReportLab es una biblioteca de Python para generar documentos PDF programáticamente.

#### 8.4.2 Uso en el Proyecto

reportlab puede utilizarse para:

- **Generación de Reportes:**
  - Exportación de dashboards a PDF
  - Generación de reportes de progreso
  - Creación de documentos con visualizaciones

- **Exportación:**
  - Exportación de resultados de análisis
  - Generación de certificados de completación

#### 8.4.3 Casos de Uso Específicos

- Exportación de dashboards a PDF
- Generación de reportes de progreso del usuario
- Certificados de completación de niveles

---

### 8.5 kaleido

**Versión:** Sin especificar (última versión)  
**Tipo:** Servidor de imágenes para exportación de gráficos  
**Documentación oficial:** https://github.com/plotly/Kaleido

#### 8.5.1 Descripción

Kaleido es un servidor de imágenes multiplataforma para exportar gráficos de Plotly a imágenes estáticas (PNG, SVG, PDF, etc.).

#### 8.5.2 Uso en el Proyecto

kaleido se utiliza para:

- **Exportación de Gráficos:**
  - Conversión de gráficos Plotly interactivos a imágenes estáticas
  - Exportación de visualizaciones para reportes
  - Generación de imágenes para documentación

- **Integración con Plotly:**
  - `fig.write_image()` para exportar gráficos
  - Generación de imágenes para PDFs y documentos

#### 8.5.3 Casos de Uso Específicos

- Exportación de dashboards con gráficos Plotly
- Generación de reportes PDF con visualizaciones
- Creación de imágenes para documentación

---

## 9. Arquitectura de Dependencias

### 9.1 Dependencias Principales

Las dependencias principales (core dependencies) son aquellas esenciales para el funcionamiento básico de la aplicación:

1. **streamlit** - Framework web principal
2. **pandas** - Manipulación de datos
3. **numpy** - Operaciones numéricas (dependencia de pandas)
4. **SQLite** (sqlite3) - Base de datos embebida por defecto (incluida en Python)
5. **Supabase** - Plataforma de base de datos PostgreSQL (alternativa a SQLite)
6. **psycopg2-binary** - Conexión a base de datos PostgreSQL/Supabase
7. **bcrypt** - Seguridad de contraseñas

### 9.2 Dependencias de Visualización

Dependencias específicas para visualización de datos:

1. **plotly** - Visualizaciones interactivas
2. **matplotlib** - Visualizaciones estáticas
3. **seaborn** - Visualizaciones estadísticas
4. **kaleido** - Exportación de gráficos Plotly

### 9.3 Dependencias de Soporte

Dependencias que proporcionan funcionalidades auxiliares:

1. **openpyxl** - Procesamiento de Excel
2. **pyyaml** - Configuración
3. **requests** - Comunicación HTTP
4. **reportlab** - Generación de PDFs

### 9.4 Dependencias Opcionales

Dependencias que pueden no estar activamente utilizadas pero están disponibles:

1. **scikit-learn** - Machine learning (no utilizado en niveles actuales)
2. **scipy** - Análisis estadístico avanzado
3. **streamlit-authenticator** - Autenticación alternativa

---

## 10. Gestión de Versiones

### 10.1 Estrategia de Versionado

El proyecto utiliza versionado semántico con restricciones mínimas:
- Versiones mínimas especificadas con `>=`
- Permite actualizaciones de parches y características menores
- No especifica versiones máximas (permite actualizaciones)

### 10.2 Compatibilidad

- **Python:** Compatible con Python 3.8+ (implícito por versiones de dependencias)
- **Streamlit:** >= 1.28.0 (versión relativamente reciente)
- **Pandas:** >= 2.0.0 (versión mayor, incluye cambios significativos)

### 10.3 Actualizaciones Recomendadas

Se recomienda mantener las dependencias actualizadas para:
- Correcciones de seguridad
- Mejoras de rendimiento
- Nuevas características
- Compatibilidad con versiones más recientes de Python

---

## 11. Instalación y Configuración

### 11.1 Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 11.2 Dependencias del Sistema

Algunas dependencias requieren bibliotecas del sistema:
- **psycopg2-binary:** Incluye binarios precompilados (no requiere PostgreSQL instalado)
- **kaleido:** Puede requerir dependencias del sistema según la plataforma

### 11.3 Configuración de Entorno

Variables de entorno potencialmente requeridas:
- Credenciales de base de datos Supabase (host, puerto, nombre de base de datos, usuario, contraseña)
- URL de conexión a Supabase
- Configuraciones de autenticación
- Rutas de archivos de configuración

---

## 12. Consideraciones de Rendimiento

### 12.1 Optimizaciones Implementadas

- **Caché de Streamlit:** Uso de `@st.cache_data` para datos de muestra
- **Lazy Loading:** Carga de datos solo cuando se necesitan
- **Consultas Optimizadas:** Uso eficiente de consultas a base de datos

### 12.2 Limitaciones Conocidas

- **Tamaño de Archivos:** Limitaciones en carga de archivos grandes
- **Rendimiento de Visualizaciones:** Gráficos complejos pueden ser lentos
- **Base de Datos:** Dependencia de latencia de red para Supabase (conexión a servidor en la nube)

---

## 13. Seguridad

### 13.1 Medidas de Seguridad Implementadas

- **Hashing de Contraseñas:** Uso de bcrypt para almacenamiento seguro
- **Autenticación:** Sistema de autenticación robusto
- **Validación de Datos:** Validación de entrada de usuario
- **Manejo de Errores:** Manejo seguro de excepciones

### 13.2 Mejores Prácticas

- No almacenar contraseñas en texto plano
- Validar todas las entradas de usuario
- Usar conexiones seguras (HTTPS/SSL) para comunicación con Supabase
- Mantener dependencias actualizadas para parches de seguridad

---

## 14. Conclusiones

El stack tecnológico de la Plataforma TCC está cuidadosamente seleccionado para proporcionar una base sólida y moderna para una aplicación educativa de análisis de datos. La combinación de Streamlit para la interfaz, Pandas para manipulación de datos, Plotly para visualizaciones interactivas, y Supabase (PostgreSQL gestionado) para persistencia, crea un ecosistema coherente y potente.

Las dependencias están bien organizadas y cada una cumple un propósito específico dentro de la arquitectura del sistema. La elección de versiones mínimas permite flexibilidad mientras garantiza funcionalidades esenciales.

El stack es escalable y permite futuras extensiones, como se evidencia por la inclusión de bibliotecas como scikit-learn que, aunque no se utilizan actualmente, están disponibles para funcionalidades avanzadas futuras.

---

## Referencias

- Documentación oficial de cada biblioteca mencionada
- Archivo `requirements.txt` del proyecto
- Código fuente del proyecto TCC
- Mejores prácticas de la industria para desarrollo de aplicaciones de datos

---

**Fin del Documento**

