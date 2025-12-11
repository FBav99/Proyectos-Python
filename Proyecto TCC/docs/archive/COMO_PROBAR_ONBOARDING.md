# 🧪 Cómo Probar el Sistema de Onboarding

## 📋 Opciones para Probar

Tienes **3 formas** de probar el onboarding:

---

## ✅ Opción 1: Botón en la Sidebar (Más Fácil) 🎯

**Pasos:**
1. Inicia sesión en la aplicación
2. Mira en la **sidebar izquierda**
3. Verás un botón **"🎯 Ver Tour de Introducción"**
4. Haz clic en él
5. El tour comenzará inmediatamente

**Ventaja:** No necesitas crear usuarios nuevos ni modificar la base de datos.

---

## ✅ Opción 2: Crear un Usuario Nuevo 👤

**Pasos:**
1. Ve a la página de **Registro** (`pages/05_Registro.py`)
2. Crea una cuenta nueva
3. Después del registro, el tour se mostrará automáticamente

**Ventaja:** Prueba el flujo completo de usuario nuevo.

---

## ✅ Opción 3: Resetear el Estado de Onboarding en la BD 🔄

Si ya tienes un usuario y quieres que vea el tour de nuevo:

**Opción A: Usando SQL directamente**

```sql
-- Para SQLite
UPDATE users SET onboarding_completed = 0 WHERE username = 'tu_usuario';

-- Para PostgreSQL/Supabase
UPDATE users SET onboarding_completed = FALSE WHERE username = 'tu_usuario';
```

**Opción B: Usando Python**

```python
from core.database import DatabaseManager

db = DatabaseManager()
with db.get_connection() as conn:
    cursor = conn.cursor()
    if db.db_type == "supabase":
        cursor.execute(
            "UPDATE users SET onboarding_completed = FALSE WHERE username = %s",
            ('tu_usuario',)
        )
    else:
        cursor.execute(
            "UPDATE users SET onboarding_completed = 0 WHERE username = ?",
            ('tu_usuario',)
        )
    conn.commit()
```

---

## 🚀 Pasos Iniciales (Primera Vez)

### 1. Ejecutar la Migración de Base de Datos

Antes de probar, necesitas agregar la columna `onboarding_completed` a la tabla `users`:

```bash
# Desde la raíz del proyecto
python migrations/add_onboarding_column.py
```

O manualmente:

**SQLite:**
```sql
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT 0;
```

**PostgreSQL/Supabase:**
```sql
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
```

### 2. Iniciar la Aplicación

```bash
streamlit run Inicio.py
```

### 3. Probar el Tour

Usa cualquiera de las 3 opciones mencionadas arriba.

---

## 🎨 Qué Esperar

Cuando el tour se active, verás:

1. **Paso 1:** Bienvenida general
2. **Paso 2:** Explicación de los niveles de aprendizaje
3. **Paso 3:** Información sobre carga de datos
4. **Paso 4:** Información sobre dashboards
5. **Paso 5:** Mensaje final

**Navegación:**
- **⬅️ Atrás:** Volver al paso anterior
- **Saltar Tour:** Salir del tour sin completarlo
- **Siguiente ➡️:** Avanzar al siguiente paso
- **Finalizar ✓:** Completar el tour (último paso)

---

## 🔍 Verificar que Funciona

### Verificar en la Base de Datos

Después de completar el tour, puedes verificar que se guardó:

```sql
-- Ver el estado de onboarding de todos los usuarios
SELECT username, onboarding_completed FROM users;
```

### Verificar en el Código

El tour no se mostrará automáticamente si:
- `onboarding_completed = TRUE` (o `1` en SQLite)
- El usuario es OAuth (no usuarios de BD)

---

## 🐛 Troubleshooting

### El tour no aparece

1. **Verifica la migración:**
   ```sql
   PRAGMA table_info(users);  -- SQLite
   -- o
   \d users  -- PostgreSQL
   ```
   Debe existir la columna `onboarding_completed`

2. **Verifica el estado del usuario:**
   ```sql
   SELECT onboarding_completed FROM users WHERE username = 'tu_usuario';
   ```
   Debe ser `FALSE` o `0` para que aparezca

3. **Verifica que no eres usuario OAuth:**
   El tour solo funciona para usuarios de base de datos, no OAuth

### El botón no aparece en la sidebar

- Verifica que estás autenticado
- Verifica que NO eres usuario OAuth
- El botón solo aparece para usuarios de base de datos

---

## 📝 Notas

- El tour se guarda en la base de datos, así que solo se muestra una vez por defecto
- Puedes usar el botón de la sidebar para reactivarlo cuando quieras
- El tour es completamente personalizable editando `ONBOARDING_STEPS` en `utils/ui/onboarding.py`

---

¡Listo para probar! 🚀

