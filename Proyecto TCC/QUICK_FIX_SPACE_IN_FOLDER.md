# ⚡ Fix Rápido: Espacio en Nombre de Carpeta

## 🔍 Problema

Tu carpeta se llama **"Proyecto TCC"** (con espacio), y el error muestra `TCC/requirements.txt`, lo que sugiere que Streamlit Cloud está truncando el nombre en el espacio.

## ✅ Solución Rápida

### Paso 1: Verificar Configuración Actual

En Streamlit Cloud → Settings, verifica:

**Si Main file path es:**
- ❌ `TCC/Inicio.py` → **Cambiar a** `Inicio.py` 
- ❌ `Proyecto TCC/Inicio.py` → **Cambiar a** `Inicio.py` (si repo root es "Proyecto TCC")
- ✅ `Inicio.py` → Está correcto, pero verifica que el repo root esté bien configurado

### Paso 2: Verificar Repo Root

**Caso A: Tu repo de GitHub es "Proyecto TCC" (con espacio)**
- Main file path: `Inicio.py`
- Streamlit Cloud buscará `requirements.txt` en la raíz

**Caso B: Tu repo de GitHub es "Proyectos Python" y contiene "Proyecto TCC"**
- Main file path: `Proyecto TCC/Inicio.py` (con el espacio, tal cual)
- Streamlit Cloud buscará `Proyecto TCC/requirements.txt`

### Paso 3: Si Nada Funciona

Renombra la carpeta para eliminar el espacio:
1. Localmente: `git mv "Proyecto TCC" ProyectoTCC`
2. Commit: `git commit -m "Rename folder to remove space"`
3. Push: `git push`
4. En Streamlit Cloud: Cambia Main file path a `ProyectoTCC/Inicio.py` (si aplica)

## 🎯 Solución Más Probable

**En Streamlit Cloud Settings:**
- Repository: Tu repo de GitHub
- Branch: `main`
- **Main file path**: `Inicio.py` (sin subdirectorios, sin espacios en el path)

Esto debería hacer que Streamlit Cloud busque `requirements.txt` en la misma ubicación que `Inicio.py`.

