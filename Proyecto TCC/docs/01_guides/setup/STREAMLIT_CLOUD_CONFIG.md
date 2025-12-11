# ⚙️ Configuración de Streamlit Cloud - Estructura del Directorio

## 📁 Estructura Actual del Repositorio

Según tu GitHub:
```
Proyectos-Python/          ← Repositorio root de GitHub
  └── Proyecto TCC/        ← Subdirectorio (con ESPACIO)
      ├── Inicio.py        ← Archivo principal
      ├── requirements.txt ← Archivo de dependencias
      ├── pages/
      ├── core/
      └── ...
```

## ⚙️ Configuración Correcta en Streamlit Cloud

### Settings que DEBES tener:

1. **Repository**: `Proyectos-Python` (o tu repo completo)
2. **Branch**: `main` (o tu branch principal)
3. **Main file path**: `Proyecto TCC/Inicio.py` 
   - ✅ **CON el espacio** entre "Proyecto" y "TCC"
   - ✅ **EXACTAMENTE así**: `Proyecto TCC/Inicio.py`
   - ❌ **NO**: `TCC/Inicio.py`
   - ❌ **NO**: `ProyectoTCC/Inicio.py`
   - ❌ **NO**: `Inicio.py`

### ¿Por qué el error `TCC/requirements.txt`?

El error sugiere que Streamlit Cloud está:
1. Truncando "Proyecto TCC" en el espacio
2. Solo viendo "TCC"
3. Buscando `TCC/requirements.txt` en lugar de `Proyecto TCC/requirements.txt`

## ✅ Solución

### Paso 1: Verificar Main File Path

En Streamlit Cloud → Settings → Main file path debe ser:

```
Proyecto TCC/Inicio.py
```

**Exactamente así, con el espacio incluido.**

### Paso 2: Si Sigue Fallando

Si después de configurar correctamente sigue fallando, el problema puede ser cómo Streamlit Cloud maneja espacios en nombres de carpetas.

**Opción A: Renombrar la carpeta (RECOMENDADO)**

```bash
# En tu terminal, desde "Proyectos Python"
git mv "Proyecto TCC" "ProyectoTCC"
git commit -m "Rename folder to remove space for Streamlit Cloud compatibility"
git push
```

Luego en Streamlit Cloud:
- Main file path: `ProyectoTCC/Inicio.py`

**Opción B: Configurar para desplegar desde el subdirectorio**

Algunas versiones de Streamlit Cloud permiten configurar el "Working directory" o "Root directory". Si tienes esta opción:
- Set Root directory: `Proyecto TCC`
- Main file path: `Inicio.py`

## 🔍 Verificación

Después de configurar:

1. **Revisa los logs** en Streamlit Cloud → Manage app → Logs
2. Debería mostrar: `Processing dependencies...`
3. Y luego: `Successfully installed...`

Si sigue mostrando `TCC/requirements.txt`, el problema es el espacio en el nombre de la carpeta.

## 💡 Recomendación Final

**La solución más confiable es renombrar la carpeta** para eliminar el espacio:
- `Proyecto TCC` → `ProyectoTCC`

Esto evitará problemas futuros con herramientas que no manejan bien espacios en nombres de carpetas.

