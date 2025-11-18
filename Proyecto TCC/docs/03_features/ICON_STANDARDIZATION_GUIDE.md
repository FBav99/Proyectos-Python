# 🎨 Guía de Estandarización de Iconos

## Descripción

Esta guía explica cómo usar las herramientas para reemplazar emojis por iconos PNG reales y mantener un conjunto de iconos consistente en todo el proyecto.

## Herramientas Disponibles

### 1. `emoji_to_icon_converter.py` - Convertir Emojis a Iconos PNG ⭐ RECOMENDADO

Esta es la herramienta principal para reemplazar emojis por iconos PNG reales usando el sistema de iconos existente.

### 2. `icon_standardizer.py` - Estandarizar Iconos

Herramienta para estandarizar emojis (mantiene emojis pero los unifica).

## Herramienta Principal: `emoji_to_icon_converter.py`

### ¿Qué hace?

Esta herramienta reemplaza **todos los emojis en el código** por llamadas al sistema de iconos que devuelve imágenes PNG reales. Esto significa que en lugar de mostrar emojis, se mostrarán iconos PNG consistentes.

### Uso Básico

#### 1. Ver qué se convertiría (Dry Run)

```bash
python utils/ui/emoji_to_icon_converter.py
```

O explícitamente:

```bash
python utils/ui/emoji_to_icon_converter.py --dry-run
```

Esto mostrará todos los cambios que se harían **sin modificar archivos**.

#### 2. Generar Reporte Detallado

```bash
python utils/ui/emoji_to_icon_converter.py --report
```

Esto genera `emoji_conversion_report.json` con:
- Archivos que contienen emojis
- Qué emojis tienen iconos PNG disponibles
- Contexto donde se usan (page_icon, markdown, strings, etc.)

#### 3. Aplicar Conversión

**⚠️ IMPORTANTE**: Haz backup o commit de Git antes de ejecutar esto.

```bash
python utils/ui/emoji_to_icon_converter.py --apply
```

Esto:
- Reemplaza emojis por llamadas a `get_icon()` o `replace_emojis()`
- Agrega imports necesarios automáticamente
- Mantiene la funcionalidad pero usa iconos PNG

### Ejemplos de Conversión

#### Antes:
```python
st.set_page_config(
    page_title="Nivel 1",
    page_icon="📚",
    layout="wide"
)

st.success("✅ Operación exitosa")
st.markdown("📊 Aquí están los datos")
```

#### Después:
```python
from utils.ui.icon_system import get_icon, replace_emojis

st.set_page_config(
    page_title="Nivel 1",
    page_icon=get_icon("📚", 20),
    layout="wide"
)

st.success(replace_emojis("✅ Operación exitosa"))
st.markdown(replace_emojis("📊 Aquí están los datos"))
```

### Contextos Soportados

La herramienta detecta automáticamente el contexto y aplica la conversión apropiada:

- **`page_icon`**: Reemplaza por `get_icon(emoji, 20)`
- **`st.markdown()`**: Envuelve con `replace_emojis()`
- **`st.success/error/warning/info()`**: Envuelve con `replace_emojis()`
- **F-strings**: Reemplaza emoji por `{get_icon(emoji, 20)}`
- **Strings normales**: Envuelve con `replace_emojis()`

## Herramienta Secundaria: `icon_standardizer.py`

La herramienta `utils/ui/icon_standardizer.py` permite:

1. **Analizar** el uso de iconos en todo el proyecto
2. **Generar reportes** de iconos encontrados y sugerencias de reemplazo
3. **Reemplazar en bulk** emojis por iconos estandarizados
4. **Crear constantes** de iconos para uso consistente

## Uso Básico

### 1. Analizar Uso de Iconos

Primero, analiza qué iconos se están usando en el proyecto:

```bash
python utils/ui/icon_standardizer.py --analyze
```

Esto mostrará:
- Total de archivos analizados
- Iconos únicos encontrados
- Emojis sin mapeo a estándares

### 2. Generar Reporte Detallado

Para obtener un reporte completo en JSON:

```bash
python utils/ui/icon_standardizer.py --report
```

Esto genera `icon_replacement_report.json` con:
- Lista de todos los iconos encontrados
- Ubicaciones donde se usan
- Sugerencias de reemplazo estandarizado
- Emojis sin mapeo

### 3. Dry Run (Simulación)

Antes de hacer cambios reales, ejecuta en modo simulación:

```bash
python utils/ui/icon_standardizer.py --dry-run
```

Esto mostrará todos los cambios que se harían sin modificar archivos.

### 4. Aplicar Estandarización

Una vez revisado el dry-run, aplica los cambios:

```bash
python utils/ui/icon_standardizer.py
```

**⚠️ Importante**: Asegúrate de tener un backup o commit de Git antes de ejecutar esto.

### 5. Crear Archivo de Constantes

Para crear un archivo con constantes de iconos estandarizados:

```bash
python utils/ui/icon_standardizer.py --create-constants
```

Esto crea `utils/ui/icon_constants.py` con constantes como:
- `ICON_NIVEL_1 = "📚"`
- `ICON_INICIO = "🏠"`
- `ICON_EXITO = "✅"`
- etc.

## Iconos Estandarizados

### Niveles de Aprendizaje
- **Nivel 0**: 🌟 (Introducción)
- **Nivel 1**: 📚 (Básico)
- **Nivel 2**: 🔍 (Filtros)
- **Nivel 3**: 📊 (Métricas)
- **Nivel 4**: 🚀 (Avanzado)

### Navegación
- **Inicio**: 🏠
- **Ayuda**: ❓
- **Dashboard**: 📊
- **Configuración**: ⚙️
- **Usuario**: 👤

### Acciones
- **Agregar**: ➕
- **Eliminar**: 🗑️
- **Editar**: 📝
- **Guardar**: 💾
- **Exportar**: 📤
- **Importar**: 📥
- **Buscar**: 🔍
- **Actualizar**: 🔄

### Estados
- **Éxito**: ✅
- **Error**: ❌
- **Advertencia**: ⚠️
- **Información**: ℹ️
- **Cargando**: ⏳

### Seguridad
- **Seguridad**: 🔐
- **Bloqueado**: 🔒
- **Desbloqueado**: 🔓
- **Autenticación**: 🔑
- **OAuth**: 🌐

### Datos y Análisis
- **Datos**: 📊
- **Gráfico**: 📈
- **Tabla**: 📋
- **Métricas**: 📊
- **Cálculo**: 🧮

## Uso de Constantes de Iconos

Una vez creado el archivo de constantes, puedes usarlo así:

```python
from utils.ui.icon_constants import ICON_NIVEL_1, ICON_EXITO, get_standard_icon

# Usar constantes directamente
st.page_config(page_icon=ICON_NIVEL_1)

# O usar la función helper
icon_html = get_standard_icon('nivel1', size=24)
st.markdown(icon_html, unsafe_allow_html=True)
```

## Integración con Sistema de Iconos Existente

El sistema de iconos existente (`utils/ui/icon_system.py`) ya mapea emojis a archivos PNG. La estandarización complementa esto asegurando que:

1. Los emojis usados sean consistentes
2. Se use el sistema de iconos PNG cuando esté disponible
3. Los iconos tengan significado semántico claro

## Flujo de Trabajo Recomendado

### Para Reemplazar Emojis por Iconos PNG (Recomendado)

1. **Generar reporte**: `python utils/ui/emoji_to_icon_converter.py --report`
2. **Revisar reporte**: Abre `emoji_conversion_report.json` para ver qué se puede convertir
3. **Dry run**: `python utils/ui/emoji_to_icon_converter.py` (muestra cambios sin aplicar)
4. **Backup**: Haz commit de Git o backup antes de continuar
5. **Aplicar conversión**: `python utils/ui/emoji_to_icon_converter.py --apply`
6. **Verificar**: Prueba la aplicación para asegurar que los iconos se muestran correctamente
7. **Commit**: Guarda los cambios en Git

### Para Solo Estandarizar Emojis (sin convertir a PNG)

1. **Análisis inicial**: Ejecuta `--analyze` para ver el estado actual
2. **Revisar reporte**: Genera y revisa `icon_replacement_report.json`
3. **Dry run**: Ejecuta `--dry-run` para ver cambios propuestos
4. **Backup**: Haz commit de Git o backup antes de continuar
5. **Aplicar cambios**: Ejecuta sin `--dry-run` para aplicar
6. **Crear constantes**: Ejecuta `--create-constants` para generar constantes
7. **Actualizar código**: Reemplaza emojis hardcodeados por constantes donde sea posible
8. **Verificar**: Revisa que todo funcione correctamente

## Personalización

### Agregar Nuevos Iconos Estandarizados

Edita `utils/ui/icon_standardizer.py` y agrega al diccionario `STANDARD_ICONS`:

```python
STANDARD_ICONS = {
    # ... iconos existentes ...
    'nuevo_icono': '🆕',
}
```

### Modificar Mapeos de Reemplazo

Edita el diccionario `EMOJI_TO_STANDARD` para cambiar qué emojis se reemplazan:

```python
EMOJI_TO_STANDARD = {
    # ... mapeos existentes ...
    '🆕': 'nuevo_icono',
}
```

## Ejemplos de Reemplazo

### Antes:
```python
st.page_config(page_icon="📚")
st.success("✅ Operación exitosa")
st.error("❌ Error en la operación")
```

### Después (con constantes):
```python
from utils.ui.icon_constants import ICON_NIVEL_1, ICON_EXITO, ICON_ERROR

st.page_config(page_icon=ICON_NIVEL_1)
st.success(f"{ICON_EXITO} Operación exitosa")
st.error(f"{ICON_ERROR} Error en la operación")
```

### Después (con sistema de iconos PNG):
```python
from utils.ui.icon_system import get_icon
from utils.ui.icon_constants import ICON_NIVEL_1, ICON_EXITO

st.page_config(page_icon=ICON_NIVEL_1)
st.markdown(f"{get_icon(ICON_EXITO, 20)} Operación exitosa", unsafe_allow_html=True)
```

## Notas Importantes

- ⚠️ **Siempre haz backup** antes de ejecutar reemplazos en bulk
- ✅ **Revisa el dry-run** cuidadosamente antes de aplicar cambios
- 🔍 **Verifica manualmente** archivos críticos después de reemplazos
- 📝 **Documenta cambios** en commits de Git con mensajes descriptivos
- 🧪 **Prueba la aplicación** después de aplicar cambios

## Solución de Problemas

### El script no encuentra archivos
- Verifica que estés ejecutando desde la raíz del proyecto
- Revisa que los directorios de exclusión sean correctos

### Reemplazos incorrectos
- Revisa el reporte JSON generado
- Ajusta los mapeos en `EMOJI_TO_STANDARD`
- Ejecuta dry-run antes de aplicar cambios reales

### Iconos PNG no se muestran
- Verifica que los archivos PNG existan en `assets/images/icons/`
- Revisa que el sistema de iconos esté correctamente configurado
- Usa el fallback a emoji si el PNG no existe

## Referencias

- `utils/ui/icon_system.py` - Sistema de iconos PNG
- `utils/ui/icon_standardizer.py` - Herramienta de estandarización
- `utils/ui/icon_constants.py` - Constantes de iconos (generado)
- `assets/images/icons/` - Archivos PNG de iconos

