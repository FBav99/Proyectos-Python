#!/usr/bin/env python3
"""
Migration script to add nivel0_completed column to user_progress table
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add nivel0_completed column to existing user_progress table"""
    db_path = "tcc_database.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. No migration needed.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if nivel0_completed column already exists
        cursor.execute("PRAGMA table_info(user_progress)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'nivel0_completed' in columns:
            print("nivel0_completed column already exists. No migration needed.")
            conn.close()
            return
        
        # Add the nivel0_completed column
        print("Adding nivel0_completed column to user_progress table...")
        cursor.execute("""
            ALTER TABLE user_progress 
            ADD COLUMN nivel0_completed BOOLEAN DEFAULT 0
        """)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(user_progress)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'nivel0_completed' in columns:
            print("✅ nivel0_completed column verified in database")
        else:
            print("❌ Error: nivel0_completed column not found after migration")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_database()
