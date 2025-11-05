# 🔧 Fix: Requirements.txt Error en Streamlit Cloud

## ❌ Error

```
error: Failed to parse: `TCC/requirements.txt`
```

Esto indica que Streamlit Cloud está intentando leer el archivo desde una ruta incorrecta.

## 🎯 Causa Probable: Espacio en el Nombre de la Carpeta

Si tu carpeta se llama **"Proyecto TCC"** (con espacio), Streamlit Cloud puede estar truncando el nombre en el espacio y solo viendo "TCC", lo que causa el error `TCC/requirements.txt`.

## ✅ Solución

### Opción 1: Verificar Configuración de Streamlit Cloud (RECOMENDADO)

1. Ve a tu app en Streamlit Cloud
2. Click en **Settings** (⚙️)
3. Verifica el campo **Main file path**
4. **Si tu repo root es "Proyecto TCC":**
   - Main file path debe ser: `Inicio.py` (sin subdirectorios)
   - **NO** debe ser: `Proyecto TCC/Inicio.py` o `TCC/Inicio.py`
5. **Si tu repo root es "Proyectos Python":**
   - Main file path debe ser: `Proyecto TCC/Inicio.py` (con el espacio)
   - O mejor aún, configura Streamlit Cloud para desplegar desde el subdirectorio "Proyecto TCC"

### Opción 2: Usar Subdirectorio en Streamlit Cloud (SI el repo root es "Proyectos Python")

Si tu repositorio de GitHub es:
```
Proyectos Python/
  Proyecto TCC/
    Inicio.py
    requirements.txt
```

Entonces en Streamlit Cloud:
1. **Repository**: Selecciona tu repo
2. **Branch**: `main` (o tu branch)
3. **Main file path**: `Proyecto TCC/Inicio.py` (con el espacio, tal cual)
4. Streamlit Cloud buscará `requirements.txt` en `Proyecto TCC/requirements.txt`

### Opción 3: Renombrar la Carpeta (SOLUCIÓN PERMANENTE)

Si puedes renombrar la carpeta para eliminar el espacio:
1. Renombra `Proyecto TCC` → `ProyectoTCC` (sin espacio)
2. Actualiza el Main file path en Streamlit Cloud
3. Haz commit y push

**Nota:** Esto requerirá actualizar todas las referencias en git, así que es mejor verificar primero las opciones 1 y 2.

### Opción 2: Verificar Estructura del Repositorio

Asegúrate de que `requirements.txt` esté en la **raíz del repositorio** que Streamlit Cloud está desplegando.

Si tu estructura es:
```
Proyectos Python/
  Proyecto TCC/
    requirements.txt  ← Debe estar aquí
    Inicio.py
    pages/
```

Y Streamlit Cloud está configurado para desplegar desde `Proyecto TCC`, entonces está bien.

### Opción 3: Verificar el Formato de requirements.txt

El archivo debe tener exactamente este formato (sin espacios extra, sin caracteres especiales):

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
openpyxl>=3.1.0
streamlit-authenticator>=0.4.2
pyyaml>=6.0.0
requests>=2.31.0
scikit-learn>=1.3.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
bcrypt>=4.0.0
psycopg2-binary>=2.9.0
```

**Importante:**
- Una dependencia por línea
- Sin espacios al inicio de cada línea
- Sin líneas vacías al final (o una línea vacía máxima)

### Opción 4: Verificar que el Archivo Esté Commiteado

```bash
# Verificar que requirements.txt está en git
git ls-files | grep requirements.txt

# Si no aparece, agregarlo
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

## 🔍 Verificación

Después de hacer los cambios:

1. **Haz commit y push** de los cambios
2. **Espera** a que Streamlit Cloud se reinicie
3. **Revisa los logs** en Streamlit Cloud → Manage app → Logs
4. Debería decir algo como: "Successfully installed..." en lugar del error

## 📝 Nota sobre el Error

El error `TCC/requirements.txt` sugiere que Streamlit Cloud está interpretando el nombre del archivo como parte de una ruta. Esto puede pasar si:

- El repositorio tiene una estructura anidada
- Streamlit Cloud está configurado con un Main file path incorrecto
- Hay un problema con cómo GitHub está estructurado

**Solución más común:** Verificar que el Main file path en Streamlit Cloud apunte correctamente a `Inicio.py` sin subdirectorios.

