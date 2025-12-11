-- ============================================================================
-- Migration: Add onboarding_completed column to users table
-- Database: PostgreSQL / Supabase
-- Date: 2025
-- ============================================================================
-- 
-- Esta migración agrega la columna onboarding_completed a la tabla users
-- para rastrear si el usuario ha completado el tour de introducción.
--
-- Ejecutar este script en Supabase SQL Editor:
-- 1. Ve a tu proyecto en Supabase
-- 2. Abre el SQL Editor
-- 3. Pega este script
-- 4. Ejecuta el script
-- ============================================================================

-- Agregar columna onboarding_completed si no existe
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE;

-- Verificar que la columna fue agregada (opcional - puedes ejecutar esto para confirmar)
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'users' AND column_name = 'onboarding_completed';

-- Actualizar usuarios existentes para que tengan onboarding_completed = FALSE
-- (esto es opcional, pero asegura consistencia)
UPDATE users 
SET onboarding_completed = FALSE 
WHERE onboarding_completed IS NULL;

-- ============================================================================
-- ✅ Migración completada
-- ============================================================================
-- 
-- La columna onboarding_completed ahora está disponible en la tabla users.
-- Valores posibles:
--   - FALSE: El usuario aún no ha completado el tour de introducción
--   - TRUE: El usuario ha completado el tour de introducción
--
-- ============================================================================



