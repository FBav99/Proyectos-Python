# 🧹 Guía de Limpieza Automática de Datos

## 📋 Descripción General

El módulo de limpieza automática de datos te permite preparar y limpiar tus datasets antes del análisis, eliminando inconsistencias, normalizando formatos y mejorando la calidad general de los datos.

## 🚀 Funcionalidades Principales

### 1. 🧹 Limpieza de Espacios en Blanco
- **Eliminar espacios al inicio y final** de cadenas de texto
- **Normalizar múltiples espacios** a uno solo
- **Eliminar cadenas vacías** y convertirlas a valores nulos

### 2. 📝 Normalización de Texto
- **Cambiar a minúsculas** (`lower`)
- **Cambiar a mayúsculas** (`upper`)
- **Título de caso** (`title`) - Primera letra de cada palabra en mayúscula
- **Capitalizar** (`capitalize`) - Solo la primera letra en mayúscula

### 3. 🔄 Reemplazo de Valores
- **Reemplazos globales**: Aplicar el mismo reemplazo a todas las columnas
- **Reemplazos específicos por columna**: Diferentes reemplazos para cada columna
- **Interfaz intuitiva** para agregar múltiples reemplazos

### 4. 🔤 Caracteres Especiales
- **Remover caracteres especiales** manteniendo alfanuméricos
- **Preservar espacios** o eliminarlos
- **Caracteres personalizados** que quieras mantener

### 5. 🌍 Normalización de Acentos
- **Remover acentos** completamente
- **Normalizar acentos** a formato estándar
- **Mejora la consistencia** en datos en español

### 6. 📞 Estandarización de Teléfonos
- **Formato internacional**: `+1-555-123-4567`
- **Formato nacional**: `(555) 123-4567`
- **Formato simple**: Solo números
- **Detección automática** de columnas con números de teléfono

### 7. 📧 Estandarización de Emails
- **Convertir a minúsculas**
- **Eliminar espacios**
- **Detección automática** de columnas con emails

### 8. 🔄 Manejo de Duplicados
- **Eliminar filas duplicadas**
- **Seleccionar columnas** para identificar duplicados
- **Opciones de retención**: primera, última o todas las ocurrencias

### 9. ❌ Valores Faltantes
- **Detección automática** del mejor método según el tipo de dato
- **Métodos disponibles**:
  - `auto`: Detecta automáticamente (mediana para numéricos, moda para categóricos)
  - `mean`: Media aritmética
  - `median`: Mediana
  - `mode`: Valor más frecuente
  - `forward`: Llenar hacia adelante
  - `backward`: Llenar hacia atrás
- **Valores personalizados** por columna

## 🎯 Cómo Usar el Módulo

### Paso 1: Acceder a la Limpieza
1. Ve al **Dashboard Principal**
2. Haz clic en **"🧹 Limpiar Datos"**
3. O sube un archivo y selecciona **"🧽 Limpieza Automática"**

### Paso 2: Cargar Datos
- **Subir archivo**: CSV, Excel (.xlsx, .xls)
- **Usar datasets de ejemplo**: Para practicar

### Paso 3: Configurar Limpieza Automática
Selecciona las opciones que deseas aplicar:

```python
# Opciones recomendadas para la mayoría de casos
✅ Limpiar espacios en blanco
✅ Normalizar mayúsculas/minúsculas
✅ Remover duplicados
✅ Llenar valores faltantes

# Opciones opcionales según tus datos
🔤 Remover caracteres especiales
🌍 Normalizar acentos
📞 Estandarizar teléfonos
📧 Estandarizar emails
```

### Paso 4: Limpieza Manual Avanzada
Usa las pestañas para control más granular:

#### 📝 Texto
- Selecciona columnas específicas
- Elige tipo de normalización de caso
- Opciones para acentos y caracteres especiales

#### 🔄 Reemplazos
- Agrega reemplazos globales
- Aplica múltiples reemplazos

#### 📊 Datos
- Manejo específico de duplicados
- Configuración de valores faltantes

#### 📋 Historial
- Revisa todas las operaciones realizadas
- Estadísticas de cambios

## 💡 Casos de Uso Comunes

### 1. Datos de Clientes
```python
# Limpieza típica para datos de clientes
cleaner.clean_whitespace()  # Limpiar espacios
cleaner.normalize_text_case(case_type='title')  # Nombres en formato título
cleaner.standardize_emails()  # Emails en minúsculas
cleaner.standardize_phone_numbers()  # Teléfonos en formato estándar
cleaner.remove_duplicates(subset=['email'])  # Eliminar duplicados por email
```

### 2. Datos de Ventas
```python
# Limpieza para datos de ventas
cleaner.clean_whitespace()  # Limpiar espacios
cleaner.normalize_text_case(case_type='lower')  # Productos en minúsculas
cleaner.fill_missing_values(method='auto')  # Llenar valores faltantes
cleaner.remove_duplicates()  # Eliminar duplicados
```

### 3. Datos de Encuestas
```python
# Limpieza para datos de encuestas
cleaner.clean_whitespace()  # Limpiar espacios
cleaner.normalize_accents(remove_accents=True)  # Remover acentos
cleaner.replace_values(replacements={
    'Sí': 'Si',
    'No': 'No',
    'N/A': 'No aplica'
})  # Estandarizar respuestas
```

## 🔧 Uso Programático

### Inicializar el Limpiador
```python
from utils.data_cleaner import DataCleaner

# Crear instancia del limpiador
cleaner = DataCleaner(df)
```

### Aplicar Limpieza Automática
```python
# Opciones de limpieza
cleaning_options = {
    'whitespace': True,
    'case_normalization': True,
    'special_characters': False,
    'accents': False,
    'duplicates': True,
    'missing_values': True
}

# Aplicar limpieza
cleaned_df = cleaner.apply_auto_cleaning(cleaning_options)
```

### Limpieza Manual
```python
# Limpiar espacios
cleaner.clean_whitespace()

# Normalizar caso
cleaner.normalize_text_case(case_type='lower')

# Reemplazar valores
cleaner.replace_values(replacements={'old': 'new'})

# Obtener datos limpiados
cleaned_df = cleaner.get_cleaned_data()
```

### Obtener Resumen
```python
summary = cleaner.get_cleaning_summary()
print(f"Operaciones realizadas: {summary['total_operations']}")
print(f"Filas removidas: {summary['rows_removed']}")
```

## 📊 Monitoreo y Control

### Historial de Operaciones
- Cada operación se registra automáticamente
- Incluye detalles de cambios realizados
- Timestamp de cada operación

### Comparación de Datos
- **Antes vs Después**: Estadísticas comparativas
- **Métricas de cambio**: Filas/columnas removidas
- **Uso de memoria**: Optimización automática

### Control de Calidad
- **Puntuación de calidad** automática
- **Recomendaciones** basadas en el análisis
- **Detección de inconsistencias**

## ⚠️ Consideraciones Importantes

### 1. Backup de Datos Originales
- El limpiador mantiene una copia de los datos originales
- Puedes resetear a cualquier momento con `reset_to_original()`

### 2. Orden de Operaciones
- La limpieza se aplica en el orden especificado
- Algunas operaciones pueden afectar otras
- Revisa el historial para entender el impacto

### 3. Tipos de Datos
- Las operaciones se adaptan automáticamente al tipo de dato
- Las columnas numéricas no se ven afectadas por limpieza de texto
- Las fechas se preservan en su formato original

### 4. Rendimiento
- Para datasets grandes, considera aplicar limpieza por lotes
- Algunas operaciones pueden ser costosas en memoria
- Usa el monitoreo de memoria para optimizar

## 🎓 Ejemplos Prácticos

### Ejemplo 1: Limpieza Básica
```python
# Dataset con inconsistencias básicas
cleaner = DataCleaner(df)

# Limpieza automática básica
cleaning_options = {
    'whitespace': True,
    'case_normalization': True,
    'duplicates': True,
    'missing_values': True
}

cleaned_df = cleaner.apply_auto_cleaning(cleaning_options)
```

### Ejemplo 2: Limpieza Avanzada
```python
# Dataset con problemas complejos
cleaner = DataCleaner(df)

# Limpieza paso a paso
cleaner.clean_whitespace()
cleaner.normalize_text_case(case_type='title')
cleaner.normalize_accents(remove_accents=True)
cleaner.standardize_phone_numbers(format_type='international')
cleaner.standardize_emails()
cleaner.remove_duplicates(subset=['email', 'phone'])
cleaner.fill_missing_values(method='auto')

cleaned_df = cleaner.get_cleaned_data()
```

### Ejemplo 3: Limpieza Personalizada
```python
# Limpieza con reemplazos específicos
cleaner = DataCleaner(df)

# Reemplazos específicos por columna
custom_replacements = {
    'categoria': {
        'Electrónicos': 'Electronics',
        'Ropa': 'Clothing',
        'Hogar': 'Home'
    },
    'estado': {
        'Activo': 'Active',
        'Inactivo': 'Inactive'
    }
}

cleaner.replace_values(custom_replacements=custom_replacements)
cleaned_df = cleaner.get_cleaned_data()
```

## 🔍 Solución de Problemas

### Problema: Datos no se limpian
- Verifica que las columnas seleccionadas existan
- Revisa el tipo de datos de las columnas
- Consulta el historial de operaciones

### Problema: Pérdida de datos
- Usa `reset_to_original()` para volver al estado inicial
- Revisa las opciones de limpieza aplicadas
- Verifica el resumen de cambios

### Problema: Rendimiento lento
- Aplica limpieza por columnas específicas
- Usa opciones de limpieza más selectivas
- Considera procesar en lotes para datasets grandes

## 📚 Recursos Adicionales

- **Documentación de pandas**: Para operaciones avanzadas
- **Guías de calidad de datos**: Mejores prácticas
- **Ejemplos de datasets**: Para practicar diferentes escenarios

---

¡Con este módulo de limpieza automática, tus datos estarán listos para análisis de alta calidad! 🚀
