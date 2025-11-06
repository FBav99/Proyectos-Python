import streamlit as st
import random
from datetime import datetime
from core.auth_config import update_user_progress, check_achievement
from core.database import db_manager

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

def create_quiz(level, username):
    """Create and display a quiz for a specific level"""
    
    st.markdown(f"## 🧠 Quiz - Nivel {level[-1]}")
    st.markdown("### Pon a prueba tus conocimientos")
    
    # Get questions for the level
    questions = QUIZ_QUESTIONS.get(level, [])
    
    if not questions:
        st.error("No hay preguntas disponibles para este nivel.")
        return
    
    # Initialize quiz state
    if f'quiz_{level}_started' not in st.session_state:
        st.session_state[f'quiz_{level}_started'] = False
        st.session_state[f'quiz_{level}_current_question'] = 0
        st.session_state[f'quiz_{level}_score'] = 0
        st.session_state[f'quiz_{level}_answers'] = []
        st.session_state[f'quiz_{level}_completed'] = False
    
    # Start quiz
    if not st.session_state[f'quiz_{level}_started']:
        st.markdown("""
        ### 📋 Instrucciones:
        - Responde 5 preguntas sobre los conceptos aprendidos
        - Cada pregunta tiene 4 opciones, solo una es correcta
        - Obtendrás retroalimentación inmediata
        - Necesitas al menos 3 respuestas correctas para aprobar
        
        **¡Buena suerte! 🍀**
        """)
        
        if st.button("🚀 Comenzar Quiz", type="primary"):
            st.session_state[f'quiz_{level}_started'] = True
            st.rerun()
        return
    
    # Quiz in progress
    if not st.session_state[f'quiz_{level}_completed']:
        current_q = st.session_state[f'quiz_{level}_current_question']
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"### Pregunta {current_q + 1} de {len(questions)}")
            st.markdown(f"**{question['question']}**")
            
            # Show feedback for current question if answer was already confirmed
            if f'quiz_{level}_answered_{current_q}' in st.session_state:
                feedback = st.session_state[f'quiz_{level}_answered_{current_q}']
                if feedback['is_correct']:
                    st.success("🎉 ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: **{feedback['correct_answer']}**")
                
                st.info(f"💡 **Explicación:** {feedback['explanation']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Show button to continue to next question
                    if st.button("➡️ Siguiente Pregunta", type="primary", use_container_width=True):
                        # Move to next question
                        st.session_state[f'quiz_{level}_current_question'] += 1
                        
                        if st.session_state[f'quiz_{level}_current_question'] >= len(questions):
                            st.session_state[f'quiz_{level}_completed'] = True
                        
                        st.rerun()
                with col2:
                    if st.button("🔄 Reiniciar Quiz", use_container_width=True):
                        st.session_state[f'quiz_{level}_started'] = False
                        st.session_state[f'quiz_{level}_current_question'] = 0
                        st.session_state[f'quiz_{level}_score'] = 0
                        st.session_state[f'quiz_{level}_answers'] = []
                        st.session_state[f'quiz_{level}_completed'] = False
                        # Clear all answered flags
                        for i in range(len(questions)):
                            if f'quiz_{level}_answered_{i}' in st.session_state:
                                del st.session_state[f'quiz_{level}_answered_{i}']
                        st.rerun()
            else:
                # Display options
                selected_option = st.radio(
                    "Selecciona tu respuesta:",
                    question['options'],
                    key=f"quiz_{level}_q{current_q}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirmar Respuesta"):
                        # Check answer
                        correct = question['options'].index(selected_option) == question['correct']
                        
                        # Store feedback in session state so it persists after rerun
                        st.session_state[f'quiz_{level}_answered_{current_q}'] = {
                            'is_correct': correct,
                            'correct_answer': question['options'][question['correct']],
                            'explanation': question['explanation']
                        }
                        
                        if correct:
                            st.session_state[f'quiz_{level}_score'] += 1
                        
                        # Store answer
                        st.session_state[f'quiz_{level}_answers'].append({
                            'question': question['question'],
                            'selected': selected_option,
                            'correct': question['options'][question['correct']],
                            'is_correct': correct,
                            'explanation': question['explanation']
                        })
                        
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Reiniciar Quiz"):
                        st.session_state[f'quiz_{level}_started'] = False
                        st.session_state[f'quiz_{level}_current_question'] = 0
                        st.session_state[f'quiz_{level}_score'] = 0
                        st.session_state[f'quiz_{level}_answers'] = []
                        st.session_state[f'quiz_{level}_completed'] = False
                        # Clear all answered flags
                        for i in range(len(questions)):
                            if f'quiz_{level}_answered_{i}' in st.session_state:
                                del st.session_state[f'quiz_{level}_answered_{i}']
                        st.rerun()
    
    # Quiz completed
    else:
        show_quiz_results(level, username, questions)

def show_quiz_results(level, username, questions):
    """Show quiz results and achievements"""
    
    score = st.session_state[f'quiz_{level}_score']
    total_questions = len(questions)
    percentage = (score / total_questions) * 100
    passed = score >= 3
    
    st.markdown("## 🎯 Resultados del Quiz")
    
    # Score display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Puntuación", f"{score}/{total_questions}")
    with col2:
        st.metric("Porcentaje", f"{percentage:.1f}%")
    with col3:
        status = "✅ Aprobado" if passed else "❌ No Aprobado"
        st.metric("Estado", status)
    
    # Progress bar
    st.progress(percentage / 100)
    
    # Results message
    if passed:
        st.success("🎉 ¡Felicitaciones! Has aprobado el quiz.")
        st.session_state[f'quiz_{level}_passed'] = True
        
        # Check for perfect score achievement
        if score == total_questions:
            new_achievements = check_achievement(username, 'quiz_perfect')
            if new_achievements:
                st.balloons()
                st.success("🏆 ¡Logro desbloqueado: Maestro del Quiz!")
    else:
        st.error("📚 Necesitas al menos 3 respuestas correctas para aprobar. ¡Sigue estudiando!")
        st.session_state[f'quiz_{level}_passed'] = False
    
    # Detailed results
    st.markdown("### 📋 Respuestas Detalladas")
    
    for i, answer in enumerate(st.session_state[f'quiz_{level}_answers']):
        with st.expander(f"Pregunta {i + 1}: {answer['question']}"):
            if answer['is_correct']:
                st.success(f"✅ Tu respuesta: {answer['selected']}")
            else:
                st.error(f"❌ Tu respuesta: {answer['selected']}")
                st.info(f"✅ Respuesta correcta: {answer['correct']}")
            
            st.markdown(f"💡 **Explicación:** {answer['explanation']}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Intentar de Nuevo"):
            st.session_state[f'quiz_{level}_started'] = False
            st.session_state[f'quiz_{level}_current_question'] = 0
            st.session_state[f'quiz_{level}_score'] = 0
            st.session_state[f'quiz_{level}_answers'] = []
            st.session_state[f'quiz_{level}_completed'] = False
            st.rerun()
    
    with col2:
        if st.button("🏠 Volver al Nivel"):
            st.session_state[f'quiz_{level}_started'] = False
            st.session_state[f'quiz_{level}_completed'] = False
            st.rerun()
    
    # Save quiz attempt to database
    save_quiz_attempt(level, username, score, total_questions, percentage, passed, st.session_state[f'quiz_{level}_answers'])
    
    # Update user progress
    if passed:
        update_user_progress(username, quiz_scores={level: percentage})
        
        # Check for level completion achievement
        if level == 'nivel1' and not st.session_state.get('nivel1_completed', False):
            new_achievements = check_achievement(username, 'level_completion')
            if new_achievements:
                st.success("🏆 ¡Logro desbloqueado: Primer Nivel Completado!")

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
    
    st.markdown("## 🏆 Logros Desbloqueados")
    
    if not achievements:
        st.info("🎯 ¡Completa niveles y quizzes para desbloquear logros!")
        return
    
    achievement_info = {
        'first_level': {
            'title': '🎓 Primer Paso',
            'description': 'Completaste tu primer nivel de aprendizaje',
            'icon': '🎓'
        },
        'all_levels': {
            'title': '🏆 Maestro del Análisis',
            'description': 'Completaste todos los niveles del curso',
            'icon': '🏆'
        },
        'quiz_master': {
            'title': '🧠 Maestro del Quiz',
            'description': 'Obtuviste puntuación perfecta en un quiz',
            'icon': '🧠'
        },
        'data_analyst': {
            'title': '📊 Analista de Datos',
            'description': 'Creaste 5 análisis de datos',
            'icon': '📊'
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
    st.markdown("### 🎯 Próximos Logros")
    
    if 'first_level' not in achievements:
        st.info("🎓 Completa el Nivel 1 para desbloquear 'Primer Paso'")
    
    if 'quiz_master' not in achievements:
        st.info("🧠 Obtén puntuación perfecta en cualquier quiz para desbloquear 'Maestro del Quiz'")
    
    if 'data_analyst' not in achievements:
        analyses_count = progress.get('data_analyses_created', 0)
        remaining = 5 - analyses_count
        st.info(f"📊 Crea {remaining} análisis más para desbloquear 'Analista de Datos'")
