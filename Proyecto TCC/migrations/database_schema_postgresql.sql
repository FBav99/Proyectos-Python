-- ============================================================================
-- PostgreSQL DDL for TCC Data Analysis Platform
-- Compatible with Supabase
-- Use this file to generate ERD in DrawSQL
-- ============================================================================

-- ============================================================================
-- 1. USERS TABLE - Authentication and User Profiles
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP,
    onboarding_completed BOOLEAN DEFAULT FALSE
);

-- ============================================================================
-- 2. USER_SESSIONS TABLE - Session Management
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 3. USER_PROGRESS TABLE - Learning Progress Tracking
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nivel0_completed BOOLEAN DEFAULT FALSE,
    nivel1_completed BOOLEAN DEFAULT FALSE,
    nivel2_completed BOOLEAN DEFAULT FALSE,
    nivel3_completed BOOLEAN DEFAULT FALSE,
    nivel4_completed BOOLEAN DEFAULT FALSE,
    total_time_spent INTEGER DEFAULT 0,
    data_analyses_created INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 4. QUIZ_ATTEMPTS TABLE - Quiz Results
-- ============================================================================
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    level VARCHAR(20) NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    passed BOOLEAN NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_taken INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 5. QUIZ_ANSWERS TABLE - Detailed Quiz Answers
-- ============================================================================
CREATE TABLE IF NOT EXISTS quiz_answers (
    id SERIAL PRIMARY KEY,
    quiz_attempt_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    selected_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    explanation TEXT,
    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
);

-- ============================================================================
-- 6. RATE_LIMITING TABLE - Security Rate Limiting
-- ============================================================================
CREATE TABLE IF NOT EXISTS rate_limiting (
    id SERIAL PRIMARY KEY,
    identifier VARCHAR(100) NOT NULL,
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    locked_until TIMESTAMP
);

-- ============================================================================
-- 7. DASHBOARDS TABLE - Dashboard Configurations
-- Note: Components are stored as JSON in dashboard_config column
-- ============================================================================
CREATE TABLE IF NOT EXISTS dashboards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    dashboard_name VARCHAR(100) NOT NULL,
    dashboard_config TEXT NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 8. SURVEY_RESPONSES TABLE - Survey Responses (All Types)
-- ============================================================================
CREATE TABLE IF NOT EXISTS survey_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    survey_type VARCHAR(50) NOT NULL,
    level VARCHAR(20),
    responses TEXT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, survey_type, level)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- User authentication indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token);

-- Session management indexes
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);

-- Progress tracking indexes
CREATE INDEX IF NOT EXISTS idx_progress_user_id ON user_progress(user_id);

-- Quiz indexes
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_level ON quiz_attempts(user_id, level);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_completed ON quiz_attempts(completed_at);

-- Dashboard indexes
CREATE INDEX IF NOT EXISTS idx_dashboards_user_id ON dashboards(user_id);
CREATE INDEX IF NOT EXISTS idx_dashboards_public ON dashboards(is_public);

-- Rate limiting indexes
CREATE INDEX IF NOT EXISTS idx_rate_limiting_identifier ON rate_limiting(identifier);
CREATE INDEX IF NOT EXISTS idx_rate_limiting_last_attempt ON rate_limiting(last_attempt);

-- Survey indexes
CREATE INDEX IF NOT EXISTS idx_survey_user_type ON survey_responses(user_id, survey_type);
CREATE INDEX IF NOT EXISTS idx_survey_completed ON survey_responses(completed_at);

