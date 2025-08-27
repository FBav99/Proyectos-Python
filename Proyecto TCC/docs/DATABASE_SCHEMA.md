# 🗄️ SQLite Database Schema - TCC Data Analysis Platform

## 📋 Overview

This document outlines the complete SQLite database schema for the TCC Data Analysis Learning Platform. The schema is designed to support user authentication, progress tracking, file management, dashboard creation, and comprehensive analytics.

---

## 🏗️ Database Architecture

### **Core Tables (12 Total)**
1. **Users** - Authentication & Profile Management
2. **User Sessions** - Session Management
3. **User Progress** - Learning Progress Tracking
4. **Quiz Attempts** - Quiz Results & Scoring
5. **Quiz Answers** - Detailed Quiz Responses
6. **Achievements** - User Achievement System
7. **Uploaded Files** - File Storage & Management
8. **File Analysis Sessions** - Analysis History
9. **Dashboards** - Saved Dashboard Configurations
10. **Dashboard Components** - Individual Dashboard Elements
11. **User Activity Log** - Activity Tracking & Analytics
12. **System Metrics** - Application Performance Metrics

---

## 📊 Detailed Table Schemas

### 1. **Users Table** - User Authentication & Profile
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    email_verified BOOLEAN DEFAULT 0,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP
);
```

**Purpose**: Store user authentication data, profile information, and security settings.

**Key Features**:
- Secure password hashing
- Email verification system
- Password reset functionality
- Account lockout protection
- Login attempt tracking

---

### 2. **User Sessions Table** - Session Management
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Manage user sessions, track activity, and enable secure logout.

**Key Features**:
- Secure session tokens
- Activity tracking
- Automatic session expiration
- IP and user agent logging

---

### 3. **User Progress Table** - Learning Progress Tracking
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    nivel1_completed BOOLEAN DEFAULT 0,
    nivel2_completed BOOLEAN DEFAULT 0,
    nivel3_completed BOOLEAN DEFAULT 0,
    nivel4_completed BOOLEAN DEFAULT 0,
    total_time_spent INTEGER DEFAULT 0, -- in minutes
    data_analyses_created INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Track user learning progress across all levels and activities.

**Key Features**:
- Level completion tracking
- Time spent learning
- Analysis creation counter
- Progress persistence

---

### 4. **Quiz Attempts Table** - Quiz Results
```sql
CREATE TABLE quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    level VARCHAR(20) NOT NULL, -- 'nivel1', 'nivel2', etc.
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    passed BOOLEAN NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_taken INTEGER, -- in seconds
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Store quiz attempt results and performance metrics.

**Key Features**:
- Score tracking per level
- Pass/fail status
- Time tracking
- Performance analytics

---

### 5. **Quiz Answers Table** - Detailed Quiz Responses
```sql
CREATE TABLE quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_attempt_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    selected_answer TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    explanation TEXT,
    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
);
```

**Purpose**: Store detailed responses for each quiz question.

**Key Features**:
- Question-by-question tracking
- Correct/incorrect responses
- Explanations for learning
- Detailed analytics

---

### 6. **Achievements Table** - User Achievement System
```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_type VARCHAR(50) NOT NULL, -- 'first_level', 'quiz_master', etc.
    achievement_title VARCHAR(100) NOT NULL,
    achievement_description TEXT,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Track user achievements and gamification elements.

**Key Features**:
- Achievement unlocking
- Progress motivation
- Gamification tracking
- Achievement history

---

### 7. **Uploaded Files Table** - File Storage & Management
```sql
CREATE TABLE uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL, -- in bytes
    file_type VARCHAR(50) NOT NULL, -- 'csv', 'xlsx', 'xls'
    file_path VARCHAR(500) NOT NULL, -- path to stored file
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Manage user-uploaded data files and their metadata.

**Key Features**:
- File metadata storage
- Access tracking
- File organization
- Storage management

---

### 8. **File Analysis Sessions Table** - Analysis History
```sql
CREATE TABLE file_analysis_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    session_name VARCHAR(100),
    filters_applied TEXT, -- JSON string of filters
    metrics_calculated TEXT, -- JSON string of metrics
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_minutes INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);
```

**Purpose**: Track analysis sessions and their configurations.

**Key Features**:
- Analysis session history
- Filter configurations
- Metric calculations
- Session duration tracking

---

### 9. **Dashboards Table** - Saved Dashboard Configurations
```sql
CREATE TABLE dashboards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    dashboard_name VARCHAR(100) NOT NULL,
    dashboard_config TEXT NOT NULL, -- JSON configuration
    is_public BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Store user-created dashboard configurations.

**Key Features**:
- Dashboard persistence
- Public/private sharing
- Configuration storage
- Access tracking

---

### 10. **Dashboard Components Table** - Individual Dashboard Elements
```sql
CREATE TABLE dashboard_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dashboard_id INTEGER NOT NULL,
    component_type VARCHAR(50) NOT NULL, -- 'chart', 'metric', 'table'
    component_config TEXT NOT NULL, -- JSON configuration
    position_x INTEGER,
    position_y INTEGER,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dashboard_id) REFERENCES dashboards(id) ON DELETE CASCADE
);
```

**Purpose**: Store individual dashboard component configurations.

**Key Features**:
- Component positioning
- Layout management
- Configuration storage
- Component types

---

### 11. **User Activity Log Table** - Activity Tracking & Analytics
```sql
CREATE TABLE user_activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL, -- 'login', 'upload', 'analysis', 'quiz'
    activity_details TEXT, -- JSON details
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Purpose**: Track user activities for analytics and security.

**Key Features**:
- Activity monitoring
- Security auditing
- Usage analytics
- Behavior tracking

---

### 12. **System Metrics Table** - Application Performance Metrics
```sql
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    metric_unit VARCHAR(20),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data TEXT -- JSON for additional context
);
```

**Purpose**: Track system performance and application metrics.

**Key Features**:
- Performance monitoring
- System health tracking
- Metric collection
- Trend analysis

---

## 🔍 Database Indexes for Performance

```sql
-- User authentication indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_reset_token ON users(reset_token);

-- Session management indexes
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);

-- Progress tracking indexes
CREATE INDEX idx_progress_user_id ON user_progress(user_id);

-- Quiz indexes
CREATE INDEX idx_quiz_attempts_user_level ON quiz_attempts(user_id, level);
CREATE INDEX idx_quiz_attempts_completed ON quiz_attempts(completed_at);

-- File management indexes
CREATE INDEX idx_files_user_id ON uploaded_files(user_id);
CREATE INDEX idx_files_uploaded_at ON uploaded_files(uploaded_at);

-- Dashboard indexes
CREATE INDEX idx_dashboards_user_id ON dashboards(user_id);
CREATE INDEX idx_dashboards_public ON dashboards(is_public);

-- Activity tracking indexes
CREATE INDEX idx_activity_user_type ON user_activity_log(user_id, activity_type);
CREATE INDEX idx_activity_created ON user_activity_log(created_at);
```

---

## 🚀 Implementation Phases

### **Phase 1: Core Authentication** (Priority: High)
- Users table
- User Sessions table
- Basic authentication system
- Password hashing and security

### **Phase 2: Progress Tracking** (Priority: High)
- User Progress table
- Quiz Attempts table
- Quiz Answers table
- Achievements table

### **Phase 3: File Management** (Priority: Medium)
- Uploaded Files table
- File Analysis Sessions table
- File storage system

### **Phase 4: Dashboard System** (Priority: Medium)
- Dashboards table
- Dashboard Components table
- Dashboard persistence

### **Phase 5: Analytics & Monitoring** (Priority: Low)
- User Activity Log table
- System Metrics table
- Performance monitoring

---

## 🔧 Database Utilities

### **Connection Management**
```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('tcc_database.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

### **Migration System**
```python
def run_migrations():
    """Run database migrations in order"""
    migrations = [
        "001_create_users_table.sql",
        "002_create_sessions_table.sql",
        # ... more migrations
    ]
    
    for migration in migrations:
        with open(f"migrations/{migration}") as f:
            sql = f.read()
            with get_db_connection() as conn:
                conn.executescript(sql)
                conn.commit()
```

---

## 📊 Data Relationships

### **User-Centric Relationships**
```
Users (1) ←→ (Many) User Sessions
Users (1) ←→ (1) User Progress
Users (1) ←→ (Many) Quiz Attempts
Users (1) ←→ (Many) Achievements
Users (1) ←→ (Many) Uploaded Files
Users (1) ←→ (Many) Dashboards
Users (1) ←→ (Many) Activity Logs
```

### **Quiz Relationships**
```
Quiz Attempts (1) ←→ (Many) Quiz Answers
Users (1) ←→ (Many) Quiz Attempts
```

### **File Relationships**
```
Uploaded Files (1) ←→ (Many) File Analysis Sessions
Users (1) ←→ (Many) Uploaded Files
```

### **Dashboard Relationships**
```
Dashboards (1) ←→ (Many) Dashboard Components
Users (1) ←→ (Many) Dashboards
```

---

## 🗺️ Entity Relationship Diagram (ERD)

### **Visual Database Schema Overview**

```
                    ┌─────────────────────────────────────────────────┐
                    │                    USERS                       │
                    │              (Central Hub Table)               │
                    │  ┌─────────────────────────────────────────┐   │
                    │  │ id (PK)                                │   │
                    │  │ username (UNIQUE)                      │   │
                    │  │ email (UNIQUE)                         │   │
                    │  │ password_hash                          │   │
                    │  │ first_name, last_name                  │   │
                    │  │ created_at, last_login                 │   │
                    │  │ is_active, failed_login_attempts       │   │
                    │  │ email_verified, reset_token            │   │
                    │  └─────────────────────────────────────────┘   │
                    └─────────────────────┬───────────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
               ┌────▼────┐         ┌──────▼──────┐        ┌────▼────┐
               │USER     │         │USER         │        │ACHIEVE- │
               │SESSIONS │         │PROGRESS     │        │MENTS    │
               │(1:Many) │         │(1:1)        │        │(1:Many) │
               │         │         │             │        │         │
               │session_ │         │nivel1_compl.│        │achievem. │
               │token    │         │nivel2_compl.│        │_type    │
               │expires_ │         │nivel3_compl.│        │title    │
               │at       │         │nivel4_compl.│        │unlocked_│
               │ip_addr  │         │total_time   │        │at       │
               └─────────┘         └─────────────┘        └─────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
               ┌────▼────┐         ┌──────▼──────┐        ┌────▼────┐
               │QUIZ     │         │UPLOADED     │        │DASH-    │
               │ATTEMPTS │         │FILES        │        │BOARDS   │
               │(1:Many) │         │(1:Many)     │        │(1:Many) │
               │         │         │             │        │         │
               │level    │         │filename     │        │dashboard│
               │score    │         │file_size    │        │_name    │
               │percentage│        │file_type    │        │dashboard│
               │passed   │         │file_path    │        │_config  │
               │time_taken│        │uploaded_at  │        │is_public│
               └────┬────┘         └──────┬──────┘        └────┬────┘
                    │                     │                    │
               ┌────▼────┐         ┌──────▼──────┐        ┌────▼────┐
               │QUIZ     │         │FILE         │        │DASHBOARD│
               │ANSWERS  │         │ANALYSIS     │        │COMPONENTS│
               │(1:Many) │         │SESSIONS     │        │(1:Many) │
               │         │         │(1:Many)     │        │         │
               │question_│         │session_name │        │component│
               │text     │         │filters_appl.│        │_type    │
               │selected_│         │metrics_calc.│        │component│
               │answer   │         │duration_min.│        │_config  │
               │is_correct│        │created_at   │        │position │
               └─────────┘         └─────────────┘        └─────────┘

                    ┌─────────────────────────────────────────────────┐
                    │              ANALYTICS TABLES                   │
                    │                                                 │
               ┌────▼────┐                                    ┌────▼────┐
               │USER     │                                    │SYSTEM   │
               │ACTIVITY │                                    │METRICS  │
               │LOG      │                                    │         │
               │(1:Many) │                                    │(Independent)│
               │         │                                    │         │
               │activity_│                                    │metric_  │
               │type     │                                    │name     │
               │activity_│                                    │metric_  │
               │details  │                                    │value    │
               │ip_addr  │                                    │recorded_│
               │created_ │                                    │at       │
               │at       │                                    │         │
               └─────────┘                                    └─────────┘
```

### **Relationship Types:**

#### **One-to-One (1:1)**
- **Users ↔ User Progress** - Each user has exactly one progress record

#### **One-to-Many (1:Many)**
- **Users → User Sessions** - One user can have multiple sessions
- **Users → Quiz Attempts** - One user can have multiple quiz attempts
- **Users → Achievements** - One user can unlock multiple achievements
- **Users → Uploaded Files** - One user can upload multiple files
- **Users → Dashboards** - One user can create multiple dashboards
- **Users → Activity Logs** - One user can have multiple activity records
- **Quiz Attempts → Quiz Answers** - One attempt has multiple answers
- **Uploaded Files → File Analysis Sessions** - One file can have multiple analysis sessions
- **Dashboards → Dashboard Components** - One dashboard has multiple components

#### **Independent Tables**
- **System Metrics** - Standalone table for application metrics

### **Key Design Patterns:**

#### **🔗 Central Hub Pattern**
- **Users table** acts as the central hub connecting all user-related data
- All major entities have a foreign key reference to `users.id`

#### **📊 Hierarchical Structure**
- Clear parent-child relationships (Users → Quiz Attempts → Quiz Answers)
- Logical grouping of related functionality

#### **🔄 Audit Trail**
- Timestamp fields (`created_at`, `updated_at`, `last_accessed`) for tracking
- Activity logging for security and analytics

#### **📈 Scalability Considerations**
- Indexed foreign keys for performance
- JSON fields for flexible configuration storage
- Separate tables for different concerns (authentication, progress, analytics)

---

## 🔒 Security Considerations

### **Data Protection**
- All passwords are hashed using bcrypt
- Session tokens are cryptographically secure
- SQL injection prevention through parameterized queries
- Input validation and sanitization

### **Privacy**
- User data is isolated by user_id
- Sensitive data is encrypted at rest
- Audit trails for security events
- GDPR compliance considerations

### **Performance**
- Indexed queries for fast lookups
- Connection pooling for scalability
- Regular database maintenance
- Query optimization

---

## 📈 Future Enhancements

### **Potential Additions**
1. **OAuth Integration Table** - For Google/Microsoft login
2. **User Preferences Table** - Customizable settings
3. **Notification System Table** - In-app notifications
4. **Collaboration Tables** - Shared dashboards and files
5. **API Usage Tracking** - For external integrations

### **Scalability Considerations**
- Database sharding for large user bases
- Read replicas for analytics queries
- Caching layer for frequently accessed data
- Backup and recovery procedures

---

*This schema provides a comprehensive foundation for the TCC Data Analysis Platform while maintaining flexibility for future enhancements.*
