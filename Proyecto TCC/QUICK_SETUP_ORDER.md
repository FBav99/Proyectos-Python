# 🚀 Orden Rápido: Configurar Supabase en Streamlit Cloud

## ⚡ Orden Exacto (15 minutos)

### 1️⃣ **Crear Supabase** (5 min)
```
1. Ve a https://supabase.com
2. Crea cuenta → New Project
3. Guarda la contraseña del database
4. Ve a Settings → Database → Connection string (URI)
5. Copia la connection string completa
```

### 2️⃣ **Agregar requirements.txt** (2 min)
Crea o actualiza `requirements.txt` en la raíz del proyecto:
```txt
streamlit
streamlit-authenticator
bcrypt
psycopg2-binary
```

Haz commit y push a GitHub.

### 3️⃣ **Configurar Secrets en Streamlit Cloud** (3 min)
```
1. Ve a https://share.streamlit.io
2. Tu app → Settings → Secrets
3. Agrega esto:
```

```toml
[database]
db_type = "supabase"

[supabase]
connection_string = "postgresql://postgres:TU_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
```

**⚠️ Reemplaza:**
- `TU_PASSWORD` con tu contraseña real
- `xxxxx` con tu project reference

### 4️⃣ **Verificar** (2 min)
```
1. Espera que Streamlit Cloud se reinicie
2. Ve a tu app → página "Admin Backup"
3. Debe decir "PostgreSQL/Supabase"
4. Prueba registrar un usuario
5. Verifica en Supabase Table Editor que aparezca
```

## ✅ Listo!

Después de esto:
- ✅ Tu app usa Supabase
- ✅ Los datos son persistentes
- ✅ No se pierden en reinicios semanales
- ✅ Puedes enfocarte en otras features

---

## 📝 Checklist Visual

```
□ Crear proyecto Supabase
□ Guardar connection string
□ Crear/actualizar requirements.txt (agregar psycopg2-binary)
□ Push a GitHub
□ Configurar secrets en Streamlit Cloud
□ Esperar reinicio
□ Verificar en Admin Backup page
□ Probar registro de usuario
□ Verificar en Supabase dashboard
```

---

## 🆘 Si algo falla

**Error: psycopg2 not found**
→ Verifica que `psycopg2-binary` esté en requirements.txt y hayas hecho push

**Error: Connection failed**
→ Verifica que la connection string esté correcta (sin espacios, password correcta)

**Sigue usando SQLite**
→ Verifica que en secrets diga `db_type = "supabase"` (no "sqlite")

---

**Tiempo total: ~15 minutos** ⏱️

