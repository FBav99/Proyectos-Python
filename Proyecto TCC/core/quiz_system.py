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

    # Remove legacy flags and selection keys
    for idx in range(total_questions):
        st.session_state.pop(f'{prefix}_answered_{idx}', None)
        st.session_state.pop(f'{prefix}_q{idx}', None)
        st.session_state.pop(f'{prefix}_q_{idx}', None)
        st.session_state.pop(f'{prefix}_submit_{idx}', None)

    if keep_expanded:
        st.session_state[f'{prefix}_expanded'] = True
    else:
        st.session_state.pop(f'{prefix}_expanded', None)
def create_quiz(level, username):
    """Create and display a quiz for a specific level."""

    questions = QUIZ_QUESTIONS.get(level, [])

    if not questions:
        st.error("No hay preguntas disponibles para este nivel.")
        return

    prefix = f'quiz_{level}'
    expander_key = f'{prefix}_expanded'
    skipped_key = f'{prefix}_skipped'

    if st.session_state.get(skipped_key):
        st.info("Has pospuesto este quiz. Puedes retomarlo cuando quieras. Recuerda que necesitas aprobarlo para completar el nivel.")

    # Always keep expander open if quiz is completed or started
    if st.session_state.get(f'{prefix}_started') or st.session_state.get(f'{prefix}_completed'):
        st.session_state[expander_key] = True

    # If quiz is completed, force expander to stay open
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
        
        # Ensure answers are preserved if quiz is completed
        if st.session_state.get(f'{prefix}_completed', False) and f'{prefix}_answers' not in st.session_state:
            st.session_state[f'{prefix}_answers'] = []

        total_questions = len(questions)

        if not st.session_state[f'{prefix}_started']:
            st.markdown("""
            #### 📋 Instrucciones
            - Responde 5 preguntas relacionadas con lo aprendido en este nivel.
            - Cada pregunta tiene 4 opciones y solo una es correcta.
            - El orden de las preguntas cambia cada vez para que practiques mejor.
            - Necesitas al menos 3 respuestas correctas para aprobar el nivel.
            """)

            col_start, col_skip = st.columns([2, 1])
            with col_start:
                if st.button("🚀 Comenzar Quiz", type="primary", use_container_width=True, key=f"{prefix}_start"):
                    st.session_state[f'{prefix}_question_order'] = random.sample(range(total_questions), total_questions)
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

        if not st.session_state.get(f'{prefix}_question_order'):
            st.session_state[f'{prefix}_question_order'] = random.sample(range(total_questions), total_questions)

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
                key=f"{prefix}_q_{current_index}"
            )

            col_answer, col_restart = st.columns([2, 1])
            with col_answer:
                if st.button("✅ Enviar y continuar", type="primary", use_container_width=True, key=f"{prefix}_submit_{current_index}"):
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
            show_quiz_results(level, username, questions, expander_key)


def show_quiz_results(level, username, questions, expander_key):
    """Show quiz results and achievements."""

    prefix = f'quiz_{level}'
    st.session_state[expander_key] = True  # Force expander to stay open

    # Verify that quiz data exists
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

    # Only save quiz attempt once when results are first shown
    if not st.session_state.get(f'{prefix}_saved', False):
        save_quiz_attempt(level, username, score, total_questions, percentage, passed, answers)
        st.session_state[f'{prefix}_saved'] = True
        
        if passed:
            update_user_progress(username, quiz_scores={level: percentage})

            if level == 'nivel1' and not st.session_state.get('nivel1_completed', False):
                new_achievements = check_achievement(username, 'level_completion')
                if new_achievements:
                    st.markdown(replace_emojis("🏆 ¡Logro desbloqueado: Primer Nivel Completado!"), unsafe_allow_html=True)

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
    
    # Progress towards next achievements
    st.markdown(replace_emojis("### 🎯 Próximos Logros"), unsafe_allow_html=True)
    
    if 'first_level' not in achievements:
        st.info("🎓 Completa el Nivel 1 para desbloquear 'Primer Paso'")
    
    if 'quiz_master' not in achievements:
        st.info("🧠 Obtén puntuación perfecta en cualquier quiz para desbloquear 'Maestro del Quiz'")
    
    if 'data_analyst' not in achievements:
        analyses_count = progress.get('data_analyses_created', 0)
        remaining = 5 - analyses_count
        st.markdown(f"{get_icon('📊', 20)} Crea {remaining} análisis más para desbloquear 'Analista de Datos'", unsafe_allow_html=True)
