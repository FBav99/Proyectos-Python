"""
Admin page for database backup and export
This page allows exporting SQLite data before migration to Supabase
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.database import db_manager, get_database_info
from core.auth_service import get_current_user
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

def reset_supabase_database():
    """Drop all tables in Supabase to start fresh"""
    try:
        if db_manager.db_type != "supabase":
            return False
        
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
                except Exception:
                    pass  # Table might not exist
            
            conn.commit()
            return True
    
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def reset_sqlite_database():
    """Delete SQLite database file to start fresh"""
    try:
        import os
        from core.database import DB_PATH
        
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            return True
        return True  # File doesn't exist, that's fine
    except Exception as e:
        st.error(f"Error: {e}")
        return False

@safe_main
def main():
    """Admin backup page"""
    st.set_page_config(
        page_title="Admin - Backup Database",
        page_icon="💾",
        layout="wide"
    )
    
    # Check if user is authenticated (optional - you can remove this if you want it public)
    # For now, we'll make it accessible but warn users
    current_user = get_current_user()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">💾 Backup de Base de Datos</h1>
        <p style="color: white; font-size: 1.1rem;">Exporta tus datos antes de migrar a Supabase</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Database info
    st.markdown("### 📊 Información de la Base de Datos")
    
    db_info = get_database_info()
    
    if not db_info.get('exists'):
        st.error("❌ No se encontró la base de datos")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tipo de Base de Datos", db_info.get('db_type', 'Unknown'))
    with col2:
        st.metric("Usuarios", db_info.get('user_count', 0))
    with col3:
        if db_info.get('file_size_mb'):
            st.metric("Tamaño", f"{db_info.get('file_size_mb', 0)} MB")
        else:
            st.metric("Tamaño", "N/A")
    
    st.markdown("---")
    
    # Export section
    st.markdown("### 📥 Exportar Datos")
    
    st.info("""
    **⚠️ Importante en Streamlit Cloud:**
    - Los datos en SQLite se pierden cada semana cuando se reinicia la aplicación
    - Exporta tus datos regularmente para no perder información
    - Después de migrar a Supabase, tus datos serán persistentes
    """)
    
    if st.button("📥 Exportar Todos los Datos", type="primary", use_container_width=True):
        try:
            from migrations.export_sqlite_data import export_all_data
            
            with st.spinner("Exportando datos..."):
                output_file = export_all_data()
            
            if output_file:
                st.success(f"✅ Datos exportados exitosamente!")
                st.info(f"📁 Archivo: `{output_file}`")
                
                # Try to read and offer download
                try:
                    import json
                    with open(output_file, 'r', encoding='utf-8') as f:
                        export_data = json.load(f)
                    
                    # Create download button
                    json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="⬇️ Descargar Archivo de Backup",
                        data=json_str,
                        file_name=f"backup_{Path(output_file).stem}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.warning(f"No se pudo crear el botón de descarga: {e}")
                
                st.markdown("""
                ### 📋 Datos Exportados:
                - ✅ Usuarios
                - ✅ Progreso de usuarios
                - ✅ Intentos de cuestionarios
                """)
                
                st.markdown("""
                ### 🔄 Próximos Pasos:
                1. **Guarda este archivo** en un lugar seguro
                2. **Configura Supabase** en Streamlit Cloud secrets
                3. **Ejecuta la migración** usando `migrate_sqlite_to_supabase.py`
                4. **Verifica** que todos los datos se migraron correctamente
                """)
            else:
                st.error("❌ Error al exportar los datos")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.code(str(e), language="python")
    
    st.markdown("---")
    
    # Migration info
    st.markdown("### 🚀 Migración a Supabase")
    
    st.markdown("""
    Para migrar tus datos a Supabase y hacerlos persistentes:
    
    1. **Exporta tus datos** usando el botón arriba
    2. **Configura Supabase** en Streamlit Cloud:
       - Ve a Settings → Secrets
       - Agrega tu configuración de Supabase:
       ```toml
       [database]
       db_type = "supabase"
       
       [supabase]
       connection_string = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
       ```
    3. **Ejecuta la migración** localmente o en un script:
       ```bash
       python migrations/migrate_sqlite_to_supabase.py backups/export_file.json
       ```
    4. **Verifica** que los datos se migraron correctamente
    
    📚 Lee más en: `SUPABASE_SETUP_GUIDE.md`
    """)
    
    st.markdown("---")
    
    # Reset section
    st.markdown("### 🔄 Resetear Base de Datos")
    
    st.warning("""
    **⚠️ ADVERTENCIA:**
    - Esto eliminará TODOS los datos de la base de datos
    - Usuarios, progreso, cuestionarios - TODO se perderá
    - Esta acción NO se puede deshacer
    - Solo usa esto si quieres empezar completamente desde cero
    """)
    
    if st.button("🗑️ Resetear Base de Datos (Empezar desde Cero)", type="secondary", use_container_width=True):
        confirm = st.text_input("Escribe 'RESETEAR' para confirmar:")
        
        if confirm == "RESETEAR":
            try:
                from migrations.reset_database import reset_sqlite_database, reset_supabase_database
                from core.database import init_database
                
                db_info = get_database_info()
                db_type = db_info.get('db_type', 'SQLite')
                
                with st.spinner("Reseteando base de datos..."):
                    if 'Supabase' in db_type:
                        success = reset_supabase_database()
                    else:
                        success = reset_sqlite_database()
                    
                    if success:
                        # Reinitialize
                        init_database()
                        st.success("✅ Base de datos reseteada exitosamente!")
                        st.info("🎉 Ahora tienes una base de datos limpia y vacía")
                        st.rerun()
                    else:
                        st.error("❌ Error al resetear la base de datos")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        elif confirm:
            st.error("Por favor escribe exactamente 'RESETEAR' para confirmar")
    
    # Navigation
    st.markdown("---")
    if st.button("🏠 Volver al Inicio", use_container_width=True):
        st.switch_page("Inicio.py")

if __name__ == "__main__":
    main()

