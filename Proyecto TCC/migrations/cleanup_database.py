#!/usr/bin/env python3
"""
🗑️ Script de Limpieza de Base de Datos - Plataforma TCC
Elimina las tablas no utilizadas y mantiene solo las esenciales
"""

import sqlite3
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import db_manager

def cleanup_unused_tables():
    """Eliminar tablas no utilizadas de la base de datos"""
    
    print("🗑️ Iniciando limpieza de base de datos...")
    
    # Tablas a eliminar (no implementadas en el proyecto actual)
    tables_to_drop = [
        'achievements',
        'system_metrics'
    ]
    
    # Índices a eliminar
    indexes_to_drop = [
        # No hay índices específicos para eliminar en esta limpieza
    ]
    
    try:
        with db_manager.get_connection() as conn:
            # Verificar tablas existentes antes de la limpieza
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row['name'] for row in cursor.fetchall()]
            
            print(f"📊 Tablas existentes antes de la limpieza: {len(existing_tables)}")
            for table in existing_tables:
                print(f"   - {table}")
            
            # Eliminar tablas no utilizadas
            for table in tables_to_drop:
                if table in existing_tables:
                    conn.execute(f"DROP TABLE IF EXISTS {table}")
                    print(f"✅ Tabla eliminada: {table}")
                else:
                    print(f"ℹ️  Tabla no encontrada: {table}")
            
            # Eliminar índices relacionados
            for index in indexes_to_drop:
                try:
                    conn.execute(f"DROP INDEX IF EXISTS {index}")
                    print(f"✅ Índice eliminado: {index}")
                except Exception as e:
                    print(f"ℹ️  Índice no encontrado: {index}")
            
            # Verificar tablas restantes después de la limpieza
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            remaining_tables = [row['name'] for row in cursor.fetchall()]
            
            print(f"\n📊 Tablas restantes después de la limpieza: {len(remaining_tables)}")
            for table in remaining_tables:
                print(f"   - {table}")
            
            # Verificar que las tablas esenciales permanecen
            essential_tables = [
                'users', 'user_sessions', 'user_progress', 
                'quiz_attempts', 'quiz_answers', 'rate_limiting'
            ]
            
            missing_essential = [table for table in essential_tables if table not in remaining_tables]
            
            if missing_essential:
                print(f"❌ ERROR: Faltan tablas esenciales: {missing_essential}")
                return False
            else:
                print("✅ Todas las tablas esenciales están presentes")
            
            conn.commit()
            print("\n🎉 Limpieza de base de datos completada exitosamente!")
            return True
            
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        return False

def show_database_info():
    """Mostrar información actual de la base de datos"""
    try:
        info = db_manager.get_database_info()
        print("\n📊 Información de la Base de Datos:")
        print(f"   Existe: {info['exists']}")
        print(f"   Tamaño: {info['file_size_mb']} MB")
        print(f"   Usuarios: {info['user_count']}")
        print(f"   Tablas: {len(info['tables'])}")
        
        if info['exists']:
            print("\n📋 Tablas actuales:")
            for table in info['tables']:
                print(f"   - {table}")
                
    except Exception as e:
        print(f"❌ Error obteniendo información: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🗑️  LIMPIADOR DE BASE DE DATOS TCC")
    print("=" * 60)
    
    # Mostrar información antes de la limpieza
    show_database_info()
    
    # Confirmar con el usuario
    print("\n⚠️  ADVERTENCIA: Este proceso eliminará permanentemente las siguientes tablas:")
    print("   - achievements (sistema de logros)")
    print("   - system_metrics (métricas del sistema)")
    
    print("\n✅ Las siguientes tablas se MANTENDRÁN:")
    print("   - users (autenticación)")
    print("   - user_progress (progreso)")
    print("   - quiz_attempts (cuestionarios)")
    print("   - quiz_answers (respuestas)")
    print("   - rate_limiting (seguridad)")
    print("   - uploaded_files (carga de archivos)")
    print("   - file_analysis_sessions (análisis de archivos)")
    print("   - dashboards (configuraciones de dashboard)")
    print("   - dashboard_components (componentes de dashboard)")
    print("   - user_activity_log (actividad, opcional)")
    
    response = input("\n¿Continuar con la limpieza? (s/N): ").strip().lower()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        if cleanup_unused_tables():
            print("\n🎯 Próximos pasos:")
            print("1. Actualizar core/database.py para no crear las tablas eliminadas")
            print("2. Verificar que la aplicación funcione correctamente")
            print("3. Ejecutar tests si están disponibles")
        else:
            print("\n❌ La limpieza falló. Revisar errores antes de continuar.")
    else:
        print("\n❌ Limpieza cancelada por el usuario.")

if __name__ == "__main__":
    main()
