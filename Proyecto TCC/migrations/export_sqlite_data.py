"""
Export SQLite data to JSON format for backup and migration
This script exports all user data from SQLite database to a JSON file
that can be used to restore data or migrate to Supabase
"""

import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.database import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_users():
    """Export all users from database"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, username, email, first_name, last_name, 
                       created_at, last_login, is_active, email_verified
                FROM users
                ORDER BY id
            """)
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row['id'],
                    'username': row['username'],
                    'email': row['email'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'created_at': row['created_at'],
                    'last_login': row['last_login'],
                    'is_active': bool(row['is_active']),
                    'email_verified': bool(row.get('email_verified', False))
                })
            
            return users
    except Exception as e:
        logger.error(f"Error exporting users: {e}")
        return []

def export_user_progress():
    """Export all user progress from database"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.execute("""
                SELECT user_id, nivel1_completed, nivel2_completed, 
                       nivel3_completed, nivel4_completed, total_time_spent,
                       data_analyses_created, last_updated
                FROM user_progress
                ORDER BY user_id
            """)
            
            progress = []
            for row in cursor.fetchall():
                progress.append({
                    'user_id': row['user_id'],
                    'nivel1_completed': bool(row['nivel1_completed']),
                    'nivel2_completed': bool(row['nivel2_completed']),
                    'nivel3_completed': bool(row['nivel3_completed']),
                    'nivel4_completed': bool(row['nivel4_completed']),
                    'total_time_spent': row['total_time_spent'],
                    'data_analyses_created': row['data_analyses_created'],
                    'last_updated': row['last_updated']
                })
            
            return progress
    except Exception as e:
        logger.error(f"Error exporting user progress: {e}")
        return []

def export_quiz_attempts():
    """Export all quiz attempts from database"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, user_id, level, score, total_questions, 
                       percentage, passed, completed_at, time_taken
                FROM quiz_attempts
                ORDER BY id
            """)
            
            attempts = []
            for row in cursor.fetchall():
                attempts.append({
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'level': row['level'],
                    'score': row['score'],
                    'total_questions': row['total_questions'],
                    'percentage': float(row['percentage']) if row['percentage'] else 0.0,
                    'passed': bool(row['passed']),
                    'completed_at': row['completed_at'],
                    'time_taken': row['time_taken']
                })
            
            return attempts
    except Exception as e:
        logger.error(f"Error exporting quiz attempts: {e}")
        return []

def export_all_data(output_file=None):
    """Export all data from SQLite database to JSON file"""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"backups/sqlite_export_{timestamp}.json"
    
    # Create backups directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    logger.info("🔄 Starting SQLite data export...")
    
    # Export all data
    data = {
        'export_date': datetime.now().isoformat(),
        'export_type': 'sqlite_full',
        'users': export_users(),
        'user_progress': export_user_progress(),
        'quiz_attempts': export_quiz_attempts()
    }
    
    # Write to JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Data exported successfully to: {output_file}")
        logger.info(f"   - Users: {len(data['users'])}")
        logger.info(f"   - User Progress: {len(data['user_progress'])}")
        logger.info(f"   - Quiz Attempts: {len(data['quiz_attempts'])}")
        
        return output_file
    except Exception as e:
        logger.error(f"❌ Error writing export file: {e}")
        return None

def main():
    """Main export function"""
    logger.info("🚀 Starting SQLite data export...")
    
    # Check if database exists
    if not db_manager.check_database_exists():
        logger.error("❌ Database does not exist")
        return False
    
    # Export data
    output_file = export_all_data()
    
    if output_file:
        logger.info("🎉 Export completed successfully!")
        logger.info(f"📁 Backup file: {output_file}")
        logger.info("💡 You can use this file to restore data or migrate to Supabase")
        return True
    else:
        logger.error("❌ Export failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

