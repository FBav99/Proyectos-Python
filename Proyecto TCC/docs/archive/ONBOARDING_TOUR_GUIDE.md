# 🎯 Guía de Implementación: Sistema de Tour Guiado (Onboarding)

## 📋 Resumen

Este documento explica cómo implementar un sistema de tour guiado para nuevos usuarios en la plataforma Streamlit, similar a las experiencias de onboarding en aplicaciones móviles.

---

## 🚀 Opciones Disponibles

### **Opción 1: Tour Simple con Streamlit (Recomendado) ✅**

**Ventajas:**
- ✅ No requiere JavaScript
- ✅ Fácil de implementar
- ✅ Funciona en todas las plataformas
- ✅ Ya implementado en `utils/ui/onboarding.py`

**Características:**
- Pasos progresivos con botones de navegación
- Diseño visual atractivo con gradientes
- Persistencia en base de datos
- Opción de saltar el tour

### **Opción 2: Tour con JavaScript (Más Avanzado)**

Si quieres un tour más sofisticado con highlights y tooltips, puedes usar bibliotecas como:
- **Intro.js** - Biblioteca JavaScript para tours interactivos
- **Shepherd.js** - Otra opción popular
- **Driver.js** - Moderna y liviana

**Requiere:** Integración con `st.components.v1.html` y JavaScript personalizado

---

## 📦 Implementación: Opción 1 (Recomendada)

### Paso 1: Agregar Columna a la Base de Datos

Necesitas agregar una columna `onboarding_completed` a la tabla `users`.

**Para SQLite:**
```sql
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT 0;
```

**Para PostgreSQL/Supabase:**
```sql
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
```

**O ejecuta este script Python:**
```python
# migrations/add_onboarding_column.py
from core.database import DatabaseManager

db = DatabaseManager()
with db.get_connection() as conn:
    cursor = conn.cursor()
    try:
        if db.db_type == "supabase":
            cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE")
        else:
            cursor.execute("ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT 0")
        conn.commit()
        print("✅ Columna onboarding_completed agregada exitosamente")
    except Exception as e:
        print(f"⚠️ La columna ya existe o error: {e}")
```

### Paso 2: Integrar en Inicio.py

Agrega el tour después de la autenticación:

```python
# En Inicio.py, después de la línea 131 (después del welcome message)

from utils.ui.onboarding import show_onboarding_tour, check_onboarding_status
from core.database import DatabaseManager

# ... código existente ...

# ============================================================================
# SECCIÓN ONBOARDING - Tour guiado para nuevos usuarios
# ============================================================================
if 'oauth_provider' not in current_user:
    db_manager = DatabaseManager()
    user_id = current_user['id']
    
    # Check if user needs onboarding (first time or not completed)
    onboarding_completed = check_onboarding_status(user_id, db_manager)
    
    # Show onboarding if:
    # 1. User hasn't completed it in DB, OR
    # 2. User just registered (registration_welcome exists), OR
    # 3. User manually requests it (session state)
    should_show_onboarding = (
        not onboarding_completed or 
        welcome_data is not None or
        st.session_state.get('show_onboarding', False)
    )
    
    if should_show_onboarding:
        onboarding_active = show_onboarding_tour(user_id, db_manager)
        
        # If onboarding is active, don't show other content
        if onboarding_active:
            st.stop()  # Stop rendering rest of page
```

### Paso 3: Agregar Botón para Reactivar Tour (Opcional)

En la sidebar o en algún lugar visible, agrega:

```python
# En algún lugar de la UI (sidebar, ayuda, etc.)
if st.button("🎯 Ver Tour de Introducción"):
    st.session_state.show_onboarding = True
    st.session_state.onboarding_step = 0
    st.session_state.onboarding_active = True
    st.rerun()
```

---

## 🎨 Personalización

### Modificar los Pasos del Tour

Edita `utils/ui/onboarding.py`, sección `ONBOARDING_STEPS`:

```python
ONBOARDING_STEPS = [
    {
        "title": replace_emojis("👋 ¡Bienvenido!"),
        "content": """
        <p>Tu mensaje personalizado aquí...</p>
        <ul>
            <li>Punto 1</li>
            <li>Punto 2</li>
        </ul>
        """,
    },
    # Agrega más pasos...
]
```

### Cambiar el Diseño

Modifica los estilos CSS en la función `show_onboarding_tour()`:

```python
# Cambiar colores del gradiente
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

# Cambiar a otros colores, ej:
# background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
# background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```

---

## 🔧 Opción 2: Tour con JavaScript (Intro.js)

Si quieres un tour más sofisticado, aquí hay un ejemplo básico:

### Crear componente HTML

```python
# utils/ui/js_tour.py
import streamlit.components.v1 as components

def show_intro_js_tour():
    intro_js_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intro.js@7.2.0/minified/intro.min.css">
        <script src="https://cdn.jsdelivr.net/npm/intro.js@7.2.0/minified/intro.min.js"></script>
    </head>
    <body>
        <script>
        if (typeof introJs !== 'undefined') {
            introJs().setOptions({
                steps: [
                    {
                        element: '#step1',
                        intro: 'Bienvenido a la plataforma!',
                    },
                    {
                        element: '#step2',
                        intro: 'Aquí puedes ver tus datos',
                    },
                    // Agrega más pasos...
                ]
            }).start();
        }
        </script>
    </body>
    </html>
    """
    components.html(intro_js_html, height=0)
```

**Limitación:** Streamlit no expone fácilmente los IDs de elementos, por lo que esta opción es más compleja.

---

## ✅ Ventajas del Enfoque Actual (Opción 1)

1. **Simple y Funcional** - No requiere JavaScript externo
2. **Persistente** - Guarda el estado en la base de datos
3. **Personalizable** - Fácil de modificar contenido y diseño
4. **Accesible** - Funciona en todas las plataformas Streamlit
5. **No Invasivo** - El usuario puede saltar cuando quiera

---

## 🎯 Próximos Pasos

1. ✅ Ejecuta el script de migración para agregar la columna
2. ✅ Integra el tour en `Inicio.py`
3. ✅ Personaliza los pasos según tus necesidades
4. ✅ Prueba con un usuario nuevo
5. ⚙️ (Opcional) Agrega botón para reactivar el tour

---

## 📝 Notas

- El tour se muestra automáticamente para usuarios nuevos
- Los usuarios pueden saltar el tour en cualquier momento
- El estado se guarda en la base de datos para no mostrar el tour repetidamente
- El tour es completamente personalizable mediante `ONBOARDING_STEPS`

---

¿Necesitas ayuda con la implementación? El código ya está listo en `utils/ui/onboarding.py` 🚀

