"""
Survey System for TCC Data Analysis Platform
Handles initial, level-specific, and final surveys for user feedback
"""

import streamlit as st
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from core.database import db_manager

logger = logging.getLogger(__name__)


def _adapt_query(query: str) -> str:
    """Adjust placeholder style depending on database backend."""
    if db_manager.db_type == "supabase":
        return query.replace("?", "%s")
    return query


class SurveySystem:
    """Handles survey management and responses"""
    
    def __init__(self):
        self.survey_types = {
            'initial': 'Initial Survey',
            'level': 'Level Survey',
            'final': 'Final Survey'
        }
        self._completion_cache: Dict[tuple, bool] = {}
        self._response_cache: Dict[tuple, Dict[str, Any]] = {}
    
    @staticmethod
    def _cache_key(user_id: int, survey_type: str, level: Optional[str]) -> tuple:
        """Create a hashable cache key for survey lookups."""
        return (user_id, survey_type, level or "__NO_LEVEL__")
    
    def _invalidate_cache(self, user_id: int, survey_type: str, level: Optional[str]):
        """Invalidate cached data for a specific survey combination."""
        key = self._cache_key(user_id, survey_type, level)
        self._completion_cache.pop(key, None)
        self._response_cache.pop(key, None)
    
    def _ensure_table_exists(self):
        """Ensure survey_responses table exists"""
        try:
            db_manager.create_survey_responses_table()
        except Exception as e:
            logger.warning(f"Could not create survey_responses table (may already exist): {e}")
    
    def save_survey_response(self, user_id: int, survey_type: str, responses: Dict[str, Any], level: Optional[str] = None) -> bool:
        """Save survey response to database"""
        cache_payload = None
        try:
            # Ensure survey_responses table exists
            self._ensure_table_exists()
            key = self._cache_key(user_id, survey_type, level)
            
            with db_manager.get_connection() as conn:
                # Convert responses to JSON string
                responses_json = json.dumps(responses, ensure_ascii=False)
                
                # Check if survey already exists for this user/type/level
                if db_manager.db_type == "sqlite":
                    if level:
                        cursor = conn.execute("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level = ?
                        """, (user_id, survey_type, level))
                    else:
                        cursor = conn.execute("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level IS NULL
                        """, (user_id, survey_type,))
                    existing = cursor.fetchone()
                else:
                    cursor = conn.cursor()
                    if level:
                        cursor.execute(_adapt_query("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level = ?
                        """), (user_id, survey_type, level))
                    else:
                        cursor.execute(_adapt_query("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level IS NULL
                        """), (user_id, survey_type,))
                    existing = cursor.fetchone()
                
                if existing:
                    # Update existing response
                    if db_manager.db_type == "sqlite":
                        if level:
                            conn.execute("""
                                UPDATE survey_responses 
                                SET responses = ?, completed_at = CURRENT_TIMESTAMP
                                WHERE user_id = ? AND survey_type = ? AND level = ?
                            """, (responses_json, user_id, survey_type, level))
                        else:
                            conn.execute("""
                                UPDATE survey_responses 
                                SET responses = ?, completed_at = CURRENT_TIMESTAMP
                                WHERE user_id = ? AND survey_type = ? AND level IS NULL
                            """, (responses_json, user_id, survey_type,))
                    else:
                        if level:
                            cursor.execute(_adapt_query("""
                                UPDATE survey_responses 
                                SET responses = ?, completed_at = CURRENT_TIMESTAMP
                                WHERE user_id = ? AND survey_type = ? AND level = ?
                            """), (responses_json, user_id, survey_type, level))
                        else:
                            cursor.execute(_adapt_query("""
                                UPDATE survey_responses 
                                SET responses = ?, completed_at = CURRENT_TIMESTAMP
                                WHERE user_id = ? AND survey_type = ? AND level IS NULL
                            """), (responses_json, user_id, survey_type,))
                else:
                    # Insert new response
                    if db_manager.db_type == "sqlite":
                        conn.execute("""
                            INSERT INTO survey_responses (user_id, survey_type, level, responses)
                            VALUES (?, ?, ?, ?)
                        """, (user_id, survey_type, level, responses_json))
                    else:
                        cursor.execute(_adapt_query("""
                            INSERT INTO survey_responses (user_id, survey_type, level, responses)
                            VALUES (?, ?, ?, ?)
                        """), (user_id, survey_type, level, responses_json))
                conn.commit()
                cache_payload = responses_json
                
        except Exception as e:
            logger.error(f"Error saving survey response: {e}")
            return False
        else:
            # Update caches on success
            self._completion_cache[key] = True
            try:
                self._response_cache[key] = json.loads(cache_payload) if cache_payload is not None else responses
            except Exception:
                self._response_cache.pop(key, None)
            return True
    
    def has_completed_survey(self, user_id: int, survey_type: str, level: Optional[str] = None) -> bool:
        """Check if user has completed a specific survey"""
        try:
            # Ensure survey_responses table exists
            self._ensure_table_exists()
            key = self._cache_key(user_id, survey_type, level)
            
            if key in self._completion_cache:
                return self._completion_cache[key]
            
            with db_manager.get_connection() as conn:
                # Use conn.execute for SQLite compatibility
                if db_manager.db_type == "sqlite":
                    if level:
                        cursor = conn.execute("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level = ?
                        """, (user_id, survey_type, level))
                    else:
                        cursor = conn.execute("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level IS NULL
                        """, (user_id, survey_type,))
                else:
                    cursor = conn.cursor()
                    if level:
                        cursor.execute(_adapt_query("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level = ?
                        """), (user_id, survey_type, level))
                    else:
                        cursor.execute(_adapt_query("""
                            SELECT id FROM survey_responses 
                            WHERE user_id = ? AND survey_type = ? AND level IS NULL
                        """), (user_id, survey_type,))
                
                exists = cursor.fetchone() is not None
                self._completion_cache[key] = exists
                if not exists:
                    self._response_cache.pop(key, None)
                return exists
                
        except Exception as e:
            logger.error(f"Error checking survey completion: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def get_survey_response(self, user_id: int, survey_type: str, level: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get user's survey response"""
        try:
            key = self._cache_key(user_id, survey_type, level)
            if key in self._response_cache:
                return self._response_cache[key]
            
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                if level:
                    cursor.execute(_adapt_query("""
                        SELECT responses FROM survey_responses 
                        WHERE user_id = ? AND survey_type = ? AND level = ?
                    """), (user_id, survey_type, level))
                else:
                    cursor.execute(_adapt_query("""
                        SELECT responses FROM survey_responses 
                        WHERE user_id = ? AND survey_type = ? AND level IS NULL
                    """), (user_id, survey_type,))
                
                result = cursor.fetchone()
                
                if result:
                    parsed = json.loads(result[0] if isinstance(result[0], str) else result['responses'])
                    self._completion_cache[key] = True
                    self._response_cache[key] = parsed
                    return parsed
                
                self._completion_cache[key] = False
                self._response_cache.pop(key, None)
                return None
                
        except Exception as e:
            logger.error(f"Error getting survey response: {e}")
            return None
    
    def get_all_survey_responses(self, survey_type: Optional[str] = None) -> list:
        """Get all survey responses (for admin/analytics)"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                if survey_type:
                    cursor.execute(_adapt_query("""
                        SELECT * FROM survey_responses 
                        WHERE survey_type = ?
                        ORDER BY completed_at DESC
                    """), (survey_type,))
                else:
                    cursor.execute(_adapt_query("""
                        SELECT * FROM survey_responses 
                        ORDER BY completed_at DESC
                    """))
                
                results = cursor.fetchall()
                responses = []
                
                for row in results:
                    if isinstance(row, dict):
                        row_dict = dict(row)
                    else:
                        # Convert to dict for SQLite Row objects
                        row_dict = dict(zip([col[0] for col in cursor.description], row))
                    
                    # Parse JSON responses
                    if 'responses' in row_dict:
                        row_dict['responses'] = json.loads(row_dict['responses'])
                    
                    responses.append(row_dict)
                
                return responses
                
        except Exception as e:
            logger.error(f"Error getting all survey responses: {e}")
            return []


# Global survey system instance
survey_system = SurveySystem()

