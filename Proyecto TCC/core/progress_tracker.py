# Nombre del Archivo: progress_tracker.py
# Descripción: Servicio de seguimiento de progreso para la plataforma de análisis de datos TCC - Maneja progreso de aprendizaje, completación de niveles y análisis de progreso
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

from utils.ui.icon_system import get_icon, replace_emojis

import streamlit as st
import logging
import copy
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from core.database import db_manager

logger = logging.getLogger(__name__)

# Clase - Rastreador de Progreso
class ProgressTracker:
    """Maneja el seguimiento del progreso de aprendizaje del usuario"""
    
    def __init__(self):
        self.levels = ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']
        self._cache: Dict[int, Dict[str, Any]] = {}
    
    # Cache - Invalidar Cache de Progreso
    def _invalidate_cache(self, user_id: int):
        """Remover progreso en caché para un usuario."""
        self._cache.pop(user_id, None)
    
    # Consulta - Obtener Progreso de Usuario
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Obtener información completa del progreso del usuario"""
        try:
            if user_id in self._cache:
                return copy.deepcopy(self._cache[user_id])
            
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM user_progress WHERE user_id = ?
                """, (user_id,))
                progress = cursor.fetchone()
                
                if not progress:
                    # Base de Datos - Crear registro de progreso si no existe
                    self.create_user_progress(user_id)
                    return self.get_user_progress(user_id)
                
                # Conversion - Convertir a diccionario
                progress_dict = dict(progress)
                
                # Calculo - Agregar campos calculados
                progress_dict['total_progress'] = self.calculate_total_progress(progress_dict)
                progress_dict['completed_count'] = self.count_completed_levels(progress_dict)
                progress_dict['current_level'] = self.get_current_level(progress_dict)
                
                self._cache[user_id] = copy.deepcopy(progress_dict)
                return copy.deepcopy(progress_dict)
                
        except Exception as e:
            logger.error(f"Error getting user progress: {e}")
            default_progress = self.get_default_progress()
            self._cache[user_id] = copy.deepcopy(default_progress)
            return default_progress
    
    # Creacion - Crear Registro de Progreso
    def create_user_progress(self, user_id: int) -> bool:
        """Crear registro de progreso inicial para nuevo usuario"""
        try:
            with db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO user_progress (user_id, last_updated)
                    VALUES (?, ?)
                """, (user_id, datetime.now().isoformat()))
                conn.commit()
            self._invalidate_cache(user_id)
            return True
        except Exception as e:
            logger.error(f"Error creating user progress: {e}")
            return False
    
    # Actualizacion - Actualizar Progreso de Usuario
    def update_user_progress(self, user_id: int, **kwargs) -> bool:
        """Actualizar campos de progreso del usuario"""
        try:
            # Consulta - Construir consulta de actualización dinámicamente
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                # Validacion - Verificar si el campo es de completación de nivel u otros campos permitidos
                is_level_field = any(field.startswith(level) for level in self.levels)
                is_allowed_field = field in ['total_time_spent', 'data_analyses_created']
                
                if is_level_field or is_allowed_field:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
            
            # Timestamp - Agregar timestamp
            update_fields.append("last_updated = ?")
            values.append(datetime.now().isoformat())
            values.append(user_id)
            
            query = f"""
                UPDATE user_progress 
                SET {', '.join(update_fields)}
                WHERE user_id = ?
            """
            
            with db_manager.get_connection() as conn:
                conn.execute(query, values)
                conn.commit()
            
            self._invalidate_cache(user_id)
            return True
            
        except Exception as e:
            logger.error(f"Error updating user progress: {e}")
            return False
    
    # Progreso - Completar Nivel
    def complete_level(self, user_id: int, level_name: str) -> bool:
        """Marcar un nivel como completado"""
        try:
            if level_name not in self.levels:
                logger.error(f"Invalid level name: {level_name}")
                return False
            
            # Actualizacion - Actualizar completación de nivel
            success = self.update_user_progress(
                user_id, 
                **{f"{level_name}_completed": True}
            )
            
            if success:
                # Nota - Las columnas de timestamp de completación no existen en el esquema actual
                # Actualizar timestamp de completación cuando se actualice el esquema
                
                # Logging - Registrar completación
                self.log_progress_activity(user_id, 'level_completed', {
                    'level': level_name,
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error completing level: {e}")
            return False
    
    # Progreso - Reiniciar Progreso de Nivel
    def reset_level_progress(self, user_id: int, level_name: str) -> bool:
        """Reiniciar progreso para un nivel específico"""
        try:
            if level_name not in self.levels:
                logger.error(f"Invalid level name: {level_name}")
                return False
            
            # Actualizacion - Reiniciar completación de nivel
            success = self.update_user_progress(
                user_id,
                **{f"{level_name}_completed": False}
            )
            
            if success:
                # Nota - Las columnas de timestamp de completación no existen en el esquema actual
                # Limpiar timestamp de completación cuando se actualice el esquema
                
                # Logging - Registrar reinicio
                self.log_progress_activity(user_id, 'level_reset', {
                    'level': level_name,
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting level progress: {e}")
            return False
    
    # Progreso - Reiniciar Todo el Progreso
    def reset_all_progress(self, user_id: int) -> bool:
        """Reiniciar todo el progreso de niveles para un usuario"""
        try:
            reset_fields = {}
            for level in self.levels:
                reset_fields[f"{level}_completed"] = False
                # Nota - Solo reiniciar timestamp de completación si la columna existe
                # Nota - El esquema de base de datos aún no incluye columnas *_completed_at
            
            success = self.update_user_progress(user_id, **reset_fields)
            
            if success:
                # Logging - Registrar reinicio completo
                self.log_progress_activity(user_id, 'all_progress_reset', {
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting all progress: {e}")
            return False
    
    # Actualizacion - Actualizar Tiempo de Estudio
    def update_time_spent(self, user_id: int, minutes: int) -> bool:
        """Actualizar tiempo total de aprendizaje"""
        try:
            # Consulta - Obtener tiempo actual gastado
            current_progress = self.get_user_progress(user_id)
            current_time = current_progress.get('total_time_spent', 0)
            
            # Calculo - Agregar nuevo tiempo
            new_time = current_time + minutes
            
            return self.update_user_progress(user_id, total_time_spent=new_time)
            
        except Exception as e:
            logger.error(f"Error updating time spent: {e}")
            return False
    
    # Contador - Incrementar Analisis Creados
    def increment_analyses_created(self, user_id: int) -> bool:
        """Incrementar contador de análisis de datos creados"""
        try:
            # Consulta - Obtener contador actual
            current_progress = self.get_user_progress(user_id)
            current_count = current_progress.get('data_analyses_created', 0)
            
            # Calculo - Incrementar contador
            new_count = current_count + 1
            
            return self.update_user_progress(user_id, data_analyses_created=new_count)
            
        except Exception as e:
            logger.error(f"Error incrementing analyses count: {e}")
            return False
    
    # Calculo - Calcular Progreso Total
    def calculate_total_progress(self, progress_dict: Dict[str, Any]) -> float:
        """Calcular porcentaje de progreso total"""
        try:
            completed_count = self.count_completed_levels(progress_dict)
            total_levels = len(self.levels)
            return (completed_count / total_levels) * 100
        except Exception as e:
            logger.error(f"Error calculating total progress: {e}")
            return 0.0
    
    # Contador - Contar Niveles Completados
    def count_completed_levels(self, progress_dict: Dict[str, Any]) -> int:
        """Contar niveles completados"""
        try:
            completed = 0
            for level in self.levels:
                if progress_dict.get(f"{level}_completed", False):
                    completed += 1
            return completed
        except Exception as e:
            logger.error(f"Error counting completed levels: {e}")
            return 0
    
    # Consulta - Obtener Nivel Actual
    def get_current_level(self, progress_dict: Dict[str, Any]) -> str:
        """Obtener el nivel actual en el que el usuario debe trabajar"""
        try:
            for level in self.levels:
                if not progress_dict.get(f"{level}_completed", False):
                    return level
            return "completed"  # All levels completed
        except Exception as e:
            logger.error(f"Error getting current level: {e}")
            return "nivel1"
    
    # Estadisticas - Obtener Estadisticas de Niveles
    def get_level_stats(self, user_id: int) -> Dict[str, Any]:
        """Obtener estadísticas detalladas para todos los niveles"""
        try:
            progress = self.get_user_progress(user_id)
            stats = {}
            
            for level in self.levels:
                completed = progress.get(f"{level}_completed", False)
                completed_at = progress.get(f"{level}_completed_at")
                
                stats[level] = {
                    'completed': completed,
                    'completed_at': completed_at,
                    'status': replace_emojis('✅ Completado') if completed else '⏳ Pendiente'
                }
            
            # Estadisticas - Agregar estadísticas generales
            stats['overall'] = {
                'total_progress': progress.get('total_progress', 0),
                'completed_count': progress.get('completed_count', 0),
                'current_level': progress.get('current_level', 'nivel1'),
                'total_time': progress.get('total_time_spent', 0),
                'analyses_created': progress.get('data_analyses_created', 0)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting level stats: {e}")
            return {}
    
    # Inicializacion - Obtener Progreso por Defecto
    def get_default_progress(self) -> Dict[str, Any]:
        """Obtener estructura de progreso por defecto"""
        default_progress = {
            'user_id': None,
            'last_updated': datetime.now().isoformat(),
            'total_time_spent': 0,
            'data_analyses_created': 0
        }
        
        # Inicializacion - Agregar campos de nivel
        for level in self.levels:
            default_progress[f"{level}_completed"] = False
            default_progress[f"{level}_completed_at"] = None
        
        return default_progress
    
    # Logging - Registrar Actividad de Progreso
    def log_progress_activity(self, user_id: int, activity_type: str, details: Dict[str, Any]):
        """Registrar actividades relacionadas con progreso"""
        try:
            # Nota - Esto podría extenderse para registrar en una tabla separada progress_activity
            logger.info(f"Progress activity - User {user_id}: {activity_type} - {details}")
        except Exception as e:
            logger.error(f"Error logging progress activity: {e}")

# Instancia - Instancia Global de Rastreador de Progreso
progress_tracker = ProgressTracker()
