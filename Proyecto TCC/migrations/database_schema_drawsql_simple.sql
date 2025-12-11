-- ============================================================================
-- PostgreSQL DDL for DrawSQL ERD Generator
-- Contains only the 8 tables currently in use
-- ============================================================================

CREATE TABLE users (
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

CREATE TABLE user_sessions (
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

CREATE TABLE user_progress (
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

CREATE TABLE quiz_attempts (
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

CREATE TABLE quiz_answers (
    id SERIAL PRIMARY KEY,
    quiz_attempt_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    selected_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    explanation TEXT,
    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
);

CREATE TABLE rate_limiting (
    id SERIAL PRIMARY KEY,
    identifier VARCHAR(100) NOT NULL,
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    locked_until TIMESTAMP
);

CREATE TABLE dashboards (
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

CREATE TABLE survey_responses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    survey_type VARCHAR(50) NOT NULL,
    level VARCHAR(20),
    responses TEXT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, survey_type, level)
);

