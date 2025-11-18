-- ============================================================================
-- SAMPLE DATA INSERTS FOR TCC PLATFORM
-- ============================================================================
-- This file contains sample INSERT statements for users and survey responses
-- Password for all users: "Password123!" (hashed with bcrypt)
-- ============================================================================

-- ============================================================================
-- USERS TABLE INSERTS
-- ============================================================================
-- Note: All passwords are hashed using bcrypt for "Password123!"
-- The password hash is: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZqZqZq
-- (This is a placeholder - actual hashes should be generated using bcrypt)

-- User 1: Student - Beginner
INSERT INTO users (
    username, email, password_hash, first_name, last_name,
    created_at, last_login, is_active, failed_login_attempts,
    email_verified, verification_token, reset_token, reset_token_expires
) VALUES (
    'maria.garcia',
    'maria.garcia@example.com',
    '$2b$12$1JK9LvM7vNt51UOlq4lh0..AW4bcdzb519zSjWzi3RC4On2QNPNUq',
    'María',
    'García',
    datetime('now', '-30 days'),
    datetime('now', '-1 day'),
    1,
    0,
    1,
    NULL,
    NULL,
    NULL
);

-- User 2: Professional - Intermediate
INSERT INTO users (
    username, email, password_hash, first_name, last_name,
    created_at, last_login, is_active, failed_login_attempts,
    email_verified, verification_token, reset_token, reset_token_expires
) VALUES (
    'carlos.rodriguez',
    'carlos.rodriguez@example.com',
    '$2b$12$rAE40O0rrp1vEZY/U/oW7.hsAtHDHu1bU9gQAe59Ui/ZokdIZSeN6',
    'Carlos',
    'Rodríguez',
    datetime('now', '-25 days'),
    datetime('now', '-2 hours'),
    1,
    0,
    1,
    NULL,
    NULL,
    NULL
);

-- User 3: Analyst - Advanced
INSERT INTO users (
    username, email, password_hash, first_name, last_name,
    created_at, last_login, is_active, failed_login_attempts,
    email_verified, verification_token, reset_token, reset_token_expires
) VALUES (
    'ana.martinez',
    'ana.martinez@example.com',
    '$2b$12$ytruQhVOlD5cwpt4WOUTBO2g38TCPAVIVvv95efOmP9fLQW13UCle',
    'Ana',
    'Martínez',
    datetime('now', '-20 days'),
    datetime('now', '-5 hours'),
    1,
    0,
    1,
    NULL,
    NULL,
    NULL
);

-- User 4: Manager - Expert
INSERT INTO users (
    username, email, password_hash, first_name, last_name,
    created_at, last_login, is_active, failed_login_attempts,
    email_verified, verification_token, reset_token, reset_token_expires
) VALUES (
    'juan.lopez',
    'juan.lopez@example.com',
    '$2b$12$4rRiUzaITbmoKC6SDwRCguw/MNgbGLBU98ch5aIVsatykkYLbDpSu',
    'Juan',
    'López',
    datetime('now', '-15 days'),
    datetime('now', '-1 hour'),
    1,
    0,
    1,
    NULL,
    NULL,
    NULL
);

-- User 5: Student - Beginner (No surveys completed)
INSERT INTO users (
    username, email, password_hash, first_name, last_name,
    created_at, last_login, is_active, failed_login_attempts,
    email_verified, verification_token, reset_token, reset_token_expires
) VALUES (
    'laura.sanchez',
    'laura.sanchez@example.com',
    '$2b$12$KQIBAgkkRpst9keD0wKMa.sI6V5f.50BfDRffIELG45RWMpd2wG/6',
    'Laura',
    'Sánchez',
    datetime('now', '-10 days'),
    datetime('now', '-30 minutes'),
    1,
    0,
    1,
    NULL,
    NULL,
    NULL
);

-- ============================================================================
-- SURVEY RESPONSES TABLE INSERTS
-- ============================================================================
-- Note: Responses are stored as JSON strings
-- Survey types: 'initial', 'level', 'final'
-- Levels: 'nivel0', 'nivel1', 'nivel2', 'nivel3', 'nivel4'

-- Initial Survey for User 1 (maria.garcia - ID: 1)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    1,
    'initial',
    NULL,
    '{"data_analysis_experience": "Principiante - He usado Excel básico o herramientas similares", "occupation_selection": "Estudiante", "what_they_do": "Estudiante", "occupation_detail": "", "excel_usage_frequency": "Varias veces por semana", "learning_goals": "Aprender a crear dashboards básicos", "motivation": "Mejorar mis habilidades para mi carrera", "completed_at": "2025-01-15T10:30:00"}',
    datetime('now', '-25 days')
);

-- Initial Survey for User 2 (carlos.rodriguez - ID: 2)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    2,
    'initial',
    NULL,
    '{"data_analysis_experience": "Intermedio - He creado tablas y gráficos básicos", "occupation_selection": "Empleado/a en área administrativa", "what_they_do": "Empleado/a en área administrativa", "occupation_detail": "", "excel_usage_frequency": "Diariamente", "learning_goals": "Automatizar reportes y análisis", "motivation": "Mejorar la eficiencia en mi trabajo", "completed_at": "2025-01-20T14:15:00"}',
    datetime('now', '-20 days')
);

-- Initial Survey for User 3 (ana.martinez - ID: 3)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'initial',
    NULL,
    '{"data_analysis_experience": "Avanzado - He usado herramientas como Power BI, Tableau, o Python", "occupation_selection": "Analista o especialista en datos/BI", "what_they_do": "Analista o especialista en datos/BI", "occupation_detail": "", "excel_usage_frequency": "Diariamente", "learning_goals": "Explorar nuevas técnicas y metodologías", "motivation": "Mantenerme actualizado en el campo", "completed_at": "2025-01-25T09:00:00"}',
    datetime('now', '-15 days')
);

-- Initial Survey for User 4 (juan.lopez - ID: 4)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    4,
    'initial',
    NULL,
    '{"data_analysis_experience": "Experto - Trabajo profesionalmente con análisis de datos", "occupation_selection": "Liderazgo o gerencia", "what_they_do": "Liderazgo o gerencia", "occupation_detail": "", "excel_usage_frequency": "Diariamente", "learning_goals": "Enseñar a mi equipo mejores prácticas", "motivation": "Capacitar a mi equipo", "completed_at": "2025-01-30T16:45:00"}',
    datetime('now', '-10 days')
);

-- Level Survey for User 1 - Nivel 0
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    1,
    'level',
    'nivel0',
    '{"clarity_rating": 5, "difficulty_rating": 2, "usefulness_rating": 5, "engagement_rating": 4, "pace_rating": 4, "what_liked": "La introducción fue muy clara y fácil de seguir", "suggestions": "Podría tener más ejemplos visuales", "additional_comments": "Excelente introducción, muy clara", "completed_at": "2025-01-16T11:00:00"}',
    datetime('now', '-24 days')
);

-- Level Survey for User 1 - Nivel 1
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    1,
    'level',
    'nivel1',
    '{"clarity_rating": 4, "difficulty_rating": 3, "usefulness_rating": 5, "engagement_rating": 5, "pace_rating": 4, "what_liked": "Los ejemplos prácticos fueron muy útiles", "suggestions": "", "additional_comments": "Muy útil para empezar", "completed_at": "2025-01-18T15:30:00"}',
    datetime('now', '-22 days')
);

-- Level Survey for User 2 - Nivel 0
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    2,
    'level',
    'nivel0',
    '{"clarity_rating": 4, "difficulty_rating": 1, "usefulness_rating": 4, "engagement_rating": 4, "pace_rating": 3, "what_liked": "Bien estructurado", "suggestions": "", "additional_comments": "Buen nivel introductorio", "completed_at": "2025-01-21T10:15:00"}',
    datetime('now', '-19 days')
);

-- Level Survey for User 2 - Nivel 1
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    2,
    'level',
    'nivel1',
    '{"clarity_rating": 5, "difficulty_rating": 2, "usefulness_rating": 5, "engagement_rating": 5, "pace_rating": 4, "what_liked": "El contenido fue perfecto para mi nivel", "suggestions": "", "additional_comments": "Perfecto para mi nivel", "completed_at": "2025-01-22T14:00:00"}',
    datetime('now', '-18 days')
);

-- Level Survey for User 2 - Nivel 2
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    2,
    'level',
    'nivel2',
    '{"clarity_rating": 4, "difficulty_rating": 3, "usefulness_rating": 5, "engagement_rating": 4, "pace_rating": 4, "what_liked": "Los filtros son muy útiles para mi trabajo diario", "suggestions": "Más ejemplos de filtros complejos", "additional_comments": "Los filtros son muy útiles", "completed_at": "2025-01-23T16:30:00"}',
    datetime('now', '-17 days')
);

-- Level Survey for User 3 - Nivel 0
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'level',
    'nivel0',
    '{"clarity_rating": 3, "difficulty_rating": 1, "usefulness_rating": 3, "engagement_rating": 3, "pace_rating": 2, "what_liked": "", "suggestions": "Podría ser más avanzado", "additional_comments": "Muy básico para mi nivel", "completed_at": "2025-01-26T09:30:00"}',
    datetime('now', '-14 days')
);

-- Level Survey for User 3 - Nivel 1
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'level',
    'nivel1',
    '{"clarity_rating": 4, "difficulty_rating": 2, "usefulness_rating": 4, "engagement_rating": 4, "pace_rating": 3, "what_liked": "Bien explicado", "suggestions": "", "additional_comments": "Buen contenido", "completed_at": "2025-01-27T11:00:00"}',
    datetime('now', '-13 days')
);

-- Level Survey for User 3 - Nivel 2
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'level',
    'nivel2',
    '{"clarity_rating": 5, "difficulty_rating": 2, "usefulness_rating": 5, "engagement_rating": 5, "pace_rating": 4, "what_liked": "Excelente explicación de filtros", "suggestions": "", "additional_comments": "Excelente nivel", "completed_at": "2025-01-28T13:15:00"}',
    datetime('now', '-12 days')
);

-- Level Survey for User 3 - Nivel 3
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'level',
    'nivel3',
    '{"clarity_rating": 5, "difficulty_rating": 3, "usefulness_rating": 5, "engagement_rating": 5, "pace_rating": 5, "what_liked": "Las métricas son muy útiles para mi trabajo", "suggestions": "", "additional_comments": "Muy útil para métricas", "completed_at": "2025-01-29T15:45:00"}',
    datetime('now', '-11 days')
);

-- Level Survey for User 3 - Nivel 4
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'level',
    'nivel4',
    '{"clarity_rating": 4, "difficulty_rating": 4, "usefulness_rating": 5, "engagement_rating": 4, "pace_rating": 4, "what_liked": "Los dashboards personalizables son excelentes", "suggestions": "Más templates predefinidos", "additional_comments": "Nivel avanzado bien estructurado", "completed_at": "2025-01-30T17:00:00"}',
    datetime('now', '-10 days')
);

-- Final Survey for User 3 (completed all levels)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    3,
    'final',
    NULL,
    '{"overall_satisfaction": 5, "learning_achievement": 5, "ease_of_use": 5, "content_quality": 5, "recommendation_likelihood": 5, "best_aspect": "La estructura y organización de los niveles", "most_challenging_aspect": "Ninguno - Todo fue fácil", "general_comments": "Excelente plataforma, muy bien estructurada", "what_to_add": "Más casos de uso del mundo real", "additional_feedback": "Recomendaría esta plataforma a mis colegas", "completed_at": "2025-01-31T10:00:00"}',
    datetime('now', '-9 days')
);

-- Final Survey for User 2 (completed some levels)
INSERT INTO survey_responses (
    user_id, survey_type, level, responses, completed_at
) VALUES (
    2,
    'final',
    NULL,
    '{"overall_satisfaction": 4, "learning_achievement": 4, "ease_of_use": 5, "content_quality": 4, "recommendation_likelihood": 4, "best_aspect": "La claridad de las explicaciones", "most_challenging_aspect": "Aplicar lo aprendido en ejercicios", "general_comments": "Muy buena experiencia de aprendizaje", "what_to_add": "Más ejercicios prácticos", "additional_feedback": "", "completed_at": "2025-02-01T14:30:00"}',
    datetime('now', '-8 days')
);

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. All user passwords are set to "Password123!" (hashed with bcrypt)
--    Each user has a unique hash (generated with bcrypt.gensalt())
--    Use generate_password_hash.py to create new password hashes
--
-- 2. User IDs are auto-incremented, so adjust foreign keys in survey_responses
--    if inserting users in a different order
--
-- 3. Survey responses are stored as JSON strings. Make sure to escape quotes
--    properly when modifying the JSON content. Use single quotes for SQL strings
--    and double quotes inside JSON.
--
-- 4. Dates use SQLite datetime() function for relative dates. 
--    For PostgreSQL/Supabase, use: CURRENT_TIMESTAMP - INTERVAL '30 days'
--
-- 5. Survey Types:
--    - 'initial': Initial survey (no level required)
--    - 'level': Level-specific survey (requires level: 'nivel0', 'nivel1', etc.)
--    - 'final': Final survey (no level required)
--
-- 6. To use this file:
--    SQLite: sqlite3 your_database.db < database_sample_data.sql
--    PostgreSQL: psql -d your_database -f database_sample_data.sql
-- ============================================================================

