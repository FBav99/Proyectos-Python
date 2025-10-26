# Escalera - Plataforma de Aprendizaje de Análisis de Datos

## Slide 1: Portada
**Título:** Escalera
**Subtítulo:** Sistema Interactivo de Aprendizaje de Análisis de Datos
**Autor:** Fernando Bavera y Juan Jose Villalba
**Fecha:** Octubre 2025

---

## Slide 2: Problema Identificado

### El Desafío
- Las personas sin experiencia técnica necesitan aprender análisis de datos
- Las herramientas tradicionales son complejas y abrumadoras
- Falta de recursos educativos estructurados y progresivos
- Curva de aprendizaje muy pronunciada

### Consecuencias
- Abandono temprano del aprendizaje
- Frustración por falta de guía clara
- Dificultad para aplicar conocimientos a casos reales
- Barrera de entrada alta al análisis de datos

---

## Slide 3: Solución Propuesta

### TCC Learning Platform
Una plataforma web interactiva que enseña análisis de datos mediante:

**Sistema de Aprendizaje Progresivo**
- 5 niveles de dificultad incremental
- Desde conceptos básicos hasta análisis avanzados
- Aprendizaje "learning by doing"

**Características Principales**
- Interfaz intuitiva y amigable
- Ejemplos prácticos con datos reales
- Feedback inmediato
- Sin requisitos previos de programación

---

## Slide 4: Arquitectura del Sistema

### Stack Tecnológico
**Frontend & Backend:**
- **Streamlit** - Framework de aplicaciones web en Python
- **Python 3.x** - Lenguaje de programación principal

**Análisis de Datos:**
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas
- **Plotly** - Visualizaciones interactivas

**Base de Datos:**
- **SQLite** - Base de datos local
- Gestión de usuarios y progreso

**Seguridad:**
- Sistema de autenticación robusto
- Hash de contraseñas (bcrypt)
- Gestión segura de sesiones

---

## Slide 5: Sistema de Niveles - Overview

### Estructura del Aprendizaje

| Nivel | Tema | Duración | Habilidad Adquirida |
|-------|------|----------|---------------------|
| 🌟 **Nivel 0** | Introducción | 15-20 min | Conceptos de datos |
| 📚 **Nivel 1** | Preparación | 20-30 min | Cargar y preparar datos |
| 🔍 **Nivel 2** | Filtros | 20-25 min | Filtrar información |
| 📊 **Nivel 3** | Métricas | 25-30 min | Calcular KPIs |
| 🚀 **Nivel 4** | Avanzado | 30-40 min | Visualizaciones profesionales |

**Tiempo Total:** 2.5 - 3 horas de aprendizaje completo

---

## Slide 6: Nivel 0 - Introducción

### ¿Qué son los datos?
**Objetivo:** Fundamentos conceptuales

**Contenido:**
- Tipos de datos (numéricos, texto, fechas, booleanos)
- Estructura de datos (filas y columnas)
- Calidad de datos (limpios vs sucios)
- ¿Qué puedes hacer con los datos?

**Ejemplo Práctico:**
- Dataset TechStore (ventas de electrónicos)
- Comparación de datos limpios vs problemáticos
- Filtros interactivos básicos

**Resultado:** Usuario entiende qué son los datos y por qué importan

---

## Slide 7: Nivel 1 - Preparación de Datos

### Cargar y Verificar Datos
**Objetivo:** Preparación técnica de datos

**Contenido:**
- Formatos de archivo (CSV, Excel, JSON)
- Cómo estructurar datos correctamente
- Proceso de carga de archivos
- Verificación de calidad
- Entender la estructura del dataset

**Práctica:**
- Subir archivo propio o usar ejemplo
- Análisis automático de calidad
- Identificación de problemas (duplicados, valores faltantes, outliers)

**Resultado:** Usuario puede cargar y verificar datos correctamente

---

## Slide 8: Nivel 2 - Filtros

### Organizar y Encontrar Información
**Objetivo:** Dominar filtros de datos

**Contenido:**
- Filtros por fecha (rangos, períodos específicos)
- Filtros por categorías y regiones
- Filtros numéricos con deslizadores
- Combinación de múltiples filtros
- Impacto en métricas

**Ejemplo Práctico:**
- Análisis de ventas por región
- Filtrado temporal (trimestres, meses)
- Comparación de categorías
- Filtros combinados para insights específicos

**Resultado:** Usuario puede filtrar datos para análisis específicos

---

## Slide 9: Nivel 3 - Métricas y KPIs

### Calcular e Interpretar KPIs
**Objetivo:** Entender métricas de negocio

**Contenido:**
- ¿Qué son los KPIs?
- Métricas clave de negocio
- Cómo identificar métricas importantes
- Interpretar y analizar resultados
- Tomar decisiones basadas en datos

**Práctica:**
- Cálculo de ventas totales, promedios
- Análisis por categoría y región
- Gráficos automáticos
- Quiz de comprensión (80% para pasar)

**Resultado:** Usuario puede calcular e interpretar KPIs importantes

---

## Slide 10: Nivel 4 - Análisis Avanzado

### Visualizaciones Profesionales
**Objetivo:** Crear análisis completos

**Contenido:**
- Cálculos personalizados avanzados
- Visualizaciones interactivas (Plotly)
- Creación de dashboards
- Análisis de correlaciones
- Comunicar insights

**Características:**
- Gráficos de barras, líneas, pie charts
- Mapas de calor de correlaciones
- Filtros interactivos en tiempo real
- Dashboard personalizable
- Quiz final

**Resultado:** Usuario crea dashboards profesionales independientemente

---

## Slide 11: Funcionalidades Clave

### Dashboard en Blanco
**Construcción Manual de Dashboards**
- Agregar componentes (métricas, gráficos, tablas)
- Configuración personalizada
- Filtros globales interactivos
- Exportación a múltiples formatos
- Guardar y reutilizar dashboards

### Limpieza Automática de Datos
**Herramienta de Data Cleaning**
- Eliminar espacios en blanco
- Normalizar mayúsculas/minúsculas
- Estandarizar teléfonos y emails
- Remover duplicados
- Reemplazar valores nulos
- Descargar datos limpios

---

## Slide 12: Datasets Disponibles

### Datos de Ejemplo Variados

**TechStore (E-commerce)** - Principal
- 1,000 registros de ventas
- 8 columnas (fecha, producto, categoría, ventas, región, etc.)
- Calidad: 95% (limpio) / 75% (sucio para práctica)

**Otros Datasets:**
- **Healthcare:** 800 registros médicos (práctica intermedia)
- **Finance:** 1,200 transacciones financieras
- **Sales:** 1,500 registros con patrones estacionales
- **Education:** 500 estudiantes universitarios
- **Dataset Sucio:** 225 registros para práctica de limpieza

---

## Slide 13: Sistema de Autenticación

### Seguridad y Gestión de Usuarios

**Características:**
- Registro de nuevos usuarios
- Login tradicional (usuario/contraseña)
- Login con OAuth (Google, etc.)
- Recuperación de contraseña
- Gestión segura de sesiones

**Base de Datos:**
- SQLite local
- Hash de contraseñas con bcrypt
- Tracking de progreso por usuario
- Guardado automático de avances

**Privacidad:**
- Datos de usuario protegidos
- No compartir información personal
- Sesiones seguras

---

## Slide 14: Progreso y Gamificación

### Sistema de Seguimiento

**Tracking de Progreso:**
- Porcentaje de completitud (0% - 100%)
- Niveles completados (X/5)
- Tiempo invertido
- Dashboards creados

**Badges Desbloqueables:**
- 🌟 Nivel 0: "Iniciador de Datos"
- 📚 Nivel 1: "Preparador de Datos"
- 🔍 Nivel 2: "Explorador de Datos"
- 📊 Nivel 3: "Analista de Métricas"
- 🚀 Nivel 4: "Maestro de Dashboards"

**Motivación:**
- Feedback visual inmediato
- Celebraciones al completar niveles
- Progreso visible en todo momento

---

## Slide 15: Caso de Uso Real

### Ejemplo: María González

**Perfil:**
- Sin experiencia previa en análisis de datos
- Dueña de pequeño negocio
- Necesita analizar sus ventas

**Su Viaje:**

**Día 1 (60 min):**
- Registro en la plataforma
- Completa Nivel 0 y 1
- Aprende conceptos básicos
- Carga su primer dataset

**Día 2 (90 min):**
- Completa Niveles 2 y 3
- Domina filtros y KPIs
- Analiza ventas por región

**Día 3 (60 min):**
- Completa Nivel 4
- Crea dashboard profesional
- Obtiene insights accionables

**Resultado:** Dashboard de análisis Q4 2023 con métricas clave, gráficos interactivos y filtros

---

## Slide 16: Dashboard Final - Ejemplo

### Dashboard Creado por María

**Componentes:**
- **KPIs Principales:** Ventas totales, promedio, pedidos, calificación
- **Filtros Globales:** Fecha, categoría, región, ventas mínimas
- **Visualizaciones:**
  - Gráfico de barras: Ventas por categoría
  - Gráfico circular: Distribución por región
  - Gráfico de líneas: Tendencias mensuales
  - Tabla: Top 10 productos

**Insights Descubiertos:**
- Q4 representa 31% de ventas anuales
- Región Norte lidera con 34%
- Electronica es la categoría más rentable
- Pico de ventas en abril y noviembre

---

## Slide 17: Arquitectura Modular

### Organización del Código

**Estructura:**
```
📁 core/ - Módulos principales
  ├── auth_service.py - Autenticación
  ├── database.py - Base de datos
  ├── quiz_system.py - Cuestionarios
  └── data_quality_analyzer.py - Calidad

📁 utils/ - Utilidades organizadas
  ├── analysis/ - Cálculos, filtros, métricas
  ├── dashboard/ - Componentes de dashboard
  ├── data/ - Manejo y limpieza de datos
  ├── learning/ - Sistema educativo
  ├── system/ - Exportación, GIFs
  └── ui/ - Componentes de interfaz

📁 pages/ - Niveles de aprendizaje
📁 data/ - Datasets de ejemplo
```

**Ventajas:**
- Mantenibilidad alta
- Código reutilizable
- Fácil de testear
- Escalable

---

## Slide 18: Ventajas Competitivas

### ¿Por qué TCC Learning Platform?

**Vs. Excel:**
- ✅ Guía paso a paso estructurada
- ✅ Validación automática
- ✅ Feedback inmediato
- ✅ No requiere conocimientos previos

**Vs. Python/R:**
- ✅ Sin necesidad de programar
- ✅ Interfaz visual intuitiva
- ✅ Curva de aprendizaje suave
- ✅ Resultados inmediatos

**Vs. Tableau/Power BI:**
- ✅ Gratis y open source
- ✅ Enfoque educativo
- ✅ Aprender haciendo
- ✅ Sin licencias costosas

**Vs. Cursos Online:**
- ✅ Práctica desde el minuto 1
- ✅ Tus propios datos
- ✅ A tu propio ritmo
- ✅ Herramienta + educación

---

## Slide 19: Métricas del Proyecto

### Números del Sistema

**Código:**
- **~15,000 líneas** de código Python
- **30+ módulos** organizados
- **40+ funciones** de análisis
- **5 niveles** completos de aprendizaje

**Documentación:**
- **25+ documentos** técnicos
- **4 guías** de flujo de usuario
- **15,000+ palabras** de documentación
- **Ejemplos** en cada nivel

**Funcionalidades:**
- **6 datasets** de ejemplo
- **20+ tipos** de visualizaciones
- **3 formatos** de exportación
- **10+ operaciones** de limpieza

**Testing:**
- Usuario completa curso en **2.5-3 horas**
- Tasa de completitud objetivo: **>80%**
- Satisfacción esperada: **>4/5**

---

## Slide 20: Resultados de Aprendizaje

### Habilidades Adquiridas

**Al Completar el Curso, el Usuario Puede:**

✅ **Conceptual:**
- Entender qué son los datos y sus tipos
- Comprender la importancia de la calidad
- Conocer el proceso de análisis de datos

✅ **Técnico:**
- Cargar y verificar archivos CSV/Excel
- Aplicar filtros complejos
- Calcular métricas y KPIs
- Limpiar datos con problemas

✅ **Práctico:**
- Crear visualizaciones interactivas
- Construir dashboards profesionales
- Interpretar resultados
- Comunicar insights

✅ **Profesional:**
- Analizar datos de negocio
- Tomar decisiones basadas en datos
- Crear reportes visuales
- Trabajar de forma autónoma

---

## Slide 21: Impacto y Beneficios

### Valor Generado

**Para Usuarios:**
- Habilidad valiosa en el mercado laboral
- Capacidad de análisis de datos
- Autonomía en la toma de decisiones
- Portfolio con dashboards reales

**Para Negocios:**
- Empleados con capacidades de análisis
- Mejor toma de decisiones
- Cultura data-driven
- ROI en formación

**Para Educación:**
- Herramienta pedagógica efectiva
- Aprendizaje activo
- Recurso gratuito
- Escalable a muchos estudiantes

**Medible:**
- Tiempo de aprendizaje: **2.5-3 horas** (vs 40+ horas en cursos tradicionales)
- Costo: **$0** (vs $500-2000 en cursos pagos)
- Retención: Aprendizaje por práctica
- Aplicabilidad: Inmediata con datos reales

---

## Slide 22: Casos de Uso

### Aplicaciones Reales

**Pequeños Negocios:**
- Analizar ventas mensuales
- Identificar productos más rentables
- Detectar tendencias estacionales
- Optimizar inventario

**Estudiantes:**
- Proyectos universitarios
- Análisis de encuestas
- Visualización de datos
- Desarrollo de portfolio

**Profesionales:**
- Reportes de gestión
- KPIs departamentales
- Análisis de rendimiento
- Presentaciones ejecutivas

**Educadores:**
- Enseñar análisis de datos
- Ejercicios prácticos
- Evaluación de estudiantes
- Demostración de conceptos

---

## Slide 23: Tecnologías y Herramientas

### Stack Completo

**Backend:**
```python
Python 3.x
├── Streamlit (framework web)
├── Pandas (análisis de datos)
├── NumPy (cálculos numéricos)
├── Plotly (visualizaciones)
├── SQLite (base de datos)
└── bcrypt (seguridad)
```

**Frontend:**
- Streamlit UI Components
- Custom CSS styling
- Responsive design
- Interactive widgets

**Deployment:**
- Local: `streamlit run Inicio.py`
- Cloud: Compatible con Streamlit Cloud
- Docker: Containerizable
- Requirements: `requirements.txt`

**Versionamiento:**
- Git & GitHub
- Documentación versionada
- Ramas: main, pruebas, desarrollo

---

## Slide 24: Características Técnicas

### Detalles de Implementación

**Gestión de Estado:**
- Session State de Streamlit
- Persistencia de progreso en DB
- Cache de datos optimizado
- Recargas eficientes

**Performance:**
- Carga de datos optimizada
- Filtros en tiempo real
- Gráficos interactivos rápidos
- Manejo eficiente de memoria

**Escalabilidad:**
- Arquitectura modular
- Separación de concerns
- Código reutilizable
- Fácil de extender

**Mantenibilidad:**
- Código documentado
- Estructura clara
- Convenciones de naming
- Tests posibles

---

## Slide 25: Roadmap Futuro

### Próximas Mejoras

**Corto Plazo (3 meses):**
- 🎯 Más datasets de ejemplo (10+ industrias)
- 📱 Optimización mobile
- 🌐 Múltiples idiomas (inglés, portugués)
- 💾 Exportación a PDF/PowerPoint

**Mediano Plazo (6 meses):**
- 🤝 Colaboración multi-usuario
- ☁️ Integración con servicios cloud
- 📊 Análisis predictivo básico
- 🎓 Certificado de completitud

**Largo Plazo (12 meses):**
- 🤖 Sugerencias con IA
- 📈 Análisis de series temporales avanzado
- 🔗 APIs para integración externa
- 👥 Comunidad de usuarios

---

## Slide 26: Demostración

### Video/Screenshots

**[AQUÍ INCLUIR CAPTURAS DE PANTALLA O DEMO EN VIVO]**

**Mostrar:**
1. Pantalla de inicio y login
2. Dashboard principal con progreso
3. Nivel interactivo (ej: Nivel 2 con filtros)
4. Dashboard personalizado creado
5. Limpieza de datos en acción

**Duración sugerida:** 3-5 minutos

---

## Slide 27: Proceso de Desarrollo

### Metodología

**Fases del Proyecto:**

**1. Investigación (2 semanas)**
- Análisis de necesidades
- Estudio de herramientas existentes
- Definición de alcance

**2. Diseño (2 semanas)**
- Arquitectura del sistema
- Diseño de niveles
- Wireframes y UX

**3. Desarrollo (8 semanas)**
- Implementación de módulos
- Sistema de niveles
- Base de datos y autenticación
- Dashboards y visualizaciones

**4. Testing (2 semanas)**
- Pruebas funcionales
- Testing de usuario
- Corrección de bugs
- Optimización

**5. Documentación (1 semana)**
- Guías de usuario
- Documentación técnica
- Guías de flujo

---

## Slide 28: Desafíos y Soluciones

### Retos Superados

**Desafío 1: Complejidad del Aprendizaje**
- **Problema:** Análisis de datos es intimidante
- **Solución:** Sistema progresivo de niveles, feedback constante

**Desafío 2: Datos Sucios en la Realidad**
- **Problema:** Datos reales tienen problemas
- **Solución:** Herramienta de limpieza automática integrada

**Desafío 3: Mantener Motivación**
- **Problema:** Usuarios abandonan temprano
- **Solución:** Gamificación, badges, progreso visible

**Desafío 4: Balance Simplicidad/Potencia**
- **Problema:** Ser simple pero útil
- **Solución:** Interfaz simple con capacidades profesionales

---

## Slide 29: Conclusiones

### Logros Principales

✅ **Plataforma funcional completa**
- 5 niveles de aprendizaje progresivo
- Sistema de autenticación robusto
- Base de datos integrada

✅ **Experiencia de usuario excelente**
- Interfaz intuitiva
- Feedback inmediato
- Aprendizaje práctico

✅ **Herramientas profesionales**
- Dashboards personalizables
- Limpieza automática de datos
- Visualizaciones interactivas

✅ **Documentación exhaustiva**
- Guías técnicas completas
- Flujos de usuario detallados
- Ejemplos prácticos

**Objetivo Cumplido:** Democratizar el análisis de datos con herramienta educativa efectiva y gratuita

---

## Slide 30: Llamado a la Acción

### Próximos Pasos

**Para Probar la Plataforma:**
```bash
git clone [tu-repositorio]
pip install -r requirements.txt
streamlit run Inicio.py
```

**Credenciales Demo:**
- Usuario: `demo_user`
- Contraseña: `demo123`

**Recursos:**
- 📖 Documentación completa en `/docs`
- 🎥 Video demo: [enlace]
- 💻 Código fuente: [GitHub]
- 📧 Contacto: [tu-email]

**Feedback Bienvenido:**
- Sugerencias de mejora
- Reportar bugs
- Solicitar features
- Contribuciones al código

---

## Slide 31: Agradecimientos

### Créditos

**Tecnologías Open Source Utilizadas:**
- Streamlit Team
- Pandas Development Team
- Plotly Team
- Python Software Foundation

**Recursos:**
- Datasets de ejemplo adaptados de fuentes públicas
- Inspiración de plataformas educativas existentes
- Feedback de usuarios beta

**Especial Agradecimiento:**
- [Profesores/Mentores]
- [Colaboradores]
- [Institución]

---

## Slide 32: Contacto y Links

### Información de Contacto

**Proyecto:**
- **Nombre:** TCC Learning Platform
- **Versión:** 1.0
- **Fecha:** Octubre 2024

**Desarrollador:**
- **Nombre:** [Tu Nombre Completo]
- **Email:** [tu-email@ejemplo.com]
- **LinkedIn:** [tu-perfil]
- **GitHub:** [tu-usuario]

**Links del Proyecto:**
- **Repositorio:** [URL de GitHub]
- **Demo en Vivo:** [URL si está desplegado]
- **Documentación:** [URL de docs]
- **Video Demo:** [URL de video]

**¿Preguntas?**

---

# INSTRUCCIONES PARA GAMMA

## Cómo Usar Este Contenido en Gamma:

1. **Copiar el Contenido:**
   - Copia TODO el contenido de este documento
   - Desde "# TCC Learning Platform" hasta el final

2. **Pegar en Gamma:**
   - Ve a gamma.app
   - Crea una nueva presentación
   - Selecciona "Pegar contenido" o "Import from text"
   - Pega el contenido completo

3. **Configuración Recomendada:**
   - **Tema:** Profesional o Moderno
   - **Colores:** Azul/Verde (tech) o Morado/Azul (educativo)
   - **Tipografía:** Sans-serif moderna (Inter, Roboto)
   - **Animaciones:** Sutiles, profesionales

4. **Personalizar:**
   - Reemplaza [Tu Nombre] con tu nombre real
   - Agrega [tu-email] y links reales
   - Incluye capturas de pantalla en Slide 26
   - Ajusta logos y branding según necesites

5. **Ajustes Finales:**
   - Revisa el orden de slides
   - Ajusta colores a tu preferencia
   - Agrega logos si es necesario
   - Verifica ortografía y formato

6. **Tips para la Presentación:**
   - Slides 1-5: Contexto y problema (5 min)
   - Slides 6-11: Sistema de niveles (10 min)
   - Slides 12-17: Funcionalidades técnicas (8 min)
   - Slides 18-25: Arquitectura y ventajas (7 min)
   - Slides 26-28: Demo y desafíos (5 min)
   - Slides 29-32: Conclusiones y cierre (5 min)
   - **Total:** 40 minutos (ajustable)

## Notas Importantes:

- Las **tablas** se formatean mejor manualmente en Gamma
- Los **bloques de código** pueden necesitar ajuste de sintaxis
- Las **viñetas** deben mantenerse para claridad
- Los **emojis** ayudan a hacer la presentación más visual

## Elementos Visuales Sugeridos ():

- **Slide 4:** Diagrama de arquitectura
- **Slide 5:** Timeline o tabla visual
- **Slide 15:** Foto de persona/avatar para María
- **Slide 16:** Screenshot del dashboard
- **Slide 26:** Demo en vivo o video embebido
- **Slide 27:** Diagrama de Gantt o timeline


