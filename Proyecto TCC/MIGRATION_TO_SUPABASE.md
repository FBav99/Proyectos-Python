# 🚀 Guía de Migración a Supabase

## ✅ Estado Actual

Tu aplicación ya está preparada para migrar a Supabase. Se han realizado las siguientes correcciones:

### Cambios Realizados

1. **Todas las tablas ahora soportan PostgreSQL**
   - Cambiado `INTEGER PRIMARY KEY AUTOINCREMENT` → `SERIAL PRIMARY KEY` para PostgreSQL
   - Cambiado valores booleanos `0/1` → `TRUE/FALSE` para PostgreSQL
   - Todas las queries usan `cursor.execute()` en lugar de `conn.execute()` para compatibilidad

2. **Conexión mejorada**
   - El connection manager maneja correctamente PostgreSQL
   - Soporte para RealDictCursor (para acceso tipo dict a las filas)

3. **Dependencias**
   - `psycopg2-binary>=2.9.0` ya está en `requirements.txt`

## 📋 Pasos para Migrar

### Paso 1: Crear Proyecto en Supabase

1. Ve a https://supabase.com
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto:
   - Nombre: `tcc-data-platform` (o el que prefieras)
   - Región: La más cercana a tus usuarios
   - Contraseña de base de datos: **GUARDA ESTA CONTRASEÑA**

### Paso 2: Obtener Connection String

1. En el dashboard de Supabase, ve a **Settings** → **Database**
2. En la sección **Connection string**, usa el formato **URI**
3. Copia el connection string, debería verse así:
   ```
   postgresql://postgres:[TU-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
4. **Reemplaza `[TU-PASSWORD]`** con la contraseña que creaste

### Paso 3: Configurar Streamlit Cloud Secrets

1. En Streamlit Cloud, ve a tu app → **Settings** → **Secrets**
2. Actualiza o crea los siguientes secrets:

```toml
# Database Configuration
[database]
# Cambiar de "sqlite" a "supabase"
db_type = "supabase"

# Supabase Connection
[supabase]
connection_string = "postgresql://postgres:TU_PASSWORD_AQUI@db.xxxxx.supabase.co:5432/postgres"
```

**⚠️ IMPORTANTE:** Reemplaza:
- `TU_PASSWORD_AQUI` con tu contraseña real
- `xxxxx` con tu project reference de Supabase

### Paso 4: Desplegar

1. Haz commit y push de tus cambios
2. Streamlit Cloud detectará los cambios y redesplegará automáticamente
3. La primera vez que se ejecute, creará todas las tablas automáticamente

### Paso 5: Verificar

1. Una vez desplegado, registra un nuevo usuario
2. Verifica en Supabase Dashboard → **Table Editor** que las tablas se crearon
3. Confirma que puedes iniciar sesión con el nuevo usuario

## 🔄 Migración de Datos Existentes (Opcional)

Si tienes datos en SQLite que quieres migrar:

1. **Exportar datos de SQLite:**
   ```bash
   python migrations/export_sqlite_data.py
   ```

2. **Migrar a Supabase:**
   ```bash
   python migrations/migrate_sqlite_to_supabase.py backups/sqlite_export_YYYYMMDD_HHMMSS.json
   ```

**Nota:** Para proyectos nuevos, es mejor empezar con una base de datos limpia.

## ✅ Checklist de Migración

- [ ] Creé cuenta/proyecto en Supabase
- [ ] Guardé la contraseña de la base de datos
- [ ] Obtuve el connection string
- [ ] Actualicé Streamlit Cloud secrets con `db_type = "supabase"`
- [ ] Agregué el connection string a secrets
- [ ] Desplegué la aplicación
- [ ] Verifiqué que las tablas se crearon en Supabase
- [ ] Probé registro/login de usuario
- [ ] (Opcional) Migré datos existentes

## 🐛 Solución de Problemas

### Error: "psycopg2 not installed"
- Verifica que `requirements.txt` incluye `psycopg2-binary>=2.9.0`
- Streamlit Cloud debería instalarlo automáticamente

### Error: "Connection refused" o "Connection timeout"
- Verifica que el connection string es correcto
- Verifica que la contraseña está correctamente codificada (URL encoding si tiene caracteres especiales)
- Asegúrate de que el proyecto de Supabase está activo (los proyectos gratuitos se pausan después de 1 semana de inactividad)

### Tablas no se crean
- Verifica que `db_type = "supabase"` en secrets (no "sqlite")
- Revisa los logs de Streamlit Cloud para ver errores
- Verifica que el connection string tiene permisos suficientes

### Datos no persisten
- Verifica que estás usando Supabase (no SQLite local)
- Confirma que las queries están usando `db_manager.get_connection()`
- Revisa que no hay errores en los logs

## 📊 Ventajas de Supabase

1. **Persistencia**: Los datos persisten entre reinicios de la app
2. **Escalabilidad**: Fácil de escalar cuando sea necesario
3. **Backups automáticos**: Supabase hace backups automáticos
4. **Dashboard**: Interfaz web para ver y gestionar datos
5. **Gratis**: Tier gratuito generoso para proyectos escolares

## 🔙 Volver a SQLite (si es necesario)

Si necesitas volver a SQLite temporalmente:

```toml
[database]
db_type = "sqlite"
```

Y elimina o comenta la sección `[supabase]` en secrets.

---

**¡Listo!** Tu aplicación ahora está lista para usar Supabase en producción. 🎉

