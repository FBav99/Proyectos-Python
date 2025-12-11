# 🔒 Global Error Handling - Ocultar Rutas en Tracebacks

## 🎯 Problema

Streamlit muestra tracebacks completos con rutas de archivos cuando hay errores, lo cual expone información sensible sobre la estructura del proyecto.

## ✅ Solución

Se ha creado un sistema de manejo de errores global que:
- ✅ Oculta rutas de archivos en tracebacks
- ✅ Muestra mensajes amigables al usuario
- ✅ Mantiene logs completos para debugging (solo server-side)

---

## 🚀 Uso Rápido

### Para Nuevas Páginas

Simplemente agrega el decorador `@safe_main` a tu función `main()`:

```python
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling at module level
configure_streamlit_error_handling()

@safe_main
def main():
    """Tu código aquí"""
    st.set_page_config(...)
    # ... resto del código
```

### Ejemplo Completo

```python
import streamlit as st
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

configure_streamlit_error_handling()

@safe_main
def main():
    st.set_page_config(page_title="Mi Página")
    
    # Tu código aquí - cualquier error será capturado y sanitizado
    st.write("Contenido de la página")

if __name__ == "__main__":
    main()
```

---

## 📋 Aplicar a Todas las Páginas

Para aplicar esto a todas tus páginas existentes, agrega estas líneas al inicio de cada archivo `.py` en `pages/`:

```python
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

configure_streamlit_error_handling()

@safe_main
def main():
    # ... código existente ...
```

---

## 🔧 Qué Hace el Sistema

### 1. Sanitización de Rutas

Convierte rutas como:
```
/mount/src/proyectos-python/Proyecto TCC/pages/06_Recuperar_Password.py
```

En:
```
[APP]/pages/[FILE].py
```

### 2. Mensajes de Error Amigables

En lugar de mostrar el traceback completo, muestra mensajes como:
- "❌ Archivo no encontrado"
- "❌ Error de permisos"
- "❌ Error del sistema"

### 3. Logging Completo (Solo Server-Side)

Los errores completos se guardan en los logs del servidor, pero no se muestran al usuario.

---

## 📝 Páginas que Ya Están Protegidas

- ✅ `pages/06_Recuperar_Password.py` - Ya aplicado

---

## 🔄 Aplicar a Otras Páginas

Para aplicar a otras páginas, simplemente agrega:

```python
# Al inicio del archivo
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

configure_streamlit_error_handling()

# Antes de la función main()
@safe_main
def main():
    # ... código existente ...
```

---

## 🎛️ Modo Debug (Opcional)

Si quieres ver detalles técnicos durante desarrollo, agrega:

```python
st.session_state.debug_mode = True
```

Esto mostrará un expander con información técnica (aún sanitizada).

---

## ⚠️ Notas Importantes

1. **No elimina los errores** - Solo los oculta del usuario
2. **Los logs completos** siguen disponibles en el servidor
3. **Funciona con Streamlit Cloud** - Detecta automáticamente el entorno
4. **No afecta el debugging local** - Fuera de Streamlit muestra tracebacks normales

---

## 🔍 Ver Errores Completos (Para Desarrolladores)

Los errores completos se guardan en:
- **Streamlit Cloud**: Logs del servidor (click "Manage app" → Logs)
- **Local**: Console output (fuera de Streamlit)

---

## ✅ Checklist de Aplicación

Para cada página que quieras proteger:

- [ ] Agregar `from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling`
- [ ] Agregar `configure_streamlit_error_handling()` al inicio del módulo
- [ ] Agregar `@safe_main` decorator antes de `def main():`
- [ ] Probar que los errores se muestran de forma amigable

---

**💡 Tip:** Puedes aplicar esto gradualmente página por página, o todas a la vez.

