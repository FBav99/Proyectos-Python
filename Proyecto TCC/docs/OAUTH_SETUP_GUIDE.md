# 🌐 Guía de Configuración OAuth - Google y Microsoft

## 📋 Índice
1. [Configuración de Google OAuth](#configuración-de-google-oauth)
2. [Configuración de Microsoft OAuth](#configuración-de-microsoft-oauth)
3. [Configuración Local](#configuración-local)
4. [Pruebas y Verificación](#pruebas-y-verificación)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🔵 Configuración de Google OAuth

### Paso 1: Crear Proyecto en Google Cloud Console

1. **Accede** a [Google Cloud Console](https://console.cloud.google.com/)
2. **Crea un nuevo proyecto** o selecciona uno existente
3. **Habilita las APIs necesarias:**
   - Google+ API
   - Google OAuth2 API

### Paso 2: Configurar Credenciales OAuth 2.0

1. **Ve a** "APIs & Services" > "Credentials"
2. **Haz clic en** "Create Credentials" > "OAuth 2.0 Client IDs"
3. **Selecciona** "Web application"
4. **Configura los URIs autorizados:**

#### Para Desarrollo Local:
```
Authorized JavaScript origins:
- http://localhost:8501
- http://127.0.0.1:8501

Authorized redirect URIs:
- http://localhost:8501/oauth_callback
- http://127.0.0.1:8501/oauth_callback
```

#### Para Producción:
```
Authorized JavaScript origins:
- https://tu-dominio.com
- https://app.tu-dominio.com

Authorized redirect URIs:
- https://tu-dominio.com/oauth_callback
- https://app.tu-dominio.com/oauth_callback
```

### Paso 3: Obtener Credenciales

1. **Copia el Client ID** (formato: `xxx.apps.googleusercontent.com`)
2. **Copia el Client Secret**
3. **Guarda estas credenciales** de forma segura

---

## 🔴 Configuración de Microsoft OAuth

### Paso 1: Registrar Aplicación en Azure Portal

1. **Accede** a [Azure Portal](https://portal.azure.com/)
2. **Ve a** "Azure Active Directory" > "App registrations"
3. **Haz clic en** "New registration"
4. **Configura la aplicación:**
   - **Name:** Tu aplicación (ej: "TCC Data Analysis App")
   - **Supported account types:** "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI:** Web > `http://localhost:8501/oauth_callback`

### Paso 2: Configurar Permisos

1. **Ve a** "API permissions"
2. **Haz clic en** "Add a permission"
3. **Selecciona** "Microsoft Graph"
4. **Elige** "Delegated permissions"
5. **Selecciona:**
   - `openid`
   - `email`
   - `profile`
   - `User.Read`

### Paso 3: Crear Client Secret

1. **Ve a** "Certificates & secrets"
2. **Haz clic en** "New client secret"
3. **Agrega descripción** y selecciona expiración
4. **Copia el valor** del secret (solo se muestra una vez)

### Paso 4: Obtener Credenciales

1. **Copia el Application (client) ID**
2. **Copia el Client Secret** (del paso anterior)
3. **Guarda estas credenciales** de forma segura

---

## ⚙️ Configuración Local

### Paso 1: Crear Archivo de Secretos

1. **Crea el directorio** `.streamlit` en tu proyecto:
```bash
mkdir .streamlit
```

2. **Copia el archivo de ejemplo:**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

3. **Edita** `.streamlit/secrets.toml` con tus credenciales:

```toml
# OAuth Configuration
oauth_configured = true

# Google OAuth Configuration
[google_oauth]
client_id = "tu-google-client-id.apps.googleusercontent.com"
client_secret = "tu-google-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"

# Microsoft OAuth Configuration
[microsoft_oauth]
client_id = "tu-microsoft-client-id"
client_secret = "tu-microsoft-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"
```

### Paso 2: Instalar Dependencias

```bash
pip install requests
```

### Paso 3: Verificar Configuración

1. **Ejecuta** tu aplicación:
```bash
streamlit run Inicio.py
```

2. **Accede** a `http://localhost:8501`
3. **Haz clic en** "🌐 Login con Google/Microsoft"
4. **Verifica** que aparezcan los botones de OAuth

---

## 🧪 Pruebas y Verificación

### Prueba de Google OAuth

1. **Haz clic en** "🔵 Iniciar sesión con Google"
2. **Deberías ser redirigido** a Google
3. **Inicia sesión** con tu cuenta de Google
4. **Autoriza** la aplicación
5. **Deberías regresar** a tu app y estar logueado

### Prueba de Microsoft OAuth

1. **Haz clic en** "🔴 Iniciar sesión con Microsoft"
2. **Deberías ser redirigido** a Microsoft
3. **Inicia sesión** con tu cuenta de Microsoft
4. **Autoriza** la aplicación
5. **Deberías regresar** a tu app y estar logueado

### Verificación de Usuario Creado

1. **Después del login OAuth**, verifica que se creó el usuario:
2. **Revisa** `config/config.yaml`
3. **Deberías ver** un nuevo usuario con:
   - `oauth_provider: "google"` o `oauth_provider: "microsoft"`
   - `oauth_id: "..."` (ID único del proveedor)

---

## 🔧 Solución de Problemas

### Error: "OAuth no está configurado"

**Solución:**
1. Verifica que `oauth_configured = true` en `secrets.toml`
2. Verifica que las credenciales estén correctas
3. Reinicia la aplicación

### Error: "redirect_uri_mismatch"

**Solución:**
1. Verifica que el redirect URI en `secrets.toml` coincida con el configurado en Google/Microsoft
2. Para desarrollo: `http://localhost:8501/oauth_callback`
3. Para producción: `https://tu-dominio.com/oauth_callback`

### Error: "invalid_client"

**Solución:**
1. Verifica que el Client ID y Client Secret sean correctos
2. Copia exactamente las credenciales de Google Cloud Console/Azure Portal
3. No incluyas espacios extra

### Error: "state parameter mismatch"

**Solución:**
1. Limpia el caché del navegador
2. Reinicia la aplicación
3. Intenta el login nuevamente

### Error: "scope not allowed"

**Solución:**
1. Verifica que los scopes estén configurados correctamente
2. Para Google: `openid email profile`
3. Para Microsoft: `openid email profile User.Read`

---

## 🚀 Configuración para Producción

### Cambios Necesarios

1. **Actualiza URIs** en Google Cloud Console/Azure Portal
2. **Cambia redirect_uri** en `secrets.toml`:
```toml
redirect_uri = "https://tu-dominio.com/oauth_callback"
```

3. **Configura HTTPS** en tu servidor
4. **Usa variables de entorno** para las credenciales

### Variables de Entorno (Recomendado)

```bash
# En tu servidor
export GOOGLE_CLIENT_ID="tu-client-id"
export GOOGLE_CLIENT_SECRET="tu-client-secret"
export MICROSOFT_CLIENT_ID="tu-client-id"
export MICROSOFT_CLIENT_SECRET="tu-client-secret"
```

Y en `secrets.toml`:
```toml
[google_oauth]
client_id = "${GOOGLE_CLIENT_ID}"
client_secret = "${GOOGLE_CLIENT_SECRET}"

[microsoft_oauth]
client_id = "${MICROSOFT_CLIENT_ID}"
client_secret = "${MICROSOFT_CLIENT_SECRET}"
```

---

## 📚 Recursos Adicionales

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Microsoft OAuth Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)
- [Streamlit Secrets Management](https://docs.streamlit.io/library/advanced-features/secrets-management)
- [OAuth 2.0 Security Best Practices](https://tools.ietf.org/html/rfc6819)

---

## 🔒 Consideraciones de Seguridad

### Mejores Prácticas

1. **Nunca subas** `secrets.toml` a Git
2. **Usa variables de entorno** en producción
3. **Rota las credenciales** regularmente
4. **Configura URIs específicos** (no wildcards)
5. **Usa HTTPS** en producción
6. **Implementa rate limiting** si es necesario

### Monitoreo

1. **Revisa logs** de Google Cloud Console/Azure Portal
2. **Monitorea** intentos de login fallidos
3. **Configura alertas** para actividad sospechosa

---

*Esta guía se actualiza regularmente. Última actualización: Diciembre 2024*
