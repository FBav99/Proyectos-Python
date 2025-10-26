# 🔐 Guía de Autenticación - Streamlit-Authenticator vs Streamlit Built-in

## 📋 Índice
1. [Sistema Actual: Streamlit-Authenticator](#sistema-actual-streamlit-authenticator)
2. [Registro de Usuarios](#registro-de-usuarios)
3. [Recuperación de Contraseñas](#recuperación-de-contraseñas)
4. [Comparación con Streamlit Built-in](#comparación-con-streamlit-built-in)
5. [Implementación de OAuth (Google/Microsoft)](#implementación-de-oauth)
6. [Mejores Prácticas](#mejores-prácticas)

---

## 🏗️ Sistema Actual: Streamlit-Authenticator

### ¿Qué es Streamlit-Authenticator?
Streamlit-Authenticator es una biblioteca de terceros que proporciona un sistema de autenticación completo para aplicaciones Streamlit. Ofrece:

- ✅ **Registro de usuarios** con validación
- ✅ **Inicio de sesión** seguro
- ✅ **Recuperación de contraseñas**
- ✅ **Gestión de sesiones** con cookies
- ✅ **Hashing de contraseñas** automático
- ✅ **CAPTCHA** para seguridad
- ✅ **Autenticación de dos factores** (2FA)

### Estructura de Archivos
```
config/
├── config.yaml          # Configuración de usuarios y cookies
core/
├── auth_config.py       # Configuración del sistema de autenticación
pages/
├── 05_Registro.py       # Página de registro de usuarios
├── 06_Recuperar_Password.py  # Página de recuperación de contraseñas
```

### Configuración Actual
```yaml
# config/config.yaml
credentials:
  usernames:
    demo_user:
      email: demo@example.com
      first_name: Demo
      last_name: User
      password: demo123  # Se hashea automáticamente
cookie:
  expiry_days: 30
  key: some_signature_key
  name: some_cookie_name
```

---

## 📝 Registro de Usuarios

### Cómo Funciona
1. **Usuario accede** a `/pages/05_Registro.py`
2. **Completa el formulario** con:
   - Nombre y apellido
   - Email
   - Nombre de usuario
   - Contraseña (con validación)
   - CAPTCHA
3. **Sistema valida** y crea la cuenta
4. **Actualiza** `config.yaml` automáticamente
5. **Usuario puede iniciar sesión** inmediatamente

### Código de Ejemplo
```python
# En pages/05_Registro.py
email, username, name = authenticator.register_user(
    location='main',
    fields={
        'Form name': 'Registro de Usuario',
        'First name': 'Nombre',
        'Last name': 'Apellido',
        'Email': 'Correo Electrónico',
        'Username': 'Nombre de Usuario',
        'Password': 'Contraseña',
        'Repeat password': 'Repetir Contraseña',
        'Register': 'Registrarse'
    },
    captcha=True,
    clear_on_submit=True
)
```

### Características de Seguridad
- 🔒 **Hashing automático** de contraseñas
- 🤖 **CAPTCHA** para prevenir bots
- ✅ **Validación** de campos obligatorios
- 📧 **Verificación** de email único
- 👤 **Verificación** de username único

---

## 🔑 Recuperación de Contraseñas

### Cómo Funciona
1. **Usuario accede** a `/pages/06_Recuperar_Password.py`
2. **Ingresa su username**
3. **Completa CAPTCHA**
4. **Sistema genera** nueva contraseña aleatoria
5. **Muestra** la nueva contraseña al usuario
6. **Actualiza** `config.yaml` automáticamente

### Código de Ejemplo
```python
# En pages/06_Recuperar_Password.py
username, email, new_password = authenticator.forgot_password(
    location='main',
    fields={
        'Form name': 'Recuperar Contraseña',
        'Username': 'Nombre de Usuario',
        'Captcha': 'Captcha',
        'Submit': 'Recuperar Contraseña'
    },
    captcha=True,
    clear_on_submit=True
)
```

---

## 🔄 Comparación con Streamlit Built-in

### Streamlit-Authenticator (Actual)
| Característica | ✅ Ventajas | ❌ Desventajas |
|---|---|---|
| **Registro** | Completo con validación | Requiere configuración manual |
| **Almacenamiento** | YAML local | No escalable para producción |
| **Seguridad** | Hashing, CAPTCHA, 2FA | Sin encriptación de archivo |
| **Personalización** | Total control | Más código para mantener |
| **Dependencias** | Una biblioteca adicional | Posibles conflictos |

### Streamlit Built-in Authentication
| Característica | ✅ Ventajas | ❌ Desventajas |
|---|---|---|
| **Simplicidad** | Integrado en Streamlit | Funcionalidad limitada |
| **OAuth** | Google, Microsoft, GitHub | Solo OAuth, no registro local |
| **Seguridad** | Manejo por Streamlit | Menos control |
| **Escalabilidad** | Cloud-ready | Requiere configuración cloud |
| **Mantenimiento** | Streamlit lo maneja | Menos personalizable |

### ¿Cuándo Usar Cada Uno?

#### Streamlit-Authenticator (Recomendado para tu caso)
- ✅ **Proyectos educativos** como el tuyo
- ✅ **Aplicaciones internas**
- ✅ **Prototipos y MVPs**
- ✅ **Control total** sobre la experiencia
- ✅ **Registro local** de usuarios

#### Streamlit Built-in
- ✅ **Aplicaciones de producción**
- ✅ **Integración con OAuth** (Google, Microsoft)
- ✅ **Aplicaciones cloud**
- ✅ **Equipos grandes** con SSO

---

## 🌐 Implementación de OAuth (Google/Microsoft) - ✅ IMPLEMENTADO

### Sistema Híbrido Implementado

He implementado un sistema híbrido que combina **Streamlit-Authenticator** con **OAuth de Google y Microsoft**. Esto te da lo mejor de ambos mundos:

- ✅ **Registro local** con Streamlit-Authenticator
- ✅ **Login OAuth** con Google y Microsoft
- ✅ **Gestión unificada** de usuarios
- ✅ **Flexibilidad total** para los usuarios

### Archivos Implementados

```
pages/
├── 07_OAuth_Login.py          # Página de login OAuth
.streamlit/
├── secrets.toml.example       # Ejemplo de configuración
docs/
├── OAUTH_SETUP_GUIDE.md       # Guía completa de configuración
test_oauth.py                  # Script de prueba
```

### Cómo Funciona

1. **Usuario accede** a `/pages/07_OAuth_Login.py`
2. **Elige** entre Google, Microsoft o login local
3. **Si elige OAuth:**
   - Se redirige al proveedor (Google/Microsoft)
   - Usuario autoriza la aplicación
   - Se crea automáticamente un usuario local
   - Se inicia sesión automáticamente
4. **Si elige local:** Usa Streamlit-Authenticator normal

### Configuración Rápida

1. **Copia el archivo de ejemplo:**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. **Configura tus credenciales** en `.streamlit/secrets.toml`:
```toml
oauth_configured = true

[google_oauth]
client_id = "tu-google-client-id.apps.googleusercontent.com"
client_secret = "tu-google-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"

[microsoft_oauth]
client_id = "tu-microsoft-client-id"
client_secret = "tu-microsoft-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"
```

3. **Ejecuta el test:**
```bash
python test_oauth.py
```

4. **Inicia la aplicación:**
```bash
streamlit run Inicio.py
```

### Ventajas del Sistema Híbrido

| Característica | Streamlit-Authenticator | OAuth | Sistema Híbrido |
|---|---|---|---|
| **Registro** | ✅ Completo | ❌ No disponible | ✅ Completo |
| **Login OAuth** | ❌ No disponible | ✅ Google/Microsoft | ✅ Google/Microsoft |
| **Control** | ✅ Total | ❌ Limitado | ✅ Total |
| **Escalabilidad** | ⚠️ Local | ✅ Cloud | ✅ Ambos |
| **Mantenimiento** | 🔧 Manual | 🚀 Automático | 🔧 Manual |

### Documentación Completa

Para configuración detallada, consulta:
- 📖 [Guía de Configuración OAuth](docs/OAUTH_SETUP_GUIDE.md)
- 🔧 [Solución de Problemas](docs/OAUTH_SETUP_GUIDE.md#solución-de-problemas)
- 🚀 [Configuración para Producción](docs/OAUTH_SETUP_GUIDE.md#configuración-para-producción)

### Configuración de OAuth

#### Google OAuth
1. **Crear proyecto** en Google Cloud Console
2. **Habilitar** Google+ API
3. **Crear credenciales** OAuth 2.0
4. **Configurar** URIs de redirección
5. **Agregar** client_id y client_secret

#### Microsoft OAuth
1. **Registrar aplicación** en Azure Portal
2. **Configurar** permisos de Microsoft Graph
3. **Crear** client secret
4. **Configurar** redirect URIs

---

## 🛡️ Mejores Prácticas

### Seguridad
- 🔒 **Cambiar** `some_signature_key` por una clave única
- 🔐 **Usar** variables de entorno para secretos
- 📧 **Validar** emails con confirmación
- 🤖 **Mantener** CAPTCHA habilitado
- 🔄 **Rotar** contraseñas regularmente

### Configuración Recomendada
```yaml
# config/config.yaml mejorado
cookie:
  expiry_days: 7  # Sesiones más cortas
  key: ${COOKIE_SECRET_KEY}  # Variable de entorno
  name: tcc_auth_cookie
credentials:
  usernames: {}
pre-authorized:
  emails: []  # Emails pre-autorizados para registro
```

### Estructura de Archivos Segura
```
.env                    # Variables de entorno (NO subir a Git)
config/
├── config.yaml         # Configuración de usuarios
├── config.example.yaml # Ejemplo sin datos sensibles
core/
├── auth_config.py      # Configuración de autenticación
├── secrets.py          # Manejo de secretos
```

---

## 🚀 Próximos Pasos

### Inmediatos
1. ✅ **Probar** el sistema de registro
2. ✅ **Configurar** recuperación de contraseñas
3. ✅ **Personalizar** mensajes y UI
4. ✅ **Agregar** validaciones adicionales

### Futuros
1. 🌐 **Implementar** OAuth (Google/Microsoft)
2. 📧 **Agregar** confirmación por email
3. 🔐 **Implementar** 2FA
4. 📊 **Agregar** analytics de usuarios
5. 🗄️ **Migrar** a base de datos (PostgreSQL/MongoDB)

---

## 📚 Recursos Adicionales

- [Streamlit-Authenticator GitHub](https://github.com/mkhorasani/Streamlit-Authenticator)
- [Streamlit Authentication Docs](https://docs.streamlit.io/library/advanced-features/authentication)
- [Google OAuth Setup](https://developers.google.com/identity/protocols/oauth2)
- [Microsoft OAuth Setup](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

---

*Esta guía se actualiza regularmente. Última actualización: Diciembre 2024*
