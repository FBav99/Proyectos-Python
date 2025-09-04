-- 🗑️ Limpieza de Tablas No Utilizadas - Plataforma TCC
-- Este script elimina las tablas que no están implementadas en el proyecto actual

-- ⚠️ ADVERTENCIA: Este script eliminará datos permanentemente
-- Solo ejecutar si estás seguro de que no necesitas estas tablas

BEGIN TRANSACTION;

-- 1. Eliminar tabla de archivos subidos (no implementada)
DROP TABLE IF EXISTS file_analysis_sessions;
DROP TABLE IF EXISTS uploaded_files;

-- 2. Eliminar tablas de dashboard (no implementadas)
DROP TABLE IF EXISTS dashboard_components;
DROP TABLE IF EXISTS dashboards;

-- 3. Eliminar tabla de métricas del sistema (no implementada)
DROP TABLE IF EXISTS system_metrics;

-- 4. Eliminar índices relacionados con las tablas eliminadas
DROP INDEX IF EXISTS idx_files_user_id;
DROP INDEX IF EXISTS idx_files_uploaded_at;
DROP INDEX IF EXISTS idx_dashboards_user_id;
DROP INDEX IF EXISTS idx_dashboards_public;

-- 5. Verificar que las tablas esenciales permanecen
-- Las siguientes tablas DEBEN permanecer:
-- - users (autenticación)
-- - user_sessions (gestión de sesiones)
-- - user_progress (seguimiento de progreso)
-- - quiz_attempts (resultados de cuestionarios)
-- - quiz_answers (respuestas de cuestionarios)
-- - rate_limiting (protección de seguridad)
-- - achievements (opcional, para gamificación)
-- - user_activity_log (opcional, para auditoría)

COMMIT;

-- ✅ Verificación: Mostrar tablas restantes
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
