from utils.ui.icon_system import get_icon, replace_emojis
"""
Reset database - Wipe all data and start fresh
Use this to start with a clean database
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.database import db_manager, init_database, DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_sqlite_database():
    """Delete SQLite database file to start fresh"""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            logger.info(f"{get_icon("✅", 20)} Deleted SQLite database: {DB_PATH}")
            return True
        else:
            logger.info("ℹ️  SQLite database doesn't exist, nothing to delete")
            return True
    except Exception as e:
        logger.error(f"{get_icon("❌", 20)} Error deleting database: {e}")
        return False

def reset_supabase_database():
    """Drop all tables in Supabase to start fresh"""
    try:
        if db_manager.db_type != "supabase":
            logger.warning("Not using Supabase, skipping Supabase reset")
            return False
        
        logger.warning("⚠️  Resetting Supabase will DELETE ALL DATA!")
        logger.warning("This will drop all tables. Make sure you have a backup if needed.")
        
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Drop all tables in reverse order (to handle foreign keys)
            tables_to_drop = [
                'quiz_answers',
                'quiz_attempts',
                'user_progress',
                'user_sessions',
                'users',
                'uploaded_files',
                'file_analysis_sessions',
                'dashboards',
                'dashboard_components',
                'user_activity_log',
                'rate_limiting'
            ]
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    logger.info(f"  Dropped table: {table}")
                except Exception as e:
                    logger.debug(f"  Could not drop {table}: {e}")
            
            conn.commit()
            logger.info(replace_emojis("✅ Supabase database reset complete"))
            return True
    
    except Exception as e:
        logger.error(f"{get_icon("❌", 20)} Error resetting Supabase: {e}")
        return False

def main():
    """Main reset function"""
    logger.info(replace_emojis("🔄 Starting database reset..."))
    
    # Check database type
    db_type = db_manager.db_type
    logger.info(f"Database type: {db_type}")
    
    if db_type == "supabase":
        logger.warning("⚠️  WARNING: You are about to DELETE ALL DATA from Supabase!")
        response = input("Type 'RESET' to confirm: ")
        if response != "RESET":
            logger.info(replace_emojis("❌ Reset cancelled"))
            return False
        
        success = reset_supabase_database()
    else:
        logger.info("Resetting SQLite database...")
        success = reset_sqlite_database()
    
    if success:
        logger.info(replace_emojis("🔄 Reinitializing database with fresh tables..."))
        try:
            init_database()
            logger.info(replace_emojis("✅ Database reset and reinitialized successfully!"))
            logger.info(replace_emojis("🎉 You now have a clean, empty database"))
            return True
        except Exception as e:
            logger.error(f"{get_icon("❌", 20)} Error reinitializing database: {e}")
            return False
    else:
        logger.error(replace_emojis("❌ Reset failed"))
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

