# 📦 Archivo - Surveys Archivados

Esta carpeta contiene los archivos de surveys que fueron removidos de la aplicación pero se mantienen aquí para referencia futura.

## 📋 Archivos Archivados

- **99_Survey_Inicial.py** - Encuesta inicial para nuevos usuarios
- **99_Survey_Nivel.py** - Encuestas específicas después de completar cada nivel
- **99_Survey_Final.py** - Encuesta final después de completar todos los niveles

## 📝 Nota

Estos archivos **NO** aparecen en la aplicación Streamlit ya que están en una subcarpeta. Streamlit solo detecta archivos `.py` directamente en la carpeta `pages/`, no en subcarpetas.

Si en el futuro necesitas reactivar estos surveys:
1. Mueve los archivos de vuelta a `pages/`
2. Restaura las referencias en:
   - `Inicio.py`
   - `utils/learning/learning_progress.py`
   - `pages/00_Nivel_0_Introduccion.py`
   - `pages/01_Nivel_1_Basico.py`
   - `pages/02_Nivel_2_Filtros.py`
   - `pages/03_Nivel_3_Metricas.py`
   - `pages/04_Nivel_4_Avanzado.py`

## 🔧 Sistema de Surveys

El sistema de surveys (`core/survey_system.py`) y las tablas de base de datos relacionadas **se mantienen intactos** por si se necesitan en el futuro.

---
**Fecha de archivado:** 12/09/2025

