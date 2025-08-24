# 📊 Panel de Análisis de Datos - Proyecto TCC

## 🚀 Inicio Rápido

### Ejecutar la aplicación:
```bash
# Con autenticación (recomendado)
streamlit run Inicio.py

# Sin autenticación
streamlit run main.py
```

### Credenciales de acceso:
- **Usuario**: `demo_user`
- **Contraseña**: `demo123`

## 📚 Documentación

La documentación completa del proyecto se encuentra en la carpeta [`docs/`](docs/):

- 📖 **[README Principal](docs/README.md)** - Documentación completa del proyecto
- 📁 **[Estructura del Proyecto](docs/PROJECT_STRUCTURE.md)** - Organización de carpetas y módulos
- 📋 **[Resumen de Integración](docs/INTEGRATION_SUMMARY.md)** - Resumen de funcionalidades
- 🎬 **[Implementación de GIFs](docs/IMPLEMENTACION_GIFS.md)** - Guía de GIFs
- 🎬 **[Guía de Creación de GIFs](docs/GIF_CREATION_GUIDE.md)** - Cómo crear GIFs

## 🏗️ Estructura del Proyecto

```
Proyecto TCC/
├── 📄 Inicio.py                    # Página principal con autenticación
├── 📄 main.py                      # Dashboard principal (sin autenticación)
├── 📁 core/                        # Módulos principales del sistema
├── 📁 utils/                       # Utilidades y herramientas
├── 📁 pages/                       # Páginas de niveles de aprendizaje
├── 📁 data/                        # Datos y datasets
├── 📁 config/                      # Archivos de configuración
├── 📁 docs/                        # Documentación
└── 📁 assets/                      # Recursos multimedia
```

> 📋 **Para más detalles**: Consulta [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md)

## 🎯 Sistema de Aprendizaje por Niveles

1. **📚 Nivel 1: Básico** - Preparación de datos
2. **🔍 Nivel 2: Filtros** - Análisis de datos
3. **📊 Nivel 3: Métricas** - KPIs y análisis
4. **🚀 Nivel 4: Avanzado** - Cálculos y visualizaciones

## 🔧 Tecnologías Utilizadas

- **Streamlit** - Framework web para aplicaciones de datos
- **Pandas** - Manipulación y análisis de datos
- **Plotly** - Visualizaciones interactivas
- **Streamlit-Authenticator** - Sistema de autenticación
- **PyYAML** - Configuración de archivos

## 📝 Notas

- El proyecto está organizado en módulos para facilitar el mantenimiento
- Todos los imports han sido actualizados para reflejar la nueva estructura
- La documentación está centralizada en la carpeta `docs/`
- Se incluye un archivo `.gitignore` completo para mantener limpio el repositorio
