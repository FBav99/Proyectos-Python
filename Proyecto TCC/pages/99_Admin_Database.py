"""
Página de Administración de Base de Datos
Permite inspeccionar y administrar la base de datos SQLite en Streamlit Cloud
"""

import streamlit as st
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
from core.database import db_manager
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling
from utils.ui import auth_ui

# Configure error handling
configure_streamlit_error_handling()

# Initialize sidebar
auth_ui.init_sidebar()

def get_database_info() -> Dict:
    """Get comprehensive database information"""
    db_path = 'tcc_database.db'
    
    info = {
        'exists': False,
        'size': 0,
        'path': '',
        'tables': [],
        'table_counts': {},
        'total_records': 0
    }
    
    if os.path.exists(db_path):
        info['exists'] = True
        info['size'] = os.path.getsize(db_path)
        info['path'] = os.path.abspath(db_path)
        
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in cursor.fetchall()]
                info['tables'] = tables
                
                # Get record counts for each table
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        info['table_counts'][table] = count
                        info['total_records'] += count
                    except:
                        info['table_counts'][table] = 'Error'
        
        except Exception as e:
            st.error(f"Error reading database: {e}")
    
    return info

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def execute_query(query: str) -> tuple:
    """Execute a SQL query and return results"""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Check if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                return True, columns, rows
            else:
                # For INSERT, UPDATE, DELETE
                conn.commit()
                return True, None, None
    except Exception as e:
        return False, None, str(e)

@safe_main
def main():
    """Página de administración de base de datos"""
    st.set_page_config(
        page_title="Administración de Base de Datos",
        page_icon="🗄️",
        layout="wide"
    )
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🗄️ Administración de Base de Datos</h1>
        <p style="color: white; font-size: 1.1rem;">Inspecciona y administra tu base de datos SQLite</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication (optional - you can make this require admin)
    current_user = auth_ui.get_current_user()
    if not current_user:
        st.warning("⚠️ Esta página requiere autenticación")
        if st.button("🔐 Ir a Iniciar Sesión"):
            st.switch_page("Inicio.py")
        return
    
    # Tabs for different admin functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Estado General", 
        "📋 Ver Tablas", 
        "🔍 Query SQL", 
        "💾 Backup/Exportar"
    ])
    
    with tab1:
        st.markdown("### 📊 Estado de la Base de Datos")
        
        db_info = get_database_info()
        
        if not db_info['exists']:
            st.error("❌ Base de datos no encontrada")
            st.info("La base de datos se creará automáticamente cuando se use por primera vez")
            return
        
        # Display database info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📁 Estado", "✅ Activa" if db_info['exists'] else "❌ No encontrada")
            st.metric("💾 Tamaño", format_file_size(db_info['size']))
        
        with col2:
            st.metric("📊 Tablas", len(db_info['tables']))
            st.metric("📝 Registros Totales", db_info['total_records'])
        
        with col3:
            st.info(f"**Ruta:**\n`{db_info['path']}`")
            st.info(f"**Última verificación:**\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        st.markdown("### 📋 Resumen por Tabla")
        
        if db_info['table_counts']:
            # Create a DataFrame-like display
            st.markdown("""
            <style>
            .table-container {
                overflow-x: auto;
            }
            </style>
            """, unsafe_allow_html=True)
            
            for table, count in db_info['table_counts'].items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{table}**")
                with col2:
                    if isinstance(count, int):
                        st.write(f"`{count:,}` registros")
                    else:
                        st.write(f"`{count}`")
    
    with tab2:
        st.markdown("### 📋 Explorar Tablas")
        
        db_info = get_database_info()
        
        if not db_info['tables']:
            st.warning("No hay tablas en la base de datos")
            return
        
        # Table selector
        selected_table = st.selectbox(
            "Selecciona una tabla para ver su contenido",
            db_info['tables'],
            key="table_selector"
        )
        
        if selected_table:
            # Pagination
            col1, col2 = st.columns([1, 4])
            with col1:
                limit = st.number_input("Registros por página", min_value=10, max_value=1000, value=50, step=10)
            with col2:
                offset = st.number_input("Saltar registros", min_value=0, value=0, step=limit)
            
            # Query table data
            try:
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get total count
                    cursor.execute(f"SELECT COUNT(*) FROM {selected_table}")
                    total_count = cursor.fetchone()[0]
                    
                    # Get column names
                    cursor.execute(f"PRAGMA table_info({selected_table})")
                    columns = [row[1] for row in cursor.fetchall()]
                    
                    # Get data with pagination
                    query = f"SELECT * FROM {selected_table} LIMIT {limit} OFFSET {offset}"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    
                    st.info(f"📊 Mostrando {len(rows)} de {total_count} registros en `{selected_table}`")
                    
                    if rows:
                        # Display as table
                        import pandas as pd
                        df = pd.DataFrame(rows, columns=columns)
                        st.dataframe(df, use_container_width=True, height=400)
                    else:
                        st.info("No hay registros en esta tabla")
            
            except Exception as e:
                st.error(f"Error al leer la tabla: {e}")
    
    with tab3:
        st.markdown("### 🔍 Query SQL Personalizado")
        st.warning("⚠️ **ADVERTENCIA:** Solo ejecuta queries que comprendas. Las operaciones de escritura (INSERT, UPDATE, DELETE) son permanentes.")
        
        # Query input
        query = st.text_area(
            "Escribe tu query SQL:",
            height=150,
            placeholder="SELECT * FROM users LIMIT 10;",
            help="Ejemplo: SELECT * FROM users WHERE is_active = 1;"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            execute_btn = st.button("▶️ Ejecutar Query", type="primary", use_container_width=True)
        
        if execute_btn and query:
            success, columns, results = execute_query(query.strip())
            
            if success:
                if columns and results:
                    # SELECT query - show results
                    st.success("✅ Query ejecutado exitosamente")
                    
                    import pandas as pd
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df, use_container_width=True)
                    
                    st.info(f"📊 Resultados: {len(results)} filas, {len(columns)} columnas")
                else:
                    # Non-SELECT query
                    st.success("✅ Query ejecutado exitosamente (operación de escritura)")
            else:
                st.error(f"❌ Error al ejecutar query: {results}")
        
        # Quick queries
        st.markdown("---")
        st.markdown("### 🚀 Queries Rápidas")
        
        quick_queries = {
            "Ver todos los usuarios": "SELECT id, username, email, created_at, is_active FROM users;",
            "Usuarios activos": "SELECT id, username, email FROM users WHERE is_active = 1;",
            "Conteo por tabla": """
            SELECT 
                'users' as tabla, COUNT(*) as registros FROM users
            UNION ALL
            SELECT 'user_sessions', COUNT(*) FROM user_sessions
            UNION ALL
            SELECT 'user_progress', COUNT(*) FROM user_progress
            UNION ALL
            SELECT 'quiz_attempts', COUNT(*) FROM quiz_attempts;
            """,
            "Ver sesiones activas": """
            SELECT us.*, u.username 
            FROM user_sessions us 
            JOIN users u ON us.user_id = u.id 
            WHERE us.expires_at > datetime('now')
            ORDER BY us.last_activity DESC;
            """
        }
        
        for query_name, query_sql in quick_queries.items():
            if st.button(f"▶️ {query_name}", key=f"quick_{query_name}"):
                st.text_area("Query:", query_sql, height=100, key=f"query_{query_name}")
                success, columns, results = execute_query(query_sql.strip())
                
                if success and columns and results:
                    import pandas as pd
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df, use_container_width=True)
    
    with tab4:
        st.markdown("### 💾 Backup y Exportación")
        
        db_info = get_database_info()
        
        if not db_info['exists']:
            st.error("❌ Base de datos no encontrada")
            return
        
        st.info(f"**Base de datos:** `{db_info['path']}`\n**Tamaño:** {format_file_size(db_info['size'])}")
        
        # Export options
        st.markdown("#### 📤 Exportar Datos")
        
        export_format = st.radio(
            "Formato de exportación:",
            ["CSV por tabla", "SQL Dump", "JSON"],
            horizontal=True
        )
        
        if export_format == "CSV por tabla":
            selected_table = st.selectbox("Selecciona tabla:", db_info['tables'])
            
            if st.button("📥 Exportar a CSV", type="primary"):
                try:
                    with db_manager.get_connection() as conn:
                        import pandas as pd
                        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
                        
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Descargar CSV",
                            data=csv,
                            file_name=f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error al exportar: {e}")
        
        elif export_format == "SQL Dump":
            st.info("""
            **SQL Dump:** Exporta la estructura y datos de la base de datos en formato SQL.
            
            Para crear un dump completo, puedes usar:
            ```bash
            sqlite3 tcc_database.db .dump > backup.sql
            ```
            
            En Streamlit Cloud, esto se puede hacer desde la consola del servidor.
            """)
        
        elif export_format == "JSON":
            selected_table = st.selectbox("Selecciona tabla:", db_info['tables'])
            
            if st.button("📥 Exportar a JSON", type="primary"):
                try:
                    with db_manager.get_connection() as conn:
                        import pandas as pd
                        import json
                        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
                        json_data = df.to_json(orient='records', indent=2)
                        
                        st.download_button(
                            label="⬇️ Descargar JSON",
                            data=json_data,
                            file_name=f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                except Exception as e:
                    st.error(f"Error al exportar: {e}")
        
        # Database integrity check
        st.markdown("---")
        st.markdown("#### 🔍 Verificación de Integridad")
        
        if st.button("🔍 Verificar Integridad de la Base de Datos", type="secondary"):
            try:
                with db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA integrity_check")
                    result = cursor.fetchone()
                    
                    if result[0] == 'ok':
                        st.success("✅ Base de datos íntegra")
                    else:
                        st.error(f"❌ Problemas detectados: {result[0]}")
            except Exception as e:
                st.error(f"Error al verificar: {e}")
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🔗 Navegación")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    with col2:
        if st.button("🔐 Cerrar Sesión", use_container_width=True):
            from core.auth_service import logout_user
            logout_user()
            st.rerun()

if __name__ == "__main__":
    main()

