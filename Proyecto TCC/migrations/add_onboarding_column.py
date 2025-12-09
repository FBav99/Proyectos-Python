"""
Migration Script: Add onboarding_completed column to users table
Run this script to add the onboarding_completed column needed for the onboarding tour system
"""

from core.database import DatabaseManager

def add_onboarding_column():
    """Add onboarding_completed column to users table"""
    db = DatabaseManager()
    
    print("🔄 Agregando columna onboarding_completed a la tabla users...")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            if db.db_type == "supabase":
                # PostgreSQL/Supabase
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE
                """)
                print("✅ Columna agregada exitosamente (PostgreSQL/Supabase)")
            else:
                # SQLite
                try:
                    cursor.execute("""
                        ALTER TABLE users 
                        ADD COLUMN onboarding_completed BOOLEAN DEFAULT 0
                    """)
                    print("✅ Columna agregada exitosamente (SQLite)")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print("ℹ️ La columna ya existe, no se necesita agregar")
                    else:
                        raise
            
            conn.commit()
            print("✅ Migración completada exitosamente")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        print("💡 Si la columna ya existe, puedes ignorar este error")

if __name__ == "__main__":
    add_onboarding_column()

