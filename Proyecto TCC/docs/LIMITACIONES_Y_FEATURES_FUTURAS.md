# 🔍 Limitaciones Actuales y Features Futuras - Proyecto TCC

## 📋 Resumen Ejecutivo

Este documento identifica las limitaciones actuales del proyecto y propone features que podrían implementarse en el futuro para mejorar la plataforma de análisis de datos educativa.

---

## 🚨 LIMITACIONES ACTUALES

### 1. **Gestión de Archivos y Datos**

#### 1.1 Almacenamiento de Archivos
- **Limitación**: Los archivos subidos se almacenan en memoria (session state) y se pierden al cerrar la sesión
- **Impacto**: Los usuarios deben volver a subir archivos cada vez que inician sesión
- **Evidencia**: No hay persistencia de archivos en `uploaded_files` table (tabla existe pero no se usa completamente)
- **Solución Futura**: Implementar almacenamiento real de archivos (local o cloud storage)

#### 1.2 Tamaño de Archivos
- **Limitación**: No hay límites explícitos de tamaño de archivo
- **Impacto**: Archivos muy grandes pueden causar problemas de rendimiento o timeouts
- **Solución Futura**: Implementar validación de tamaño máximo (ej: 50MB) y procesamiento por chunks

#### 1.3 Formatos de Archivo
- **Limitación**: Solo soporta CSV y Excel (.xlsx, .xls)
- **Impacto**: No se pueden cargar JSON, Parquet, bases de datos, APIs, etc.
- **Solución Futura**: Agregar soporte para JSON, Parquet, conexiones a bases de datos (SQL), APIs REST
- **✅ Mejora Implementada**: Ahora se detectan y permiten seleccionar hojas específicas cuando un archivo Excel contiene múltiples hojas

#### 1.4 Gestión de Múltiples Datasets
- **Limitación**: Solo se puede trabajar con un dataset a la vez
- **Impacto**: No se pueden comparar o combinar múltiples fuentes de datos
- **Solución Futura**: Sistema de gestión de múltiples datasets con capacidad de merge/join

---

### 2. **Sistema de Dashboard**

#### 2.1 Persistencia de Dashboards
- **Limitación**: Los dashboards se pueden guardar en la base de datos, pero no hay interfaz completa para gestionarlos
- **Impacto**: Los usuarios no pueden fácilmente cargar, editar o compartir dashboards guardados
- **Evidencia**: Tabla `dashboards` existe pero funcionalidad limitada en `dashboard_repository.py`
- **Solución Futura**: 
  - Interfaz de gestión de dashboards guardados
  - Sistema de versionado de dashboards
  - Compartir dashboards entre usuarios

#### 2.2 Templates de Dashboard
- **Limitación**: Solo hay 3 templates básicos (KPI, Analítico, Detallado)
- **Impacto**: Opciones limitadas para diferentes casos de uso
- **Solución Futura**: 
  - Más templates especializados (ventas, marketing, recursos humanos, etc.)
  - Editor visual de dashboards drag-and-drop
  - Templates personalizables por el usuario

#### 2.3 Componentes de Visualización
- **Limitación**: Tipos de gráficos limitados (línea, barra, pie, correlación)
- **Impacto**: No se pueden crear visualizaciones más avanzadas
- **Solución Futura**: 
  - Gráficos de dispersión, heatmaps, treemaps, sunburst
  - Mapas geográficos (si hay datos de ubicación)
  - Gráficos de Gantt, funnel charts, waterfall charts

#### 2.4 Interactividad de Dashboards
- **Limitación**: Los dashboards son estáticos una vez creados
- **Impacto**: No se pueden crear dashboards interactivos con drill-down o filtros dinámicos
- **Solución Futura**: 
  - Filtros globales que afectan múltiples componentes
  - Drill-down en gráficos
  - Tooltips personalizados con información adicional

---

### 3. **Sistema de Aprendizaje**

#### 3.1 Progreso de Usuarios OAuth
- **Limitación**: Los usuarios OAuth no tienen seguimiento de progreso completo
- **Impacto**: Usuarios que se registran con Google/GitHub no pueden guardar su progreso
- **Evidencia**: En `Inicio.py` líneas 87-93, usuarios OAuth usan valores por defecto
- **Solución Futura**: Integrar progreso para usuarios OAuth en la base de datos

#### 3.2 Sistema de Logros/Gamificación
- **Limitación**: La tabla `achievements` existe pero no está implementada
- **Impacto**: No hay incentivos adicionales para completar niveles o tareas
- **Solución Futura**: 
  - Sistema de badges/logros
  - Puntos y rankings
  - Certificados al completar todos los niveles

#### 3.3 Contenido Adaptativo
- **Limitación**: El contenido es el mismo para todos los usuarios
- **Impacto**: No se adapta al nivel de conocimiento o ritmo de aprendizaje del usuario
- **Solución Futura**: 
  - Rutas de aprendizaje personalizadas
  - Contenido adicional para usuarios avanzados
  - Recomendaciones basadas en el progreso

#### 3.4 Evaluación y Feedback
- **Limitación**: Los quizzes son básicos y no hay feedback detallado
- **Impacto**: Los usuarios no reciben retroalimentación constructiva sobre errores
- **Solución Futura**: 
  - Explicaciones más detalladas en quizzes
  - Sugerencias de repaso basadas en respuestas incorrectas
  - Sistema de práctica adicional

---

### 4. **Análisis de Datos**

#### 4.1 Cálculos Avanzados
- **Limitación**: Cálculos limitados a operaciones básicas y temporales simples
- **Impacto**: No se pueden hacer análisis estadísticos avanzados
- **Solución Futura**: 
  - Análisis estadístico (regresión, correlación avanzada)
  - Análisis predictivo básico (forecasting)
  - Segmentación automática (clustering básico)

#### 4.2 Detección Automática de Insights
- **Limitación**: Los usuarios deben descubrir insights manualmente
- **Impacto**: Usuarios novatos pueden no identificar patrones importantes
- **Solución Futura**: 
  - Sistema de detección automática de anomalías
  - Sugerencias de análisis relevantes
  - Alertas automáticas sobre cambios significativos

#### 4.3 Comparaciones Temporales
- **Limitación**: Comparaciones temporales básicas (YTD, MoM)
- **Impacto**: Análisis de tendencias limitado
- **Solución Futura**: 
  - Comparaciones año sobre año (YoY)
  - Análisis de estacionalidad
  - Proyecciones y forecasting

---

### 5. **Limpieza de Datos**

#### 5.1 Operaciones Avanzadas
- **Limitación**: Limpieza básica (espacios, duplicados, valores faltantes)
- **Impacto**: No se pueden manejar casos más complejos
- **Solución Futura**: 
  - Detección y corrección de outliers
  - Normalización de datos categóricos
  - Transformaciones de datos (pivot, unpivot, melt)
  - Validación de reglas de negocio personalizadas

#### 5.2 Historial y Reversión
- **Limitación**: Historial de limpieza existe pero no hay reversión fácil
- **Impacto**: Difícil deshacer cambios si se comete un error
- **Solución Futura**: 
  - Sistema de undo/redo completo
  - Guardado de versiones de datos limpios
  - Comparación antes/después visual

---

### 6. **Exportación y Reportes**

#### 6.1 Formatos de Exportación
- **Limitación**: Solo Excel, CSV y Markdown
- **Impacto**: No se pueden exportar a formatos más profesionales
- **Solución Futura**: 
  - Exportación a PDF con formato profesional
  - Exportación a PowerPoint para presentaciones
  - Exportación a HTML interactivo
  - Exportación a imágenes (PNG, SVG) de alta calidad

#### 6.2 Reportes Automáticos
- **Limitación**: No hay generación automática de reportes
- **Impacto**: Los usuarios deben crear reportes manualmente cada vez
- **Solución Futura**: 
  - Plantillas de reportes personalizables
  - Programación de reportes automáticos (email)
  - Reportes comparativos (período vs período)

---

### 7. **Colaboración y Compartir**

#### 7.1 Compartir Dashboards
- **Limitación**: No hay funcionalidad de compartir
- **Impacto**: Los usuarios no pueden colaborar o compartir análisis
- **Solución Futura**: 
  - Enlaces públicos para dashboards
  - Compartir con usuarios específicos
  - Permisos de edición/visualización

#### 7.2 Comentarios y Anotaciones
- **Limitación**: No hay sistema de comentarios
- **Impacto**: No se pueden agregar notas o explicaciones a análisis
- **Solución Futura**: 
  - Anotaciones en gráficos
  - Comentarios en dashboards
  - Notas explicativas por componente

---

### 8. **Rendimiento y Escalabilidad**

#### 8.1 Procesamiento de Datos Grandes
- **Limitación**: Todo se procesa en memoria
- **Impacto**: Datasets grandes pueden causar problemas de rendimiento
- **Solución Futura**: 
  - Procesamiento lazy (lazy evaluation)
  - Muestreo inteligente para visualizaciones
  - Caché de resultados de análisis

#### 8.2 Optimización de Consultas
- **Limitación**: No hay optimización específica para consultas de base de datos
- **Impacto**: Consultas pueden ser lentas con muchos usuarios
- **Solución Futura**: 
  - Índices adicionales en tablas frecuentemente consultadas
  - Caché de consultas comunes
  - Paginación para listas largas

---

### 9. **Seguridad y Privacidad**

#### 9.1 Encriptación de Datos
- **Limitación**: Datos sensibles pueden no estar encriptados
- **Impacto**: Riesgo de seguridad si hay brechas
- **Solución Futura**: 
  - Encriptación de archivos subidos
  - Encriptación de datos en reposo
  - Encriptación de comunicaciones (HTTPS obligatorio)

#### 9.2 Control de Acceso Granular
- **Limitación**: Control de acceso básico (solo autenticación)
- **Impacto**: No hay roles o permisos específicos
- **Solución Futura**: 
  - Sistema de roles (admin, usuario, invitado)
  - Permisos granulares por funcionalidad
  - Auditoría de accesos y cambios

#### 9.3 Cumplimiento de Regulaciones
- **Limitación**: No hay características específicas de GDPR/privacidad
- **Impacto**: Puede no cumplir con regulaciones de privacidad
- **Solución Futura**: 
  - Exportación de datos del usuario (GDPR)
  - Eliminación de datos (right to be forgotten)
  - Consentimiento explícito para procesamiento de datos

---

### 10. **Integración y APIs**

#### 10.1 Integraciones Externas
- **Limitación**: No hay integraciones con servicios externos
- **Impacto**: No se pueden importar datos de fuentes externas automáticamente
- **Solución Futura**: 
  - Integración con Google Sheets, Airtable
  - Conexión a APIs populares (Salesforce, HubSpot)
  - Webhooks para actualizaciones automáticas

#### 10.2 API REST
- **Limitación**: No hay API para acceso programático
- **Impacto**: No se puede integrar con otros sistemas
- **Solución Futura**: 
  - API REST completa
  - Autenticación por tokens
  - Documentación de API (Swagger/OpenAPI)

---

## 🚀 FEATURES FUTURAS PROPUESTAS

### Prioridad Alta (Impacto Alto, Esfuerzo Medio)

#### 1. **Sistema de Gestión de Dashboards Completo**
- **Descripción**: Interfaz completa para guardar, cargar, editar y compartir dashboards
- **Beneficios**: Los usuarios pueden reutilizar y compartir análisis
- **Esfuerzo**: Medio-Alto
- **Dependencias**: Tabla `dashboards` ya existe

#### 2. **Persistencia de Archivos**
- **Descripción**: Guardar archivos subidos en storage (local o cloud)
- **Beneficios**: Los usuarios no pierden sus datos al cerrar sesión
- **Esfuerzo**: Medio
- **Dependencias**: Configurar storage (S3, local filesystem, etc.)

#### 3. **Soporte para Más Formatos de Archivo**
- **Descripción**: Agregar JSON, Parquet, conexiones a bases de datos
- **Beneficios**: Mayor flexibilidad para importar datos
- **Esfuerzo**: Medio
- **Dependencias**: Librerías adicionales (pyarrow para Parquet, etc.)

#### 4. **Sistema de Progreso para Usuarios OAuth**
- **Descripción**: Integrar seguimiento de progreso para usuarios OAuth
- **Beneficios**: Todos los usuarios pueden guardar su progreso
- **Esfuerzo**: Bajo-Medio
- **Dependencias**: Modificar lógica de autenticación OAuth

#### 5. **Editor Visual de Dashboards**
- **Descripción**: Interfaz drag-and-drop para crear dashboards
- **Beneficios**: Facilita la creación de dashboards personalizados
- **Esfuerzo**: Alto
- **Dependencias**: Librería de drag-and-drop (react-dnd, etc.)

---

### Prioridad Media (Impacto Medio, Esfuerzo Variable)

#### 6. **Sistema de Logros y Gamificación**
- **Descripción**: Badges, puntos, rankings
- **Beneficios**: Mayor engagement y motivación
- **Esfuerzo**: Medio
- **Dependencias**: Tabla `achievements` ya existe

#### 7. **Exportación a PDF y PowerPoint**
- **Descripción**: Generar reportes profesionales en PDF/PPT
- **Beneficios**: Reportes listos para presentaciones
- **Esfuerzo**: Medio
- **Dependencias**: Librerías de generación de PDF/PPT

#### 8. **Más Tipos de Gráficos**
- **Descripción**: Scatter plots, heatmaps, treemaps, mapas
- **Beneficios**: Visualizaciones más ricas y apropiadas
- **Esfuerzo**: Medio
- **Dependencias**: Plotly ya soporta estos gráficos

#### 9. **Análisis Estadístico Avanzado**
- **Descripción**: Regresión, correlación avanzada, forecasting básico
- **Beneficios**: Análisis más profundo
- **Esfuerzo**: Alto
- **Dependencias**: Librerías estadísticas (scipy, statsmodels)

#### 10. **Sistema de Compartir y Colaboración**
- **Descripción**: Compartir dashboards, comentarios, anotaciones
- **Beneficios**: Colaboración entre usuarios
- **Esfuerzo**: Alto
- **Dependencias**: Sistema de permisos, notificaciones

---

### Prioridad Baja (Impacto Bajo o Esfuerzo Alto)

#### 11. **API REST Completa**
- **Descripción**: API para acceso programático
- **Beneficios**: Integración con otros sistemas
- **Esfuerzo**: Muy Alto
- **Dependencias**: Framework API (FastAPI, Flask)

#### 12. **Integraciones con Servicios Externos**
- **Descripción**: Google Sheets, Airtable, APIs populares
- **Beneficios**: Importación automática de datos
- **Esfuerzo**: Alto
- **Dependencias**: APIs de servicios externos

#### 13. **Aprendizaje Adaptativo**
- **Descripción**: Contenido personalizado según nivel del usuario
- **Beneficios**: Mejor experiencia de aprendizaje
- **Esfuerzo**: Muy Alto
- **Dependencias**: Sistema de recomendaciones, ML básico

#### 14. **Procesamiento de Big Data**
- **Descripción**: Manejo eficiente de datasets muy grandes
- **Beneficios**: Escalabilidad
- **Esfuerzo**: Muy Alto
- **Dependencias**: Tecnologías de big data (Dask, Spark)

---

## 📊 Matriz de Priorización

| Feature | Impacto | Esfuerzo | Prioridad | Tiempo Estimado |
|---------|---------|----------|-----------|-----------------|
| Gestión de Dashboards | Alto | Medio | 🔴 Alta | 2-3 semanas |
| Persistencia de Archivos | Alto | Medio | 🔴 Alta | 1-2 semanas |
| Más Formatos de Archivo | Medio | Bajo-Medio | 🔴 Alta | 1 semana |
| Progreso OAuth | Medio | Bajo | 🔴 Alta | 3-5 días |
| Editor Visual Dashboards | Alto | Alto | 🟡 Media | 4-6 semanas |
| Sistema de Logros | Medio | Medio | 🟡 Media | 2 semanas |
| Exportación PDF/PPT | Medio | Medio | 🟡 Media | 1-2 semanas |
| Más Gráficos | Medio | Bajo-Medio | 🟡 Media | 1 semana |
| Análisis Estadístico | Alto | Alto | 🟡 Media | 4-6 semanas |
| Compartir/Colaboración | Medio | Alto | 🟡 Media | 3-4 semanas |
| API REST | Bajo | Muy Alto | 🟢 Baja | 8-12 semanas |
| Integraciones Externas | Bajo | Alto | 🟢 Baja | 4-6 semanas |
| Aprendizaje Adaptativo | Medio | Muy Alto | 🟢 Baja | 8-12 semanas |
| Big Data | Bajo | Muy Alto | 🟢 Baja | 12+ semanas |

---

## 🎯 Recomendaciones de Implementación

### Fase 1 (Próximos 2-3 meses)
1. **Persistencia de Archivos** - Crítico para UX
2. **Progreso OAuth** - Fácil de implementar, alto impacto
3. **Más Formatos de Archivo** - Aumenta flexibilidad
4. **Gestión de Dashboards** - Completa funcionalidad existente

### Fase 2 (3-6 meses)
5. **Sistema de Logros** - Aumenta engagement
6. **Exportación PDF/PPT** - Mejora profesionalismo
7. **Más Tipos de Gráficos** - Mejora visualizaciones
8. **Editor Visual de Dashboards** - Diferencia competitiva

### Fase 3 (6-12 meses)
9. **Análisis Estadístico Avanzado** - Valor agregado
10. **Sistema de Compartir** - Colaboración
11. **Integraciones Externas** - Ecosistema

### Fase 4 (12+ meses)
12. **API REST** - Si hay demanda
13. **Aprendizaje Adaptativo** - Si hay recursos
14. **Big Data** - Solo si es necesario

---

## 📝 Notas Finales

- **Enfoque Iterativo**: Implementar features de forma incremental
- **Feedback de Usuarios**: Priorizar según feedback real de usuarios
- **Mantenibilidad**: Asegurar que nuevas features no compliquen el código existente
- **Documentación**: Documentar todas las nuevas features
- **Testing**: Asegurar tests para nuevas funcionalidades

---

## ✅ MEJORAS IMPLEMENTADAS

### Soporte para Múltiples Hojas en Archivos Excel

**Fecha de Implementación**: Enero 2025  
**Descripción**: Se implementó detección automática y selección de hojas cuando un archivo Excel contiene múltiples hojas.

**Funcionalidad**:
- Detección automática del número de hojas en archivos Excel
- Selector de hoja cuando hay más de una hoja disponible
- Advertencia informativa cuando se detectan múltiples hojas
- Carga automática de la primera hoja si solo hay una

**Archivos Modificados**:
- `utils/data/data_handling.py` - Función `load_excel_with_sheet_selection()` y `get_excel_sheet_names()`
- `core/data_loader.py` - Actualizado para usar la nueva función
- `pages/01_Nivel_1_Basico.py` - Actualizado para soportar selección de hojas
- `pages/08_Dashboard_Blanco.py` - Actualizado para soportar selección de hojas

**Impacto**: Los usuarios ahora pueden trabajar con archivos Excel que contienen múltiples hojas sin perder datos o confundirse sobre qué hoja se está cargando.

---

**Última Actualización**: Enero 2025  
**Autor**: Análisis del Proyecto TCC  
**Versión**: 1.1


