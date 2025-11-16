# Documentación de Niveles de Aprendizaje
## Plataforma de Análisis de Datos TCC

**Autor:** Fernando Bavera Villalba  
**Fecha:** 2025  
**Versión:** 1.0

---

## Resumen Ejecutivo

La Plataforma de Análisis de Datos TCC implementa un sistema de aprendizaje progresivo estructurado en cinco niveles consecutivos, diseñado para capacitar a usuarios sin experiencia previa en análisis de datos. Cada nivel está compuesto por componentes pedagógicos específicos, actividades prácticas interactivas, sistemas de evaluación mediante cuestionarios, y mecanismos de seguimiento del progreso del usuario. El sistema utiliza un dataset unificado de ventas de una tienda de tecnología (TechStore) que evoluciona en calidad y complejidad a través de los niveles, facilitando la comprensión gradual de conceptos fundamentales hasta técnicas avanzadas de análisis y visualización.

---

## 1. Introducción

### 1.1 Contexto

La plataforma TCC ha sido desarrollada como una solución educativa integral para el aprendizaje de análisis de datos, dirigida a usuarios sin conocimientos previos en el área. El sistema implementa una metodología de aprendizaje progresivo que guía al usuario desde conceptos fundamentales hasta la creación de dashboards profesionales.

### 1.2 Objetivo del Documento

Este documento proporciona una descripción técnica detallada de cada nivel de aprendizaje, especificando sus componentes, contenidos, metodologías pedagógicas y mecanismos de evaluación, siguiendo un formato de documentación académica tipo tesis.

### 1.3 Estructura del Sistema de Niveles

El sistema comprende cinco niveles numerados del 0 al 4, cada uno con objetivos de aprendizaje específicos, componentes pedagógicos estructurados, y requisitos de progresión secuencial. La completación de cada nivel es un prerrequisito para acceder al siguiente, garantizando una progresión ordenada del conocimiento.

---

## 2. Nivel 0: Introducción - Conceptos Fundamentales de Datos

### 2.1 Descripción General

El Nivel 0 constituye el punto de entrada fundamental al sistema de aprendizaje, diseñado específicamente para establecer las bases conceptuales que permitirán al usuario comprender la naturaleza, organización y utilidad de los datos en contextos de análisis. Este nivel está orientado a usuarios completamente nuevos en el área de análisis de datos, por lo que no requiere conocimientos previos y se enfoca en construir una comprensión sólida desde cero.

El nivel introduce al usuario en el mundo de los datos mediante una aproximación pedagógica que combina explicaciones conceptuales con ejemplos prácticos del mundo real. Se establece el contexto narrativo de TechStore, una tienda de tecnología ficticia cuyos datos de ventas servirán como hilo conductor a lo largo de todos los niveles del sistema. Esta narrativa unificada permite al usuario desarrollar familiaridad con un dataset específico mientras aprende conceptos generales aplicables a cualquier contexto de análisis.

La estructura del nivel está organizada en cinco conceptos fundamentales que progresan desde la definición básica de datos hasta la comprensión del proceso completo de análisis. Cada concepto se presenta mediante tarjetas educativas (step cards) que incluyen definiciones, ejemplos contextualizados y explicaciones sobre la importancia práctica de cada concepto. El nivel también incorpora una sección comparativa que muestra la diferencia entre datos limpios y datos con problemas de calidad, estableciendo desde el inicio la importancia de la calidad de datos en el análisis efectivo.

### 2.2 Objetivos de Aprendizaje

Los objetivos de aprendizaje del Nivel 0 están diseñados para establecer una base conceptual sólida. El usuario debe ser capaz de comprender la definición y naturaleza fundamental de los datos, reconociendo que los datos son información que puede medirse, contarse o describirse, y que existen en múltiples formas y contextos. Se busca que el usuario pueda identificar y clasificar los diferentes tipos de datos, incluyendo datos numéricos (enteros, decimales, porcentajes), datos de texto (nombres, categorías, descripciones), datos de fecha y hora, datos booleanos (sí/no, verdadero/falso), y datos especiales como geográficos, imágenes, audio/video y datos de sensores IoT.

Adicionalmente, el nivel tiene como objetivo que el usuario entienda la estructura organizacional de datos en formato tabular, comprendiendo cómo las filas representan registros individuales y las columnas representan tipos de información específica. El usuario debe reconocer las capacidades básicas de análisis de datos, incluyendo la capacidad de descubrir tendencias, hacer comparaciones, encontrar patrones y tomar decisiones basadas en datos. Finalmente, se busca que el usuario pueda diferenciar entre datos limpios y datos con problemas de calidad, comprendiendo el impacto que la calidad de datos tiene en la efectividad del análisis.

### 2.3 Componentes del Nivel

El Nivel 0 está estructurado mediante una serie de componentes pedagógicos interconectados que guían al usuario a través de una experiencia de aprendizaje progresiva. La sección de introducción establece el contexto del nivel, presentando el título y descripción, junto con una barra de progreso general del sistema que permite al usuario visualizar su avance en el curso completo. Se incluye un resumen de progresión del usuario y una vista previa del nivel actual que ayuda a establecer expectativas claras sobre lo que se aprenderá.

La sección de objetivos de aprendizaje proporciona una descripción detallada de los contenidos que el usuario dominará, estableciendo conexión con el caso de uso práctico de TechStore. Esta narrativa contextual ayuda al usuario a entender la relevancia práctica de los conceptos que está aprendiendo, transformando conceptos abstractos en aplicaciones concretas.

El contenido principal del nivel se presenta mediante cinco tarjetas de conceptos (step cards) que cubren los fundamentos del análisis de datos. La primera tarjeta aborda la pregunta fundamental "¿Qué son los datos?", proporcionando una definición conceptual amplia acompañada de ejemplos de datos en la vida real que incluyen contextos familiares como tiendas, restaurantes, teléfonos móviles y datos climáticos. Esta aproximación ayuda al usuario a reconocer que los datos están presentes en todos los aspectos de la vida cotidiana, no solo en contextos técnicos.

La segunda tarjeta explora los tipos de datos que existen, presentando una taxonomía completa que va desde los tipos más básicos (numéricos, texto, fecha/hora, booleanos) hasta tipos especiales como datos geográficos, imágenes, audio/video y datos de sensores IoT. Esta clasificación ayuda al usuario a desarrollar un vocabulario técnico básico mientras comprende la diversidad de información que puede ser analizada.

La tercera tarjeta responde a la pregunta "¿Qué puedes hacer con los datos?", explorando las capacidades fundamentales del análisis de datos. Se explica cómo los datos permiten descubrir tendencias, hacer comparaciones entre diferentes períodos o categorías, encontrar patrones que no son evidentes a simple vista, y tomar decisiones informadas basadas en evidencia en lugar de intuición.

La cuarta tarjeta aborda "¿Cómo se ven los datos organizados?", introduciendo la estructura tabular que es fundamental en el análisis de datos. Se explica cómo las tablas organizan la información mediante filas (que representan registros individuales) y columnas (que representan tipos de información), utilizando ejemplos prácticos de tablas de ventas que el usuario puede visualizar y comprender inmediatamente.

La quinta y última tarjeta conceptual explora "¿Qué es el análisis de datos?", presentando el proceso completo de análisis desde la formulación de preguntas hasta la comunicación de resultados. Se explica el ciclo de análisis que incluye preguntar, recopilar, limpiar, explorar, analizar y comunicar, estableciendo un marco conceptual que el usuario utilizará en todos los niveles subsecuentes.

La sección de demostración visual incorpora GIFs animados explicativos que complementan el contenido textual, proporcionando representaciones visuales de los conceptos clave. En caso de que los recursos visuales no estén disponibles, se proporciona información descriptiva que mantiene la efectividad pedagógica del nivel.

La sección de ejemplo práctico presenta el dataset TechStore en su versión limpia, permitiendo al usuario ver una implementación concreta de los conceptos aprendidos. Esta sección incluye la identificación de tipos de datos en el dataset real, explicación de las posibilidades de análisis que estos datos permiten, y una comparación detallada entre datos limpios y datos con problemas de calidad. Esta comparación es particularmente importante ya que establece desde el inicio la importancia de la calidad de datos, mostrando métricas específicas que demuestran cómo los problemas de calidad afectan la confiabilidad del análisis.

La sección interactiva permite al usuario explorar activamente el dataset mediante controles que permiten filtrar datos por categoría y visualizar estadísticas básicas. Esta exploración interactiva transforma el aprendizaje pasivo en una experiencia activa donde el usuario puede experimentar directamente con los conceptos aprendidos.

Las secciones de consejos y actividad práctica proporcionan orientación adicional, identificando errores comunes que los usuarios deben evitar y estableciendo buenas prácticas para trabajar con datos. Los ejercicios prácticos guiados permiten al usuario aplicar los conceptos aprendidos mediante la identificación de tipos de datos, comparación de calidad de datos, y formulación de preguntas sobre los datos que pueden ser respondidas mediante análisis.

### 2.4 Sistema de Evaluación y Progreso

El sistema de evaluación del Nivel 0 implementa un quiz compuesto por cinco preguntas de opción múltiple que cubren los conceptos fundamentales presentados en el nivel. Las preguntas evalúan la comprensión de la definición de datos, los tipos principales de datos, la estructura de tablas (específicamente la distinción entre filas y columnas), y el concepto general de análisis de datos. El sistema requiere que el usuario apruebe el quiz con un mínimo del 60% de respuestas correctas (3 de 5 preguntas) antes de poder marcar el nivel como completado. Cada pregunta incluye retroalimentación explicativa que no solo indica si la respuesta es correcta o incorrecta, sino que proporciona una explicación detallada que refuerza el aprendizaje.

El sistema de progreso implementa una barra de progreso general que muestra el avance del usuario a través de todos los niveles (0-100%), junto con un contador de niveles completados. Se incluye un sistema de logros y badges visuales que proporcionan retroalimentación positiva y motivación adicional. La verificación de completación se realiza mediante un checkbox que el usuario debe marcar después de aprobar el quiz, y todo el progreso se guarda persistentemente en la base de datos. Tras completar el nivel, el usuario es redirigido a una encuesta específica del nivel que permite recopilar retroalimentación sobre la experiencia de aprendizaje.

### 2.5 Dataset Utilizado

El Nivel 0 utiliza el dataset TechStore en su versión limpia (clean), que consiste en datos de ventas de una tienda de tecnología ficticia. Este dataset está específicamente diseñado para ejemplificar conceptos básicos con datos bien organizados y estructurados. Las columnas principales incluyen Fecha, Producto, Categoría, Cantidad, Ventas, Región y Calificación, proporcionando una variedad de tipos de datos que permiten al usuario ver ejemplos concretos de datos numéricos, de texto, de fecha y categóricos. El propósito de utilizar datos limpios en este nivel inicial es permitir que el usuario se enfoque en comprender los conceptos fundamentales sin distracciones causadas por problemas de calidad de datos, que serán introducidos en el Nivel 1.

### 2.6 Metodología Pedagógica

El Nivel 0 utiliza una aproximación pedagógica constructivista que presenta conceptos abstractos seguidos de ejemplos concretos y aplicaciones prácticas. La metodología sigue una secuencia lógica que va desde la explicación teórica, pasando por ejemplos visuales, hasta la práctica interactiva y finalmente la evaluación. Esta progresión permite al usuario construir su comprensión de manera gradual, conectando conceptos abstractos con experiencias concretas.

Una característica distintiva de la metodología es la comparación explícita entre datos limpios y datos problemáticos, que se presenta tanto en el contenido teórico como en los ejemplos prácticos. Esta comparación ayuda al usuario a desarrollar una comprensión temprana de la importancia de la calidad de datos, estableciendo una base para los niveles subsecuentes donde se abordará la limpieza de datos de manera más detallada.

El uso de una narrativa contextual unificada (el caso TechStore) proporciona continuidad y contexto que facilita la comprensión. En lugar de presentar ejemplos aislados, todos los ejemplos están conectados a un caso de uso coherente que el usuario puede seguir a lo largo de todo el curso, facilitando la retención y aplicación de los conceptos aprendidos.

### 2.7 Requisitos de Acceso

El Nivel 0 es el nivel inicial del sistema y, por lo tanto, no requiere la completación de niveles previos. Sin embargo, el acceso está restringido a usuarios autenticados en el sistema, garantizando que cada usuario tenga una sesión individual donde su progreso puede ser rastreado y guardado. Esta autenticación también permite personalizar la experiencia de aprendizaje según el progreso individual del usuario.

---

## 3. Nivel 1: Básico - Preparación y Carga de Datos

### 3.1 Descripción General

El Nivel 1 representa la transición del usuario desde la comprensión conceptual de los datos hacia la aplicación práctica de esos conceptos en contextos reales de trabajo. Este nivel introduce los aspectos técnicos fundamentales de preparación y carga de datos, enseñando los procedimientos necesarios para trabajar efectivamente con archivos de datos en herramientas de análisis. El nivel está diseñado para que el usuario adquiera competencias prácticas inmediatamente aplicables, estableciendo las bases técnicas que permitirán el trabajo efectivo con datos en los niveles subsecuentes.

Una característica distintiva del Nivel 1 es su enfoque en la calidad de datos, presentando al usuario por primera vez con datos que contienen problemas reales que deben ser identificados y comprendidos. Mientras que el Nivel 0 utilizó datos limpios para facilitar la comprensión conceptual, el Nivel 1 utiliza el dataset TechStore en su versión "dirty" (con problemas), permitiendo al usuario experimentar directamente con los desafíos que presenta trabajar con datos del mundo real. Esta experiencia práctica es fundamental para desarrollar la capacidad crítica de identificar problemas de calidad de datos antes de proceder con el análisis.

El nivel está estructurado como una guía práctica paso a paso que lleva al usuario desde la selección del formato de archivo apropiado hasta la verificación completa de que los datos se han cargado correctamente. Cada paso está diseñado para construir sobre el anterior, creando una secuencia lógica de aprendizaje que culmina con la capacidad del usuario de cargar y verificar sus propios archivos de datos mediante la funcionalidad interactiva de carga de archivos incluida en el nivel.

### 3.2 Objetivos de Aprendizaje

Los objetivos de aprendizaje del Nivel 1 están orientados hacia el desarrollo de competencias prácticas. El usuario debe ser capaz de seleccionar el formato de archivo apropiado para diferentes tipos de datos, comprendiendo las ventajas y limitaciones de formatos como CSV, Excel y JSON, y reconociendo qué formatos son adecuados para diferentes contextos de análisis. Se busca que el usuario pueda preparar la estructura de datos siguiendo mejores prácticas, entendiendo principios fundamentales como que una fila debe representar un registro individual y una columna debe representar un tipo de información específica.

El usuario debe desarrollar la capacidad de cargar archivos de datos en la plataforma utilizando diferentes métodos (arrastrar y soltar, explorador de archivos, o carga desde URL), y más importante aún, debe ser capaz de verificar la integridad y calidad de los datos cargados. Esta verificación incluye la identificación de problemas comunes como datos faltantes, formatos incorrectos, duplicados y valores atípicos. Finalmente, el usuario debe ser capaz de comprender la estructura y tipos de datos de un dataset cargado, interpretando información técnica como el número de filas y columnas, los tipos de datos en cada columna, y los valores únicos presentes.

### 3.3 Componentes del Nivel

El Nivel 1 está estructurado mediante componentes pedagógicos que combinan instrucción teórica con práctica activa. La sección de introducción establece el contexto del nivel, presentando el título y descripción junto con elementos de seguimiento del progreso que incluyen la barra de progreso general, resumen de progresión, y reconocimiento del logro del nivel anterior si ha sido completado. Se incluye una vista previa del nivel actual y una conexión explícita con el Nivel 0, ayudando al usuario a entender cómo los conceptos fundamentales aprendidos anteriormente se aplican ahora en contextos prácticos.

La sección de objetivos de aprendizaje proporciona una descripción detallada de los contenidos que serán dominados, estableciendo expectativas claras y conectando los nuevos aprendizajes con los conocimientos previos. Esta conexión es particularmente importante ya que el usuario ahora aplicará los conceptos de tipos de datos y estructura tabular aprendidos en el Nivel 0 a situaciones prácticas de preparación y carga de archivos.

El contenido principal se presenta mediante cinco tarjetas de pasos prácticos que guían al usuario a través del proceso completo de preparación y carga de datos. La primera tarjeta aborda la selección del formato de archivo correcto, presentando formatos recomendados como CSV (para datos simples y máxima compatibilidad), Excel (para datos con formato y múltiples hojas), y JSON (para estructuras complejas). Se explican los criterios de selección y se identifican formatos a evitar como PDF, imágenes y documentos Word que no están diseñados para análisis tabular.

La segunda tarjeta se enfoca en la preparación correcta de la estructura de datos, estableciendo reglas fundamentales de organización que incluyen el principio de que una fila debe representar un registro individual y una columna debe representar un tipo de información específica. Se proporcionan ejemplos contrastantes de estructuras correctas e incorrectas, y se enfatiza la importancia de encabezados claros y descriptivos que faciliten el análisis posterior.

La tercera tarjeta detalla el proceso de carga de archivos en la herramienta, explicando paso a paso cómo realizar la carga mediante diferentes métodos disponibles. Se cubren opciones como arrastrar y soltar, uso del explorador de archivos, y carga desde URL, junto con identificación de problemas comunes que pueden surgir durante el proceso de carga como archivos muy grandes, formatos no soportados, o archivos corruptos.

La cuarta tarjeta se centra en la verificación de que los datos se cargaron correctamente, proporcionando un checklist comprehensivo de verificación que incluye revisar que todos los datos sean visibles, que las fechas tengan el formato correcto, que no haya datos extraños o símbolos raros, y que el conteo de filas y columnas coincida con lo esperado. Se explica qué buscar específicamente, incluyendo datos faltantes, formato incorrecto, duplicados y valores atípicos, y se identifican señales claras de que la carga fue exitosa.

La quinta y última tarjeta ayuda al usuario a entender la estructura de los datos cargados, explicando qué información básica debe revisar como el número de filas y columnas, los tipos de datos presentes, y los valores únicos en cada columna. Se proporciona guía sobre cómo interpretar esta información y se sugieren preguntas útiles que el usuario debe hacerse para asegurar que comprende completamente su dataset.

La sección de demostración visual incorpora un GIF animado que muestra el proceso completo de preparación y carga de un archivo CSV, proporcionando una representación visual del flujo de trabajo que complementa las explicaciones textuales.

La sección de ejemplo práctico presenta el dataset TechStore en su versión "dirty", permitiendo al usuario ver directamente los problemas de calidad que pueden existir en datos reales. Esta sección incluye análisis detallado de la estructura de datos, comparación explícita entre datos sin procesar y datos limpios, identificación sistemática de problemas de calidad, y métricas que demuestran el impacto de la limpieza de datos en la confiabilidad del análisis.

La sección de carga de archivos es una característica distintiva del nivel, proporcionando un componente interactivo completo que permite al usuario cargar sus propios archivos de datos. Este componente soporta formatos CSV y Excel (.xlsx, .xls), realiza análisis automático de los datos cargados, y presenta visualización comprehensiva de información técnica del dataset incluyendo detalles por columna (tipo de datos, valores no nulos, valores faltantes) y estadísticas descriptivas. Esta funcionalidad práctica permite al usuario aplicar inmediatamente los conceptos aprendidos con sus propios datos.

Las secciones de consejos y actividad práctica proporcionan orientación adicional, identificando errores comunes que los usuarios deben evitar al preparar datos y estableciendo buenas prácticas para la preparación efectiva de datos. Los ejercicios prácticos guiados permiten al usuario practicar la preparación de archivos y la carga y verificación de datos en un entorno controlado.

### 3.4 Sistema de Evaluación y Progreso

El sistema de evaluación implementa un quiz de cinco preguntas de opción múltiple que cubre los aspectos prácticos presentados en el nivel, incluyendo formatos de archivo comunes, estructura de archivos CSV, proceso de carga, verificación de datos, y tipos de datos en columnas. El sistema requiere aprobación con mínimo 60% antes de permitir la completación del nivel. El sistema de progreso verifica la completación del Nivel 0 como prerrequisito, implementa seguimiento del progreso general, sistema de logros, y guardado persistente del progreso.

### 3.5 Dataset Utilizado

El Nivel 1 utiliza el dataset TechStore en su versión "dirty" (sin procesar), que contiene problemas de calidad intencionalmente incluidos para fines educativos. Estos problemas incluyen valores faltantes, inconsistencias en nombres y formatos, filas duplicadas, y valores atípicos. El propósito de utilizar datos problemáticos es enseñar al usuario a identificar y comprender estos problemas antes de que se aborden técnicas de limpieza en niveles posteriores. Esta experiencia práctica es fundamental para desarrollar la capacidad crítica de evaluar la calidad de datos.

### 3.6 Metodología Pedagógica

El Nivel 1 combina instrucción directa con práctica activa, siguiendo una secuencia que va desde la explicación de procedimientos, pasando por demostración visual, hasta la práctica con datos propios y finalmente la verificación. La comparación explícita entre datos problemáticos y limpios ayuda al usuario a desarrollar una comprensión clara de cómo los problemas de calidad afectan el análisis. El componente interactivo de carga de archivos reales transforma el aprendizaje teórico en experiencia práctica inmediata, permitiendo al usuario aplicar los conceptos aprendidos con sus propios datos.

### 3.7 Requisitos de Acceso

El acceso al Nivel 1 requiere que el usuario esté autenticado en el sistema y haya completado el Nivel 0. Esta verificación de prerrequisitos garantiza que el usuario tenga la base conceptual necesaria antes de abordar los aspectos prácticos de preparación y carga de datos.

---

## 4. Nivel 2: Filtros - Organización y Segmentación de Datos

### 4.1 Descripción General

El Nivel 2 marca una transición importante en el aprendizaje del usuario, moviéndose desde la preparación y carga de datos hacia la exploración activa y segmentación de información. Este nivel introduce al usuario en el uso sistemático de filtros como herramienta fundamental para encontrar información específica dentro de un dataset, enseñando diferentes tipos de filtros y las estrategias para combinarlos efectivamente en análisis más precisos y dirigidos.

El nivel está diseñado bajo el principio de que los datos, por sí solos, contienen demasiada información para ser analizados efectivamente sin herramientas de segmentación. Los filtros permiten al usuario enfocarse en subconjuntos específicos de datos que son relevantes para preguntas particulares, transformando un dataset completo en vistas focalizadas que facilitan el análisis. Esta capacidad de segmentación es fundamental para cualquier análisis de datos efectivo, ya que permite al usuario responder preguntas específicas sin distraerse con información irrelevante.

Una característica distintiva del Nivel 2 es su enfoque en la interactividad y el feedback inmediato. El nivel incluye un panel completo de filtros interactivos que permite al usuario experimentar en tiempo real con diferentes combinaciones de filtros, observando cómo cada filtro afecta los resultados y las métricas calculadas. Esta experiencia práctica es esencial para desarrollar la intuición sobre cómo los filtros funcionan y cómo deben ser aplicados estratégicamente.

El nivel utiliza el dataset TechStore en su versión limpia, permitiendo que el usuario se enfoque completamente en aprender a filtrar sin distracciones causadas por problemas de calidad de datos. Esta elección pedagógica es intencional, ya que permite al usuario desarrollar competencia en el uso de filtros antes de enfrentar los desafíos adicionales de trabajar con datos problemáticos.

### 4.2 Objetivos de Aprendizaje

Los objetivos de aprendizaje del Nivel 2 están orientados hacia el desarrollo de competencias en segmentación y organización de datos. El usuario debe ser capaz de aplicar filtros de fecha para analizar períodos específicos, comprendiendo cómo seleccionar rangos de fechas, períodos específicos, o fechas únicas según las necesidades del análisis. Debe desarrollar la capacidad de filtrar datos por categorías y regiones, reconociendo cómo estos filtros categóricos permiten enfocarse en segmentos específicos del negocio o mercado.

El usuario debe aprender a utilizar filtros numéricos mediante deslizadores interactivos, estableciendo rangos de valores para variables numéricas como precios, ventas, o calificaciones. Más importante aún, debe desarrollar la capacidad de combinar múltiples filtros simultáneamente para realizar análisis detallados y específicos, entendiendo cómo diferentes combinaciones de filtros permiten responder preguntas complejas sobre los datos.

Finalmente, el usuario debe comprender profundamente cómo los filtros afectan las métricas calculadas, reconociendo que cuando se aplican filtros, todas las métricas (totales, promedios, conteos) se recalculan para reflejar solo los datos filtrados, mientras que los datos originales permanecen intactos. Esta comprensión es fundamental para interpretar correctamente los resultados de análisis filtrados.

### 4.3 Componentes del Nivel

El Nivel 2 está estructurado mediante componentes pedagógicos que enfatizan la práctica interactiva y el aprendizaje activo. La sección de introducción establece el contexto del nivel, presentando el título y descripción junto con elementos de seguimiento del progreso, reconocimiento del logro del nivel anterior, y una vista previa del nivel actual que conecta explícitamente con el Nivel 1, ayudando al usuario a entender cómo la preparación de datos aprendida anteriormente ahora se aplica en la exploración y segmentación.

La sección de objetivos de aprendizaje proporciona una descripción detallada de los contenidos, estableciendo conexión con los niveles anteriores y explicando cómo los conceptos de estructura de datos y tipos de datos ahora se aplican en la práctica de filtrado.

El contenido principal se presenta mediante cinco tarjetas de conceptos de filtrado que progresan desde filtros simples hasta combinaciones complejas. La primera tarjeta aborda el uso de filtros de fecha, explicando los diferentes tipos disponibles incluyendo rangos de fechas (desde una fecha hasta otra), períodos específicos (último mes, este año), y fechas únicas. Se proporcionan ejemplos prácticos de uso como analizar ventas del último trimestre o comparar resultados entre dos meses.

La segunda tarjeta explora el filtrado por categorías y regiones, explicando cómo los filtros categóricos permiten enfocarse en segmentos específicos. Se cubren filtros por categoría de productos, servicios, o tipos de cliente, así como filtros por región que pueden incluir países, estados, ciudades, o zonas geográficas. Esta tarjeta ayuda al usuario a entender cómo los filtros categóricos son fundamentales para análisis comparativos.

La tercera tarjeta introduce los filtros numéricos mediante deslizadores interactivos, explicando cómo establecer rangos de valores para variables numéricas. Se cubren diferentes tipos de filtros numéricos como rangos de precios, ventas mínimas, calificaciones, o cualquier otra variable numérica. Se explica el uso práctico de deslizadores, incluyendo cómo mover los controles para establecer valores mínimos y máximos, y cómo los resultados se actualizan automáticamente.

La cuarta tarjeta se enfoca en la combinación de múltiples filtros, proporcionando ejemplos prácticos de combinaciones efectivas como fecha más categoría (para analizar ventas de electrónicos en diciembre), región más precio (para identificar productos caros en el norte), o combinaciones más complejas que incluyen tres o más filtros simultáneamente. Se proporcionan consejos estratégicos sobre cómo combinar filtros efectivamente, incluyendo la importancia de empezar con un filtro y agregar más gradualmente, y cómo verificar que no se esté filtrando demasiado (resultando en muy pocos datos).

La quinta y última tarjeta aborda el impacto de los filtros en las métricas, explicando cómo cuando se aplican filtros, todas las métricas se recalculan para reflejar solo los datos filtrados. Se explica que los totales solo suman los productos filtrados, los promedios solo consideran los valores visibles, y los conteos solo incluyen los registros filtrados. Se enfatiza la importancia crítica de recordar que los filtros no cambian los datos originales, que siempre se pueden quitar para ver todo nuevamente, y que los filtros se aplican en tiempo real.

La sección de demostración visual incorpora un GIF animado que muestra el proceso completo de aplicación de filtros, proporcionando una representación visual del flujo de trabajo que complementa las explicaciones textuales.

La sección de ejemplo práctico interactivo es el componente central del nivel, proporcionando un panel completo de filtros interactivos que permite al usuario experimentar directamente con todos los tipos de filtros aprendidos. El panel incluye un filtro de fecha con selector de rango que permite seleccionar fechas de inicio y fin, un filtro por categoría mediante selectbox que permite elegir una categoría específica o ver todas, un filtro por región también mediante selectbox, y filtros numéricos mediante sliders para ventas y calificación que permiten establecer rangos de valores.

Esta sección interactiva muestra visualmente los resultados filtrados, actualizando automáticamente las métricas según los filtros aplicados, y presentando una tabla de datos filtrados que el usuario puede examinar. Esta experiencia práctica es fundamental ya que permite al usuario ver inmediatamente el impacto de cada filtro y cada combinación de filtros, desarrollando intuición práctica sobre cómo usar los filtros efectivamente.

Las secciones de consejos y actividad práctica proporcionan orientación adicional, identificando errores comunes como usar filtros muy restrictivos que resultan en pocos o ningún resultado, olvidar quitar filtros cuando se cambia de análisis, o usar filtros contradictorios. Se establecen buenas prácticas como planificar el análisis antes de filtrar, usar filtros gradualmente, verificar que los resultados sean los esperados, y documentar qué filtros se usaron para poder repetir el análisis.

### 4.4 Sistema de Evaluación y Progreso

El sistema de evaluación implementa un quiz de cinco preguntas que cubre los conceptos de filtrado presentados, incluyendo tipos de filtros disponibles, uso de filtros de fecha, combinación de filtros, y efecto de filtros en métricas. El sistema requiere aprobación con mínimo 60% antes de permitir la completación del nivel. El sistema de progreso verifica la completación del Nivel 1 como prerrequisito, implementa seguimiento del progreso general, sistema de logros, y guardado persistente del progreso.

### 4.5 Dataset Utilizado

El Nivel 2 utiliza el dataset TechStore en su versión limpia (clean), que consiste en datos preparados y consistentes sin problemas de calidad. Esta elección permite que el usuario se enfoque completamente en aprender a filtrar sin distracciones causadas por problemas de datos. Los datos están completos y consistentes, proporcionando una base sólida para el análisis de filtrado y permitiendo que el usuario experimente con todos los tipos de filtros sin preocuparse por problemas de calidad que interfieran con el aprendizaje.

### 4.6 Metodología Pedagógica

El Nivel 2 utiliza una metodología de aprendizaje activo mediante práctica interactiva intensiva. La secuencia pedagógica sigue un flujo que va desde la explicación de conceptos, pasando por demostración visual, hasta la práctica interactiva con controles reales y finalmente la observación de resultados. El feedback inmediato al aplicar filtros es una característica distintiva, permitiendo al usuario ver instantáneamente cómo cada acción afecta los resultados. La visualización en tiempo real de cambios en métricas ayuda al usuario a desarrollar una comprensión intuitiva de cómo los filtros funcionan y cómo deben ser aplicados estratégicamente.

### 4.7 Requisitos de Acceso

El acceso al Nivel 2 requiere que el usuario esté autenticado en el sistema y haya completado el Nivel 1. Esta verificación de prerrequisitos garantiza que el usuario tenga la base práctica necesaria (preparación y carga de datos) antes de abordar la segmentación y organización de datos mediante filtros.

---

## 5. Nivel 3: Métricas - KPIs y Análisis de Rendimiento

### 5.1 Descripción General

El Nivel 3 representa un punto de inflexión en el aprendizaje del usuario, moviéndose desde la manipulación técnica de datos hacia la extracción de significado y valor de negocio. Este nivel introduce al usuario en el concepto fundamental de métricas e indicadores clave de rendimiento (KPIs), enseñando no solo cómo calcular estas métricas, sino más importante aún, cómo interpretarlas y utilizarlas para tomar decisiones informadas basadas en datos.

El nivel está diseñado bajo la premisa de que los datos, por sí solos, no proporcionan valor hasta que se transforman en métricas que pueden ser interpretadas y utilizadas para la toma de decisiones. El usuario ha aprendido en niveles anteriores a preparar datos, cargarlos, y filtrarlos, pero ahora debe aprender a extraer significado de esos datos mediante el cálculo y análisis de métricas que respondan a preguntas de negocio específicas.

Una característica distintiva del Nivel 3 es su enfoque en la integración de conocimientos previos. El nivel conecta explícitamente con conceptos de todos los niveles anteriores: utiliza los tipos de datos aprendidos en el Nivel 0, aplica la preparación de datos del Nivel 1, y utiliza los filtros del Nivel 2 para calcular métricas segmentadas. Esta integración ayuda al usuario a ver cómo todos los conceptos aprendidos se combinan para crear análisis significativos.

El nivel también introduce al usuario en el análisis agregado, enseñando cómo agrupar datos por categorías y regiones para calcular métricas comparativas. Esta capacidad de análisis comparativo es fundamental para identificar patrones, tendencias y oportunidades de mejora en cualquier contexto de negocio.

### 5.2 Objetivos de Aprendizaje

Los objetivos de aprendizaje del Nivel 3 están orientados hacia el desarrollo de competencias en cálculo, interpretación y aplicación de métricas. El usuario debe ser capaz de comprender qué son las métricas y KPIs, reconociendo que las métricas son números que proporcionan información importante sobre el estado de un negocio o actividad, y que los KPIs son las métricas más críticas que indican si se están alcanzando los objetivos.

El usuario debe desarrollar la capacidad de identificar métricas clave para diferentes tipos de negocio, comprendiendo que no todas las métricas son igualmente importantes y que la selección de métricas relevantes depende del contexto y objetivos específicos. Debe aprender a interpretar y analizar métricas, no solo viendo los números sino entendiendo qué significan, cómo se relacionan entre sí, y qué implicaciones tienen para el negocio.

Más importante aún, el usuario debe desarrollar la capacidad de utilizar métricas para la toma de decisiones, comprendiendo el proceso de decisión basada en datos que incluye revisar métricas regularmente, identificar problemas o oportunidades, generar hipótesis, tomar acción, y medir resultados. Finalmente, debe ser capaz de calcular métricas básicas como totales, promedios y conteos, y realizar análisis por categorías y regiones para identificar patrones y comparaciones.

### 5.3 Componentes del Nivel

El Nivel 3 está estructurado mediante componentes pedagógicos que integran teoría y práctica de manera cohesiva. La sección de introducción establece el contexto del nivel, presentando el título y descripción junto con elementos de seguimiento del progreso, reconocimiento del logro del nivel anterior, y una vista previa del nivel actual. Se incluye una conexión explícita con todos los niveles anteriores, ayudando al usuario a entender cómo los conceptos fundamentales, la preparación de datos, y los filtros ahora se combinan en el cálculo de métricas.

La sección de objetivos de aprendizaje proporciona una descripción detallada de los contenidos, estableciendo el contexto de integración de conocimientos previos y explicando cómo este nivel representa la culminación de los aprendizajes anteriores en la capacidad de extraer significado de los datos.

El contenido principal se presenta mediante cuatro tarjetas de conceptos de métricas que progresan desde la comprensión básica hasta la aplicación práctica. La primera tarjeta aborda la pregunta fundamental "¿Qué son las métricas y KPIs?", proporcionando una definición comprehensiva que explica que las métricas son números que miden algo importante, y que los KPIs son las métricas más críticas. Se presentan diferentes tipos de métricas incluyendo métricas de cantidad (cuántos productos, cuántos clientes), métricas de dinero (cuánto se ganó, cuánto se gastó), métricas de tiempo (cuánto tiempo se tarda), y métricas de calidad (qué tan bien funciona algo). Se proporcionan ejemplos concretos de KPIs comunes como ventas totales, número de clientes, satisfacción del cliente, y tiempo de entrega.

La segunda tarjeta se enfoca en identificar métricas clave para diferentes tipos de negocio, explicando el proceso de identificación que incluye preguntarse qué se quiere lograr, identificar qué números indicarán si se está logrando, elegir 3-5 métricas principales para enfocarse, y evitar medir todo. Se proporcionan ejemplos específicos por tipo de negocio: para una tienda online las métricas clave incluyen ventas, visitantes y tasa de conversión; para servicios de consultoría incluyen horas facturables, satisfacción del cliente y proyectos completados; para un restaurante incluyen ventas por mesa, tiempo de espera y calificaciones de clientes.

La tercera tarjeta aborda la interpretación y análisis de métricas, explicando que interpretar métricas significa no solo ver los números sino entender qué están diciendo y qué acciones tomar. Se presentan diferentes tipos de análisis incluyendo análisis de tendencias (¿los números van subiendo o bajando?), comparaciones (¿cómo se comparan con períodos anteriores?), análisis de patrones (¿hay patrones que se repiten?), y análisis de correlación (¿cuando una cosa sube, otra también sube?). Se proporcionan preguntas clave para interpretar métricas como si el número es bueno o malo, por qué cambió, qué se puede hacer para mejorarlo, y qué consecuencias tiene el cambio.

La cuarta y última tarjeta se centra en usar métricas para tomar decisiones, explicando que las métricas no son solo para ver sino para actuar. Se presenta el proceso de decisión basada en datos que incluye revisar métricas regularmente, identificar problemas o oportunidades, generar hipótesis sobre qué está pasando, tomar acción basada en los datos, y medir el resultado de las acciones. Se identifican errores comunes a evitar como enfocarse solo en una métrica, no considerar el contexto, tomar decisiones sin entender la causa, e ignorar tendencias a largo plazo.

La sección de ejemplo práctico presenta el dataset TechStore limpio y recuerda al usuario los tipos de datos aprendidos en el Nivel 0, estableciendo conexión explícita con los fundamentos conceptuales.

La sección de cálculo de métricas básicas presenta el cálculo práctico de métricas principales incluyendo ventas totales (suma de todas las ventas), promedio de ventas (promedio de las ventas individuales), cantidad total (suma de todas las cantidades vendidas), y calificación promedio (promedio de las calificaciones de productos). Estas métricas se visualizan mediante componentes de métricas de Streamlit que presentan los valores de manera clara y destacada.

La sección de análisis por categoría introduce al usuario en el análisis agregado, mostrando cómo agrupar datos por categoría y calcular ventas totales por cada categoría. Los resultados se visualizan mediante un gráfico de barras que permite comparar visualmente las ventas entre diferentes categorías, y se presenta una tabla de resultados que proporciona los valores exactos.

La sección de análisis por región aplica el mismo concepto de análisis agregado pero agrupando por región geográfica, permitiendo al usuario identificar qué regiones tienen mejor o peor rendimiento. Nuevamente se utiliza visualización mediante gráfico de barras y tabla de resultados para presentar la información de manera clara.

La sección de práctica interactiva permite al usuario aplicar los conceptos aprendidos mediante filtros interactivos que permiten seleccionar categoría y región específicas. El sistema calcula automáticamente las métricas filtradas, mostrando cómo los filtros aprendidos en el Nivel 2 se combinan con el cálculo de métricas. Se incluyen visualizaciones de datos filtrados, gráficos de tendencias temporales que muestran cómo las ventas cambian con el tiempo, y gráficos por categoría que permiten análisis comparativos más detallados.

### 5.4 Sistema de Evaluación y Progreso

El sistema de evaluación implementa un quiz de cinco preguntas que cubre los conceptos de métricas presentados, incluyendo definición de métricas y KPIs, identificación de métricas clave, interpretación de métricas, y uso de métricas para decisiones. El sistema requiere aprobación con mínimo 60% antes de permitir la completación del nivel. El sistema de progreso verifica la completación de los Niveles 1 y 2 como prerrequisitos, implementa seguimiento del progreso general, sistema de logros, y guardado persistente del progreso.

### 5.5 Dataset Utilizado

El Nivel 3 utiliza el dataset TechStore en su versión limpia (clean), que consiste en datos preparados y consistentes sin problemas de calidad. Esta elección permite que el usuario se enfoque completamente en aprender a calcular e interpretar métricas sin distracciones causadas por problemas de datos. Los datos están completos y consistentes, proporcionando una base sólida para el análisis agregado y el cálculo de KPIs que requiere datos de calidad para producir resultados confiables.

### 5.6 Metodología Pedagógica

El Nivel 3 integra conceptos teóricos con cálculo práctico mediante una secuencia pedagógica que va desde la definición conceptual, pasando por ejemplos, hasta el cálculo práctico y finalmente la interpretación. La conexión explícita con conceptos de niveles anteriores ayuda al usuario a ver cómo todos los aprendizajes se integran en el análisis de métricas. La práctica interactiva con filtros y métricas permite al usuario experimentar directamente cómo los filtros afectan las métricas calculadas, desarrollando una comprensión práctica de la relación entre segmentación de datos y cálculo de métricas.

### 5.7 Requisitos de Acceso

El acceso al Nivel 3 requiere que el usuario esté autenticado en el sistema y haya completado los Niveles 1 y 2. Esta verificación de prerrequisitos garantiza que el usuario tenga la base práctica necesaria (preparación y carga de datos, y uso de filtros) antes de abordar el cálculo e interpretación de métricas.

---

## 6. Nivel 4: Avanzado - Cálculos y Visualizaciones Avanzadas

### 6.1 Descripción General

El Nivel 4 constituye la culminación del sistema de aprendizaje, representando el nivel más avanzado donde todos los conocimientos previos se integran para capacitar al usuario en la creación de análisis profesionales completos. Este nivel enseña cálculos personalizados avanzados que van más allá de las métricas básicas, visualizaciones interactivas complejas utilizando tecnologías modernas como Plotly, y la creación de dashboards profesionales que comunican insights de manera efectiva.

El nivel está diseñado bajo el principio de que el análisis de datos efectivo requiere no solo la capacidad de calcular métricas básicas, sino también la habilidad de crear métricas derivadas personalizadas que respondan a preguntas de negocio específicas. El usuario ha aprendido en niveles anteriores a trabajar con datos, filtrarlos, y calcular métricas básicas, pero ahora debe desarrollar la capacidad de crear sus propias fórmulas y cálculos que extraigan insights más profundos de los datos.

Una característica distintiva del Nivel 4 es su enfoque en la integración completa de todos los conceptos aprendidos. El nivel conecta explícitamente con todos los niveles anteriores, mostrando cómo los tipos de datos (Nivel 0), la preparación de datos (Nivel 1), los filtros (Nivel 2), y las métricas básicas (Nivel 3) se combinan para crear análisis avanzados y dashboards profesionales. Esta integración ayuda al usuario a ver el panorama completo de cómo todos los aprendizajes se unen en aplicaciones prácticas reales.

El nivel también introduce al usuario en técnicas avanzadas de visualización que van más allá de gráficos básicos, incluyendo visualizaciones interactivas con capacidades de zoom, tooltips, y selección, análisis de tendencias temporales con múltiples series, y análisis de correlaciones mediante matrices de calor. Estas técnicas avanzadas permiten al usuario crear visualizaciones que no solo muestran datos, sino que facilitan la exploración activa y el descubrimiento de insights.

Finalmente, el nivel culmina con la creación de dashboards profesionales completos, enseñando al usuario cómo combinar métricas, visualizaciones, y filtros en una presentación cohesiva que cuenta una historia con los datos. Esta capacidad de crear dashboards es fundamental para comunicar insights de manera efectiva a diferentes audiencias, transformando el análisis técnico en narrativas comprensibles y accionables.

### 6.2 Objetivos de Aprendizaje

Los objetivos de aprendizaje del Nivel 4 están orientados hacia el desarrollo de competencias avanzadas en análisis y comunicación de datos. El usuario debe ser capaz de crear cálculos personalizados avanzados incluyendo porcentajes (para entender proporciones), promedios ponderados (para dar más importancia a ciertos valores), cambios porcentuales (para medir crecimiento o declive), y ratios (para comparar diferentes métricas). Debe desarrollar la capacidad de generar visualizaciones interactivas utilizando Plotly, comprendiendo cómo crear gráficos que permitan exploración activa mediante zoom, tooltips informativos, filtros integrados, y selección de elementos.

El usuario debe ser capaz de crear dashboards profesionales con múltiples componentes, entendiendo cómo organizar métricas clave, visualizaciones, y filtros en un layout coherente y efectivo. Debe desarrollar la capacidad de interpretar y comunicar insights de datos, no solo encontrando descubrimientos importantes en los datos, sino también comunicándolos de manera efectiva mediante visualizaciones y narrativas claras.

Finalmente, el usuario debe ser capaz de realizar análisis de correlaciones para identificar relaciones entre variables, y crear análisis de tendencias temporales avanzados que muestren cómo múltiples métricas evolucionan con el tiempo. Estas capacidades avanzadas permiten al usuario realizar análisis más sofisticados que van más allá de métricas simples.

### 6.3 Componentes del Nivel

El Nivel 4 está estructurado mediante componentes pedagógicos que integran todos los conocimientos previos en aplicaciones avanzadas. La sección de introducción establece el contexto del nivel, presentando el título y descripción junto con elementos de seguimiento del progreso, reconocimiento del logro del nivel anterior, y una vista previa del nivel actual. Se incluye un resumen completo de la jornada de aprendizaje que recapitula todos los niveles anteriores, ayudando al usuario a ver cómo ha progresado desde conceptos fundamentales hasta técnicas avanzadas.

La sección de objetivos de aprendizaje proporciona una descripción detallada de los contenidos avanzados, estableciendo el contexto de integración de todos los conceptos previos y explicando cómo este nivel representa la aplicación práctica de todos los aprendizajes anteriores.

El contenido principal se presenta mediante cuatro tarjetas de conceptos avanzados que progresan desde cálculos personalizados hasta comunicación de insights. La primera tarjeta aborda la creación de cálculos personalizados avanzados, explicando diferentes tipos de cálculos que el usuario puede crear incluyendo porcentajes (para calcular qué parte del total representa algo), promedios ponderados (para promedios que dan más importancia a ciertos valores), cambios porcentuales (para medir cuánto aumentó o disminuyó algo), y ratios y proporciones (para comparaciones entre diferentes valores). Se proporcionan ejemplos concretos de fórmulas como margen de ganancia ((Precio de venta - Costo) / Precio de venta × 100), porcentaje de crecimiento ((Valor actual - Valor anterior) / Valor anterior × 100), y promedio ponderado (Suma de (Valor × Peso) / Suma de pesos).

La segunda tarjeta se enfoca en generar visualizaciones interactivas, explicando diferentes tipos de visualizaciones incluyendo gráficos de línea (para mostrar tendencias a lo largo del tiempo), gráficos de barras (para comparar categorías), gráficos de dispersión (para ver relaciones entre dos variables), y mapas de calor (para mostrar patrones en tablas de datos). Se explican las características interactivas que hacen estas visualizaciones poderosas, incluyendo zoom y panorámica para explorar detalles, tooltips que muestran información al pasar el mouse, filtros que permiten cambiar la vista de los datos, y selección de elementos para análisis específicos.

La tercera tarjeta aborda la creación de dashboards profesionales, explicando los elementos de un dashboard efectivo incluyendo métricas clave (KPIs) en la parte superior, visualizaciones que explican las métricas, filtros que permiten cambiar la vista de los datos, y navegación para moverse entre diferentes vistas. Se presentan principios de diseño que incluyen mantener el diseño limpio y sin distracciones, usar colores de manera consistente y significativa, organizar la información de más importante a menos importante, y asegurar que sea fácil de entender para la audiencia.

La cuarta y última tarjeta se centra en interpretar y comunicar insights, explicando cómo encontrar insights buscando patrones inesperados en los datos, comparando diferentes períodos o grupos, identificando valores atípicos o anomalías, y conectando diferentes métricas para ver el panorama completo. Se explica cómo comunicar insights efectivamente contando una historia con los datos, explicando qué significa cada insight para el negocio, sugiriendo acciones específicas basadas en los datos, y usando visualizaciones para respaldar las conclusiones.

La sección de ejemplo práctico presenta el dataset TechStore limpio y establece conexión explícita con todos los conceptos previos, mostrando cómo todos los aprendizajes se integran en un análisis avanzado completo.

La sección de cálculos avanzados presenta el cálculo práctico de métricas derivadas incluyendo margen de ganancia (calculado como porcentaje de ganancia sobre ventas), ingresos totales (calculado multiplicando ventas por cantidad), y eficiencia de ventas (calculada como ingresos totales dividido por cantidad). Estas métricas avanzadas se visualizan mediante componentes de métricas que presentan los valores de manera destacada, demostrando cómo los cálculos personalizados proporcionan insights más profundos que las métricas básicas.

La sección de visualizaciones interactivas es el componente central del nivel, proporcionando un conjunto completo de herramientas de visualización avanzada. Se incluyen filtros avanzados mediante sliders y multiselect que permiten al usuario controlar dinámicamente qué datos se visualizan. Los gráficos interactivos con Plotly incluyen un gráfico de barras por categoría con escala de colores que permite comparar visualmente las ventas entre categorías, y un gráfico de pastel por región que muestra la distribución de ventas geográficamente.

El análisis de tendencias temporales incluye subplots con múltiples series que muestran ventas diarias y margen de ganancia simultáneamente, permitiendo al usuario identificar relaciones temporales entre diferentes métricas. Los gráficos de línea interactivos permiten explorar tendencias con zoom y tooltips que proporcionan información detallada sobre puntos específicos.

El análisis de correlaciones presenta una matriz de correlación con mapa de calor que muestra las relaciones entre diferentes variables numéricas, permitiendo al usuario identificar qué métricas están relacionadas y en qué medida. Se proporciona interpretación de correlaciones explicando que valores cercanos a 1 indican correlación positiva fuerte, valores cercanos a -1 indican correlación negativa fuerte, y valores cercanos a 0 indican poca o ninguna correlación.

La sección de creación de dashboard personalizado permite al usuario aplicar todos los conceptos aprendidos mediante la configuración de un dashboard completo. El usuario puede seleccionar qué métricas mostrar, qué visualizaciones incluir, y el sistema genera dinámicamente un dashboard según la selección con un layout personalizado. Esta funcionalidad práctica permite al usuario crear su propio dashboard profesional aplicando todos los principios aprendidos.

Las secciones de consejos proporcionan orientación adicional, identificando errores comunes en análisis avanzado y estableciendo buenas prácticas para la creación de dashboards efectivos.

### 6.4 Sistema de Evaluación y Progreso

El sistema de evaluación implementa un quiz de cinco preguntas que cubre los conceptos avanzados presentados, incluyendo cálculos personalizados, visualizaciones interactivas, dashboards, y comunicación de insights. El sistema requiere aprobación con mínimo 60% antes de permitir la completación del nivel. El sistema de progreso verifica la completación de los Niveles 1, 2 y 3 como prerrequisitos, implementa seguimiento del progreso general, sistema de logros finales, y guardado persistente del progreso. Tras completar el nivel, el usuario tiene acceso a opciones post-completación incluyendo encuesta del nivel 4, encuesta final del curso, y acceso al Dashboard en Blanco donde puede crear dashboards personalizados independientes.

### 6.5 Dataset Utilizado

El Nivel 4 utiliza el dataset TechStore en su versión limpia (clean), que consiste en datos preparados y consistentes sin problemas de calidad. Esta elección permite que el usuario se enfoque completamente en técnicas avanzadas de análisis y visualización sin distracciones causadas por problemas de datos. Los datos están completos y consistentes, proporcionando una base sólida para análisis estadísticos avanzados, cálculos de correlación, y visualizaciones complejas que requieren datos de alta calidad para producir resultados confiables y significativos.

### 6.6 Metodología Pedagógica

El Nivel 4 utiliza un enfoque de integración y aplicación mediante una secuencia pedagógica que incluye revisión de conceptos previos, introducción de nuevos conceptos avanzados, aplicación práctica, y finalmente creación independiente. La integración explícita de todos los niveles anteriores ayuda al usuario a ver cómo todos los aprendizajes se combinan en aplicaciones prácticas reales. El proyecto práctico de creación de dashboard permite al usuario aplicar todos los conceptos aprendidos en un proyecto completo que demuestra competencia en análisis avanzado de datos.

### 6.7 Requisitos de Acceso

El acceso al Nivel 4 requiere que el usuario esté autenticado en el sistema y haya completado los Niveles 1, 2 y 3. Esta verificación de prerrequisitos garantiza que el usuario tenga la base completa de conocimientos necesaria (conceptos fundamentales, preparación de datos, filtros, y métricas básicas) antes de abordar técnicas avanzadas de análisis y visualización.

---

## 7. Componentes Comunes del Sistema

### 7.1 Sistema de Autenticación

Todos los niveles requieren autenticación de usuario mediante:
- Verificación de sesión activa
- Validación de credenciales
- Redirección a página de inicio si no está autenticado

### 7.2 Sistema de Progreso

Cada nivel implementa:
- Barra de progreso general (0-100%)
- Contador de niveles completados
- Resumen de progresión por nivel
- Sistema de logros y badges visuales
- Persistencia en base de datos

### 7.3 Sistema de Quiz

Todos los niveles incluyen:
- 5 preguntas de opción múltiple
- Requisito de aprobación: 60% (3 de 5 correctas)
- Retroalimentación explicativa
- Bloqueo de completación hasta aprobar
- Guardado de resultados

### 7.4 Sistema de Navegación

Cada nivel proporciona:
- Navegación al nivel anterior
- Navegación al nivel siguiente (si está desbloqueado)
- Navegación a página de inicio
- Navegación a página de ayuda
- Navegación a dashboard (en niveles avanzados)

### 7.5 Sistema de Encuestas

Tras completar cada nivel:
- Encuesta específica del nivel
- Encuesta final del curso (tras completar todos los niveles)
- Almacenamiento de respuestas en base de datos

---

## 8. Arquitectura de Componentes

### 8.1 Componentes de UI Reutilizables

**a) Step Cards (`create_step_card`)**
- Tarjetas de contenido estructurado
- Soporte para secciones con listas y subsecciones
- Formato HTML consistente

**b) Info Boxes (`create_info_box`)**
- Cajas informativas con diferentes estilos (info, success, warning, card)
- Contenido HTML personalizable

**c) Achievement Display (`create_achievement_display`)**
- Visualización de logros desbloqueados
- Badges con iconos y colores
- Lista de habilidades adquiridas

**d) Progression Summary (`create_progression_summary`)**
- Resumen visual del progreso
- Métricas de completación
- Visualización de logros

**e) Level Preview (`create_level_preview`)**
- Vista previa del nivel actual o siguiente
- Información sobre objetivos y contenidos

**f) Data Quality Insight (`create_data_quality_insight`)**
- Información sobre calidad de datos del nivel
- Comparación entre estados de datos

### 8.2 Componentes de Datos

**a) Sample Data Generator (`create_sample_data`)**
- Generación de datasets de ejemplo
- Versiones "clean" y "dirty"
- Dataset unificado TechStore

**b) Data Analyzer (`analyze_uploaded_data`)**
- Análisis automático de datos cargados
- Identificación de tipos de datos
- Detección de problemas de calidad

### 8.3 Componentes de Estilos

**a) Level Styles (`load_level_styles`)**
- CSS personalizado para páginas de nivel
- Estilos consistentes en toda la plataforma
- Responsive design

---

## 9. Flujo de Progresión del Usuario

### 9.1 Secuencia de Niveles

1. **Nivel 0** → Conceptos fundamentales (sin prerrequisitos)
2. **Nivel 1** → Requiere Nivel 0 completado
3. **Nivel 2** → Requiere Nivel 1 completado
4. **Nivel 3** → Requiere Niveles 1 y 2 completados
5. **Nivel 4** → Requiere Niveles 1, 2 y 3 completados

### 9.2 Mecanismo de Desbloqueo

- Verificación automática de prerrequisitos al acceder a un nivel
- Mensaje de advertencia si no se cumplen prerrequisitos
- Botón de redirección al nivel requerido

### 9.3 Persistencia de Progreso

- Guardado en base de datos PostgreSQL/Supabase
- Campos por nivel: `nivel0`, `nivel1`, `nivel2`, `nivel3`, `nivel4`
- Actualización en tiempo real
- Recuperación de progreso en sesiones futuras

---

## 10. Conclusiones

El sistema de niveles de aprendizaje de la Plataforma TCC implementa una metodología pedagógica estructurada y progresiva que guía a usuarios sin experiencia previa desde conceptos fundamentales hasta técnicas avanzadas de análisis de datos. Cada nivel está diseñado con componentes específicos que incluyen contenido teórico, ejemplos prácticos, actividades interactivas, sistemas de evaluación y mecanismos de seguimiento del progreso.

La arquitectura modular del sistema permite la reutilización de componentes, facilitando el mantenimiento y la extensión. El uso de un dataset unificado (TechStore) que evoluciona en calidad a través de los niveles proporciona continuidad pedagógica y permite al usuario ver la aplicación práctica de los conceptos aprendidos.

El sistema de evaluación mediante quizzes y la verificación de prerrequisitos garantiza que los usuarios adquieran los conocimientos necesarios antes de avanzar, mientras que los sistemas de logros y progreso proporcionan motivación y retroalimentación continua.

---

## Referencias

- Documentación interna del proyecto TCC
- Archivos fuente: `pages/00_Nivel_0_Introduccion.py` a `pages/04_Nivel_4_Avanzado.py`
- Módulos de utilidades: `utils/learning/`
- Sistema de base de datos: `core/database.py`
- Sistema de autenticación: `core/auth_service.py`

---

**Fin del Documento**

