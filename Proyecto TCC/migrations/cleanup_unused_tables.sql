-- 🗑️ Limpieza de Tablas No Utilizadas - Plataforma TCC
-- Este script elimina las tablas que no están implementadas en el proyecto actual
-- Basado en análisis de uso real en el código (ver docs/TABLE_USAGE_ANALYSIS.md)
-- Compatible con PostgreSQL/Supabase

-- ⚠️ ADVERTENCIA: Este script eliminará datos permanentemente
-- Solo ejecutar si estás seguro de que no necesitas estas tablas

BEGIN;

-- 1. Eliminar tabla de archivos subidos (no implementada)
-- Razón: Los archivos se manejan en st.session_state, no se persisten en BD
DROP TABLE IF EXISTS file_analysis_sessions CASCADE;
DROP TABLE IF EXISTS uploaded_files CASCADE;

-- 2. Eliminar tabla de componentes de dashboard (redundante)
-- Razón: Los componentes se almacenan como JSON en dashboards.dashboard_config
DROP TABLE IF EXISTS dashboard_components CASCADE;

-- 3. Eliminar tabla de log de actividad (no implementada)
-- Razón: log_activity() solo escribe al logger de Python, no a la BD
DROP TABLE IF EXISTS user_activity_log CASCADE;

-- 4. Eliminar índices relacionados con las tablas eliminadas
-- (CASCADE en DROP TABLE ya elimina los índices, pero por si acaso)
DROP INDEX IF EXISTS idx_files_user_id;
DROP INDEX IF EXISTS idx_files_uploaded_at;
DROP INDEX IF EXISTS idx_activity_user_type;
DROP INDEX IF EXISTS idx_activity_created;

-- 5. Verificar que las tablas esenciales permanecen
-- Las siguientes tablas DEBEN permanecer:
-- ✅ users (autenticación) - USADO
-- ✅ user_sessions (gestión de sesiones) - USADO
-- ✅ user_progress (seguimiento de progreso) - USADO
-- ✅ quiz_attempts (resultados de cuestionarios) - USADO
-- ✅ quiz_answers (respuestas de cuestionarios) - USADO
-- ✅ rate_limiting (protección de seguridad) - USADO
-- ✅ survey_responses (respuestas de encuestas) - USADO
-- ✅ dashboards (configuraciones de dashboard) - USADO

COMMIT;

-- ✅ Verificación: Mostrar tablas restantes (PostgreSQL/Supabase)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
