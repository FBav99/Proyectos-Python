# 🔒 Sistema de Manejo de Errores Seguro

## 📋 Descripción General

El sistema de manejo de errores seguro está diseñado para proteger la información sensible del sistema mientras proporciona mensajes de error útiles y amigables para los usuarios.

## 🛡️ Características de Seguridad

### **1. Ocultación de Información Sensible**
- **Rutas del sistema**: `C:\Users\...` → `[OCULTO]`
- **Nombres de archivos**: `Inicio.py` → `[OCULTO]`
- **Extensiones**: `.py`, `.csv`, `.xlsx` → `[OCULTO]`
- **Números de línea**: `line 123` → `línea [OCULTA]`
- **Rutas absolutas**: `C:\Proyecto\...` → `[RUTA]\`

### **2. Mensajes de Error Amigables**
- **FileNotFoundError** → "Error de archivo no encontrado"
- **PermissionError** → "Error de permisos"
- **ValueError** → "Error de datos"
- **ConnectionError** → "Error de conexión"
- **TimeoutError** → "Error de tiempo de espera"

### **3. Sistema de Reportes**
- **ID único** para cada error
- **Formulario de reporte** integrado
- **Información técnica** opcional
- **Tracking** de errores para debugging

## 🔧 Uso del Sistema

### **Función Básica**
```python
from utils.error_handler import display_error

try:
    # Tu código aquí
    result = some_function()
except Exception as e:
    display_error(e, "Contexto de la operación")
```

### **Ejecución Segura**
```python
from utils.error_handler import safe_execute

# Ejecuta la función de forma segura
result = safe_execute(some_function, arg1, arg2)
```

### **Modo Debug (Solo para desarrolladores)**
```python
# Habilitar modo debug
st.session_state.debug_mode = True

# Mostrar detalles técnicos
display_error(e, "Contexto", show_details=True)
```

## 📊 Información de Errores

### **Para Usuarios**
- ✅ Mensajes claros y útiles
- ✅ Instrucciones de acción
- ✅ Opción de reportar error
- ✅ Sin información técnica

### **Para Desarrolladores**
- 🔧 Error ID único
- 🔧 Timestamp del error
- 🔧 Stack trace completo
- 🔧 Contexto de la operación
- 🔧 Información del usuario

## 🚀 Implementación

### **1. Importar el Módulo**
```python
from utils.error_handler import display_error, safe_execute
```

### **2. Reemplazar Try-Catch Básicos**
```python
# Antes
try:
    result = function()
except Exception as e:
    st.error(f"Error: {str(e)}")

# Después
try:
    result = function()
except Exception as e:
    display_error(e, "Ejecutando función")
```

### **3. Usar Ejecución Segura**
```python
# Antes
result = function()

# Después
result = safe_execute(function)
```

## 📋 Patrones de Error Comunes

### **Errores de Archivo**
- **FileNotFoundError**: Archivo no encontrado
- **PermissionError**: Sin permisos de acceso
- **IsADirectoryError**: Intentando abrir un directorio

### **Errores de Datos**
- **ValueError**: Datos inválidos
- **KeyError**: Clave no encontrada
- **IndexError**: Índice fuera de rango

### **Errores de Sistema**
- **ConnectionError**: Problemas de conexión
- **TimeoutError**: Tiempo de espera agotado
- **MemoryError**: Memoria insuficiente

## 🔍 Debugging

### **Acceder a Información de Errores**
```python
from utils.error_handler import get_error_info

# Obtener información de un error específico
error_info = get_error_info("ERR_20241201_1430_0001")
```

### **Limpiar Logs**
```python
from utils.error_handler import clear_error_logs

# Limpiar logs de errores
clear_error_logs()
```

### **Ver Errores en Session State**
```python
# Ver todos los errores registrados
if 'debug_errors' in st.session_state:
    for error_id, error_info in st.session_state.debug_errors.items():
        st.write(f"Error ID: {error_id}")
        st.write(f"Tipo: {error_info['error_type']}")
        st.write(f"Mensaje: {error_info['error_message']}")
```

## 📤 Reportes de Error

### **Estructura del Reporte**
```python
{
    'error_id': 'ERR_20241201_1430_0001',
    'user_email': 'usuario@ejemplo.com',
    'user_description': 'Estaba subiendo un archivo CSV...',
    'include_technical': True,
    'timestamp': '2024-12-01T14:30:00'
}
```

### **Acceder a Reportes**
```python
# Ver reportes enviados
if 'error_reports' in st.session_state:
    for report in st.session_state.error_reports:
        st.write(f"Error ID: {report['error_id']}")
        st.write(f"Usuario: {report['user_email']}")
        st.write(f"Descripción: {report['user_description']}")
```

## 🎯 Mejores Prácticas

### **1. Contexto Útil**
```python
# Bueno
display_error(e, "Cargando archivo CSV")

# Malo
display_error(e, "Error")
```

### **2. Manejo Específico**
```python
# Para errores específicos
if isinstance(e, FileNotFoundError):
    st.error("El archivo no fue encontrado. Verifica la ruta.")
else:
    display_error(e, "Cargando archivo")
```

### **3. Información de Usuario**
```python
# Incluir información útil
display_error(e, f"Procesando {filename} ({file_size} bytes)")
```

## 🔐 Consideraciones de Seguridad

### **Información Protegida**
- ✅ Rutas del sistema
- ✅ Nombres de archivos internos
- ✅ Números de línea
- ✅ Información de usuario
- ✅ Configuraciones sensibles

### **Información Permitida**
- ✅ Mensajes de error genéricos
- ✅ Tipos de error
- ✅ Contexto de la operación
- ✅ Timestamps
- ✅ IDs de error únicos

## 🚀 Próximas Mejoras

### **Funcionalidades Planificadas**
- 📧 Envío automático de reportes por email
- 📊 Dashboard de errores para administradores
- 🔄 Reintentos automáticos para errores temporales
- 📈 Métricas de errores y tendencias
- 🔗 Integración con sistemas de monitoreo

### **Configuración Avanzada**
- ⚙️ Configuración por entorno (dev/prod)
- 🎯 Filtros personalizados de errores
- 📝 Templates de mensajes personalizables
- 🔔 Notificaciones en tiempo real
