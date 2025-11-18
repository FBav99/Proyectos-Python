from utils.ui.icon_system import get_icon, replace_emojis
"""
Progression tracking and achievement system for learning levels
"""

def get_level_achievements():
    """Get achievement information for each level"""
    return {
        'nivel0': {
            'title': replace_emojis('🌟 Conceptos de Datos'),
            'achievement': 'Fundamentos de Datos',
            'description': 'Has aprendido qué son los datos, sus tipos y cómo se organizan',
            'skills_gained': [
                'Identificar tipos de datos (numéricos, texto, fechas)',
                'Entender la estructura de tablas de datos',
                'Reconocer la importancia del análisis de datos'
            ],
            'next_level_preview': 'En el Nivel 1 aprenderás a preparar y cargar datos correctamente'
        },
        'nivel1': {
            'title': replace_emojis('📚 Preparación de Datos'),
            'achievement': 'Especialista en Carga de Datos',
            'description': 'Dominas la preparación y carga de archivos de datos',
            'skills_gained': [
                'Elegir formatos de archivo apropiados',
                'Estructurar datos correctamente',
                'Cargar y verificar datos sin errores',
                'Identificar problemas de calidad de datos'
            ],
            'next_level_preview': 'En el Nivel 2 aprenderás a filtrar y organizar información específica'
        },
        'nivel2': {
            'title': replace_emojis('🔍 Filtros y Organización'),
            'achievement': 'Experto en Filtros',
            'description': 'Sabes usar filtros para encontrar exactamente la información que necesitas',
            'skills_gained': [
                'Aplicar filtros de fecha para períodos específicos',
                'Filtrar por categorías y regiones',
                'Usar filtros numéricos con deslizadores',
                'Combinar múltiples filtros efectivamente'
            ],
            'next_level_preview': 'En el Nivel 3 aprenderás a calcular métricas y KPIs importantes'
        },
        'nivel3': {
            'title': replace_emojis('📊 Métricas y KPIs'),
            'achievement': 'Analista de Métricas',
            'description': 'Puedes calcular, interpretar y usar métricas para tomar decisiones',
            'skills_gained': [
                'Identificar métricas clave para el negocio',
                'Calcular KPIs importantes',
                'Interpretar tendencias y patrones',
                'Usar métricas para tomar decisiones informadas'
            ],
            'next_level_preview': 'En el Nivel 4 aprenderás a crear visualizaciones avanzadas y dashboards'
        },
        'nivel4': {
            'title': replace_emojis('🚀 Análisis Avanzado'),
            'achievement': 'Experto en Análisis de Datos',
            'description': 'Eres capaz de crear análisis complejos y dashboards profesionales',
            'skills_gained': [
                'Crear cálculos personalizados avanzados',
                'Generar visualizaciones interactivas',
                'Diseñar dashboards profesionales',
                'Comunicar insights de manera efectiva'
            ],
            'next_level_preview': '¡Felicidades! Has completado todos los niveles. Ahora puedes crear tus propios dashboards'
        }
    }

def get_progression_summary(user_progress):
    """Get a summary of user's progression across all levels"""
    achievements = get_level_achievements()
    completed_levels = []
    total_skills = 0
    
    for level, is_completed in user_progress.items():
        if is_completed and level in achievements:
            completed_levels.append(level)
            total_skills += len(achievements[level]['skills_gained'])
    
    return {
        'completed_levels': completed_levels,
        'total_skills_learned': total_skills,
        'completion_percentage': (len(completed_levels) / 5) * 100,
        'current_level': get_current_level(user_progress),
        'next_milestone': get_next_milestone(user_progress)
    }

def get_current_level(user_progress):
    """Determine the current level the user should work on"""
    level_order = ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']
    
    for level in level_order:
        if not user_progress.get(level, False):
            return level
    
    return 'completed'  # All levels completed

def get_next_milestone(user_progress):
    """Get the next milestone the user should aim for"""
    current_level = get_current_level(user_progress)
    achievements = get_level_achievements()
    
    if current_level == 'completed':
        return {
            'title': replace_emojis('🎉 ¡Curso Completado!'),
            'description': 'Has dominado todos los conceptos de análisis de datos',
            'action': 'Crear tu propio dashboard profesional'
        }
    
    if current_level in achievements:
        return {
            'title': f'{get_icon("🎯", 20)} Siguiente: {achievements[current_level]["title"]}',
            'description': achievements[current_level]['next_level_preview'],
            'action': f'Completar el {current_level.replace("nivel", "Nivel ")}'
        }
    
    return {
        'title': replace_emojis('🚀 Comienza tu viaje'),
        'description': 'Aprende los fundamentos del análisis de datos',
        'action': 'Comenzar con el Nivel 0'
    }

def get_achievement_badge(level):
    """Get achievement badge information for a level"""
    achievements = get_level_achievements()
    
    if level not in achievements:
        return None
    
    badge_colors = {
        'nivel0': '#FFD700',  # Gold
        'nivel1': '#C0C0C0',  # Silver
        'nivel2': '#CD7F32',  # Bronze
        'nivel3': '#4CAF50',  # Green
        'nivel4': '#2196F3'   # Blue
    }
    
    return {
        'title': achievements[level]['achievement'],
        'color': badge_colors.get(level, '#666666'),
        'icon': achievements[level]['title'].split()[0]  # Get the emoji
    }

def get_data_quality_insights(level, data_type):
    """Get insights about data quality for each level"""
    insights = {
        'nivel0': {
            'clean': {
                'title': 'Datos Organizados',
                'description': 'Datos limpios y bien estructurados para aprender conceptos básicos',
                'quality_score': '100%',
                'issues': 'Ninguno - Datos perfectos para aprendizaje'
            }
        },
        'nivel1': {
            'dirty': {
                'title': 'Datos Sin Procesar',
                'description': 'Datos con problemas comunes que necesitan preparación',
                'quality_score': '75%',
                'issues': 'Valores faltantes, duplicados, inconsistencias de formato'
            }
        },
        'nivel2': {
            'clean': {
                'title': 'Datos Preparados',
                'description': 'Datos limpios y listos para aplicar filtros',
                'quality_score': '95%',
                'issues': 'Mínimos - Datos optimizados para filtrado'
            }
        },
        'nivel3': {
            'clean': {
                'title': 'Datos Optimizados',
                'description': 'Datos de alta calidad para cálculos precisos',
                'quality_score': '98%',
                'issues': 'Ninguno - Datos perfectos para métricas'
            }
        },
        'nivel4': {
            'clean': {
                'title': 'Datos Profesionales',
                'description': 'Datos de nivel empresarial para análisis avanzados',
                'quality_score': '100%',
                'issues': 'Ninguno - Datos de calidad premium'
            }
        }
    }
    
    return insights.get(level, {}).get(data_type, {
        'title': 'Datos de Ejemplo',
        'description': 'Datos para demostración',
        'quality_score': '90%',
        'issues': 'Datos de muestra'
    })
