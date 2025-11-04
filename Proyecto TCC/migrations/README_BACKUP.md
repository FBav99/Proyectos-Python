# 💾 Backup y Migración de Datos - Guía Rápida

## 📋 Problema

En Streamlit Cloud, las bases de datos SQLite se reinician cada semana, lo que significa que **todos tus datos se pierden** (usuarios, progreso, cuestionarios, etc.).

## ✅ Solución

Este sistema te permite:
1. **Exportar** todos tus datos de SQLite a un archivo JSON
2. **Migrar** esos datos a Supabase (PostgreSQL) donde serán persistentes

---

## 🚀 Uso Rápido

### Opción 1: Usar la Página de Admin (Recomendado)

1. Ve a tu app en Streamlit Cloud
2. Navega a la página **"Admin Backup"** (`pages/99_Admin_Backup.py`)
3. Haz clic en **"Exportar Todos los Datos"**
4. Descarga el archivo JSON generado

### Opción 2: Ejecutar Script Localmente

```bash
# Exportar datos
python migrations/export_sqlite_data.py

# El archivo se guardará en: backups/sqlite_export_YYYYMMDD_HHMMSS.json
```

---

## 🔄 Migrar a Supabase

Una vez que tengas el archivo de exportación:

### Paso 1: Configurar Supabase

1. Crea una cuenta en [Supabase](https://supabase.com)
2. Crea un nuevo proyecto
3. Obtén tu connection string (ver `SUPABASE_SETUP_GUIDE.md`)

### Paso 2: Configurar Streamlit Cloud Secrets

En Streamlit Cloud → Settings → Secrets, agrega:

```toml
[database]
db_type = "supabase"

[supabase]
connection_string = "postgresql://postgres:TU_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
```

### Paso 3: Migrar Datos

```bash
# Ejecutar migración (localmente o en un script)
python migrations/migrate_sqlite_to_supabase.py backups/sqlite_export_YYYYMMDD_HHMMSS.json
```

**Nota:** Los usuarios necesitarán usar "Recuperar Contraseña" porque las contraseñas no se pueden migrar (están hasheadas).

---

## 📁 Archivos Incluidos

- `export_sqlite_data.py` - Exporta todos los datos de SQLite a JSON
- `migrate_sqlite_to_supabase.py` - Migra datos exportados a Supabase
- `pages/99_Admin_Backup.py` - Página web para exportar datos fácilmente

---

## ⚠️ Importante

1. **Exporta regularmente** - Antes de cada semana, exporta tus datos
2. **Guarda los backups** - Descarga los archivos JSON y guárdalos en un lugar seguro
3. **Migra a Supabase** - Una vez configurado Supabase, tus datos serán persistentes
4. **Contraseñas** - Los usuarios necesitarán resetear sus contraseñas después de la migración

---

## 🔍 Qué Datos se Exportan

- ✅ Usuarios (username, email, nombre, etc.)
- ✅ Progreso de usuarios (niveles completados, tiempo, etc.)
- ✅ Intentos de cuestionarios (puntuaciones, respuestas, etc.)

**Nota:** Las contraseñas NO se pueden exportar (están hasheadas por seguridad)

---

## 🛠️ Troubleshooting

### Error: "Database does not exist"
- Verifica que la base de datos SQLite esté creada
- Ejecuta `init_database()` primero

### Error: "Supabase is not configured"
- Verifica que `db_type = "supabase"` en Streamlit secrets
- Verifica que el connection string sea correcto

### Error: "No export file found"
- Asegúrate de ejecutar `export_sqlite_data.py` primero
- O proporciona la ruta del archivo como argumento

---

## 📚 Recursos Adicionales

- `SUPABASE_SETUP_GUIDE.md` - Guía completa de configuración de Supabase
- `docs/01_guides/DATABASE_IMPLEMENTATION_GUIDE.md` - Documentación de la base de datos

---

**💡 Tip:** Configura Supabase lo antes posible para evitar perder datos en el próximo reinicio semanal.

