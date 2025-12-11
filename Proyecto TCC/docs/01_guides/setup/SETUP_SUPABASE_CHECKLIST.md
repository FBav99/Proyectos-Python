# ✅ Checklist: Configurar Supabase en Streamlit Cloud

## 🎯 Objetivo
Configurar Supabase para que tu app use una base de datos persistente en Streamlit Cloud, sin perder datos en los reinicios semanales.

---

## 📋 PASO 1: Crear Proyecto en Supabase (5 minutos)

### 1.1 Crear cuenta
- [ ] Ve a https://supabase.com
- [ ] Crea una cuenta (con GitHub es más fácil)
- [ ] Verifica tu email si es necesario

### 1.2 Crear proyecto
- [ ] Click en "New Project"
- [ ] **Nombre del proyecto**: `tcc-data-platform` (o el que prefieras)
- [ ] **Database Password**: Crea una contraseña FUERTE (guárdala en un lugar seguro)
- [ ] **Region**: Elige la más cercana a tus usuarios
- [ ] **Pricing Plan**: Free
- [ ] Click "Create new project"
- [ ] Espera 2-3 minutos mientras se crea

### 1.3 Obtener Connection String
- [ ] En el dashboard de Supabase, ve a **Settings** (⚙️) → **Database**
- [ ] Scroll hasta "Connection string"
- [ ] Click en el tab **URI**
- [ ] Copia la connection string (se ve así):
  ```
  postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
  ```
- [ ] **IMPORTANTE**: Reemplaza `[YOUR-PASSWORD]` con la contraseña que creaste
- [ ] Guarda esta connection string completa (la necesitarás en el siguiente paso)

---

## 📋 PASO 2: Configurar Streamlit Cloud Secrets (3 minutos)

### 2.1 Ir a Streamlit Cloud
- [ ] Ve a https://share.streamlit.io
- [ ] Selecciona tu app
- [ ] Click en **Settings** (⚙️) en el menú lateral
- [ ] Click en **Secrets** en el menú

### 2.2 Agregar configuración
- [ ] En el editor de secrets, agrega esto:

```toml
[database]
db_type = "supabase"

[supabase]
connection_string = "postgresql://postgres:TU_PASSWORD_AQUI@db.xxxxx.supabase.co:5432/postgres"
```

**⚠️ IMPORTANTE:**
- Reemplaza `TU_PASSWORD_AQUI` con tu contraseña real de Supabase
- Reemplaza `xxxxx.supabase.co` con tu project reference real
- La connection string debe ser UNA línea completa, sin saltos de línea

### 2.3 Guardar
- [ ] Click en "Save"
- [ ] Streamlit Cloud reiniciará tu app automáticamente

---

## 📋 PASO 3: Agregar Dependencia (2 minutos)

### 3.1 Verificar requirements.txt
- [ ] Abre tu archivo `requirements.txt`
- [ ] Verifica que tenga esta línea:
  ```
  psycopg2-binary
  ```
- [ ] Si NO la tiene, agrégala
- [ ] Guarda el archivo
- [ ] Haz commit y push a GitHub

### 3.2 Streamlit Cloud detectará el cambio
- [ ] Streamlit Cloud se reiniciará automáticamente
- [ ] Espera a que termine de desplegar

---

## 📋 PASO 4: Verificar que Funciona (2 minutos)

### 4.1 Verificar en la app
- [ ] Ve a tu app en Streamlit Cloud
- [ ] Ve a la página **"Admin Backup"** (`pages/99_Admin_Backup.py`)
- [ ] Verifica que diga:
  - **Tipo de Base de Datos**: "PostgreSQL/Supabase" ✅
  - **Usuarios**: 0 (es normal, está vacía)

### 4.2 Probar registro
- [ ] Ve a la página de registro
- [ ] Crea un usuario de prueba
- [ ] Verifica que puedas iniciar sesión
- [ ] Ve a Admin Backup otra vez
- [ ] Verifica que ahora diga **Usuarios**: 1 ✅

### 4.3 Verificar en Supabase
- [ ] Ve al dashboard de Supabase
- [ ] Click en **Table Editor** en el menú lateral
- [ ] Deberías ver la tabla `users`
- [ ] Click en `users` - deberías ver tu usuario de prueba ✅

---

## ✅ ¡LISTO!

Si todo lo anterior funciona:
- ✅ Supabase está configurado
- ✅ Tu app usa Supabase en lugar de SQLite
- ✅ Los datos ahora son persistentes
- ✅ No se perderán en los reinicios semanales

---

## 🛠️ Troubleshooting

### Error: "psycopg2 not installed"
- **Solución**: Asegúrate de que `psycopg2-binary` esté en `requirements.txt` y haz push a GitHub

### Error: "Connection failed"
- **Solución**: Verifica que:
  - La connection string esté correcta en secrets
  - La contraseña sea la correcta (sin espacios extra)
  - El project reference sea correcto

### App sigue usando SQLite
- **Solución**: Verifica que en secrets diga `db_type = "supabase"` (no `"sqlite"`)

### No puedo ver la página Admin Backup
- **Solución**: La página está en `pages/99_Admin_Backup.py` - asegúrate de que el archivo exista

---

## 📝 Notas Importantes

1. **Contraseña de Supabase**: Guárdala en un lugar seguro. Si la pierdes, puedes resetearla en Supabase Settings → Database

2. **Project Reference**: Es la parte `xxxxx` en `db.xxxxx.supabase.co`. Lo encuentras en la URL de tu proyecto Supabase

3. **Datos Existentes**: Si tienes datos en SQLite que quieres migrar, usa el sistema de backup/export que creamos antes. Si no, simplemente empieza fresco con Supabase.

4. **Reinicio**: Después de configurar secrets, Streamlit Cloud reinicia automáticamente. Espera 1-2 minutos.

---

## 🎯 Orden de Ejecución Resumido

1. ✅ Crear proyecto Supabase → Obtener connection string
2. ✅ Agregar secrets en Streamlit Cloud
3. ✅ Agregar `psycopg2-binary` a requirements.txt
4. ✅ Verificar que funciona (Admin Backup page)
5. ✅ Probar registro de usuario
6. ✅ ¡Listo para usar!

**Tiempo total estimado: ~15 minutos**

---

## 💡 Después de Configurar

Una vez que Supabase esté funcionando:
- ✅ Puedes enfocarte en otras features
- ✅ Los usuarios no se perderán
- ✅ Todo es persistente
- ✅ No necesitas hacer backups manuales

¡Éxito! 🚀

