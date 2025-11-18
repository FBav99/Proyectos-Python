# 📅 Guía de Línea de Tiempo del Proyecto

## Descripción General

La página de **Línea de Tiempo del Proyecto** es una funcionalidad que visualiza automáticamente el historial de desarrollo del proyecto basándose en los commits del repositorio Git. Esta página proporciona una vista cronológica organizada por semanas y categorizada por tipo de acción.

## Ubicación

- **Página Streamlit**: `pages/09_Linea_Tiempo.py`
- **Utilidades**: `utils/system/project_timeline.py`

## Funcionalidades Principales

### 1. Visualización de Commits por Semana

La página agrupa automáticamente todos los commits del repositorio por semanas (desde el lunes de cada semana) y los muestra en orden cronológico inverso (más recientes primero).

### 2. Categorización de Commits

Los commits se categorizan automáticamente según su mensaje en los siguientes tipos:

- **➕ ADD**: Nuevas funcionalidades o archivos agregados
- **🔧 FIX**: Correcciones de bugs o errores
- **🗑️ REMOVE**: Eliminación de archivos o código
- **🔀 MERGE**: Fusiones de ramas
- **📚 DOCS**: Documentación
- **♻️ REFACTOR**: Refactorización o reorganización de código
- **📝 OTHER**: Otros tipos de commits

### 3. Métricas de Resumen

La página muestra las siguientes métricas en la parte superior:

- **Total de Commits**: Número total de commits en el repositorio
- **Semanas de Desarrollo**: Número de semanas con actividad
- **Inicio**: Fecha de la primera semana de desarrollo
- **Última Semana**: Fecha de la semana más reciente con actividad

### 4. Resumen por Tipo de Acción

Muestra un resumen visual con el conteo de commits por cada tipo de acción, con colores distintivos para cada categoría.

### 5. Agrupación Inteligente

Los commits similares se agrupan automáticamente para evitar duplicados visuales, mostrando:
- Commits únicos con su fecha y hash
- Commits repetidos agrupados con el rango de fechas y el número de veces que aparecen

## Cómo Funciona

### Proceso de Generación

1. **Obtención de Commits**: Utiliza `git log` para obtener todos los commits del repositorio
2. **Categorización**: Analiza el mensaje de cada commit para determinar su tipo
3. **Agrupación por Semana**: Agrupa commits por semana (lunes a domingo)
4. **Agrupación por Acción**: Dentro de cada semana, agrupa por tipo de acción
5. **Visualización**: Muestra la información de forma organizada y visual

### Funciones Principales

#### `get_git_commits(limit=None)`
Obtiene los commits del repositorio Git.

**Parámetros:**
- `limit` (opcional): Número máximo de commits a recuperar

**Retorna:**
- Lista de diccionarios con: `hash`, `date`, `message`

#### `categorize_commit(message)`
Categoriza un commit según su mensaje.

**Parámetros:**
- `message`: Mensaje del commit

**Retorna:**
- Tipo de acción (ADD, FIX, REMOVE, MERGE, DOCS, REFACTOR, OTHER)

#### `group_commits_by_week_and_action(commits)`
Agrupa commits por semana y tipo de acción.

**Parámetros:**
- `commits`: Lista de commits

**Retorna:**
- Diccionario anidado: `{week_start: {action_type: [commits]}}`

#### `get_timeline_summary(grouped_commits)`
Genera estadísticas resumidas de la línea de tiempo.

**Parámetros:**
- `grouped_commits`: Commits agrupados

**Retorna:**
- Diccionario con métricas: `total_commits`, `total_weeks`, `action_counts`, `first_week`, `last_week`

## Requisitos

### Dependencias del Sistema

- **Git**: El proyecto debe estar en un repositorio Git válido
- **Python**: Módulos estándar: `subprocess`, `datetime`, `collections`

### Dependencias del Proyecto

- `streamlit`: Para la interfaz de usuario
- `utils.ui.auth_ui`: Para la autenticación
- `core.streamlit_error_handler`: Para el manejo de errores

## Uso

### Acceso a la Página

La página está disponible en la aplicación Streamlit como:
- **Página 09**: "Línea de Tiempo del Proyecto"
- **Icono**: 📅

### Visualización

1. Al acceder a la página, se cargan automáticamente los commits del repositorio
2. Si no se pueden cargar los commits, se muestra una advertencia
3. Los commits se muestran organizados por semanas
4. Cada semana muestra los commits agrupados por tipo de acción
5. Los commits similares se agrupan para facilitar la lectura

## Convenciones de Commits

Para que la categorización funcione correctamente, los mensajes de commit deben seguir estas convenciones:

- **ADD**: `ADD: descripción` o `add: descripción`
- **FIX**: `FIX: descripción` o `fix: descripción`
- **REMOVE**: `REMOVE: descripción` o `remove: descripción`
- **MERGE**: Cualquier mensaje que contenga "MERGE" o "merge"
- **DOCS**: Mensajes que contengan "DOC", "DOCUMENTACION", "DOCUMENTATION"
- **REFACTOR**: Mensajes que contengan "REFACTOR", "ORGANIZACION", "ORGANIZATION", "MODULAR", "SEPARACION"
- **OTHER**: Cualquier otro tipo de commit

## Personalización

### Colores de Acciones

Los colores se definen en `get_action_color()`:

```python
colors = {
    'ADD': '#28a745',      # Verde
    'FIX': '#ffc107',      # Amarillo
    'REMOVE': '#dc3545',   # Rojo
    'MERGE': '#6f42c1',    # Púrpura
    'DOCS': '#17a2b8',     # Azul claro
    'REFACTOR': '#fd7e14', # Naranja
    'OTHER': '#6c757d'     # Gris
}
```

### Iconos de Acciones

Los iconos se definen en `get_action_icon()` y pueden modificarse según preferencias.

## Limitaciones

1. **Requiere Git**: El proyecto debe estar en un repositorio Git válido
2. **Acceso a Git**: Necesita permisos para ejecutar comandos `git log`
3. **Formato de Fecha**: Los commits deben tener formato de fecha estándar de Git
4. **Categorización**: Depende de las convenciones de mensajes de commit

## Solución de Problemas

### No se cargan los commits

**Problema**: Aparece el mensaje "No se pudieron cargar los commits del repositorio"

**Soluciones**:
1. Verificar que el proyecto esté en un repositorio Git válido
2. Verificar que Git esté instalado y disponible en el PATH
3. Verificar permisos de lectura del repositorio

### Commits no categorizados correctamente

**Problema**: Los commits aparecen como "OTHER" cuando deberían tener otra categoría

**Solución**: Asegurarse de que los mensajes de commit sigan las convenciones mencionadas anteriormente

## Ejemplos de Uso

### Ver el historial completo del proyecto

Simplemente accede a la página "Línea de Tiempo del Proyecto" y se mostrará automáticamente todo el historial.

### Filtrar por tipo de acción

Usa los expanders de cada tipo de acción para ver solo los commits de ese tipo.

### Ver actividad por semana

Cada semana muestra un resumen de la actividad de desarrollo durante ese período.

## Integración con el Proyecto

Esta funcionalidad se integra con:

- **Sistema de Autenticación**: Requiere autenticación de usuario
- **Manejo de Errores**: Utiliza el sistema centralizado de manejo de errores
- **UI Consistente**: Sigue el diseño y estilo del resto de la aplicación

## Notas Técnicas

- La página utiliza `unsafe_allow_html=True` para el renderizado de HTML personalizado
- Los commits se agrupan por similitud usando los primeros 35 caracteres del mensaje normalizado
- Las semanas se calculan desde el lunes (día 0) hasta el domingo (día 6)
- El formato de fecha mostrado es DD/MM/YYYY para mejor legibilidad en español

