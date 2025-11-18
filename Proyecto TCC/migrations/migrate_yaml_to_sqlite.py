from utils.ui.icon_system import get_icon, replace_emojis
"""
Migration script to transfer data from YAML config to SQLite database
This script helps migrate existing users from the old YAML-based system
"""

import yaml
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

def load_yaml_config():
    """Load existing YAML configuration"""
    config_path = 'config/config.yaml'
    
    if not os.path.exists(config_path):
        logger.warning(f"YAML config file not found: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logger.info(f"Loaded YAML config from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading YAML config: {e}")
        return None

def migrate_users_from_yaml(config):
    """Migrate users from YAML to SQLite database"""
    if not config or 'credentials' not in config:
        logger.warning("No credentials found in YAML config")
        return 0
    
    users_data = config['credentials'].get('usernames', {})
    migrated_count = 0
    
    logger.info(f"Found {len(users_data)} users to migrate")
    
    for username, user_data in users_data.items():
        try:
            # Extract user data
            email = user_data.get('email', f"{username}@migrated.com")
            first_name = user_data.get('first_name', 'Migrated')
            last_name = user_data.get('last_name', 'User')
            password = user_data.get('password', 'migrated123')  # Default password
            
            # Check if user already exists in database
            if auth_service.user_exists(username, email):
                logger.info(f"User {username} already exists in database, skipping")
                continue
            
            # Register user in database
            success, message = auth_service.register_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            if success:
                logger.info(f"Successfully migrated user: {username}")
                migrated_count += 1
            else:
                logger.error(f"Failed to migrate user {username}: {message}")
        
        except Exception as e:
            logger.error(f"Error migrating user {username}: {e}")
    
    return migrated_count

def create_backup_yaml():
    """Create a backup of the original YAML file"""
    config_path = 'config/config.yaml'
    backup_path = 'config/config.yaml.backup'
    
    if os.path.exists(config_path):
        try:
            import shutil
            shutil.copy2(config_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    return False

def verify_migration():
    """Verify that migration was successful"""
    try:
        # Check database info
        db_info = db_manager.get_database_info()
        
        if not db_info['exists']:
            logger.error("Database does not exist")
            return False
        
        logger.info(f"Database verification:")
        logger.info(f"  - Tables: {len(db_info['tables'])}")
        logger.info(f"  - Users: {db_info['user_count']}")
        logger.info(f"  - Size: {db_info['file_size_mb']} MB")
        
        # Check if users table has data
        with db_manager.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            if user_count > 0:
                logger.info(f"{get_icon("✅", 20)} Migration successful! {user_count} users in database")
                return True
            else:
                logger.warning("⚠️ No users found in database")
                return False
                
    except Exception as e:
        logger.error(f"Verification error: {e}")
        return False

def main():
    """Main migration function"""
    logger.info(replace_emojis("🚀 Starting YAML to SQLite migration..."))
    
    # Step 1: Create backup
    logger.info(replace_emojis("📋 Step 1: Creating backup..."))
    create_backup_yaml()
    
    # Step 2: Initialize database
    logger.info("🗄️ Step 2: Initializing database...")
    try:
        init_database()
        logger.info(replace_emojis("✅ Database initialized successfully"))
    except Exception as e:
        logger.error(f"{get_icon("❌", 20)} Database initialization failed: {e}")
        return False
    
    # Step 3: Load YAML config
    logger.info(replace_emojis("📄 Step 3: Loading YAML configuration..."))
    config = load_yaml_config()
    if not config:
        logger.warning("⚠️ No YAML config found, creating empty database")
        return verify_migration()
    
    # Step 4: Migrate users
    logger.info("👥 Step 4: Migrating users...")
    migrated_count = migrate_users_from_yaml(config)
    logger.info(f"{get_icon("✅", 20)} Migrated {migrated_count} users")
    
    # Step 5: Verify migration
    logger.info(replace_emojis("🔍 Step 5: Verifying migration..."))
    success = verify_migration()
    
    if success:
        logger.info(replace_emojis("🎉 Migration completed successfully!"))
        logger.info(replace_emojis("📝 Next steps:"))
        logger.info("   1. Test the new authentication system")
        logger.info("   2. Update your pages to use the new auth service")
        logger.info("   3. Remove the old YAML-based authentication")
    else:
        logger.error(replace_emojis("❌ Migration verification failed"))
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
