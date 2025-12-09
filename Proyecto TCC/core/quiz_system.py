import streamlit as st
import random
from datetime import datetime
from core.auth_config import update_user_progress, check_achievement
from core.database import db_manager

from utils.ui.icon_system import get_icon, replace_emojis
# Quiz questions for each level
QUIZ_QUESTIONS = {
    'nivel0': [
        {
            'question': '¿Qué son los datos?',
            'options': ['Información que se puede medir, contar o describir', 'Solo números', 'Solo texto', 'Solo fechas'],
            'correct': 0,
            'explanation': 'Los datos son información que se puede medir, contar o describir. Incluyen números, texto, fechas y más.'
        },
        {
            'question': '¿Cuáles son los tipos principales de datos?',
            'options': ['Solo números', 'Numéricos, texto, fecha/hora, y sí/no', 'Solo texto y números', 'Solo fechas'],
            'correct': 1,
            'explanation': 'Los datos principales son: numéricos (números), texto (palabras), fecha/hora, y datos de sí/no (verdadero/falso).'
        },
        {
            'question': 'En una tabla de datos, ¿qué representa cada fila?',
            'options': ['Un tipo de información', 'Un registro individual (una venta, un cliente, etc.)', 'Un número', 'Un color'],
            'correct': 1,
            'explanation': 'Cada fila representa un registro individual, como una venta, un cliente, o un producto.'
        },
        {
            'question': 'En una tabla de datos, ¿qué representa cada columna?',
            'options': ['Un registro completo', 'Un tipo de información específica', 'Un número aleatorio', 'Una fila'],
            'correct': 1,
            'explanation': 'Cada columna representa un tipo de información específica, como fecha, precio, o nombre del producto.'
        },
        {
            'question': '¿Qué es el análisis de datos?',
            'options': ['Solo contar números', 'Examinar información para encontrar respuestas, patrones e insights', 'Solo hacer gráficos', 'Eliminar datos'],
            'correct': 1,
            'explanation': 'El análisis de datos es examinar la información para encontrar respuestas, patrones e insights que ayuden a tomar mejores decisiones.'
        },
        {
            'question': '¿Por qué es importante organizar los datos?',
            'options': ['Para que se vean bonitos', 'Para facilitar el análisis y encontrar información rápidamente', 'Solo por costumbre', 'No es importante'],
            'correct': 1,
            'explanation': 'Organizar los datos facilita el análisis y permite encontrar información rápidamente, lo que lleva a mejores decisiones.'
        },
        {
            'question': '¿Qué es un dataset?',
            'options': ['Un solo número', 'Una colección organizada de datos relacionados', 'Un gráfico', 'Un programa'],
            'correct': 1,
            'explanation': 'Un dataset es una colección organizada de datos relacionados que se pueden analizar juntos.'
        },
        {
            'question': '¿Cuál es la diferencia entre datos cualitativos y cuantitativos?',
            'options': ['No hay diferencia', 'Cualitativos son números, cuantitativos son texto', 'Cuantitativos son números medibles, cualitativos son descripciones', 'Son lo mismo'],
            'correct': 2,
            'explanation': 'Los datos cuantitativos son números que se pueden medir (ej: edad, precio), mientras que los cualitativos son descripciones o categorías (ej: color, nombre).'
        },
        {
            'question': '¿Qué significa "datos estructurados"?',
            'options': ['Datos organizados en formato de tabla', 'Datos desordenados', 'Solo imágenes', 'Solo texto'],
            'correct': 0,
            'explanation': 'Los datos estructurados están organizados en formato de tabla con filas y columnas claramente definidas.'
        },
        {
            'question': '¿Qué es un ejemplo de dato numérico?',
            'options': ['El nombre de un producto', 'El precio de venta', 'El color de un objeto', 'La descripción'],
            'correct': 1,
            'explanation': 'El precio de venta es un dato numérico porque es un número que se puede medir y calcular.'
        },
        {
            'question': '¿Qué es un ejemplo de dato categórico?',
            'options': ['El precio', 'La cantidad vendida', 'La categoría del producto', 'El total de ventas'],
            'correct': 2,
            'explanation': 'La categoría del producto es un dato categórico porque agrupa productos en categorías como "Electrónica" o "Ropa".'
        },
        {
            'question': '¿Para qué sirven los datos en una empresa?',
            'options': ['Solo para guardar', 'Para tomar decisiones informadas y mejorar el negocio', 'Para hacer bonito', 'No sirven para nada'],
            'correct': 1,
            'explanation': 'Los datos ayudan a tomar decisiones informadas, identificar problemas, encontrar oportunidades y mejorar el negocio.'
        }
    ],
    'nivel1': [
        {
            'question': '¿Cuál es el formato más común para archivos de datos?',
            'options': ['CSV', 'TXT', 'DOC', 'PDF'],
            'correct': 0,
            'explanation': 'CSV (Comma-Separated Values) es el formato más común para datos tabulares.'
        },
        {
            'question': '¿Qué debe tener la primera fila de un archivo CSV?',
            'options': ['Datos', 'Encabezados', 'Números', 'Fechas'],
            'correct': 1,
            'explanation': 'La primera fila debe contener los nombres de las columnas (encabezados).'
        },
        {
            'question': '¿Qué significa "valores faltantes" en un dataset?',
            'options': ['Datos incorrectos', 'Celdas vacías', 'Números negativos', 'Texto largo'],
            'correct': 1,
            'explanation': 'Los valores faltantes son celdas vacías o con valores nulos en el dataset.'
        },
        {
            'question': '¿Cuál es el primer paso en el análisis de datos?',
            'options': ['Crear gráficos', 'Cargar datos', 'Hacer predicciones', 'Exportar resultados'],
            'correct': 1,
            'explanation': 'El primer paso es siempre cargar y preparar los datos correctamente.'
        },
        {
            'question': '¿Qué formato de fecha es más estándar?',
            'options': ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD', 'DD-MM-YYYY'],
            'correct': 2,
            'explanation': 'YYYY-MM-DD es el formato ISO estándar internacional.'
        },
        {
            'question': '¿Qué es un archivo Excel (.xlsx)?',
            'options': ['Solo texto', 'Un formato de hoja de cálculo que puede contener múltiples hojas', 'Solo números', 'Un programa'],
            'correct': 1,
            'explanation': 'Excel es un formato de hoja de cálculo que puede contener múltiples hojas, formato y fórmulas.'
        },
        {
            'question': '¿Qué es importante verificar al cargar datos?',
            'options': ['Solo el nombre del archivo', 'La calidad, completitud y formato de los datos', 'Solo el tamaño', 'Nada'],
            'correct': 1,
            'explanation': 'Al cargar datos es importante verificar la calidad, completitud y formato para asegurar que el análisis sea correcto.'
        },
        {
            'question': '¿Qué son los "duplicados" en un dataset?',
            'options': ['Filas que aparecen más de una vez', 'Columnas vacías', 'Datos incorrectos', 'Números grandes'],
            'correct': 0,
            'explanation': 'Los duplicados son filas que aparecen más de una vez exactamente igual en el dataset.'
        },
        {
            'question': '¿Por qué es importante limpiar los datos antes de analizarlos?',
            'options': ['Porque se ven mejor', 'Para asegurar que el análisis sea preciso y confiable', 'Solo por costumbre', 'No es importante'],
            'correct': 1,
            'explanation': 'Limpiar los datos asegura que el análisis sea preciso y confiable, eliminando errores que puedan afectar los resultados.'
        },
        {
            'question': '¿Qué significa "consistencia" en los datos?',
            'options': ['Que todos los datos sean iguales', 'Que los datos sigan el mismo formato y estándares', 'Que haya muchos datos', 'Que los datos estén ordenados'],
            'correct': 1,
            'explanation': 'La consistencia significa que los datos sigan el mismo formato y estándares a lo largo de todo el dataset.'
        },
        {
            'question': '¿Qué es mejor: un archivo CSV o Excel para datos simples?',
            'options': ['Siempre Excel', 'CSV es más simple y compatible, Excel tiene más características', 'Ninguno sirve', 'Siempre CSV'],
            'correct': 1,
            'explanation': 'CSV es más simple y compatible con más programas, mientras que Excel ofrece más características como múltiples hojas y formato.'
        },
        {
            'question': '¿Qué debes hacer si encuentras errores en los datos al cargarlos?',
            'options': ['Ignorarlos', 'Corregirlos o eliminarlos antes de continuar', 'Solo contarlos', 'Cambiar el formato'],
            'correct': 1,
            'explanation': 'Si encuentras errores, debes corregirlos o eliminarlos antes de continuar para asegurar la calidad del análisis.'
        }
    ],
    'nivel2': [
        {
            'question': '¿Qué es un filtro en análisis de datos?',
            'options': ['Un tipo de gráfico', 'Una forma de seleccionar datos específicos', 'Un cálculo matemático', 'Un formato de archivo'],
            'correct': 1,
            'explanation': 'Un filtro permite seleccionar solo los datos que cumplen ciertas condiciones.'
        },
        {
            'question': '¿Cuál es la diferencia entre filtros AND y OR?',
            'options': ['No hay diferencia', 'AND requiere que se cumplan todas las condiciones, OR solo una', 'OR es más rápido', 'AND es más preciso'],
            'correct': 1,
            'explanation': 'AND requiere que TODAS las condiciones se cumplan, OR requiere que al menos UNA se cumpla.'
        },
        {
            'question': '¿Qué significa "rangos de fechas" en filtros?',
            'options': ['Solo fechas específicas', 'Un período entre dos fechas', 'Todas las fechas', 'Fechas futuras'],
            'correct': 1,
            'explanation': 'Los rangos de fechas permiten seleccionar datos entre una fecha inicial y final.'
        },
        {
            'question': '¿Por qué es importante usar filtros?',
            'options': ['Para hacer el análisis más lento', 'Para enfocarse en datos relevantes', 'Para cambiar el formato', 'Para eliminar datos'],
            'correct': 1,
            'explanation': 'Los filtros ayudan a enfocarse en los datos más relevantes para el análisis.'
        },
        {
            'question': '¿Qué es un filtro numérico?',
            'options': ['Solo números pares', 'Condiciones basadas en valores numéricos', 'Números grandes', 'Cálculos matemáticos'],
            'correct': 1,
            'explanation': 'Los filtros numéricos permiten establecer condiciones basadas en valores numéricos (mayor que, menor que, etc.).'
        },
        {
            'question': '¿Qué es un filtro categórico?',
            'options': ['Filtrar por números', 'Seleccionar datos basados en categorías o valores de texto', 'Filtrar fechas', 'Filtrar colores'],
            'correct': 1,
            'explanation': 'Los filtros categóricos permiten seleccionar datos basados en categorías o valores de texto específicos.'
        },
        {
            'question': '¿Qué significa "filtrar por mayor que" (>)?',
            'options': ['Seleccionar valores menores', 'Seleccionar valores que son mayores a un número específico', 'Seleccionar todos los valores', 'Eliminar valores'],
            'correct': 1,
            'explanation': 'Filtrar por "mayor que" selecciona solo los valores que son mayores al número especificado.'
        },
        {
            'question': '¿Qué es combinar múltiples filtros?',
            'options': ['Usar solo un filtro', 'Aplicar varios filtros al mismo tiempo para ser más específico', 'Eliminar filtros', 'Cambiar el orden'],
            'correct': 1,
            'explanation': 'Combinar múltiples filtros permite aplicar varios criterios al mismo tiempo para encontrar datos muy específicos.'
        },
        {
            'question': '¿Qué es un filtro de texto parcial?',
            'options': ['Buscar coincidencias exactas', 'Buscar palabras o frases que contengan cierto texto', 'Solo buscar números', 'No existe'],
            'correct': 1,
            'explanation': 'Los filtros de texto parcial permiten buscar registros que contengan ciertas palabras o frases dentro del texto.'
        },
        {
            'question': '¿Por qué es útil filtrar datos por período de tiempo?',
            'options': ['Solo por estética', 'Para analizar tendencias y cambios en un período específico', 'Para hacer el análisis más lento', 'No es útil'],
            'correct': 1,
            'explanation': 'Filtrar por período de tiempo permite analizar tendencias y cambios específicos, como ventas por mes o trimestre.'
        },
        {
            'question': '¿Qué sucede si aplicas un filtro muy restrictivo?',
            'options': ['Obtienes más resultados', 'Obtienes menos resultados pero más específicos', 'No pasa nada', 'Se eliminan todos los datos'],
            'correct': 1,
            'explanation': 'Un filtro muy restrictivo reduce el número de resultados pero los hace más específicos y relevantes para tu análisis.'
        },
        {
            'question': '¿Qué es mejor: un filtro simple o múltiples filtros combinados?',
            'options': ['Siempre simple', 'Depende de lo que necesites: filtros combinados para análisis más específicos', 'Siempre múltiples', 'No importa'],
            'correct': 1,
            'explanation': 'Depende de tu necesidad: filtros simples para análisis generales, filtros combinados para análisis más específicos y detallados.'
        }
    ],
    'nivel3': [
        {
            'question': '¿Qué es una métrica en análisis de datos?',
            'options': ['Un tipo de gráfico', 'Una medida cuantificable', 'Un color', 'Un formato'],
            'correct': 1,
            'explanation': 'Una métrica es una medida cuantificable que ayuda a evaluar el rendimiento o comportamiento.'
        },
        {
            'question': '¿Qué significa "promedio" en estadísticas?',
            'options': ['El valor más alto', 'El valor más bajo', 'La suma dividida por la cantidad', 'El valor del medio'],
            'correct': 2,
            'explanation': 'El promedio es la suma de todos los valores dividida por la cantidad de valores.'
        },
        {
            'question': '¿Qué es la mediana?',
            'options': ['El valor más común', 'El valor del medio cuando están ordenados', 'El promedio', 'El valor más alto'],
            'correct': 1,
            'explanation': 'La mediana es el valor que está en el medio cuando todos los valores están ordenados.'
        },
        {
            'question': '¿Qué mide la desviación estándar?',
            'options': ['El promedio', 'La variabilidad de los datos', 'El valor máximo', 'La cantidad de datos'],
            'correct': 1,
            'explanation': 'La desviación estándar mide qué tan dispersos están los datos alrededor del promedio.'
        },
        {
            'question': '¿Qué es un KPI?',
            'options': ['Un tipo de gráfico', 'Un Indicador Clave de Rendimiento', 'Un formato de archivo', 'Un filtro'],
            'correct': 1,
            'explanation': 'KPI significa Key Performance Indicator (Indicador Clave de Rendimiento).'
        },
        {
            'question': '¿Qué es la moda?',
            'options': ['El valor más común', 'El promedio', 'El valor más alto', 'El valor más bajo'],
            'correct': 0,
            'explanation': 'La moda es el valor que aparece con mayor frecuencia en un conjunto de datos.'
        },
        {
            'question': '¿Qué es una métrica de suma (total)?',
            'options': ['El promedio', 'La suma de todos los valores', 'El valor máximo', 'La cantidad'],
            'correct': 1,
            'explanation': 'La suma total es el resultado de sumar todos los valores de una columna numérica.'
        },
        {
            'question': '¿Cuándo es útil usar la mediana en lugar del promedio?',
            'options': ['Nunca', 'Cuando hay valores extremos que pueden distorsionar el promedio', 'Siempre usar promedio', 'Cuando hay pocos datos'],
            'correct': 1,
            'explanation': 'La mediana es útil cuando hay valores extremos (outliers) que pueden distorsionar el promedio.'
        },
        {
            'question': '¿Qué es una métrica de crecimiento?',
            'options': ['El valor actual', 'El cambio porcentual entre dos períodos', 'Solo números positivos', 'El promedio'],
            'correct': 1,
            'explanation': 'Las métricas de crecimiento miden el cambio porcentual entre dos períodos, como crecimiento mensual o anual.'
        },
        {
            'question': '¿Qué es un KPI para un negocio de ventas?',
            'options': ['Solo el color del logo', 'Ventas totales, número de clientes, tasa de conversión', 'Solo el nombre', 'Solo las fechas'],
            'correct': 1,
            'explanation': 'KPIs comunes para ventas incluyen: ventas totales, número de clientes, tasa de conversión, y promedio de venta por cliente.'
        },
        {
            'question': '¿Qué significa "interpretar" una métrica?',
            'options': ['Solo ver el número', 'Entender qué significa el número y qué acciones tomar', 'Ignorarla', 'Copiarla'],
            'correct': 1,
            'explanation': 'Interpretar una métrica significa entender qué significa el número en contexto y qué acciones puedes tomar basándote en ella.'
        },
        {
            'question': '¿Por qué es importante comparar métricas?',
            'options': ['Solo para tener más números', 'Para entender tendencias, identificar problemas y tomar decisiones', 'Para complicar el análisis', 'No es importante'],
            'correct': 1,
            'explanation': 'Comparar métricas permite entender tendencias, identificar problemas, ver mejoras y tomar decisiones basadas en datos.'
        }
    ],
    'nivel4': [
        {
            'question': '¿Qué es un análisis de tendencias?',
            'options': ['Un tipo de gráfico', 'El estudio de patrones a lo largo del tiempo', 'Un cálculo matemático', 'Un filtro'],
            'correct': 1,
            'explanation': 'El análisis de tendencias estudia cómo cambian los datos a lo largo del tiempo.'
        },
        {
            'question': '¿Qué es la correlación entre variables?',
            'options': ['Una causa y efecto', 'Una relación estadística', 'Un tipo de gráfico', 'Un filtro'],
            'correct': 1,
            'explanation': 'La correlación mide la relación estadística entre dos variables, no necesariamente causalidad.'
        },
        {
            'question': '¿Qué es un outlier?',
            'options': ['Un error en los datos', 'Un valor que se desvía significativamente del patrón', 'Un tipo de gráfico', 'Un filtro'],
            'correct': 1,
            'explanation': 'Un outlier es un valor que se desvía significativamente del patrón general de los datos.'
        },
        {
            'question': '¿Qué es la segmentación de datos?',
            'options': ['Eliminar datos', 'Dividir datos en grupos similares', 'Cambiar el formato', 'Crear gráficos'],
            'correct': 1,
            'explanation': 'La segmentación divide los datos en grupos con características similares para análisis más específicos.'
        },
        {
            'question': '¿Qué es un dashboard?',
            'options': ['Un tipo de gráfico', 'Una visualización interactiva de métricas clave', 'Un filtro', 'Un cálculo'],
            'correct': 1,
            'explanation': 'Un dashboard es una visualización interactiva que muestra las métricas y KPIs más importantes.'
        },
        {
            'question': '¿Qué es una visualización interactiva?',
            'options': ['Un gráfico estático', 'Un gráfico donde puedes hacer zoom, filtrar y explorar datos', 'Solo texto', 'Un cálculo'],
            'correct': 1,
            'explanation': 'Una visualización interactiva permite explorar los datos haciendo zoom, filtrando y seleccionando elementos específicos.'
        },
        {
            'question': '¿Qué es un gráfico de barras usado para mostrar?',
            'options': ['Tendencias en el tiempo', 'Comparar valores entre diferentes categorías', 'Relaciones entre variables', 'Solo números'],
            'correct': 1,
            'explanation': 'Los gráficos de barras son ideales para comparar valores entre diferentes categorías o grupos.'
        },
        {
            'question': '¿Qué es un gráfico de líneas usado para mostrar?',
            'options': ['Comparar categorías', 'Mostrar tendencias y cambios a lo largo del tiempo', 'Mostrar proporciones', 'Mostrar relaciones'],
            'correct': 1,
            'explanation': 'Los gráficos de líneas son ideales para mostrar tendencias y cambios a lo largo del tiempo.'
        },
        {
            'question': '¿Qué es un insight en análisis de datos?',
            'options': ['Un número cualquiera', 'Un descubrimiento importante que puede llevar a acciones valiosas', 'Un error', 'Un gráfico'],
            'correct': 1,
            'explanation': 'Un insight es un descubrimiento importante en los datos que puede llevar a acciones o decisiones valiosas.'
        },
        {
            'question': '¿Qué es importante al crear un dashboard?',
            'options': ['Poner todos los datos posibles', 'Enfocarse en las métricas más importantes y mantener el diseño claro', 'Usar muchos colores', 'Poner pocos datos'],
            'correct': 1,
            'explanation': 'Un buen dashboard se enfoca en las métricas más importantes y mantiene un diseño claro y fácil de entender.'
        },
        {
            'question': '¿Qué significa "análisis comparativo"?',
            'options': ['Analizar solo un dato', 'Comparar diferentes períodos, grupos o categorías para encontrar diferencias', 'Eliminar datos', 'Solo promediar'],
            'correct': 1,
            'explanation': 'El análisis comparativo compara diferentes períodos, grupos o categorías para encontrar diferencias y patrones.'
        },
        {
            'question': '¿Qué es una visualización de dispersión (scatter plot) usada para mostrar?',
            'options': ['Solo números', 'La relación entre dos variables numéricas', 'Solo categorías', 'Solo tiempo'],
            'correct': 1,
            'explanation': 'Los gráficos de dispersión muestran la relación entre dos variables numéricas y ayudan a identificar patrones o correlaciones.'
        }
    ]
}

LEVEL_HEADERS = {
    'nivel0': 'Nivel 0: Introducción',
    'nivel1': 'Nivel 1: Básico',
    'nivel2': 'Nivel 2: Filtros',
    'nivel3': 'Nivel 3: Métricas',
    'nivel4': 'Nivel 4: Avanzado',
}

NEXT_LEVEL_DESTINATIONS = {
    'nivel0': ("pages/01_Nivel_1_Basico.py", "Nivel 1: Básico"),
    'nivel1': ("pages/02_Nivel_2_Filtros.py", "Nivel 2: Filtros"),
    'nivel2': ("pages/03_Nivel_3_Metricas.py", "Nivel 3: Métricas"),
    'nivel3': ("pages/04_Nivel_4_Avanzado.py", "Nivel 4: Avanzado"),
    'nivel4': ("Inicio.py", "Inicio"),
}


# Estado - Reiniciar Estado de Quiz
def _reset_quiz_state(level, total_questions, *, keep_expanded=False):
    """Clear quiz-related session state values."""
    prefix = f'quiz_{level}'
    keys_to_clear = [
        f'{prefix}_started',
        f'{prefix}_current_question',
        f'{prefix}_score',
        f'{prefix}_answers',
        f'{prefix}_completed',
        f'{prefix}_question_order',
        f'{prefix}_last_feedback',
        f'{prefix}_skipped',
        f'{prefix}_saved',
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)

    # Limpieza - Remover Flags y Claves de Seleccion Legacy
    for idx in range(total_questions):
        st.session_state.pop(f'{prefix}_answered_{idx}', None)
        st.session_state.pop(f'{prefix}_q{idx}', None)
        st.session_state.pop(f'{prefix}_q_{idx}', None)
        st.session_state.pop(f'{prefix}_submit_{idx}', None)
    
    # Clear selected questions so new ones are chosen on next start
    st.session_state.pop(f'{prefix}_selected_questions', None)

    if keep_expanded:
        st.session_state[f'{prefix}_expanded'] = True
    else:
        st.session_state.pop(f'{prefix}_expanded', None)
# Quiz - Crear y Mostrar Quiz
def create_quiz(level, username):
    """Create and display a quiz for a specific level."""

    # Get all questions from the question bank
    question_bank = QUIZ_QUESTIONS.get(level, [])

    if not question_bank:
        st.error("No hay preguntas disponibles para este nivel.")
        return

    # Ensure we have at least 5 questions in the bank
    if len(question_bank) < 5:
        st.error(f"Se necesitan al menos 5 preguntas en el banco. Actualmente hay {len(question_bank)}.")
        return

    prefix = f'quiz_{level}'
    expander_key = f'{prefix}_expanded'
    skipped_key = f'{prefix}_skipped'
    selected_questions_key = f'{prefix}_selected_questions'

    if st.session_state.get(skipped_key):
        st.info("Has pospuesto este quiz. Puedes retomarlo cuando quieras. Recuerda que necesitas aprobarlo para completar el nivel.")

    # UI - Mantener Expander Abierto si Quiz Completado o Iniciado
    if st.session_state.get(f'{prefix}_started') or st.session_state.get(f'{prefix}_completed'):
        st.session_state[expander_key] = True

    # UI - Forzar Expander Abierto si Quiz Completado
    if st.session_state.get(f'{prefix}_completed', False):
        expanded = True
        st.session_state[expander_key] = True
    else:
        expanded = st.session_state.get(expander_key, True)
    
    header_text = LEVEL_HEADERS.get(level, f"Nivel {level[-1]}")

    with st.expander(f"🧠 Quiz - {header_text}", expanded=expanded):
        st.markdown("### Pon a prueba tus conocimientos")

        # Only initialize quiz state if quiz hasn't been started or completed yet
        # This prevents resetting the state when returning to the page after completing the quiz
        if f'{prefix}_started' not in st.session_state and f'{prefix}_completed' not in st.session_state:
            st.session_state[f'{prefix}_started'] = False
            st.session_state[f'{prefix}_current_question'] = 0
            st.session_state[f'{prefix}_score'] = 0
            st.session_state[f'{prefix}_answers'] = []
            st.session_state[f'{prefix}_completed'] = False
            st.session_state[f'{prefix}_question_order'] = []
            st.session_state[selected_questions_key] = []
        
        # Ensure answers are preserved if quiz is completed
        if st.session_state.get(f'{prefix}_completed', False) and f'{prefix}_answers' not in st.session_state:
            st.session_state[f'{prefix}_answers'] = []

        # Get selected questions (5 random questions from the bank)
        selected_questions = st.session_state.get(selected_questions_key, [])
        if not selected_questions:
            # Select 5 random questions from the bank
            selected_questions = random.sample(question_bank, 5)
            st.session_state[selected_questions_key] = selected_questions
        
        questions = selected_questions
        total_questions = len(questions)

        if not st.session_state[f'{prefix}_started']:
            st.markdown("""
            #### 📋 Instrucciones
            - Se te presentarán 5 preguntas seleccionadas aleatoriamente de un banco más grande.
            - Cada pregunta tiene 4 opciones y solo una es correcta.
            - Las preguntas cambian cada vez que inicias el quiz.
            - Necesitas al menos 3 respuestas correctas para aprobar el nivel.
            """)

            col_start, col_skip = st.columns([2, 1])
            with col_start:
                if st.button("🚀 Comenzar Quiz", type="primary", use_container_width=True, key=f"{prefix}_start"):
                    # Select 5 random questions from the bank
                    selected_questions = random.sample(question_bank, 5)
                    st.session_state[selected_questions_key] = selected_questions
                    # Create order for the 5 selected questions
                    st.session_state[f'{prefix}_question_order'] = list(range(5))
                    st.session_state[f'{prefix}_current_question'] = 0
                    st.session_state[f'{prefix}_score'] = 0
                    st.session_state[f'{prefix}_answers'] = []
                    st.session_state[f'{prefix}_completed'] = False
                    st.session_state[f'{prefix}_started'] = True
                    st.session_state[expander_key] = True
                    st.session_state.pop(skipped_key, None)
                    st.rerun()
            with col_skip:
                if st.button("⏭️ Hacerlo más tarde", use_container_width=True, key=f"{prefix}_skip"):
                    st.session_state[expander_key] = False
                    st.session_state[skipped_key] = True
                    st.rerun()
            return

        # Ensure selected questions and question order exist
        if not st.session_state.get(selected_questions_key):
            selected_questions = random.sample(question_bank, 5)
            st.session_state[selected_questions_key] = selected_questions
            questions = selected_questions
        
        if not st.session_state.get(f'{prefix}_question_order'):
            st.session_state[f'{prefix}_question_order'] = list(range(5))

        # Always keep expander open during quiz or when completed
        if st.session_state.get(f'{prefix}_started') or st.session_state.get(f'{prefix}_completed'):
            st.session_state[expander_key] = True

        feedback = st.session_state.pop(f'{prefix}_last_feedback', None)
        if feedback:
            if feedback['is_correct']:
                st.markdown(replace_emojis("🎉 ¡Respuesta correcta!"), unsafe_allow_html=True)
            else:
                st.markdown(f"{get_icon('❌', 20)} Incorrecto. La respuesta correcta era: **{feedback['correct_answer']}**", unsafe_allow_html=True)
            st.markdown(f"{get_icon('💡', 20)} **Explicación:** {feedback['explanation']}", unsafe_allow_html=True)
            st.markdown("---")

        if not st.session_state[f'{prefix}_completed']:
            order = st.session_state[f'{prefix}_question_order']
            current_index = st.session_state[f'{prefix}_current_question']

            if current_index >= len(order):
                st.session_state[f'{prefix}_completed'] = True
                st.session_state[expander_key] = True  # Ensure expander stays open
                st.rerun()

            question = questions[order[current_index]]

            st.markdown(f"#### Pregunta {current_index + 1} de {total_questions}")
            st.markdown(f"**{question['question']}**")

            selected_option = st.radio(
                "Selecciona tu respuesta:",
                question['options'],
                key=f"{prefix}_q_{current_index}",
                index=None
            )
            
            # Validacion - Verificar que se haya seleccionado una opcion
            if selected_option is None:
                st.warning("Por favor selecciona una respuesta antes de continuar.")

            col_answer, col_restart = st.columns([2, 1])
            with col_answer:
                submit_disabled = selected_option is None
                if st.button("✅ Enviar y continuar", type="primary", use_container_width=True, key=f"{prefix}_submit_{current_index}", disabled=submit_disabled):
                    # This check is redundant but serves as a safety measure
                    if selected_option is None:
                        st.stop()
                    
                    correct = question['options'].index(selected_option) == question['correct']

                    if correct:
                        st.session_state[f'{prefix}_score'] += 1

                    st.session_state[f'{prefix}_answers'].append({
                        'question': question['question'],
                        'selected': selected_option,
                        'correct': question['options'][question['correct']],
                        'is_correct': correct,
                        'explanation': question['explanation']
                    })

                    st.session_state[f'{prefix}_last_feedback'] = {
                        'is_correct': correct,
                        'correct_answer': question['options'][question['correct']],
                        'explanation': question['explanation']
                    }

                    st.session_state[f'{prefix}_current_question'] += 1
                    if st.session_state[f'{prefix}_current_question'] >= len(order):
                        st.session_state[f'{prefix}_completed'] = True
                        st.session_state[expander_key] = True  # Ensure expander stays open
                    st.rerun()

            with col_restart:
                if st.button("🔄 Reiniciar Quiz", use_container_width=True, key=f"{prefix}_reset_{current_index}"):
                    _reset_quiz_state(level, total_questions, keep_expanded=True)
                    st.rerun()
        else:
            # Use selected questions for results display
            selected_questions = st.session_state.get(selected_questions_key, questions)
            show_quiz_results(level, username, selected_questions, expander_key)


# Quiz - Mostrar Resultados de Quiz
def show_quiz_results(level, username, questions, expander_key):
    """Show quiz results and achievements."""

    prefix = f'quiz_{level}'
    st.session_state[expander_key] = True  # Force expander to stay open

    # Validacion - Verificar que Datos de Quiz Existen
    if f'{prefix}_score' not in st.session_state or f'{prefix}_answers' not in st.session_state:
        st.error("Error: Los datos del quiz no están disponibles. Por favor, intenta el quiz nuevamente.")
        return

    score = st.session_state.get(f'{prefix}_score', 0)
    answers = st.session_state.get(f'{prefix}_answers', [])
    total_questions = len(questions)
    percentage = (score / total_questions) * 100 if total_questions else 0
    passed = score >= 3

    st.subheader(replace_emojis("🎯 Resultados del Quiz"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Puntuación", f"{score}/{total_questions}")
    with col2:
        st.metric("Porcentaje", f"{percentage:.1f}%")
    with col3:
        status = replace_emojis("✅ Aprobado") if passed else "❌ No Aprobado"
        st.metric("Estado", status)

    st.progress(percentage / 100 if total_questions else 0)

    if passed:
        st.markdown(replace_emojis("🎉 ¡Felicitaciones! Has aprobado el quiz."), unsafe_allow_html=True)
        st.session_state[f'{prefix}_passed'] = True

        if score == total_questions:
            new_achievements = check_achievement(username, 'quiz_perfect')
            if new_achievements:
                st.balloons()
                st.markdown(replace_emojis("🏆 ¡Logro desbloqueado: Maestro del Quiz!"), unsafe_allow_html=True)
    else:
        st.markdown(replace_emojis("📚 Necesitas al menos 3 respuestas correctas para aprobar. ¡Sigue estudiando!"), unsafe_allow_html=True)
        st.session_state[f'{prefix}_passed'] = False

    st.markdown(replace_emojis("### 📋 Respuestas Detalladas"), unsafe_allow_html=True)

    if not answers:
        st.warning("No hay respuestas disponibles para mostrar.")
        return

    for i, answer in enumerate(answers):
        with st.expander(f"Pregunta {i + 1}: {answer['question']}"):
            if answer['is_correct']:
                st.markdown(f"{get_icon('✅', 20)} Tu respuesta: {answer['selected']}", unsafe_allow_html=True)
            else:
                st.markdown(f"{get_icon('❌', 20)} Tu respuesta: {answer['selected']}", unsafe_allow_html=True)
                st.markdown(f"{get_icon('✅', 20)} Respuesta correcta: {answer['correct']}", unsafe_allow_html=True)

            st.markdown(f"{get_icon("💡", 20)} **Explicación:** {answer['explanation']}", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Intentar de nuevo", use_container_width=True, key=f"{prefix}_retry"):
            _reset_quiz_state(level, total_questions, keep_expanded=True)
            st.rerun()
    with col2:
        if st.button("🏠 Volver al nivel", use_container_width=True, key=f"{prefix}_back"):
            _reset_quiz_state(level, total_questions, keep_expanded=False)
            st.rerun()
    with col3:
        next_destination = NEXT_LEVEL_DESTINATIONS.get(level)
        if next_destination:
            next_page, next_label = next_destination
            if st.button(f"➡️ Ir al {next_label}", type="primary", use_container_width=True, key=f"{prefix}_next"):
                st.switch_page(next_page)

    # Base de Datos - Guardar Intento de Quiz Solo una Vez
    if not st.session_state.get(f'{prefix}_saved', False):
        save_quiz_attempt(level, username, score, total_questions, percentage, passed, answers)
        st.session_state[f'{prefix}_saved'] = True
        
        if passed:
            update_user_progress(username, quiz_scores={level: percentage})

            if level == 'nivel1' and not st.session_state.get('nivel1_completed', False):
                new_achievements = check_achievement(username, 'level_completion')
                if new_achievements:
                    st.markdown(replace_emojis("🏆 ¡Logro desbloqueado: Primer Nivel Completado!"), unsafe_allow_html=True)

# Base de Datos - Guardar Intento de Quiz
def save_quiz_attempt(level, username, score, total_questions, percentage, passed, answers_list):
    """Save quiz attempt and answers to database"""
    try:
        # Get user_id from username - query database directly
        with db_manager.get_connection() as conn:
            if db_manager.db_type == "sqlite":
                cursor = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
            else:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            
            user_result = cursor.fetchone()
            
            if not user_result:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"User not found for username: {username}")
                return False
            
            user_id = user_result[0] if isinstance(user_result, tuple) else user_result['id']
        
        # Now insert quiz attempt with the user_id
        with db_manager.get_connection() as conn:
            # Insert quiz attempt
            if db_manager.db_type == "sqlite":
                cursor = conn.execute("""
                    INSERT INTO quiz_attempts (user_id, level, score, total_questions, percentage, passed, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, level, score, total_questions, percentage, passed))
                quiz_attempt_id = cursor.lastrowid
            else:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO quiz_attempts (user_id, level, score, total_questions, percentage, passed, completed_at)
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    RETURNING id
                """, (user_id, level, score, total_questions, percentage, passed))
                quiz_attempt_id = cursor.fetchone()[0]
            
            # Insert each answer
            for answer in answers_list:
                if db_manager.db_type == "sqlite":
                    conn.execute("""
                        INSERT INTO quiz_answers (quiz_attempt_id, question_text, selected_answer, correct_answer, is_correct, explanation)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (quiz_attempt_id, answer['question'], answer['selected'], answer['correct'], answer['is_correct'], answer.get('explanation', '')))
                else:
                    cursor.execute("""
                        INSERT INTO quiz_answers (quiz_attempt_id, question_text, selected_answer, correct_answer, is_correct, explanation)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (quiz_attempt_id, answer['question'], answer['selected'], answer['correct'], answer['is_correct'], answer.get('explanation', '')))
            
            conn.commit()
            return True
            
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error saving quiz attempt: {e}")
        # Don't show error to user, just log it
        return False

# UI - Mostrar Logros de Usuario
def show_achievements(username):
    """Display user achievements"""
    from core.auth_config import get_user_progress
    
    progress = get_user_progress(username)
    achievements = progress.get('achievements', [])
    
    st.markdown(replace_emojis("## 🏆 Logros Desbloqueados"), unsafe_allow_html=True)
    
    if not achievements:
        st.markdown(replace_emojis("🎯 ¡Completa niveles y quizzes para desbloquear logros!"), unsafe_allow_html=True)
        return
    
    achievement_info = {
        'first_level': {
            'title': replace_emojis('🎓 Primer Paso'),
            'description': 'Completaste tu primer nivel de aprendizaje',
            'icon': replace_emojis('🎓')
        },
        'all_levels': {
            'title': replace_emojis('🏆 Maestro del Análisis'),
            'description': 'Completaste todos los niveles del curso',
            'icon': replace_emojis('🏆')
        },
        'quiz_master': {
            'title': '🧠 Maestro del Quiz',
            'description': 'Obtuviste puntuación perfecta en un quiz',
            'icon': '🧠'
        },
        'data_analyst': {
            'title': replace_emojis('📊 Analista de Datos'),
            'description': 'Creaste 5 análisis de datos',
            'icon': replace_emojis('📊')
        }
    }
    
    for achievement in achievements:
        if achievement in achievement_info:
            info = achievement_info[achievement]
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #ffd700, #ffed4e); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <h3>{info['icon']} {info['title']}</h3>
                <p>{info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # UI - Mostrar Progreso hacia Proximos Logros
    st.markdown(replace_emojis("### 🎯 Próximos Logros"), unsafe_allow_html=True)
    
    if 'first_level' not in achievements:
        st.info("🎓 Completa el Nivel 1 para desbloquear 'Primer Paso'")
    
    if 'quiz_master' not in achievements:
        st.info("🧠 Obtén puntuación perfecta en cualquier quiz para desbloquear 'Maestro del Quiz'")
    
    if 'data_analyst' not in achievements:
        analyses_count = progress.get('data_analyses_created', 0)
        remaining = 5 - analyses_count
        st.markdown(f"{get_icon('📊', 20)} Crea {remaining} análisis más para desbloquear 'Analista de Datos'", unsafe_allow_html=True)
