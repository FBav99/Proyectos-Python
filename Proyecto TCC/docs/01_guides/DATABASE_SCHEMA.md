# 🗄️ Esquema de Base de Datos SQLite - Plataforma TCC de Análisis de Datos

## 📋 Resumen

Este documento describe el esquema completo de la base de datos SQLite para la Plataforma de Aprendizaje de Análisis de Datos TCC. El esquema está diseñado para soportar autenticación de usuarios, seguimiento de progreso, sistema de cuestionarios y funcionalidades de aprendizaje.

---

## 🏗️ Arquitectura de la Base de Datos

### **Tablas Principales (8 Total)**
1. **Users** - Gestión de Autenticación y Perfiles
2. **User Sessions** - Gestión de Sesiones
3. **User Progress** - Seguimiento del Progreso de Aprendizaje
4. **Quiz Attempts** - Resultados de Cuestionarios
5. **Quiz Answers** - Respuestas Detalladas de Cuestionarios
6. **Rate Limiting** - Protección de Seguridad
7. **Uploaded Files** - Gestión de Archivos Subidos
8. **File Analysis Sessions** - Sesiones de Análisis de Archivos

### **Tablas de Dashboard (2 Total)**
9. **Dashboards** - Configuraciones de Dashboard
10. **Dashboard Components** - Componentes de Dashboard

### **Tablas Opcionales (1 Total)**
11. **User Activity Log** - Seguimiento de Actividad y Auditoría

---

## 📊 Esquemas Detallados de Tablas

### 1. **Users Table** - Autenticación y Perfil de Usuario
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Identificador único del usuario
    username VARCHAR(50) UNIQUE NOT NULL,          -- Nombre de usuario (único)
    email VARCHAR(100) UNIQUE NOT NULL,            -- Correo electrónico (único)
    password_hash VARCHAR(255) NOT NULL,           -- Contraseña encriptada
    first_name VARCHAR(50) NOT NULL,               -- Nombre del usuario
    last_name VARCHAR(50) NOT NULL,                -- Apellido del usuario
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la cuenta
    last_login TIMESTAMP,                          -- Último inicio de sesión
    is_active BOOLEAN DEFAULT 1,                   -- Estado activo de la cuenta
    failed_login_attempts INTEGER DEFAULT 0,       -- Intentos fallidos de login
    locked_until TIMESTAMP,                        -- Cuenta bloqueada hasta (seguridad)
    email_verified BOOLEAN DEFAULT 0,              -- Email verificado
    verification_token VARCHAR(255),                -- Token de verificación de email
    reset_token VARCHAR(255),                      -- Token para resetear contraseña
    reset_token_expires TIMESTAMP                  -- Expiración del token de reset
);
```

**Propósito**: Almacenar datos de autenticación, información del perfil y configuraciones de seguridad del usuario.

**Características Clave**:
- Encriptación segura de contraseñas con bcrypt
- Sistema de verificación de email
- Funcionalidad de reset de contraseña
- Protección contra bloqueo de cuenta
- Seguimiento de intentos fallidos de login

**Estado**: ✅ **MANTENER** - Funcionalidad esencial de autenticación

---

### 2. **User Sessions Table** - Gestión de Sesiones
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único de la sesión
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    session_token VARCHAR(255) UNIQUE NOT NULL,    -- Token único de sesión
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la sesión
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última actividad
    expires_at TIMESTAMP NOT NULL,                 -- Fecha de expiración de la sesión
    ip_address VARCHAR(45),                        -- Dirección IP del usuario
    user_agent TEXT,                               -- Navegador/dispositivo del usuario
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Gestionar sesiones de usuario, rastrear actividad y habilitar logout seguro.

**Características Clave**:
- Tokens de sesión seguros
- Rastreo de actividad
- Expiración automática de sesiones
- Logging de IP y user agent

**Estado**: ✅ **MANTENER** - Gestión de sesiones esencial

---

### 3. **User Progress Table** - Seguimiento del Progreso de Aprendizaje
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del progreso
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    nivel1_completed BOOLEAN DEFAULT 0,            -- Nivel 1 completado
    nivel2_completed BOOLEAN DEFAULT 0,            -- Nivel 2 completado
    nivel3_completed BOOLEAN DEFAULT 0,            -- Nivel 3 completado
    nivel4_completed BOOLEAN DEFAULT 0,            -- Nivel 4 completado
    total_time_spent INTEGER DEFAULT 0,            -- Tiempo total en minutos
    data_analyses_created INTEGER DEFAULT 0,       -- Análisis de datos creados
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Última actualización
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Rastrear el progreso de aprendizaje del usuario a través de todos los niveles y actividades.

**Características Clave**:
- Seguimiento de completado de niveles
- Tiempo dedicado al aprendizaje
- Contador de análisis creados
- Persistencia del progreso

**Estado**: ✅ **MANTENER** - Funcionalidad esencial de seguimiento de progreso

---

### 4. **Quiz Attempts Table** - Resultados de Cuestionarios
```sql
CREATE TABLE quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del intento
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    level VARCHAR(20) NOT NULL,                    -- Nivel del cuestionario ('nivel1', 'nivel2', etc.)
    score INTEGER NOT NULL,                        -- Puntuación obtenida
    total_questions INTEGER NOT NULL,              -- Total de preguntas
    percentage DECIMAL(5,2) NOT NULL,              -- Porcentaje de acierto
    passed BOOLEAN NOT NULL,                       -- ¿Aprobó el cuestionario?
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de completado
    time_taken INTEGER,                            -- Tiempo tomado en segundos
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Almacenar resultados de intentos de cuestionarios y métricas de rendimiento.

**Características Clave**:
- Seguimiento de puntuación por nivel
- Estado de aprobado/reprobado
- Seguimiento de tiempo
- Análisis de rendimiento

**Estado**: ✅ **MANTENER** - Sistema de cuestionarios implementado

---

### 5. **Quiz Answers Table** - Respuestas Detalladas de Cuestionarios
```sql
CREATE TABLE quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único de la respuesta
    quiz_attempt_id INTEGER NOT NULL,              -- ID del intento del cuestionario (referencia)
    question_text TEXT NOT NULL,                   -- Texto de la pregunta
    selected_answer TEXT NOT NULL,                 -- Respuesta seleccionada por el usuario
    correct_answer TEXT NOT NULL,                  -- Respuesta correcta
    is_correct BOOLEAN NOT NULL,                   -- ¿Es correcta la respuesta?
    explanation TEXT,                              -- Explicación de la respuesta
    FOREIGN KEY (quiz_attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
);
```

**Propósito**: Almacenar respuestas detalladas para cada pregunta del cuestionario.

**Características Clave**:
- Seguimiento pregunta por pregunta
- Respuestas correctas/incorrectas
- Explicaciones para el aprendizaje
- Análisis detallado

**Estado**: ✅ **MANTENER** - Sistema de cuestionarios implementado

---

### 6. **Rate Limiting Table** - Protección de Seguridad
```sql
CREATE TABLE rate_limiting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del registro
    identifier VARCHAR(100) NOT NULL,              -- Identificador (username, IP, etc.)
    attempts INTEGER DEFAULT 0,                    -- Número de intentos
    last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Último intento
    locked_until TIMESTAMP                         -- Bloqueado hasta (seguridad)
);
```

**Propósito**: Prevenir ataques de fuerza bruta y proteger la seguridad del sistema.

**Características Clave**:
- Limitación de intentos de login
- Protección contra ataques
- Bloqueo temporal de cuentas
- Seguridad del sistema

**Estado**: ✅ **MANTENER** - Protección de seguridad esencial

---

### 7. **Uploaded Files Table** - Gestión de Archivos Subidos
```sql
CREATE TABLE uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del archivo
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    filename VARCHAR(255) NOT NULL,                -- Nombre del archivo en el sistema
    original_filename VARCHAR(255) NOT NULL,       -- Nombre original del archivo
    file_size INTEGER NOT NULL,                    -- Tamaño del archivo en bytes
    file_type VARCHAR(50) NOT NULL,                -- Tipo de archivo ('csv', 'xlsx', 'xls')
    file_path VARCHAR(500) NOT NULL,               -- Ruta donde se almacena el archivo
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de subida
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Último acceso
    is_active BOOLEAN DEFAULT 1,                   -- Estado activo del archivo
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Gestionar archivos de datos subidos por los usuarios para análisis.

**Características Clave**:
- Almacenamiento de metadata de archivos
- Seguimiento de acceso y uso
- Organización por usuario
- Gestión de almacenamiento

**Estado**: ✅ **MANTENER** - Funcionalidad de carga de archivos planeada

---

### 8. **File Analysis Sessions Table** - Sesiones de Análisis de Archivos
```sql
CREATE TABLE file_analysis_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único de la sesión
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    file_id INTEGER NOT NULL,                      -- ID del archivo analizado (referencia)
    session_name VARCHAR(100),                     -- Nombre de la sesión de análisis
    filters_applied TEXT,                          -- Filtros aplicados (JSON)
    metrics_calculated TEXT,                       -- Métricas calculadas (JSON)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la sesión
    duration_minutes INTEGER,                      -- Duración de la sesión en minutos
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);
```

**Propósito**: Rastrear sesiones de análisis y configuraciones aplicadas a archivos.

**Características Clave**:
- Historial de análisis por archivo
- Configuraciones de filtros aplicados
- Métricas calculadas en cada sesión
- Seguimiento de tiempo de análisis

**Estado**: ✅ **MANTENER** - Funcionalidad de análisis de archivos planeada

---



---

### 9. **Dashboards Table** - Configuraciones de Dashboard
```sql
CREATE TABLE dashboards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del dashboard
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    dashboard_name VARCHAR(100) NOT NULL,          -- Nombre del dashboard
    dashboard_config TEXT NOT NULL,                -- Configuración del dashboard (JSON)
    is_public BOOLEAN DEFAULT 0,                   -- ¿Es público el dashboard?
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de última actualización
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Último acceso
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Almacenar configuraciones de dashboards creados por los usuarios.

**Características Clave**:
- Persistencia de dashboards personalizados
- Configuraciones en formato JSON
- Compartir dashboards públicos/privados
- Seguimiento de uso y actualizaciones

**Estado**: ✅ **MANTENER** - Funcionalidad de dashboard planeada

---

### 10. **Dashboard Components Table** - Componentes de Dashboard
```sql
CREATE TABLE dashboard_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del componente
    dashboard_id INTEGER NOT NULL,                 -- ID del dashboard (referencia)
    component_type VARCHAR(50) NOT NULL,           -- Tipo de componente ('chart', 'metric', 'table')
    component_config TEXT NOT NULL,                -- Configuración del componente (JSON)
    position_x INTEGER,                            -- Posición X en el dashboard
    position_y INTEGER,                            -- Posición Y en el dashboard
    width INTEGER,                                 -- Ancho del componente
    height INTEGER,                                -- Alto del componente
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (dashboard_id) REFERENCES dashboards(id) ON DELETE CASCADE
);
```

**Propósito**: Almacenar componentes individuales y su configuración en dashboards.

**Características Clave**:
- Componentes posicionables en dashboards
- Configuraciones flexibles por tipo
- Layout personalizable
- Persistencia de diseño

**Estado**: ✅ **MANTENER** - Funcionalidad de dashboard planeada

---

### 11. **User Activity Log Table** - Seguimiento de Actividad y Auditoría
```sql
CREATE TABLE user_activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Identificador único del registro
    user_id INTEGER NOT NULL,                      -- ID del usuario (referencia)
    activity_type VARCHAR(50) NOT NULL,            -- Tipo de actividad ('login', 'upload', 'analysis', 'quiz')
    activity_details TEXT,                         -- Detalles de la actividad (JSON)
    ip_address VARCHAR(45),                        -- Dirección IP del usuario
    user_agent TEXT,                               -- Navegador/dispositivo del usuario
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de la actividad
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Propósito**: Rastrear actividades del usuario para análisis y seguridad.

**Características Clave**:
- Monitoreo de actividades
- Auditoría de seguridad
- Análisis de uso
- Rastreo de comportamiento

**Estado**: ⚠️ **OPCIONAL** - Útil para auditoría de seguridad si es necesario

---

## 🗑️ **TABLAS NO IMPLEMENTADAS (RECOMENDADO ELIMINAR)**

### **Razones para Eliminar:**

#### **Uploaded Files Table**
- **Estado**: ❌ **NO IMPLEMENTADO**
- **Razón**: Tu aplicación usa datasets de muestra, no sistema de carga de archivos
- **Acción**: **ELIMINAR** - No se usa en el flujo actual

#### **File Analysis Sessions Table**
- **Estado**: ❌ **NO IMPLEMENTADO**
- **Razón**: No hay seguimiento de sesiones de análisis de archivos
- **Acción**: **ELIMINAR** - No implementado en tu workflow actual

#### **Dashboards Table**
- **Estado**: ❌ **NO IMPLEMENTADO**
- **Razón**: Tus dashboards se crean al momento, no se guardan
- **Acción**: **ELIMINAR** - No hay persistencia de dashboards

#### **Dashboard Components Table**
- **Estado**: ❌ **NO IMPLEMENTADO**
- **Razón**: No hay persistencia de componentes de dashboard
- **Acción**: **ELIMINAR** - No necesario para el sistema actual

#### **System Metrics Table**
- **Estado**: ❌ **NO IMPLEMENTADO**
- **Razón**: No hay recolección de métricas del sistema
- **Acción**: **ELIMINAR** - No implementado en tu sistema actual

---

## 🔍 Índices de Base de Datos para Rendimiento

```sql
-- Índices de autenticación de usuarios
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_reset_token ON users(reset_token);

-- Índices de gestión de sesiones
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);

-- Índices de seguimiento de progreso
CREATE INDEX idx_progress_user_id ON user_progress(user_id);

-- Índices de cuestionarios
CREATE INDEX idx_quiz_attempts_user_level ON quiz_attempts(user_id, level);
CREATE INDEX idx_quiz_attempts_completed ON quiz_attempts(completed_at);

-- Índices de limitación de tasa
CREATE INDEX idx_rate_limiting_identifier ON rate_limiting(identifier);
CREATE INDEX idx_rate_limiting_last_attempt ON rate_limiting(last_attempt);

-- Índices de log de actividad (si se mantiene)
CREATE INDEX idx_activity_user_type ON user_activity_log(user_id, activity_type);
CREATE INDEX idx_activity_created ON user_activity_log(created_at);
```

---

## 🚀 Fases de Implementación

### **Fase 1: Funcionalidad Core (Prioridad: Alta)**
- Tabla Users - Sistema de autenticación
- Tabla User Sessions - Gestión de sesiones
- Tabla User Progress - Seguimiento de progreso
- Tabla Rate Limiting - Protección de seguridad

### **Fase 2: Sistema de Cuestionarios (Prioridad: Alta)**
- Tabla Quiz Attempts - Resultados de cuestionarios
- Tabla Quiz Answers - Respuestas detalladas

### **Fase 3: Funcionalidades Opcionales (Prioridad: Baja)**
- Tabla Achievements - Sistema de logros (opcional)
- Tabla User Activity Log - Auditoría de actividad (opcional)

---

## 🔧 Utilidades de Base de Datos

### **Gestión de Conexiones**
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

### **Sistema de Migraciones**
```python
def run_migrations():
    """Ejecutar migraciones de base de datos en orden"""
    migrations = [
        "001_create_users_table.sql",
        "002_create_sessions_table.sql",
        "003_create_progress_table.sql",
        "004_create_quiz_tables.sql",
        "005_create_rate_limiting_table.sql"
    ]
    
    for migration in migrations:
        with open(f"migrations/{migration}") as f:
            sql = f.read()
            with get_db_connection() as conn:
                conn.executescript(sql)
                conn.commit()
```

---

## 📊 Relaciones de Datos

### **Relaciones Centradas en el Usuario**
```
Users (1) ←→ (Muchos) User Sessions
Users (1) ←→ (1) User Progress
Users (1) ←→ (Muchos) Quiz Attempts
Users (1) ←→ (Muchos) Achievements (opcional)
Users (1) ←→ (Muchos) Activity Logs (opcional)
```

### **Relaciones de Cuestionarios**
```
Quiz Attempts (1) ←→ (Muchos) Quiz Answers
Users (1) ←→ (Muchos) Quiz Attempts
```

### **Tipos de Relaciones:**

#### **Uno a Uno (1:1)**
- **Users ↔ User Progress** - Cada usuario tiene exactamente un registro de progreso

#### **Uno a Muchos (1:Muchos)**
- **Users → User Sessions** - Un usuario puede tener múltiples sesiones
- **Users → Quiz Attempts** - Un usuario puede tener múltiples intentos de cuestionario
- **Users → Achievements** - Un usuario puede desbloquear múltiples logros
- **Users → Activity Logs** - Un usuario puede tener múltiples registros de actividad
- **Quiz Attempts → Quiz Answers** - Un intento tiene múltiples respuestas

---

## 🗺️ Diagrama de Relaciones de Entidades (ERD)

### **Vista General del Esquema de Base de Datos**

```
                    ┌─────────────────────────────────────────────────┐
                    │                    USERS                       │
                    │              (Tabla Central)                   │
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
               │(1:Muchos)│         │(1:1)        │        │(1:Muchos) │
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
               │QUIZ     │         │RATE         │        │USER     │
               │ATTEMPTS │         │LIMITING     │        │ACTIVITY │
               │(1:Muchos)│         │(Independiente)│        │LOG      │
               │         │         │             │        │(1:Muchos)│
               │level    │         │identifier  │        │activity_│
               │score    │         │attempts    │        │type     │
               │percentage│        │locked_until│        │activity_│
               │passed   │         │            │        │details  │
               │time_taken│        │            │        │ip_addr  │
               └────┬────┘         └────────────┘        └─────────┘
                    │
               ┌────▼────┐
               │QUIZ     │
               │ANSWERS  │
               │(1:Muchos)│
               │         │
               │question_│
               │text     │
               │selected_│
               │answer   │
               │is_correct│
               └─────────┘
```

---

## 🔒 Consideraciones de Seguridad

### **Protección de Datos**
- Todas las contraseñas están encriptadas usando bcrypt
- Los tokens de sesión son criptográficamente seguros
- Prevención de inyección SQL a través de consultas parametrizadas
- Validación y sanitización de entrada

### **Privacidad**
- Los datos del usuario están aislados por user_id
- Los datos sensibles están encriptados en reposo
- Trazas de auditoría para eventos de seguridad
- Consideraciones de cumplimiento GDPR

### **Rendimiento**
- Consultas indexadas para búsquedas rápidas
- Pool de conexiones para escalabilidad
- Mantenimiento regular de la base de datos
- Optimización de consultas

---

## 📈 Mejoras Futuras

### **Adiciones Potenciales**
1. **Tabla de Integración OAuth** - Para login de Google/Microsoft
2. **Tabla de Preferencias de Usuario** - Configuraciones personalizables
3. **Sistema de Notificaciones** - Notificaciones en la aplicación
4. **Sistema de Colaboración** - Dashboards y archivos compartidos

### **Consideraciones de Escalabilidad**
- Particionamiento de base de datos para grandes bases de usuarios
- Réplicas de lectura para consultas analíticas
- Capa de caché para datos frecuentemente accedidos
- Procedimientos de respaldo y recuperación

---

## 🎯 **ESTRUCTURA FINAL DE LA BASE DE DATOS**

### **✅ Tablas Mantenidas (12 tablas total)**

#### **Tablas de Autenticación y Seguridad (3 tablas)**
1. **users** - Autenticación esencial ✅
2. **user_sessions** - Gestión de sesiones ✅
3. **rate_limiting** - Protección de seguridad ✅

#### **Tablas de Aprendizaje (3 tablas)**
4. **user_progress** - Seguimiento de progreso ✅
5. **quiz_attempts** - Sistema de cuestionarios ✅
6. **quiz_answers** - Respuestas de cuestionarios ✅

#### **Tablas de Archivos y Análisis (2 tablas)**
7. **uploaded_files** - Gestión de archivos subidos ✅
8. **file_analysis_sessions** - Sesiones de análisis ✅

#### **Tablas de Dashboard (2 tablas)**
9. **dashboards** - Configuraciones de dashboard ✅
10. **dashboard_components** - Componentes de dashboard ✅

#### **Tablas Opcionales (1 tabla)**
11. **user_activity_log** - Auditoría de actividad (opcional) ✅

#### **Tabla del Sistema (1 tabla)**
12. **sqlite_sequence** - Control interno de SQLite 🔧

### **🗑️ Tablas Eliminadas (2 tablas)**
- ~~`achievements`~~ - Sistema de logros (demasiado "gamey")
- ~~`system_metrics`~~ - Métricas del sistema (no implementado)

### **📊 Resumen de Cambios**
- **Antes**: 14 tablas (incluyendo 2 no implementadas)
- **Después**: 12 tablas (todas funcionales o planeadas)
- **Reducción**: 2 tablas eliminadas
- **Estado**: Base de datos limpia y enfocada en funcionalidades reales

### **🎯 Beneficios de la Limpieza**
1. **Enfoque en lo esencial**: Solo tablas que realmente necesitas
2. **Mantenimiento más simple**: Menos complejidad innecesaria
3. **Mejor rendimiento**: Menos tablas = consultas más rápidas
4. **Arquitectura clara**: Cada tabla tiene un propósito definido
5. **Preparado para el futuro**: Dashboard y archivos listos para implementar

---

*Este esquema proporciona una base sólida para la Plataforma de Análisis de Datos TCC mientras mantiene la flexibilidad para mejoras futuras.*
