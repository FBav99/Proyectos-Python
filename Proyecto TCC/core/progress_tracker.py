"""
Progress tracking service for TCC Data Analysis Platform
Handles user learning progress, level completion, and progress analytics
"""

import streamlit as st
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from core.database import db_manager

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Handles user learning progress tracking"""
    
    def __init__(self):
        self.levels = ['nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4']
    
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Get complete user progress information"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM user_progress WHERE user_id = ?
                """, (user_id,))
                progress = cursor.fetchone()
                
                if not progress:
                    # Create progress record if it doesn't exist
                    self.create_user_progress(user_id)
                    return self.get_user_progress(user_id)
                
                # Convert to dictionary
                progress_dict = dict(progress)
                
                # Add calculated fields
                progress_dict['total_progress'] = self.calculate_total_progress(progress_dict)
                progress_dict['completed_count'] = self.count_completed_levels(progress_dict)
                progress_dict['current_level'] = self.get_current_level(progress_dict)
                
                return progress_dict
                
        except Exception as e:
            logger.error(f"Error getting user progress: {e}")
            return self.get_default_progress()
    
    def create_user_progress(self, user_id: int) -> bool:
        """Create initial progress record for new user"""
        try:
            with db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO user_progress (user_id, last_updated)
                    VALUES (?, ?)
                """, (user_id, datetime.now().isoformat()))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating user progress: {e}")
            return False
    
    def update_user_progress(self, user_id: int, **kwargs) -> bool:
        """Update user progress fields"""
        try:
            # Build update query dynamically
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                # Check if field is a level completion field or other allowed fields
                is_level_field = any(field.startswith(level) for level in self.levels)
                is_allowed_field = field in ['total_time_spent', 'data_analyses_created']
                
                if is_level_field or is_allowed_field:
                    update_fields.append(f"{field} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
            
            # Add timestamp
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
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating user progress: {e}")
            return False
    
    def complete_level(self, user_id: int, level_name: str) -> bool:
        """Mark a level as completed"""
        try:
            if level_name not in self.levels:
                logger.error(f"Invalid level name: {level_name}")
                return False
            
            # Update level completion
            success = self.update_user_progress(
                user_id, 
                **{f"{level_name}_completed": True}
            )
            
            if success:
                # Note: Completion timestamp columns don't exist in current schema
                # Update completion timestamp when schema is updated
                
                # Log completion
                self.log_progress_activity(user_id, 'level_completed', {
                    'level': level_name,
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error completing level: {e}")
            return False
    
    def reset_level_progress(self, user_id: int, level_name: str) -> bool:
        """Reset progress for a specific level"""
        try:
            if level_name not in self.levels:
                logger.error(f"Invalid level name: {level_name}")
                return False
            
            # Reset level completion
            success = self.update_user_progress(
                user_id,
                **{f"{level_name}_completed": False}
            )
            
            if success:
                # Note: Completion timestamp columns don't exist in current schema
                # Clear completion timestamp when schema is updated
                
                # Log reset
                self.log_progress_activity(user_id, 'level_reset', {
                    'level': level_name,
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting level progress: {e}")
            return False
    
    def reset_all_progress(self, user_id: int) -> bool:
        """Reset all level progress for a user"""
        try:
            reset_fields = {}
            for level in self.levels:
                reset_fields[f"{level}_completed"] = False
                # Only reset completion timestamp if the column exists
                # Note: The database schema doesn't include *_completed_at columns yet
            
            success = self.update_user_progress(user_id, **reset_fields)
            
            if success:
                # Log complete reset
                self.log_progress_activity(user_id, 'all_progress_reset', {
                    'timestamp': datetime.now().isoformat()
                })
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting all progress: {e}")
            return False
    
    def update_time_spent(self, user_id: int, minutes: int) -> bool:
        """Update total time spent learning"""
        try:
            # Get current time spent
            current_progress = self.get_user_progress(user_id)
            current_time = current_progress.get('total_time_spent', 0)
            
            # Add new time
            new_time = current_time + minutes
            
            return self.update_user_progress(user_id, total_time_spent=new_time)
            
        except Exception as e:
            logger.error(f"Error updating time spent: {e}")
            return False
    
    def increment_analyses_created(self, user_id: int) -> bool:
        """Increment count of data analyses created"""
        try:
            # Get current count
            current_progress = self.get_user_progress(user_id)
            current_count = current_progress.get('data_analyses_created', 0)
            
            # Increment count
            new_count = current_count + 1
            
            return self.update_user_progress(user_id, data_analyses_created=new_count)
            
        except Exception as e:
            logger.error(f"Error incrementing analyses count: {e}")
            return False
    
    def calculate_total_progress(self, progress_dict: Dict[str, Any]) -> float:
        """Calculate total progress percentage"""
        try:
            completed_count = self.count_completed_levels(progress_dict)
            total_levels = len(self.levels)
            return (completed_count / total_levels) * 100
        except Exception as e:
            logger.error(f"Error calculating total progress: {e}")
            return 0.0
    
    def count_completed_levels(self, progress_dict: Dict[str, Any]) -> int:
        """Count completed levels"""
        try:
            completed = 0
            for level in self.levels:
                if progress_dict.get(f"{level}_completed", False):
                    completed += 1
            return completed
        except Exception as e:
            logger.error(f"Error counting completed levels: {e}")
            return 0
    
    def get_current_level(self, progress_dict: Dict[str, Any]) -> str:
        """Get the current level the user should work on"""
        try:
            for level in self.levels:
                if not progress_dict.get(f"{level}_completed", False):
                    return level
            return "completed"  # All levels completed
        except Exception as e:
            logger.error(f"Error getting current level: {e}")
            return "nivel1"
    
    def get_level_stats(self, user_id: int) -> Dict[str, Any]:
        """Get detailed statistics for all levels"""
        try:
            progress = self.get_user_progress(user_id)
            stats = {}
            
            for level in self.levels:
                completed = progress.get(f"{level}_completed", False)
                completed_at = progress.get(f"{level}_completed_at")
                
                stats[level] = {
                    'completed': completed,
                    'completed_at': completed_at,
                    'status': '✅ Completado' if completed else '⏳ Pendiente'
                }
            
            # Add overall stats
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
    
    def get_default_progress(self) -> Dict[str, Any]:
        """Get default progress structure"""
        default_progress = {
            'user_id': None,
            'last_updated': datetime.now().isoformat(),
            'total_time_spent': 0,
            'data_analyses_created': 0
        }
        
        # Add level fields
        for level in self.levels:
            default_progress[f"{level}_completed"] = False
            default_progress[f"{level}_completed_at"] = None
        
        return default_progress
    
    def log_progress_activity(self, user_id: int, activity_type: str, details: Dict[str, Any]):
        """Log progress-related activities"""
        try:
            # This could be extended to log to a separate progress_activity table
            logger.info(f"Progress activity - User {user_id}: {activity_type} - {details}")
        except Exception as e:
            logger.error(f"Error logging progress activity: {e}")

# Global progress tracker instance
progress_tracker = ProgressTracker()
