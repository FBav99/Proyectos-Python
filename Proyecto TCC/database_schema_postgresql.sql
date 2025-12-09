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
-- 7. UPLOADED_FILES TABLE - File Upload Management
-- ============================================================================
CREATE TABLE IF NOT EXISTS uploaded_files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 8. FILE_ANALYSIS_SESSIONS TABLE - Analysis Session History
-- ============================================================================
CREATE TABLE IF NOT EXISTS file_analysis_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    session_name VARCHAR(100),
    filters_applied TEXT,
    metrics_calculated TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);

-- ============================================================================
-- 9. DASHBOARDS TABLE - Dashboard Configurations
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
-- 10. DASHBOARD_COMPONENTS TABLE - Dashboard Components
-- ============================================================================
CREATE TABLE IF NOT EXISTS dashboard_components (
    id SERIAL PRIMARY KEY,
    dashboard_id INTEGER NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    component_config TEXT NOT NULL,
    position_x INTEGER,
    position_y INTEGER,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dashboard_id) REFERENCES dashboards(id) ON DELETE CASCADE
);

-- ============================================================================
-- 11. USER_ACTIVITY_LOG TABLE - Security Auditing (Optional)
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- 12. SURVEY_RESPONSES TABLE - Survey Responses (All Types)
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

-- File management indexes
CREATE INDEX IF NOT EXISTS idx_files_user_id ON uploaded_files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_uploaded_at ON uploaded_files(uploaded_at);

-- Dashboard indexes
CREATE INDEX IF NOT EXISTS idx_dashboards_user_id ON dashboards(user_id);
CREATE INDEX IF NOT EXISTS idx_dashboards_public ON dashboards(is_public);

-- Activity tracking indexes
CREATE INDEX IF NOT EXISTS idx_activity_user_type ON user_activity_log(user_id, activity_type);
CREATE INDEX IF NOT EXISTS idx_activity_created ON user_activity_log(created_at);

-- Rate limiting indexes
CREATE INDEX IF NOT EXISTS idx_rate_limiting_identifier ON rate_limiting(identifier);
CREATE INDEX IF NOT EXISTS idx_rate_limiting_last_attempt ON rate_limiting(last_attempt);

-- Survey indexes
CREATE INDEX IF NOT EXISTS idx_survey_user_type ON survey_responses(user_id, survey_type);
CREATE INDEX IF NOT EXISTS idx_survey_completed ON survey_responses(completed_at);

