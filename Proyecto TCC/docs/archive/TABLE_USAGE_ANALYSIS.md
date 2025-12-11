# 📊 Database Table Usage Analysis

## ✅ **USED TABLES (8 tables)**

### Core Authentication & Security
1. **`users`** ✅ **VITAL**
   - Used for: User registration, authentication, login
   - Queries: INSERT (registration), SELECT (login, profile), UPDATE (password, email)
   - Status: **ESSENTIAL - DO NOT REMOVE**

2. **`user_sessions`** ✅ **VITAL**
   - Used for: Session management, authentication tokens
   - Queries: INSERT (create session), SELECT (validate session)
   - Status: **ESSENTIAL - DO NOT REMOVE**

3. **`rate_limiting`** ✅ **VITAL**
   - Used for: Security protection against brute force attacks
   - Queries: INSERT, SELECT, UPDATE
   - Status: **ESSENTIAL - DO NOT REMOVE**

### Learning & Progress
4. **`user_progress`** ✅ **VITAL**
   - Used for: Tracking level completion (nivel0-4), time spent, analyses created
   - Queries: INSERT (new user), SELECT (get progress), UPDATE (level completion)
   - Status: **ESSENTIAL - DO NOT REMOVE**

5. **`quiz_attempts`** ✅ **VITAL**
   - Used for: Storing quiz results and scores
   - Queries: INSERT (save quiz attempt)
   - Status: **ESSENTIAL - DO NOT REMOVE**

6. **`quiz_answers`** ✅ **VITAL**
   - Used for: Storing individual question answers for each quiz attempt
   - Queries: INSERT (save answers)
   - Status: **ESSENTIAL - DO NOT REMOVE**

7. **`survey_responses`** ✅ **VITAL**
   - Used for: Storing survey responses (initial, level, final surveys)
   - Queries: INSERT (save response), SELECT (check completion, get responses)
   - Status: **ESSENTIAL - DO NOT REMOVE**

### Dashboard
8. **`dashboards`** ✅ **USED**
   - Used for: Persisting dashboard configurations
   - Queries: INSERT (create dashboard), SELECT (list dashboards), UPDATE (update dashboard), DELETE (delete dashboard)
   - Location: `core/dashboard_repository.py`
   - Note: Components are stored as JSON in `dashboard_config` column
   - Status: **KEEP - Currently in use**

---

## ❌ **UNUSED TABLES (4 tables)**

### File Management (Not Implemented)
1. **`uploaded_files`** ❌ **NOT USED**
   - **Status**: Table created but never written to
   - **Evidence**: No INSERT/SELECT queries found in codebase
   - **Reason**: Files are handled in `st.session_state` only, not persisted to database
   - **Recommendation**: **REMOVE** - Files are not stored in database

2. **`file_analysis_sessions`** ❌ **NOT USED**
   - **Status**: Table created but never written to
   - **Evidence**: No INSERT/SELECT queries found
   - **Reason**: Depends on `uploaded_files` table which isn't used
   - **Recommendation**: **REMOVE** - No file analysis tracking implemented

### Dashboard Components (Redundant)
3. **`dashboard_components`** ❌ **NOT USED**
   - **Status**: Table created but never written to
   - **Evidence**: No INSERT/SELECT queries found
   - **Reason**: Components are stored as JSON inside `dashboards.dashboard_config` column
   - **Location**: Components managed in `st.session_state.dashboard_components` and serialized to JSON
   - **Recommendation**: **REMOVE** - Redundant, components already stored in dashboards table

### Activity Logging (Not Implemented)
4. **`user_activity_log`** ❌ **NOT USED**
   - **Status**: Table created but never written to
   - **Evidence**: `log_activity()` method only logs to Python logger, not database
   - **Location**: `core/auth_service.py:332-338`
   - **Recommendation**: **REMOVE** - Activity logging not implemented in database

---

## 📋 **Summary**

### Current State
- **Total Tables**: 12 tables
- **Used Tables**: 8 tables ✅
- **Unused Tables**: 4 tables ❌

### Recommended Action
**Remove 4 unused tables:**
1. `uploaded_files`
2. `file_analysis_sessions`
3. `dashboard_components`
4. `user_activity_log`

### After Cleanup
- **Remaining Tables**: 8 tables (all essential and in use)
- **Cleaner Schema**: No orphaned tables
- **Better Performance**: Fewer tables = faster queries

---

## 🔧 **Implementation Notes**

### Why `dashboards` is kept but `dashboard_components` is removed:
- **`dashboards`**: Stores complete dashboard configurations including components as JSON
- **`dashboard_components`**: Separate table was planned but never implemented; components are serialized into `dashboard_config` JSON instead

### Why `uploaded_files` and `file_analysis_sessions` are removed:
- Files are uploaded via Streamlit's `st.file_uploader` and stored in session state
- No file persistence to database is implemented
- File paths/metadata are not tracked in database

### Why `user_activity_log` is removed:
- Activity logging exists but only writes to Python logger, not database
- No INSERT queries found for this table
- Can be re-added later if database logging is needed

