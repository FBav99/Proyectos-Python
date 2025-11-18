from utils.ui.icon_system import get_icon, replace_emojis
"""
Migration script to transfer data from SQLite to Supabase PostgreSQL
This script helps migrate existing users and data from SQLite to Supabase
"""

import json
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.database import db_manager, init_database
from core.auth_service import auth_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_export_file(export_file):
    """Load exported JSON data"""
    if not os.path.exists(export_file):
        logger.error(f"Export file not found: {export_file}")
        return None
    
    try:
        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded export file: {export_file}")
        return data
    except Exception as e:
        logger.error(f"Error loading export file: {e}")
        return None

def migrate_users_to_supabase(users_data):
    """Migrate users from export to Supabase"""
    if not users_data:
        logger.warning("No users data to migrate")
        return 0
    
    migrated_count = 0
    skipped_count = 0
    
    logger.info(f"Migrating {len(users_data)} users to Supabase...")
    
    # Switch to Supabase mode temporarily for migration
    original_db_type = db_manager.db_type
    if db_manager.db_type != "supabase":
        logger.warning("⚠️  Database type is not 'supabase'. Make sure Supabase is configured in Streamlit secrets.")
        logger.warning("   Set db_type = 'supabase' in your Streamlit Cloud secrets")
        return 0
    
    for user_data in users_data:
        try:
            username = user_data['username']
            email = user_data['email']
            
            # Check if user already exists
            if auth_service.user_exists(username, email):
                logger.info(f"User {username} already exists, skipping")
                skipped_count += 1
                continue
            
            # Note: We can't migrate passwords because they're hashed
            # Users will need to reset their passwords
            # For now, create a default temporary password
            temp_password = "TempPassword123!"  # Users should change this
            
            # Register user
            success, message = auth_service.register_user(
                username=username,
                email=email,
                password=temp_password,  # Temporary password
                first_name=user_data.get('first_name', 'User'),
                last_name=user_data.get('last_name', '')
            )
            
            if success:
                logger.info(f"{get_icon("✅", 20)} Migrated user: {username}")
                migrated_count += 1
            else:
                logger.error(f"{get_icon("❌", 20)} Failed to migrate user {username}: {message}")
        
        except Exception as e:
            logger.error(f"Error migrating user {user_data.get('username', 'unknown')}: {e}")
    
    logger.info(f"{get_icon("✅", 20)} Migrated {migrated_count} users, skipped {skipped_count} existing users")
    return migrated_count

def migrate_progress_to_supabase(progress_data):
    """Migrate user progress to Supabase"""
    if not progress_data:
        logger.warning("No progress data to migrate")
        return 0
    
    migrated_count = 0
    
    logger.info(f"Migrating {len(progress_data)} user progress records...")
    
    try:
        from core.progress_tracker import progress_tracker
        
        for progress in progress_data:
            try:
                user_id = progress['user_id']
                
                # Update progress
                progress_tracker.update_progress(
                    user_id,
                    nivel1_completed=progress.get('nivel1_completed', False),
                    nivel2_completed=progress.get('nivel2_completed', False),
                    nivel3_completed=progress.get('nivel3_completed', False),
                    nivel4_completed=progress.get('nivel4_completed', False),
                    total_time_spent=progress.get('total_time_spent', 0),
                    data_analyses_created=progress.get('data_analyses_created', 0)
                )
                
                migrated_count += 1
                logger.info(f"{get_icon("✅", 20)} Migrated progress for user_id: {user_id}")
            
            except Exception as e:
                logger.error(f"Error migrating progress for user_id {progress.get('user_id')}: {e}")
        
        logger.info(f"{get_icon("✅", 20)} Migrated {migrated_count} progress records")
        return migrated_count
    
    except ImportError:
        logger.error("Progress tracker not available")
        return 0

def migrate_quiz_attempts_to_supabase(quiz_attempts_data):
    """Migrate quiz attempts to Supabase"""
    if not quiz_attempts_data:
        logger.warning("No quiz attempts data to migrate")
        return 0
    
    migrated_count = 0
    
    logger.info(f"Migrating {len(quiz_attempts_data)} quiz attempts...")
    
    try:
        with db_manager.get_connection() as conn:
            # Use appropriate cursor based on database type
            if db_manager.db_type == "supabase":
                cursor = conn.cursor()
                param_placeholder = "%s"
            else:
                cursor = conn.cursor()
                param_placeholder = "?"
            
            for attempt in quiz_attempts_data:
                try:
                    # Check if attempt already exists
                    # Note: We'll skip the check for now and let PostgreSQL handle uniqueness
                    
                    # Insert quiz attempt
                    if db_manager.db_type == "supabase":
                        # PostgreSQL syntax
                        cursor.execute("""
                            INSERT INTO quiz_attempts 
                            (user_id, level, score, total_questions, percentage, passed, completed_at, time_taken)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING
                        """, (
                            attempt['user_id'],
                            attempt['level'],
                            attempt['score'],
                            attempt['total_questions'],
                            attempt['percentage'],
                            attempt['passed'],
                            attempt['completed_at'],
                            attempt.get('time_taken')
                        ))
                    else:
                        # SQLite syntax
                        cursor.execute("""
                            INSERT OR IGNORE INTO quiz_attempts 
                            (user_id, level, score, total_questions, percentage, passed, completed_at, time_taken)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            attempt['user_id'],
                            attempt['level'],
                            attempt['score'],
                            attempt['total_questions'],
                            attempt['percentage'],
                            attempt['passed'],
                            attempt['completed_at'],
                            attempt.get('time_taken')
                        ))
                    
                    migrated_count += 1
                
                except Exception as e:
                    logger.error(f"Error migrating quiz attempt {attempt.get('id')}: {e}")
            
            conn.commit()
        
        logger.info(f"{get_icon("✅", 20)} Migrated {migrated_count} quiz attempts")
        return migrated_count
    
    except Exception as e:
        logger.error(f"Error migrating quiz attempts: {e}")
        return 0

def main():
    """Main migration function"""
    logger.info(replace_emojis("🚀 Starting SQLite to Supabase migration..."))
    
    # Check if Supabase is configured
    if db_manager.db_type != "supabase":
        logger.error(replace_emojis("❌ Supabase is not configured!"))
        logger.error("   Please set db_type = 'supabase' in Streamlit Cloud secrets")
        logger.error("   And add your Supabase connection string")
        return False
    
    # Check if export file exists
    export_file = None
    if len(sys.argv) > 1:
        export_file = sys.argv[1]
    else:
        # Look for latest export file
        backups_dir = Path("backups")
        if backups_dir.exists():
            export_files = sorted(backups_dir.glob("sqlite_export_*.json"), reverse=True)
            if export_files:
                export_file = str(export_files[0])
                logger.info(f"Using latest export file: {export_file}")
    
    if not export_file:
        logger.error(replace_emojis("❌ No export file found!"))
        logger.error("   Please run export_sqlite_data.py first to create a backup")
        logger.error("   Or provide export file path as argument:")
        logger.error("   python migrate_sqlite_to_supabase.py backups/export_file.json")
        return False
    
    # Load exported data
    logger.info(replace_emojis("📄 Loading exported data..."))
    data = load_export_file(export_file)
    if not data:
        return False
    
    # Initialize Supabase database
    logger.info("🗄️ Initializing Supabase database...")
    try:
        init_database()
        logger.info(replace_emojis("✅ Database initialized"))
    except Exception as e:
        logger.error(f"{get_icon("❌", 20)} Database initialization failed: {e}")
        return False
    
    # Migrate users
    logger.info("👥 Migrating users...")
    users_migrated = migrate_users_to_supabase(data.get('users', []))
    
    # Migrate progress
    logger.info(replace_emojis("📊 Migrating user progress..."))
    progress_migrated = migrate_progress_to_supabase(data.get('user_progress', []))
    
    # Migrate quiz attempts
    logger.info(replace_emojis("📝 Migrating quiz attempts..."))
    attempts_migrated = migrate_quiz_attempts_to_supabase(data.get('quiz_attempts', []))
    
    logger.info(replace_emojis("🎉 Migration completed!"))
    logger.info(f"   - Users: {users_migrated}")
    logger.info(f"   - Progress records: {progress_migrated}")
    logger.info(f"   - Quiz attempts: {attempts_migrated}")
    logger.info("")
    logger.info("⚠️  IMPORTANT: Users will need to reset their passwords!")
    logger.info("   They can use the password recovery page to set a new password.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

