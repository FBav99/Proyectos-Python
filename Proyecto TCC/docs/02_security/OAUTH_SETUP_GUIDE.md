# Guía de Configuración OAuth - Google y Microsoft

Esta guía te ayudará a configurar la autenticación OAuth con Google y Microsoft para tu aplicación Streamlit.

## 📋 Prerrequisitos

- Una cuenta de Google (para Google OAuth)
- Una cuenta de Microsoft/Azure (para Microsoft OAuth)
- Tu aplicación Streamlit funcionando

## 🔧 Configuración de Google OAuth

### 1. Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google+ (si no está habilitada)

### 2. Configurar Credenciales OAuth

1. Ve a **APIs & Services** > **Credentials**
2. Haz clic en **Create Credentials** > **OAuth 2.0 Client IDs**
3. Selecciona **Web application**
4. Configura los URIs de redirección:
   - Para desarrollo local: `http://localhost:8501/oauth_callback`
   - Para producción: `https://tu-dominio.com/oauth_callback`

### 3. Obtener Credenciales

Anota el **Client ID** y **Client Secret** que te proporciona Google.

## 🔧 Configuración de Microsoft OAuth

### 1. Registrar Aplicación en Azure Portal

1. Ve a [Azure Portal](https://portal.azure.com/)
2. Ve a **Azure Active Directory** > **App registrations**
3. Haz clic en **New registration**
4. Completa el formulario:
   - **Name**: Nombre de tu aplicación
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: 
     - Para desarrollo: `http://localhost:8501/oauth_callback`
     - Para producción: `https://tu-dominio.com/oauth_callback`

### 2. Configurar Permisos

1. Ve a **API permissions**
2. Haz clic en **Add a permission**
3. Selecciona **Microsoft Graph** > **Delegated permissions**
4. Agrega estos permisos:
   - `openid`
   - `email`
   - `profile`
   - `User.Read`

### 3. Crear Client Secret

1. Ve a **Certificates & secrets**
2. Haz clic en **New client secret**
3. Anota el **Value** del secret (solo se muestra una vez)

### 4. Obtener Credenciales

Anota el **Application (client) ID** y el **Client Secret** que creaste.

## 📝 Configuración en Streamlit

### 1. Crear Archivo Secrets

Crea el archivo `.streamlit/secrets.toml` en la raíz de tu proyecto:

```toml
# Configuración OAuth
oauth_configured = true

# Google OAuth
[google_oauth]
client_id = "tu-google-client-id"
client_secret = "tu-google-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"

# Microsoft OAuth
[microsoft_oauth]
client_id = "tu-microsoft-client-id"
client_secret = "tu-microsoft-client-secret"
redirect_uri = "http://localhost:8501/oauth_callback"
```

### 2. Configuración para Producción

Para producción, actualiza los URIs de redirección:

```toml
# Google OAuth (Producción)
[google_oauth]
client_id = "tu-google-client-id"
client_secret = "tu-google-client-secret"
redirect_uri = "https://tu-dominio.com/oauth_callback"

# Microsoft OAuth (Producción)
[microsoft_oauth]
client_id = "tu-microsoft-client-id"
client_secret = "tu-microsoft-client-secret"
redirect_uri = "https://tu-dominio.com/oauth_callback"
```

## 🔒 Consideraciones de Seguridad

### 1. Protección de Credenciales

- **NUNCA** subas el archivo `secrets.toml` a Git
- Agrega `.streamlit/secrets.toml` a tu `.gitignore`
- Usa variables de entorno en producción

### 2. URIs de Redirección

- Configura URIs específicos para cada entorno
- No uses URIs genéricos como `http://localhost:8501`
- Verifica que los URIs coincidan exactamente

### 3. Permisos Mínimos

- Solicita solo los permisos necesarios
- Revisa regularmente los permisos de tu aplicación
- Considera usar permisos de solo lectura cuando sea posible

## 🚀 Pruebas

### 1. Probar Configuración

1. Ejecuta tu aplicación: `streamlit run Inicio.py`
2. Ve a la página de OAuth Login
3. Haz clic en "Iniciar sesión con Google" o "Iniciar sesión con Microsoft"
4. Completa el flujo de autorización

### 2. Verificar Funcionamiento

- Deberías ser redirigido de vuelta a tu aplicación
- Tu información de usuario debería mostrarse
- Deberías poder acceder a todas las funcionalidades

## 🐛 Solución de Problemas

### Error: "OAuth no está configurado"

**Causa**: El archivo `secrets.toml` no existe o `oauth_configured = false`

**Solución**:
1. Verifica que el archivo `.streamlit/secrets.toml` existe
2. Asegúrate de que `oauth_configured = true`
3. Reinicia la aplicación

### Error: "Invalid redirect URI"

**Causa**: Los URIs de redirección no coinciden

**Solución**:
1. Verifica que los URIs en Google/Microsoft coincidan con los de `secrets.toml`
2. Asegúrate de que no haya espacios extra o caracteres especiales
3. Verifica que el protocolo (http/https) sea correcto

### Error: "Client ID not found"

**Causa**: Credenciales incorrectas o no configuradas

**Solución**:
1. Verifica que el Client ID y Client Secret sean correctos
2. Asegúrate de que la aplicación esté habilitada en Google/Microsoft
3. Verifica que las APIs necesarias estén habilitadas

### Error: "Access denied"

**Causa**: Permisos insuficientes o aplicación no autorizada

**Solución**:
1. Verifica que todos los permisos necesarios estén configurados
2. Asegúrate de que la aplicación esté autorizada
3. Revisa los logs de Google/Microsoft para más detalles

## 📚 Recursos Adicionales

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Microsoft OAuth 2.0 Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)
- [Streamlit Secrets Management](https://docs.streamlit.io/library/advanced-features/secrets-management)

## 🔄 Actualizaciones

### Versión 1.0
- Configuración inicial de Google y Microsoft OAuth
- Soporte para desarrollo y producción
- Manejo de errores básico

### Próximas Mejoras
- Integración completa con base de datos
- Persistencia de sesiones OAuth
- Soporte para más proveedores OAuth
- Mejoras en la seguridad y validación
