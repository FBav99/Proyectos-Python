# 🎯 Guía de Flujo del Usuario - TCC Learning Platform

## 📋 Resumen Ejecutivo

Este documento detalla el flujo típico de un usuario regular desde su primera visita hasta la creación de un dashboard profesional. El viaje completo incluye 5 niveles de aprendizaje progresivos, uso de datasets reales, y la aplicación práctica de conceptos de análisis de datos.

**Duración estimada del flujo completo:** 3-4 horas  
**Dataset utilizado en el ejemplo:** E-commerce (Ventas de TechStore)  
**Prerrequisitos:** Ninguno - El curso está diseñado para usuarios sin experiencia previa en análisis de datos

---

## 🚀 Fase 1: Inicio y Registro (5-10 minutos)

### 1.1 Primera Visita a la Plataforma

**URL:** `http://localhost:8501` (o URL de producción)

**Experiencia del usuario:**
1. El usuario ve la página de inicio sin estar autenticado
2. Se muestra un formulario de login con opciones:
   - Iniciar sesión con credenciales existentes
   - Crear una nueva cuenta
   - Iniciar sesión con OAuth (Google/otros)

**Elementos visuales:**
- Header con título "Dashboard Principal"
- Mensaje de bienvenida
- Formulario de autenticación centralizado

### 1.2 Registro de Nueva Cuenta

**Acción del usuario:** Hacer clic en "Crear Nueva Cuenta" o navegar a `pages/05_Registro.py`

**Información requerida:**
```
- Nombre de usuario: "maria_gonzalez"
- Contraseña: ********
- Confirmar contraseña: ********
- Nombre: "María"
- Apellido: "González"
- Email: "maria.gonzalez@example.com"
```

**Validaciones automáticas:**
- Nombre de usuario único
- Contraseña con mínimo de caracteres
- Email en formato válido
- Contraseñas coincidentes

**Resultado exitoso:**
- Usuario creado en la base de datos SQLite (`tcc_database.db`)
- Redirección automática a la página de inicio
- Sesión iniciada automáticamente

### 1.3 Vista del Dashboard Principal

**Estado después del login:**
```
🏠 Inicio - Dashboard Principal

Bienvenido, María González

Progreso general: 0% (0/5 niveles completados)
```

**Secciones visibles:**
1. **Quick Start Section**
   - 🚀 Comenzar Aprendizaje
   - 📤 Subir Datos
   - 📊 Usar Datos de Ejemplo

2. **Learning Section** (si se hace clic en "Comenzar Aprendizaje")
   - Vista de los 5 niveles con estado "Por comenzar"
   - Descripción breve de cada nivel

3. **User Profile Section**
   - Nombre de usuario
   - Progreso actual (0%)
   - Niveles completados (0/5)

---

## 📚 Fase 2: Nivel 0 - Introducción (15-20 minutos)

### 2.1 Acceso al Nivel 0

**Navegación:** Dashboard Principal → "Comenzar Aprendizaje" → Nivel 0

**Página:** `pages/00_Nivel_0_Introduccion.py`

### 2.2 ¿Qué ve el usuario?

**Header:**
```
🌟 Nivel 0: Introducción
Conceptos Fundamentales de Datos

Progreso general: 0% (0/5 niveles)
```

**Objetivos de aprendizaje mostrados:**
- ¿Qué son los datos?
- Tipos de datos que existen
- ¿Qué puedes hacer con los datos?
- ¿Cómo se ven los datos organizados?
- ¿Qué es el análisis de datos?

### 2.3 Experiencia de Aprendizaje

**Paso 1: ¿Qué son los datos?**
```
María lee sobre:
- Definición de datos
- Ejemplos en la vida real (tienda, restaurante, teléfono, clima)
- Por qué son importantes
```

**Paso 2: Tipos de datos**
```
María aprende sobre:
- 🔢 Datos numéricos (enteros, decimales, porcentajes)
- 🔤 Datos de texto (nombres, categorías, descripciones)
- 📅 Datos de fecha y hora
- ✅ Datos de sí/no (booleanos)
```

**Paso 3: ¿Qué puedes hacer con los datos?**
```
María descubre:
- Descubrir tendencias
- Hacer comparaciones
- Encontrar patrones
- Tomar decisiones
```

**Paso 4: Estructura de datos**
```
María ve un ejemplo de tabla:
| Fecha | Producto | Cantidad | Precio | Cliente |
|-------|----------|----------|--------|---------|
| 15/03 | Laptop   | 1        | $800   | Juan    |
| 15/03 | Mouse    | 2        | $25    | María   |

Entiende que:
- Cada fila = un registro (una venta)
- Cada columna = un tipo de información
```

**Paso 5: El análisis de datos**
```
María aprende el proceso:
1. Preguntar → 2. Recopilar → 3. Limpiar → 
4. Explorar → 5. Analizar → 6. Comunicar
```

### 2.4 Datos de Ejemplo - TechStore

**Primera interacción con datos reales:**

María ve datos limpios de TechStore:
```
📁 Datos de ejemplo (Ventas de TechStore)
Total de registros: 1000
Columnas: 8
Período: 01/01/2023 - 31/12/2023

Columnas visibles:
- 📅 Fecha: datetime64
- 🔤 Producto: object
- 🔤 Categoria: object
- 🔢 Cantidad: int64
- 💰 Ventas: float64
- 🔤 Region: object
- ⭐ Calificacion: int64
- 💰 Ingresos: float64
```

### 2.5 Comparación: Datos Limpios vs Datos con Problemas

**María ve dos versiones del mismo dataset:**

**Datos Limpios:**
```
✅ Todos los datos completos
✅ Nombres consistentes (Electronica)
✅ Calificaciones válidas (1-5)
✅ Fechas en formato correcto
✅ Sin filas duplicadas
```

**Datos con Problemas:**
```
❌ Datos faltantes (celdas vacías)
❌ Nombres inconsistentes (Electronica vs ELECTRONICA)
❌ Calificaciones inválidas (6, 0, -1)
❌ Fechas en diferentes formatos
❌ Filas duplicadas
```

**Impacto mostrado:**
```
Métricas comparadas:
- Datos limpios: 950 registros, 100% calificaciones válidas
- Datos problemáticos: 1000 registros, 75% calificaciones válidas
```

### 2.6 Ejemplo Interactivo

**María experimenta con filtros básicos:**

```
🔍 Ver datos por categoría:
[Dropdown] Selecciona: "Electronica"

Resultados:
Total de ventas: $45,678.00
Promedio de ventas: $156.82
Registros: 291
```

**Insights que María descubre:**
- Los datos organizados son fáciles de analizar
- Los filtros ayudan a enfocarse en información específica
- Las métricas cambian según los filtros aplicados

### 2.7 Completar el Nivel 0

**María marca el checkbox:**
```
✅ He completado todos los pasos del Nivel 0
```

**Resultado:**
```
🎉 ¡Felicidades! Has completado el Nivel 0

Badge desbloqueado: 🌟 Iniciador de Datos
Progreso actualizado: 20% (1/5 niveles)

¿Qué sigue?
En el Nivel 1 aprenderás a preparar y cargar datos correctamente.

[Botón] Continuar al Nivel 1
```

**Estado en la base de datos:**
```sql
UPDATE user_progress 
SET nivel0 = TRUE 
WHERE user_id = 'maria_gonzalez_id';
```

---

## 📊 Fase 3: Nivel 1 - Preparación de Datos (20-30 minutos)

### 3.1 Acceso al Nivel 1

**Navegación:** Nivel 0 → "Continuar al Nivel 1" o Dashboard → Nivel 1

**Validación:** El sistema verifica que Nivel 0 esté completado

**Página:** `pages/01_Nivel_1_Basico.py`

### 3.2 ¿Qué ve María?

**Header:**
```
📚 Nivel 1: Básico
Preparación y Carga de Datos

Progreso general: 20% (1/5 niveles)

✅ Nivel 0 completado - Badge mostrado
```

**Conexión con el nivel anterior:**
```
🔗 Conectando con el Nivel 0
En el nivel anterior aprendiste que los datos se organizan 
en tablas con filas (registros) y columnas (tipos de información). 
Ahora vamos a ver cómo preparar esos datos para que estén 
listos para analizar.
```

### 3.3 Experiencia de Aprendizaje

**Paso 1: Elegir el formato correcto**
```
María aprende sobre:
📁 Formatos recomendados:
- CSV (.csv) - Para datos simples
- Excel (.xlsx) - Para datos con formato
- JSON (.json) - Para datos complejos

⚠️ Formatos a evitar:
- PDF - No se puede analizar directamente
- Imágenes - Necesitan procesamiento
- Word - No está diseñado para datos tabulares
```

**Paso 2: Preparar la estructura**
```
Reglas para organizar datos:
✅ Una fila = un registro
✅ Una columna = un tipo de información
✅ Encabezados claros
✅ Sin filas vacías

María ve ejemplos de:
- Estructura correcta ✅
- Estructura incorrecta ❌
```

**Paso 3: Cargar el archivo**
```
Proceso paso a paso:
1. Localiza el botón de carga
2. Selecciona tu archivo
3. Confirma la carga
4. Espera la confirmación

Problemas comunes:
⚠️ Archivo muy grande
⚠️ Formato no soportado
⚠️ Archivo corrupto
```

**Paso 4: Verificar la carga**
```
Checklist de verificación:
👀 ¿Se ven todos los datos?
📅 ¿Las fechas están correctas?
❌ ¿No hay datos extraños?
🔢 ¿El conteo es correcto?
```

**Paso 5: Entender la estructura**
```
Información a revisar:
- Número de filas
- Número de columnas
- Tipos de datos
- Valores únicos
```

### 3.4 Datos de Ejemplo - TechStore (Datos Sin Procesar)

**María ve datos con problemas reales:**

```
📁 Datos de ejemplo (Ventas de TechStore - Datos sin procesar)
Total de registros: 1050
Columnas: 8
Período: 01/01/2023 - 31/12/2023

🔍 Problemas identificados:
❌ Valores faltantes en Categoría (15 registros)
❌ Filas duplicadas (25 registros)
❌ Calificaciones fuera del rango 1-5 (12 registros)
❌ Valores atípicos en Ventas (5 registros)
```

### 3.5 Comparación: Antes y Después de Limpiar

**María ve el impacto visual:**

**Datos Sin Procesar (Izquierda):**
```
| Fecha      | Producto  | Categoria     | Ventas  | Calificacion |
|------------|-----------|---------------|---------|--------------|
| 2023-01-15 | Laptop    | Electronica   | 1200.50 | 5            |
| 2023-01-15 | Mouse     |               | 25.00   | 3            |
| 2023-01-16 | Teclado   | ELECTRONICA   | 50.00   | 6            |
| 2023-01-15 | Laptop    | Electronica   | 1200.50 | 5            | (duplicado)
```

**Datos Después de Limpiar (Derecha):**
```
| Fecha      | Producto  | Categoria   | Ventas  | Calificacion |
|------------|-----------|-------------|---------|--------------|
| 2023-01-15 | Laptop    | Electronica | 1200.50 | 5            |
| 2023-01-15 | Mouse     | Electronica | 25.00   | 3            |
| 2023-01-16 | Teclado   | Electronica | 50.00   | 5            |
```

**Mejoras aplicadas:**
```
✅ Valores faltantes eliminados o corregidos
✅ Duplicados removidos
✅ Calificaciones normalizadas (1-5)
✅ Valores atípicos corregidos
✅ Formatos consistentes
```

**Impacto de la limpieza:**
```
Registros originales: 1050
Registros limpios: 1000
Datos faltantes: 15 → 0
Duplicados: 25 → 0
Calidad general: 75% → 95%
```

### 3.6 Prueba Práctica - Subir Archivo

**María decide probar con su propio archivo:**

**Opción 1: Usar dataset de ejemplo**
```
María hace clic en "Usar Datos de Ejemplo"
Selecciona: "E-commerce" dataset
Sistema carga automáticamente 1000 registros
```

**Opción 2: Subir archivo propio**
```
María sube un archivo CSV de ventas de su negocio:
"ventas_enero_2024.csv"

Sistema procesa:
📤 Cargando archivo...
✅ Archivo cargado exitosamente: ventas_enero_2024.csv

Vista general:
Total de registros: 450
Columnas: 7
Columnas numéricas: 3
Columnas de texto: 4
```

**Análisis automático:**
```
📊 Información básica:
- Total de registros: 450
- Columnas: 7

🔍 Estructura:
📋 Columnas disponibles:
- 📅 Fecha: datetime64
- 🔤 Producto: object
- 🔢 Cantidad: int64
- 💰 Precio: float64
- 🔤 Cliente: object
- 🔤 Region: object
- ⭐ Rating: float64

📚 Análisis de calidad:
✅ Sin datos faltantes - Excelente calidad
✅ Sin filas duplicadas - Datos únicos
🔢 Columnas numéricas: Cantidad, Precio, Rating
🔤 Columnas de texto: Producto, Cliente, Region
```

### 3.7 Completar el Nivel 1

**María marca el checkbox:**
```
✅ He completado todos los pasos del Nivel 1
```

**Resultado:**
```
🎉 ¡Felicidades! Has completado el Nivel 1

Badge desbloqueado: 📚 Preparador de Datos
Progreso actualizado: 40% (2/5 niveles)

¿Qué sigue?
En el Nivel 2 aprenderás a organizar y filtrar la información 
para encontrar exactamente lo que necesitas.

[Botón] Continuar al Nivel 2
```

---

## 🔍 Fase 4: Nivel 2 - Filtros (20-25 minutos)

### 4.1 Acceso al Nivel 2

**Validación:** Sistema verifica que Nivel 1 esté completado

**Página:** `pages/02_Nivel_2_Filtros.py`

### 4.2 ¿Qué ve María?

**Header:**
```
🔍 Nivel 2: Filtros
Organizar y Filtrar Información

Progreso general: 40% (2/5 niveles)

✅ Nivel 0 completado - 🌟 Iniciador de Datos
✅ Nivel 1 completado - 📚 Preparador de Datos
```

**Conexión con niveles anteriores:**
```
🔗 Conectando con el Nivel 1
En el nivel anterior aprendiste a cargar y verificar datos. 
Ahora que tienes datos limpios y bien estructurados, puedes 
empezar a filtrarlos para encontrar información específica. 
¡Es hora de explorar tus datos!
```

### 4.3 Experiencia de Aprendizaje

**Paso 1: Filtros de fecha**
```
María aprende sobre:
📅 Tipos de filtros de fecha:
- Rango de fechas (desde-hasta)
- Período específico (último mes, este año)
- Fecha única (un día específico)

✅ Ejemplos de uso:
- Ver ventas del último trimestre
- Comparar resultados entre dos meses
- Analizar tendencias por estación
```

**Paso 2: Filtros por categorías y regiones**
```
🏷️ Filtros por categoría:
- Solo electrónicos
- Solo ropa
- Solo servicios

🌍 Filtros por región:
- Solo México
- Solo Norte
- Solo Ciudad de México
```

**Paso 3: Filtros numéricos con deslizadores**
```
🔢 Tipos de filtros numéricos:
- Rango de precios: $100 - $500
- Ventas mínimas: > 50 unidades
- Calificaciones: ≥ 4 estrellas
- Edad o antigüedad: 25-45 años

🎛️ Cómo usar deslizadores:
[===|========|===]
    min     max
```

**Paso 4: Combinar múltiples filtros**
```
🔗 Ejemplos de combinaciones:
- Fecha + Categoría: Electrónicos en diciembre
- Región + Precio: Productos caros en el norte
- Categoría + Calificación: Ropa con 5 estrellas
```

**Paso 5: Impacto en las métricas**
```
📊 Métricas que cambian con filtros:
- Total de ventas → Solo productos filtrados
- Promedio de precios → Solo productos visibles
- Número de registros → Solo resultados filtrados

⚠️ Importante:
- Los filtros no cambian tus datos originales
- Siempre puedes quitar filtros
- Los filtros se aplican en tiempo real
```

### 4.4 Datos de Ejemplo - TechStore (Datos Limpios)

**María trabaja con datos ya preparados:**

```
📁 Datos de ejemplo (Ventas de TechStore - Datos preparados)

✨ Transformación de Datos Completada
Los datos que viste en el Nivel 1 (con problemas de calidad) 
ahora están limpios y organizados.

Total de registros: 1000
Columnas: 8
Período: 01/01/2023 - 31/12/2023
```

### 4.5 Práctica Interactiva con Filtros

**María experimenta con los controles de filtro:**

**Configuración inicial:**
```
📅 Filtro por fecha:
Fecha de inicio: 01/01/2023
Fecha de fin: 31/12/2023

🏷️ Filtro por categoría:
[Dropdown] Todas

🌍 Filtro por región:
[Dropdown] Todas

💰 Rango de ventas:
Mínimas: $0 [========|] $5000
Máximas: $0 [|========] $5000

⭐ Calificación mínima:
[====|] 1-5
```

**María aplica su primer filtro:**
```
Selecciona: Categoría = "Electronica"

📊 Resultados Filtrados:
Registros originales: 1000
Registros filtrados: 350

Ventas totales: $456,789
Promedio ventas: $1,305
Ingresos totales: $523,456
Promedio ingresos: $1,495
Calificación promedio: 4.2
Productos únicos: 1
```

**María combina filtros:**
```
Paso 1: Categoría = "Electronica"
Paso 2: Región = "Norte"
Paso 3: Ventas mínimas = $500

📊 Resultados Filtrados:
Registros originales: 1000
Registros filtrados: 85

Ventas totales: $98,234
Promedio ventas: $1,155
Calificación promedio: 4.5
```

**María observa el impacto:**
```
Sin filtros → Con filtros:
1000 registros → 85 registros
$1.2M ventas → $98K ventas

Insight descubierto:
"Las ventas de Electronica en la región Norte con 
valores altos tienen mejor calificación (4.5 vs 4.2 promedio)"
```

**María prueba otro escenario:**
```
Pregunta: "¿Cómo fueron las ventas de Electronica en diciembre?"

Configuración:
- Categoría: Electronica
- Fecha inicio: 01/12/2023
- Fecha fin: 31/12/2023

Resultado:
Registros: 45
Ventas totales: $67,890
Promedio: $1,508

Insight:
"Diciembre tiene ventas 15% más altas que el promedio anual"
```

### 4.6 Consejos y Buenas Prácticas

**María aprende errores comunes:**
```
⚠️ Errores a evitar:
❌ Filtros muy restrictivos → Pocos o ningún resultado
❌ Olvidar quitar filtros → Análisis parcial sin saberlo
❌ Filtros contradictorios → Resultados confusos
❌ Ignorar el contexto → Filtros sin sentido
```

**Buenas prácticas:**
```
✅ Planifica tu análisis antes de filtrar
✅ Usa filtros gradualmente (uno a la vez)
✅ Verifica que los resultados tengan sentido
✅ Documenta qué filtros usaste
```

### 4.7 Completar el Nivel 2

**María marca el checkbox:**
```
✅ He completado todos los pasos del Nivel 2
```

**Resultado:**
```
🎉 ¡Felicidades! Has completado el Nivel 2

Badge desbloqueado: 🔍 Explorador de Datos
Progreso actualizado: 60% (3/5 niveles)

¿Qué sigue?
En el Nivel 3 aprenderás a calcular métricas y estadísticas.

[Botón] Continuar al Nivel 3
```

---

## 📊 Fase 5: Nivel 3 - Métricas y KPIs (25-30 minutos)

### 5.1 Acceso al Nivel 3

**Validación:** Sistema verifica que Niveles 1 y 2 estén completados

**Página:** `pages/03_Nivel_3_Metricas.py`

### 5.2 ¿Qué ve María?

**Header:**
```
📊 Nivel 3: Métricas
KPIs y Análisis de Rendimiento

Progreso general: 60% (3/5 niveles)

✅ Nivel 0 - 🌟 Iniciador de Datos
✅ Nivel 1 - 📚 Preparador de Datos
✅ Nivel 2 - 🔍 Explorador de Datos
```

**Conexión con todos los niveles anteriores:**
```
🔗 Conectando con Niveles Anteriores

Nivel 0: Aprendiste qué son los datos y cómo se organizan
Nivel 1: Aprendiste a prepararlos correctamente
Nivel 2: Aprendiste a filtrarlos para encontrar información específica
Nivel 3: ¡Ahora calcularás métricas importantes con esos datos filtrados!
```

### 5.3 Experiencia de Aprendizaje

**Paso 1: Entender métricas y KPIs**
```
María aprende:
📊 ¿Qué son las métricas?
- Números que miden el estado de las cosas
- "Termómetros" del negocio

🎯 ¿Qué son los KPIs?
- Indicador Clave de Rendimiento
- Las métricas MÁS importantes
- Te dicen si tu negocio va bien o mal

✅ Ejemplos de KPIs comunes:
- Ventas totales
- Número de clientes
- Satisfacción del cliente
- Tiempo de entrega
```

**Paso 2: Identificar métricas clave**
```
🔍 Cómo identificar métricas clave:
1. Pregúntate: ¿Qué quiero lograr?
2. Identifica qué números te dirán si lo estás logrando
3. Elige 3-5 métricas principales
4. Evita medir todo, enfócate en lo importante

💡 Ejemplos por tipo de negocio:
Tienda online: Ventas, visitantes, tasa de conversión
Consultoría: Horas facturables, satisfacción, proyectos completados
Restaurante: Ventas por mesa, tiempo de espera, calificaciones
```

**Paso 3: Interpretar y analizar métricas**
```
📈 Tipos de análisis:
- Análisis de tendencias: ¿Suben o bajan?
- Comparaciones: ¿Cómo vs el mes pasado?
- Análisis de patrones: ¿Se repiten?
- Análisis de correlación: ¿Relacionados?

✅ Preguntas clave:
- ¿Este número es bueno o malo?
- ¿Por qué cambió?
- ¿Qué puedo hacer para mejorarlo?
- ¿Qué consecuencias tiene?
```

**Paso 4: Usar métricas para decisiones**
```
🎯 Proceso de decisión basada en datos:
1. Revisa las métricas regularmente
2. Identifica problemas o oportunidades
3. Genera hipótesis sobre qué está pasando
4. Toma acción basada en los datos
5. Mide el resultado de tus acciones

⚠️ Errores a evitar:
- Enfocarse solo en una métrica
- No considerar el contexto
- Tomar decisiones sin entender la causa
- Ignorar tendencias a largo plazo
```

### 5.4 Ejemplo Práctico - Análisis de Ventas TechStore

**María ve métricas calculadas automáticamente:**

```
📊 Datos de Ejemplo
(1000 registros de Ventas de TechStore)

🔢 Cálculo de Métricas Básicas:

┌─────────────────────┬──────────────────────┐
│ 💰 Ventas Totales   │ 📊 Promedio de Ventas│
│ $1,245,678.50       │ $1,245.68            │
└─────────────────────┴──────────────────────┘

┌─────────────────────┬──────────────────────┐
│ 📦 Cantidad Total   │ ⭐ Calificación Prom.│
│ 2,345               │ 4.2                  │
└─────────────────────┴──────────────────────┘
```

**María ve análisis por categoría:**

```
🏷️ Análisis por Categoría

Gráfico de barras (visualización):
Electronica:    ████████████████ $567,890
Hogar:          ███████████      $345,678
Deportes:       █████████        $234,567
Libros:         ██████           $97,543

Tabla:
┌──────────────┬────────────────┐
│ Categoria    │ Ventas Totales │
├──────────────┼────────────────┤
│ Electronica  │ $567,890       │
│ Hogar        │ $345,678       │
│ Deportes     │ $234,567       │
│ Libros       │ $97,543        │
└──────────────┴────────────────┘
```

**María ve análisis por región:**

```
🌍 Análisis por Región

Gráfico de barras:
Norte:  ███████████████ $423,456
Sur:    ████████████    $356,789
Este:   ██████████      $267,890
Oeste:  █████████       $197,543

Insights automáticos:
✨ La región Norte genera 34% de las ventas totales
✨ Las regiones Norte y Sur juntas representan 63% del total
```

### 5.5 Práctica Interactiva

**María experimenta con filtros dinámicos:**

```
🎯 Práctica Interactiva

Controles:
🏷️ Seleccionar Categoría: [Dropdown: Electronica]
🌍 Seleccionar Región: [Dropdown: Norte]

📊 Resultados Filtrados:

┌──────────────────────┬───────────────────────┐
│ 💰 Ventas Filtradas  │ 📊 Promedio Filtrado  │
│ $234,567             │ $1,567                │
└──────────────────────┴───────────────────────┘

┌──────────────────────┬───────────────────────┐
│ 📋 Registros         │ ⭐ Calificación       │
│ 150                  │ 4.5                   │
└──────────────────────┴───────────────────────┘
```

**María descubre un insight:**
```
💡 Insight descubierto:
"Los productos de Electronica en la región Norte tienen:
- Ventas 25% superiores al promedio
- Calificación más alta (4.5 vs 4.2)
- Menor variabilidad en precios

Recomendación: Enfocar estrategia de marketing en esta 
combinación de categoría-región"
```

**María analiza tendencias temporales:**
```
Selecciona: Ver gráfico de ventas diarias

📈 Gráfico de línea (visualización):
Ventas diarias de Electronica en Norte

$2500 |                  ╱╲
      |              ╱  /  \  ╱
$2000 |          ╱  /      \/
      |      ╱  /
$1500 |  ╱  /
      |/
$1000 └────────────────────────────
      Ene  Feb  Mar  Abr  May  Jun

Insight: Pico de ventas en abril (probablemente campaña)
```

### 5.6 Quiz de Comprensión

**María responde el quiz para completar el nivel:**

```
🧠 Quiz de Comprensión

Pregunta 1: ¿Qué significa KPI?
○ Indicador de Progreso Importante
● Indicador Clave de Rendimiento ✓
○ Indicador de Calidad Principal
○ Indicador de Rendimiento Clave

Pregunta 2: ¿Cuál es el primer paso para usar métricas 
efectivamente?
○ Calcular muchas métricas
● Identificar qué métricas son importantes para tu objetivo ✓
○ Comparar con la competencia
○ Crear gráficos bonitos

Pregunta 3: ¿Por qué es importante interpretar métricas, 
no solo verlas?
○ Para impresionar a otros
● Para entender qué significan y qué acciones tomar ✓
○ Para llenar reportes
○ Para cumplir requisitos

[Botón] 📝 Enviar Respuestas
```

**Resultado del quiz:**
```
🎉 ¡Excelente! Obtuviste 100%

Has completado este nivel exitosamente!
[Confetti animation] 🎊

Progreso guardado en la base de datos.
```

### 5.7 Completar el Nivel 3

**Resultado:**
```
🎉 ¡Felicidades! Has completado el Nivel 3

Badge desbloqueado: 📊 Analista de Métricas
Progreso actualizado: 80% (4/5 niveles)

✅ Nivel 3 completado! Puedes continuar al siguiente nivel.

¿Qué sigue?
En el Nivel 4 aprenderás a crear cálculos personalizados, 
generar visualizaciones interactivas y crear dashboards 
completos para presentar tu información de manera profesional.

[Botón] 🚀 Ir al Nivel 4
```

---

## 🚀 Fase 6: Nivel 4 - Análisis Avanzado (30-40 minutos)

### 6.1 Acceso al Nivel 4

**Validación:** Sistema verifica que Niveles 1, 2 y 3 estén completados

**Página:** `pages/04_Nivel_4_Avanzado.py`

### 6.2 ¿Qué ve María?

**Header:**
```
🚀 Nivel 4: Avanzado
Cálculos y Visualizaciones Avanzadas

Progreso general: 80% (4/5 niveles)

¡Felicidades! Has llegado al nivel más avanzado.

✅ Nivel 0 - 🌟 Iniciador de Datos
✅ Nivel 1 - 📚 Preparador de Datos
✅ Nivel 2 - 🔍 Explorador de Datos
✅ Nivel 3 - 📊 Analista de Métricas
```

**Resumen de la jornada:**
```
🎓 Resumen de tu Jornada de Aprendizaje

Nivel 0: Aprendiste qué son los datos y cómo se organizan
Nivel 1: Aprendiste a preparar y cargar datos correctamente
Nivel 2: Aprendiste a filtrar y organizar información
Nivel 3: Aprendiste a calcular métricas y KPIs
Nivel 4: ¡Ahora crearás dashboards profesionales!
```

### 6.3 Experiencia de Aprendizaje

**Paso 1: Crear cálculos personalizados avanzados**
```
María aprende sobre:
🔢 Tipos de cálculos:
- Porcentajes: Qué parte del total representa algo
- Promedios ponderados: Promedios con importancia variable
- Cambios porcentuales: Cuánto aumentó o disminuyó
- Ratios y proporciones: Comparaciones entre valores

📝 Ejemplos de fórmulas:
Margen de ganancia = (Precio venta - Costo) / Precio venta × 100
% de crecimiento = (Valor actual - Valor anterior) / Valor anterior × 100
Promedio ponderado = Suma(Valor × Peso) / Suma(pesos)
```

**Paso 2: Generar visualizaciones interactivas**
```
📊 Tipos de visualizaciones:
- Gráficos de línea: Tendencias a lo largo del tiempo
- Gráficos de barras: Comparar categorías
- Gráficos de dispersión: Relaciones entre dos variables
- Mapas de calor: Patrones en tablas de datos

🎯 Características interactivas:
✨ Zoom y panorámica
✨ Tooltips informativos
✨ Filtros dinámicos
✨ Selección de elementos
```

**Paso 3: Crear dashboards profesionales**
```
🏗️ Elementos de un dashboard efectivo:
- Métricas clave (KPIs) en la parte superior
- Visualizaciones que explican las métricas
- Filtros para cambiar la vista
- Navegación entre vistas

💡 Principios de diseño:
✨ Diseño limpio sin distracciones
✨ Colores consistentes y significativos
✨ Organización de más a menos importante
✨ Fácil de entender para la audiencia
```

**Paso 4: Interpretar y comunicar insights**
```
🔍 Cómo encontrar insights:
- Busca patrones inesperados
- Compara diferentes períodos o grupos
- Identifica valores atípicos
- Conecta diferentes métricas

📢 Cómo comunicar insights:
- Cuenta una historia con los datos
- Explica qué significa para el negocio
- Sugiere acciones específicas
- Usa visualizaciones de respaldo
```

### 6.4 Ejemplo Práctico - Dashboard Avanzado TechStore

**María ve cálculos avanzados en acción:**

```
🔢 Cálculos Avanzados
(Aplicados automáticamente al dataset)

Nuevas columnas calculadas:
- Margen_Ganancia: 40% promedio
- Ingresos_Totales: Ventas × Cantidad
- Eficiencia_Ventas: Ingresos / Cantidad

┌──────────────────────┬─────────────────────┐
│ 💰 Ingresos Totales  │ 📈 Margen Promedio  │
│ $2,567,890.45        │ 42.3%               │
└──────────────────────┴─────────────────────┘

┌──────────────────────┬─────────────────────┐
│ 📋 Total de Pedidos  │ ⚡ Eficiencia Prom. │
│ 1,000                │ $1,094.22           │
└──────────────────────┴─────────────────────┘
```

**María interactúa con visualizaciones avanzadas:**

```
📊 Visualizaciones Interactivas

Controles de filtro:
Ventas Mínimas: [===|=========] $0 - $5000
Categorías: ☑ Electronica ☑ Hogar ☑ Deportes ☑ Libros
Regiones: ☑ Norte ☑ Sur ☑ Este ☑ Oeste

Visualización 1: Ventas por Categoría (Plotly)
[Gráfico de barras interactivo con colores degradados]
- Al pasar el mouse: Muestra valor exacto, porcentaje del total
- Zoom disponible
- Exportable como imagen
```

**María ve el gráfico de pastel interactivo:**
```
Visualización 2: Distribución de Ventas por Región

[Gráfico circular (pie chart) con Plotly]
Norte: 34.0% ($873,456)
Sur: 28.6% ($734,567)
Este: 21.4% ($549,890)
Oeste: 16.0% ($410,067)

Interacciones:
- Click en una sección: La separa del resto
- Hover: Muestra información detallada
- Leyenda: Click para ocultar/mostrar regiones
```

**María analiza tendencias temporales:**
```
📈 Análisis de Tendencias Temporales

[Gráfico de líneas doble con Plotly]

Panel 1: Ventas Diarias
$3000 |              ╱╲
      |          ╱  /  \  ╱╲
$2000 |      ╱  /      \/  \
      |  ╱  /              \
$1000 |/                     ╲
      └──────────────────────────
      Ene  Mar  May  Jul  Sep  Nov

Panel 2: Margen de Ganancia Promedio
50% |  ─────╱╲─────╱╲─────
    |       /  \   /  \
40% |      /    \ /    \
    |     /      X      \
30% |    /      / \      \
    └────────────────────────
    Ene  Mar  May  Jul  Sep  Nov

Insights automáticos:
✨ Ventas más altas en abril y noviembre
✨ Margen se mantiene estable entre 38-45%
✨ Correlación positiva entre ventas y margen
```

**María explora la matriz de correlación:**
```
🔗 Análisis de Correlaciones

[Mapa de calor con Plotly]

                 Ventas  Cantidad  Calificacion  Margen
Ventas           1.00    0.68      0.34         0.45
Cantidad         0.68    1.00      0.21         0.32
Calificacion     0.34    0.21      1.00         0.67
Margen           0.45    0.32      0.67         1.00

Colores:
🔴 Rojo = Correlación negativa fuerte
⚪ Blanco = Sin correlación
🔵 Azul = Correlación positiva fuerte

💡 Insights de Correlación:
✨ Calificación alta → Margen alto (0.67)
   "Productos bien valorados tienen mejores márgenes"

✨ Ventas → Cantidad (0.68)
   "Mayor cantidad vendida = mayores ventas totales"

✨ Calificación → Ventas (0.34)
   "Productos bien valorados tienden a vender más"
```

### 6.5 Crear Dashboard Personalizado

**María diseña su propio dashboard:**

```
🏗️ Crear tu Propio Dashboard

Paso 1: Seleccionar Métricas a Mostrar
☑ 💰 Ingresos Totales
☑ 📈 Margen de Ganancia
☑ 📋 Número de Pedidos
☑ ⚡ Eficiencia de Ventas

Paso 2: Seleccionar Visualizaciones a Incluir
☑ 🏷️ Gráfico por Categoría
☑ 🌍 Gráfico por Región
☑ 📈 Análisis de Tendencias
□ 🔗 Matriz de Correlación (desactivado para este dashboard)

[Botón] 🚀 Generar Dashboard Personalizado
```

**Dashboard personalizado generado:**
```
🎯 Tu Dashboard Personalizado

┌──────────────────────────────────────────────────────┐
│ 📊 Métricas Clave                                    │
├─────────────┬─────────────┬─────────────┬───────────┤
│💰 Ingresos  │📈 Margen    │📋 Pedidos   │⚡ Eficien. │
│$2,567,890   │42.3%        │1,000        │$1,094.22  │
└─────────────┴─────────────┴─────────────┴───────────┘

┌──────────────────────────────────────────────────────┐
│ 📈 Visualizaciones                                   │
│                                                      │
│  [Gráfico de barras - Ventas por Categoría]        │
│  Electronica: ████████████████ $567,890            │
│  Hogar:       ███████████      $345,678            │
│  Deportes:    █████████        $234,567            │
│                                                      │
│  [Gráfico circular - Distribución por Región]      │
│  Norte: 34% • Sur: 29% • Este: 21% • Oeste: 16%   │
│                                                      │
│  [Gráfico de líneas - Tendencias Temporales]       │
│  Ventas diarias con picos en abril y noviembre     │
└──────────────────────────────────────────────────────┘

María puede exportar este dashboard o guardarlo para 
referencia futura.
```

### 6.6 Quiz de Comprensión

**María responde el quiz final:**

```
🧠 Quiz de Comprensión

Pregunta 1: ¿Qué es un dashboard?
○ Un gráfico individual
● Una colección de visualizaciones y métricas organizadas ✓
○ Una tabla de datos
○ Un cálculo matemático

Pregunta 2: ¿Por qué son importantes las visualizaciones 
interactivas?
○ Porque se ven más bonitas
● Porque permiten explorar los datos de manera más profunda ✓
○ Porque son más fáciles de crear
○ Porque ocupan menos espacio

Pregunta 3: ¿Qué son los insights en análisis de datos?
○ Solo los números
● Descubrimientos importantes que pueden llevar a acciones 
  valiosas ✓
○ Los gráficos
○ Las fórmulas matemáticas

[Botón] 📝 Enviar Respuestas
```

**Resultado del quiz:**
```
🎉 ¡Excelente! Obtuviste 100%

¡Has completado todos los niveles exitosamente!
[Balloons animation] 🎈

Eres un experto en análisis de datos!
```

### 6.7 Completar el Nivel 4

**Resultado final:**
```
🎉 ¡Felicidades! Has completado el Nivel 4

Badge desbloqueado: 🚀 Maestro de Dashboards
Progreso actualizado: 100% (5/5 niveles)

🏆 ¡Has completado todos los niveles del curso!
Eres un experto en análisis de datos.

Tu progreso completo:
✅ Nivel 0 - 🌟 Iniciador de Datos
✅ Nivel 1 - 📚 Preparador de Datos
✅ Nivel 2 - 🔍 Explorador de Datos
✅ Nivel 3 - 📊 Analista de Métricas
✅ Nivel 4 - 🚀 Maestro de Dashboards

¿Qué hacer ahora?
[Botón] 🏠 Volver al Inicio
[Botón] 📊 Crear Dashboard

María hace clic en "Crear Dashboard"
```

---

## 🎨 Fase 7: Crear Dashboard Personalizado (20-30 minutos)

### 7.1 Acceso al Dashboard en Blanco

**Navegación:** Nivel 4 → "Crear Dashboard" o Dashboard Principal → "Dashboard en Blanco"

**Página:** `pages/08_Dashboard_Blanco.py`

### 7.2 ¿Qué ve María?

**Header:**
```
🎨 Dashboard en Blanco
Construye tu dashboard personalizado, María González

Estado de datos:
✅ Dataset activo: E-commerce (TechStore)
📊 1000 registros, 8 columnas
```

**Validación de datos:**
```
Sistema verifica:
1. ¿Hay datos en session_state?
   → Sí: st.session_state.sample_data existe (E-commerce dataset)

2. ¿Los datos están limpios?
   → Sí: Datos preparados en Nivel 1
```

### 7.3 Sidebar de Construcción

**María ve el panel lateral:**
```
🎨 Configuración del Dashboard

┌────────────────────────────────────┐
│ 📊 Componentes Disponibles         │
├────────────────────────────────────┤
│ [+] Agregar Componente             │
│                                    │
│ Tipos disponibles:                 │
│ • 📈 Métrica Simple                │
│ • 📊 Gráfico de Barras             │
│ • 📉 Gráfico de Líneas             │
│ • 🥧 Gráfico Circular              │
│ • 📋 Tabla de Datos                │
│ • 📝 Texto/Título                  │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ 🎨 Opciones de Diseño              │
├────────────────────────────────────┤
│ Layout: ○ 1 columna                │
│         ● 2 columnas               │
│         ○ 3 columnas               │
│                                    │
│ Tema: ○ Claro                      │
│       ● Oscuro                     │
└────────────────────────────────────┘
```

### 7.4 Construir el Dashboard Paso a Paso

**Paso 1: María agrega la primera métrica**
```
María hace clic en [+] Agregar Componente
Selecciona: 📈 Métrica Simple

Configuración:
Título: "Ventas Totales"
Columna: Ventas
Agregación: Suma
Formato: Moneda ($)
Icono: 💰

[Botón] ✅ Agregar al Dashboard

Resultado:
┌────────────────────────────────────┐
│ 💰 Ventas Totales                  │
│ $1,245,678.50                      │
└────────────────────────────────────┘
```

**Paso 2: María agrega más métricas**
```
Componente 2: Promedio de Ventas
📊 $1,245.68

Componente 3: Total de Pedidos
📋 1,000

Componente 4: Calificación Promedio
⭐ 4.2

Dashboard actual:
┌─────────────┬─────────────┬─────────────┬─────────────┐
│💰 Ventas    │📊 Promedio  │📋 Pedidos   │⭐ Calificac.│
│$1,245,678   │$1,245.68    │1,000        │4.2 / 5.0    │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Paso 3: María agrega visualizaciones**
```
Componente 5: Gráfico de Barras
Título: "Ventas por Categoría"
Eje X: Categoria
Eje Y: Ventas (suma)
Color: Automático

┌────────────────────────────────────────────────────────┐
│ 📊 Ventas por Categoría                                │
│                                                        │
│ Electronica  ████████████████ $567,890                │
│ Hogar        ███████████      $345,678                │
│ Deportes     █████████        $234,567                │
│ Libros       ██████           $97,543                 │
└────────────────────────────────────────────────────────┘

Componente 6: Gráfico Circular
Título: "Distribución por Región"
Valores: Ventas (suma)
Categorías: Region

┌────────────────────────────────────────────────────────┐
│ 🥧 Distribución por Región                             │
│                                                        │
│    ╱────────────╲                                     │
│   │  34% Norte  │                                     │
│   │             │  29% Sur                            │
│   │  Oeste 16%  │                                     │
│   │             │  21% Este                           │
│    ╲────────────╱                                     │
└────────────────────────────────────────────────────────┘
```

**Paso 4: María agrega filtros interactivos**
```
Componente 7: Panel de Filtros
Título: "🔍 Filtros Globales"

Filtros agregados:
📅 Rango de Fechas: [01/01/2023] - [31/12/2023]
🏷️ Categoría: [Todas]
🌍 Región: [Todas]
💰 Ventas Mínimas: $0

[Botón] 🔄 Aplicar Filtros

Comportamiento:
Al cambiar filtros → Todas las visualizaciones se actualizan
automáticamente en tiempo real
```

**Paso 5: María organiza el layout**
```
María arrastra y organiza los componentes:

Layout final (2 columnas):

┌────────────────────────────────────────────────────────┐
│ 🎯 Dashboard de Análisis de Ventas TechStore           │
├────────────────────────────────────────────────────────┤
│ 🔍 Filtros Globales                                    │
│ [Fecha] [Categoría] [Región] [Ventas Mín] [Aplicar]   │
├────────────────────────────────────────────────────────┤
│ 💰 Ventas  │ 📊 Promedio │ 📋 Pedidos │ ⭐ Calificac. │
│ $1.2M      │ $1,245.68   │ 1,000      │ 4.2 / 5.0    │
├────────────────────────────┬───────────────────────────┤
│ 📊 Ventas por Categoría    │ 🥧 Distribución por       │
│                            │    Región                 │
│ [Gráfico de barras]        │ [Gráfico circular]        │
│                            │                           │
├────────────────────────────┴───────────────────────────┤
│ 📈 Tendencias de Ventas Mensuales                      │
│ [Gráfico de líneas temporal]                           │
│                                                        │
├────────────────────────────────────────────────────────┤
│ 📋 Top 10 Productos                                    │
│ [Tabla con productos más vendidos]                     │
└────────────────────────────────────────────────────────┘
```

### 7.5 Prueba de Funcionalidad

**María prueba su dashboard con filtros:**

```
Escenario 1: Análisis de Electronica en el Norte
─────────────────────────────────────────────────
Filtros:
🏷️ Categoría: Electronica
🌍 Región: Norte

[Clic en "Aplicar"]

Dashboard actualizado:
┌────────────────────────────────────────────────────────┐
│ 💰 Ventas  │ 📊 Promedio │ 📋 Pedidos │ ⭐ Calificac. │
│ $234,567   │ $1,567      │ 150        │ 4.5 / 5.0    │
└────────────────────────────────────────────────────────┘

📊 Ventas por Categoría → Muestra solo Electronica
🥧 Distribución por Región → Muestra solo Norte (100%)
📈 Tendencias → Muestra solo datos de Electronica en Norte

María observa:
✨ Las ventas filtradas son $234K de los $1.2M totales
✨ La calificación en esta combinación es más alta (4.5 vs 4.2)
✨ El promedio de venta es más alto ($1,567 vs $1,245)
```

**María prueba otro escenario:**
```
Escenario 2: Análisis Q4 (Octubre-Diciembre)
──────────────────────────────────────────────
Filtros:
📅 Fecha inicio: 01/10/2023
📅 Fecha fin: 31/12/2023
🏷️ Categoría: Todas
🌍 Región: Todas

[Clic en "Aplicar"]

Dashboard actualizado:
┌────────────────────────────────────────────────────────┐
│ 💰 Ventas  │ 📊 Promedio │ 📋 Pedidos │ ⭐ Calificac. │
│ $387,456   │ $1,345      │ 288        │ 4.3 / 5.0    │
└────────────────────────────────────────────────────────┘

María descubre insights:
✨ Q4 representa 31% de las ventas anuales
✨ Promedio de venta 8% más alto en Q4
✨ Calificaciones ligeramente mejores en temporada alta
```

### 7.6 Guardar y Exportar

**María guarda su dashboard:**
```
┌────────────────────────────────────────────────────────┐
│ 💾 Guardar Dashboard                                   │
├────────────────────────────────────────────────────────┤
│ Nombre: "Dashboard Análisis TechStore Q4 2023"        │
│ Descripción: "Dashboard para análisis trimestral de   │
│              ventas por categoría y región"            │
│                                                        │
│ [Botón] 💾 Guardar Dashboard                           │
│ [Botón] 📥 Exportar como PDF                           │
│ [Botón] 📊 Exportar como Excel                         │
└────────────────────────────────────────────────────────┘

María guarda el dashboard → Confirmación:
✅ Dashboard guardado exitosamente
📋 Puedes acceder a él desde el Dashboard Principal
```

### 7.7 Uso del Dashboard en el Futuro

**María regresa al Dashboard Principal:**
```
🏠 Dashboard Principal

Dashboards Guardados:
┌────────────────────────────────────────────────────────┐
│ 📊 Mis Dashboards                                      │
├────────────────────────────────────────────────────────┤
│ • Dashboard Análisis TechStore Q4 2023                 │
│   Creado: 13/10/2024                                   │
│   Última actualización: 13/10/2024                     │
│   [Ver] [Editar] [Compartir] [Eliminar]               │
└────────────────────────────────────────────────────────┘
```

---

## 🧹 Fase 8 (Opcional): Limpieza de Datos (15-20 minutos)

### 8.1 Acceso a la Página de Limpieza

**Navegación:** Dashboard Principal → "Limpieza de Datos" o menú lateral → "10_Limpieza_Datos"

**Página:** `pages/10_Limpieza_Datos.py`

**Caso de uso:** María tiene un nuevo dataset con problemas de calidad

### 8.2 ¿Qué ve María?

```
🧹 Limpieza Automática de Datos

Limpia y prepara tus datos automáticamente antes del análisis

Funcionalidades incluidas:
🧹 Limpieza de espacios • 📝 Normalización de texto • 
🔄 Reemplazo de valores
📞 Estandarización de teléfonos • 📧 Estandarización de emails • 
❌ Manejo de valores faltantes
```

### 8.3 Subir Dataset Sucio

**María selecciona el "Dataset Sucio" de ejemplo:**

```
📊 Datasets de Ejemplo

Dataset Sucio (Limpieza):
Descripción: Dataset con múltiples problemas de calidad para 
             practicar limpieza automática
Dificultad: Avanzado
Problemas: Espacios, mayúsculas/minúsculas, acentos, teléfonos, 
           emails, duplicados, valores faltantes

[Botón] 📥 Cargar Dataset Sucio

Resultado:
✅ Dataset cargado: 225 filas, 11 columnas
```

### 8.4 Vista de Datos Sin Limpiar

**María ve los problemas:**
```
📊 Datos Actuales: 225 filas, 11 columnas

Vista previa de problemas:

| Nombre            | Email              | Telefono        | Categoria    |
|-------------------|--------------------|-----------------|--------------|
| "  Juan Pérez  "  | "MARIA@EMAIL.COM"  | "+1-555-123-45" | "ELECTRONICA"|
| "MARÍA GARCÍA"    | "  "               | "(555) 123-456" | "electronica"|
| "carlos lopez"    | "carlos@email.com" | "555-123-4567"  | "Electronica"|
| "  "              | "null"             | "5551234567"    | "  "         |

Problemas identificados:
❌ Espacios en blanco al inicio/final
❌ Inconsistencias en mayúsculas/minúsculas
❌ Formatos de teléfono diferentes
❌ Emails con problemas
❌ Valores "null", "N/A", espacios vacíos
❌ Filas duplicadas
```

### 8.5 Aplicar Operaciones de Limpieza

**María aplica limpieza automática:**

```
🧹 Operaciones de Limpieza Automática

┌────────────────────────────────────────────────────────┐
│ Operaciones Disponibles:                               │
├────────────────────────────────────────────────────────┤
│ ☑ Eliminar espacios en blanco                          │
│ ☑ Normalizar mayúsculas/minúsculas                     │
│ ☑ Eliminar acentos                                     │
│ ☑ Estandarizar formatos de teléfono                    │
│ ☑ Validar y estandarizar emails                        │
│ ☑ Reemplazar valores nulos (null, N/A, etc.)          │
│ ☑ Eliminar filas duplicadas                            │
│ ☑ Eliminar columnas vacías                             │
│ ☑ Eliminar filas completamente vacías                  │
└────────────────────────────────────────────────────────┘

[Botón] 🧽 Aplicar Limpieza Automática

Procesando...
[Barra de progreso] ████████████ 100%

✅ Limpieza completada exitosamente!
```

### 8.6 Comparación de Resultados

**María ve la transformación:**
```
📊 Comparación de Datos

Antes de limpiar:
┌─────────────┬─────────────┬──────────────┬─────────────┐
│📈 Filas Orig│🧹 Filas Limp│📉 Filas Remov│🗑️ Cols Remov│
│225          │205          │20            │0            │
└─────────────┴─────────────┴──────────────┴─────────────┘

Datos limpios:

| Nombre        | Email              | Telefono        | Categoria   |
|---------------|--------------------|-----------------|-------------|
| "Juan Perez"  | "maria@email.com"  | "+15551234567"  | "Electronica"|
| "Maria Garcia"| "maria@email.com"  | "+15551234567"  | "Electronica"|
| "Carlos Lopez"| "carlos@email.com" | "+15551234567"  | "Electronica"|

Transformaciones aplicadas:
✅ Espacios eliminados
✅ Mayúsculas/minúsculas normalizadas
✅ Acentos eliminados
✅ Teléfonos en formato estándar +1XXXXXXXXXX
✅ Emails validados y en minúsculas
✅ Valores nulos reemplazados
✅ 20 filas duplicadas eliminadas
✅ 0 columnas vacías eliminadas
```

### 8.7 Descargar Datos Limpios

**María descarga los datos procesados:**
```
💾 Descargar Datos Limpios

Archivo: datos_limpiados.csv
Tamaño: 45 KB
Formato: CSV (UTF-8)
Registros: 205

[Botón] 💾 Descargar Datos Limpiados

✅ Descarga iniciada: datos_limpiados.csv
```

**María puede ahora:**
- Usar estos datos limpios en los niveles de aprendizaje
- Crear dashboards con datos de mejor calidad
- Aplicar análisis más precisos

---

## 📈 Resumen del Flujo Completo

### Tiempo Total Estimado
```
Fase 1: Registro e Inicio          →  5-10 min
Fase 2: Nivel 0 - Introducción      → 15-20 min
Fase 3: Nivel 1 - Preparación       → 20-30 min
Fase 4: Nivel 2 - Filtros           → 20-25 min
Fase 5: Nivel 3 - Métricas          → 25-30 min
Fase 6: Nivel 4 - Avanzado          → 30-40 min
Fase 7: Dashboard Personalizado     → 20-30 min
Fase 8: Limpieza de Datos (Opc.)    → 15-20 min
────────────────────────────────────────────────
Total (sin Fase 8):                 150-185 min (2.5-3 horas)
Total (con Fase 8):                 165-205 min (2.75-3.5 horas)
```

### Progreso de María al Final

```
👤 Perfil de Usuario: María González
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Progreso General: 100% (5/5 niveles completados)

🏆 Badges Desbloqueados:
✅ 🌟 Iniciador de Datos (Nivel 0)
✅ 📚 Preparador de Datos (Nivel 1)
✅ 🔍 Explorador de Datos (Nivel 2)
✅ 📊 Analista de Métricas (Nivel 3)
✅ 🚀 Maestro de Dashboards (Nivel 4)

📈 Dashboards Creados: 1
   • Dashboard Análisis TechStore Q4 2023

📁 Datasets Utilizados:
   • E-commerce (TechStore) - Principal
   • Dataset Sucio - Para práctica de limpieza

🎯 Habilidades Adquiridas:
✅ Comprende conceptos fundamentales de datos
✅ Puede preparar y cargar datos correctamente
✅ Domina el uso de filtros para análisis
✅ Calcula e interpreta métricas y KPIs
✅ Crea visualizaciones interactivas avanzadas
✅ Construye dashboards profesionales
✅ Limpia y procesa datos con problemas de calidad

💡 Próximos Pasos Sugeridos:
• Crear dashboards adicionales con diferentes datasets
• Practicar con datos propios de su negocio
• Explorar análisis más avanzados
• Compartir dashboards con otros usuarios
```

### Conceptos Clave Aprendidos

**Datos y Estructura:**
- Qué son los datos y cómo se organizan
- Tipos de datos (numéricos, texto, fechas, booleanos)
- Estructura de tablas (filas = registros, columnas = atributos)
- Importancia de datos limpios vs datos con problemas

**Preparación de Datos:**
- Formatos de archivo (CSV, Excel, JSON)
- Cómo estructurar datos correctamente
- Carga y verificación de archivos
- Identificación de problemas de calidad
- Limpieza automática de datos

**Análisis de Datos:**
- Uso de filtros (fecha, categoría, región, numéricos)
- Combinación de filtros múltiples
- Impacto de filtros en métricas
- Cálculo de métricas básicas y avanzadas
- Interpretación de KPIs

**Visualización:**
- Gráficos de barras, líneas, circulares
- Visualizaciones interactivas con Plotly
- Tendencias temporales
- Análisis de correlaciones
- Mapas de calor

**Dashboards:**
- Diseño de dashboards efectivos
- Organización de métricas y visualizaciones
- Filtros globales interactivos
- Personalización de layouts
- Comunicación de insights

### Flujo de Datos a Través del Sistema

```
┌─────────────────┐
│  Datos Crudos   │
│  (CSV/Excel)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Carga de Datos  │
│  (Nivel 1)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Limpieza (Opc.) │
│  (Limpieza Pág.)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Datos Limpios   │
│ (Session State) │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌─────────────┐  ┌──────────────┐
│  Filtros    │  │  Métricas    │
│  (Nivel 2)  │  │  (Nivel 3)   │
└──────┬──────┘  └──────┬───────┘
       │                │
       └────────┬───────┘
                │
                ▼
       ┌─────────────────┐
       │ Visualizaciones │
       │   (Nivel 4)     │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │   Dashboard     │
       │  Personalizado  │
       └─────────────────┘
```

### Puntos de Decisión del Usuario

**1. Registro vs Login**
```
Nueva cuenta → Registro completo → Auto-login → Dashboard
Cuenta existente → Login → Dashboard
OAuth → Login rápido → Dashboard
```

**2. Fuente de Datos**
```
Opción A: Usar dataset de ejemplo → Carga inmediata → Continuar
Opción B: Subir archivo propio → Upload → Validación → Continuar
Opción C: Sin datos → Mensaje de error → Redirigir a carga
```

**3. Ruta de Aprendizaje**
```
Secuencial:    Nivel 0 → 1 → 2 → 3 → 4 → Dashboard
Saltar niveles: ❌ No permitido - Debe completar previos
Repetir nivel:  ✅ Permitido - Puede revisar en cualquier momento
```

**4. Limpieza de Datos**
```
Datos limpios → Usar directamente → Análisis
Datos sucios → Página de limpieza → Limpiar → Análisis
```

**5. Creación de Dashboard**
```
Plantilla predefinida → Seleccionar → Personalizar → Guardar
Dashboard en blanco → Construir desde cero → Guardar
```

---

## 🎯 Conclusiones y Mejores Prácticas

### Para Usuarios Nuevos
1. **Seguir el orden secuencial** - Los niveles están diseñados para construir conocimiento progresivamente
2. **Experimentar con datos de ejemplo** - Antes de usar datos propios, familiarízate con los ejemplos
3. **Completar los quizzes** - Validan comprensión y desbloquean niveles
4. **Usar filtros gradualmente** - No combinar muchos filtros al inicio
5. **Guardar dashboards** - Para referencia futura y reutilización

### Para el Sistema
1. **Validación de progreso** - Cada nivel verifica completitud del anterior
2. **Persistencia de datos** - Session state mantiene datos entre páginas
3. **Feedback visual** - Badges, progreso, y confirmaciones mantienen motivación
4. **Ejemplos prácticos** - Cada nivel incluye ejemplos interactivos
5. **Limpieza opcional** - Disponible cuando se necesita, no obligatoria

### Métricas de Éxito del Usuario
- ✅ 100% de niveles completados
- ✅ Al menos 1 dashboard creado
- ✅ Comprensión de conceptos clave validada con quizzes
- ✅ Capacidad de trabajar con datos reales
- ✅ Aplicación práctica de análisis de datos

---

**Documento creado:** 13 de Octubre, 2024  
**Última actualización:** 13 de Octubre, 2024  
**Versión:** 1.0  
**Autor:** Sistema TCC Learning Platform
