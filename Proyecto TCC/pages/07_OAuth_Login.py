import streamlit as st
import requests
import json
import os
from urllib.parse import urlencode, parse_qs, urlparse
import base64
import hashlib
import secrets
from core.auth_service import get_current_user, login_user
from core.security import security_manager, secure_oauth_callback
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling
import yaml

from utils.ui.icon_system import get_icon, replace_emojis
# Configure error handling
configure_streamlit_error_handling()

# Seguridad - Generar Estado OAuth
def generate_state():
    """Generate a random state parameter for OAuth security"""
    return secrets.token_urlsafe(32)

# Seguridad - Generar PKCE (Deprecated)
def generate_pkce():
    """(Deprecated in this app) Kept for compatibility, but PKCE is not used now."""
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')
    return code_verifier, code_challenge

# Principal - Login OAuth
@safe_main
def main():
    """Página de login con OAuth (Google/Microsoft)"""
    st.set_page_config(
        page_title="OAuth Login - Google/Microsoft",
        page_icon="🌐",
        layout="wide"
    )
    
    # UI - Inicializar Sidebar con Info de Usuario
    from utils.ui import auth_ui
    current_user = auth_ui.init_sidebar()
    
    # Validacion - Verificar si Usuario ya esta Autenticado
    if not current_user:
        current_user = get_current_user()
    if current_user:
        st.markdown(f"{get_icon('✅', 20)} Ya estás autenticado como {current_user['username']}", unsafe_allow_html=True)
        st.info("Redirigiendo al inicio...")
        st.switch_page("Inicio.py")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4285f4 0%, #34a853 50%, #fbbc05 75%, #ea4335 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🌐 Iniciar Sesión con Proveedores Externos</h1>
        <p style="color: white; font-size: 1.1rem;">Usa tu cuenta de Google o Microsoft para acceder rápidamente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle OAuth callback first
    if handle_oauth_callback():
        return  # If callback was handled, stop here
    
    # OAuth Configuration
    st.markdown(replace_emojis("### 🔐 Opciones de Inicio de Sesión"), unsafe_allow_html=True)
    
    # Validacion - Verificar si OAuth esta Configurado
    try:
        raw_flag = st.secrets.get("oauth_configured", False)
    except Exception:
        raw_flag = False
    
    if isinstance(raw_flag, bool):
        oauth_configured = raw_flag
    else:
        oauth_configured = str(raw_flag).strip().lower() in ("1", "true", "yes", "on")
    
    if not oauth_configured:
        st.warning("⚠️ OAuth no está configurado aún. Usa el login local por ahora.")
        st.info("""
        Para habilitar OAuth, necesitas:
        1. **Configurar credenciales** en `.streamlit/secrets.toml`
        2. **Crear aplicaciones** en Google Cloud Console y Azure Portal
        3. **Configurar URIs** de redirección
        
        Consulta la documentación en `docs/OAUTH_SETUP_GUIDE.md`
        """)
        
        # Fallback to local login
        st.markdown("---")
        st.markdown("### 🔑 Login Local")
        show_local_login()
    
    else:
        # OAuth is configured - show OAuth options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔵 Google OAuth")
            if st.button("🔵 Iniciar sesión con Google", use_container_width=True, type="primary"):
                handle_google_oauth()
        
        with col2:
            st.markdown("### 🔴 Microsoft OAuth (Próximamente)")
            st.button("🔴 Microsoft (no disponible aún)", use_container_width=True, disabled=True)
        
        # Also show local login as option
        st.markdown("---")
        st.markdown("### 🔑 O usar login local")
        show_local_login()
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🔗 Navegación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("📝 Crear Cuenta Local", use_container_width=True):
            st.switch_page("pages/05_Registro.py")
    
    with col3:
        if st.button("🔑 Recuperar Contraseña", use_container_width=True):
            st.switch_page("pages/06_Recuperar_Password.py")
    
    with col4:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

# UI - Mostrar Formulario de Login Local
def show_local_login():
    """Show local login form"""
    with st.form("local_login_form"):
        username = st.text_input("👤 Usuario", placeholder="Tu nombre de usuario")
        password = st.text_input("🔒 Contraseña", type="password", placeholder="Tu contraseña")
        
        col1, col2 = st.columns(2)
        with col1:
            login_submitted = st.form_submit_button("🚀 Iniciar Sesión", type="primary", use_container_width=True)
        with col2:
            if st.form_submit_button("📝 Registrarse", use_container_width=True):
                st.switch_page("pages/05_Registro.py")
    
    if login_submitted and username and password:
        success, message = login_user(username, password)
        if success:
            st.markdown(replace_emojis("✅ ¡Inicio de sesión exitoso!"), unsafe_allow_html=True)
            st.rerun()
        else:
            st.markdown(f"{get_icon("❌", 20)} {message}", unsafe_allow_html=True)

# OAuth - Manejar Flujo de Google
def handle_google_oauth():
    """Handle Google OAuth flow"""
    try:
        # Get OAuth config from secrets
        try:
            google_config = st.secrets.get("google_oauth", {})
        except Exception:
            st.markdown(replace_emojis("❌ Error al acceder a la configuración de OAuth"), unsafe_allow_html=True)
            st.info("Verifica que el archivo `.streamlit/secrets.toml` esté configurado correctamente")
            return
            
        client_id = google_config.get("client_id")
        client_secret = google_config.get("client_secret")
        redirect_uri = google_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        if not client_id or not client_secret:
            st.markdown(replace_emojis("❌ Google OAuth no está configurado correctamente"), unsafe_allow_html=True)
            st.info("Configura las credenciales de Google en `.streamlit/secrets.toml`")
            return
        
        # Generate OAuth parameters (without PKCE to avoid dependency on session state)
        state = generate_state()
        
        # Store in session state only the state and provider
        st.session_state.oauth_state = state
        st.session_state.oauth_provider = "google"
        
        # Build authorization URL (no code_challenge)
        auth_params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
        
        # Mensaje simple y amigable sin mostrar la URL completa
        st.markdown(replace_emojis("🔄 Para continuar con Google OAuth, haz clic en el siguiente botón:"), unsafe_allow_html=True)
        # Enlace como botón (se abre normalmente en nueva pestaña)
        st.markdown(
            f'<a href="{auth_url}" target="_blank" style="display:inline-block;padding:0.6em 1.4em;color:white;background-color:#4285F4;border-radius:999px;text-decoration:none;font-family:sans-serif;font-weight:600;">🔗 Continuar con Google</a>',
            unsafe_allow_html=True,
        )
        
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error en Google OAuth: {str(e)}", unsafe_allow_html=True)

# OAuth - Manejar Flujo de Microsoft
def handle_microsoft_oauth():
    """Handle Microsoft OAuth flow"""
    try:
        # Get OAuth config from secrets
        try:
            microsoft_config = st.secrets.get("microsoft_oauth", {})
        except Exception:
            st.markdown(replace_emojis("❌ Error al acceder a la configuración de OAuth"), unsafe_allow_html=True)
            st.info("Verifica que el archivo `.streamlit/secrets.toml` esté configurado correctamente")
            return
            
        client_id = microsoft_config.get("client_id")
        client_secret = microsoft_config.get("client_secret")
        redirect_uri = microsoft_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        if not client_id or not client_secret:
            st.markdown(replace_emojis("❌ Microsoft OAuth no está configurado correctamente"), unsafe_allow_html=True)
            st.info("Configura las credenciales de Microsoft en `.streamlit/secrets.toml`")
            return
        
        # Generate OAuth parameters (without PKCE)
        state = generate_state()
        
        # Store in session state only the state and provider
        st.session_state.oauth_state = state
        st.session_state.oauth_provider = "microsoft"
        
        # Build authorization URL (no code_challenge)
        auth_params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state
        }
        
        auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(auth_params)}"
        
        # Por ahora no mostramos botón activo para Microsoft (solo mensaje informativo)
        st.markdown(replace_emojis("ℹ️ Integración con Microsoft OAuth disponible próximamente."), unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error en Microsoft OAuth: {str(e)}", unsafe_allow_html=True)

# OAuth - Manejar Callback y Token
def handle_oauth_callback():
    """Handle OAuth callback and token exchange"""
    # Validacion - Verificar si estamos en un Callback
    query_params = st.query_params
    
    if 'code' in query_params and 'state' in query_params:
        code = query_params['code']
        state = query_params['state']
        
        # Secure OAuth callback validation
        stored_state = st.session_state.get('oauth_state')
        callback_valid, callback_msg = secure_oauth_callback(code, state, stored_state)
        
        if not callback_valid:
            st.markdown(f"{get_icon("❌", 20)} {callback_msg}", unsafe_allow_html=True)
            return True  # Indicate callback was handled
        
        provider = st.session_state.get('oauth_provider')
        
        # If provider was lost due to a new Streamlit session, try to infer it
        if not provider:
            try:
                google_config = st.secrets.get("google_oauth", {})
            except Exception:
                google_config = {}
            try:
                microsoft_config = st.secrets.get("microsoft_oauth", {})
            except Exception:
                microsoft_config = {}
            
            google_configured = bool(google_config.get("client_id"))
            microsoft_configured = bool(microsoft_config.get("client_id"))
            
            # Heuristic: if only one provider is configured, assume that one
            if google_configured and not microsoft_configured:
                provider = "google"
            elif microsoft_configured and not google_configured:
                provider = "microsoft"
        
        if provider == "google":
            success = handle_google_callback(code)
        elif provider == "microsoft":
            success = handle_microsoft_callback(code)
        else:
            st.markdown(replace_emojis("❌ Proveedor OAuth no reconocido"), unsafe_allow_html=True)
            return True
        
        # Clear OAuth session state
        for key in ['oauth_state', 'oauth_code_verifier', 'oauth_provider']:
            if key in st.session_state:
                del st.session_state[key]
        
        if success:
            st.markdown(replace_emojis("✅ ¡Inicio de sesión exitoso!"), unsafe_allow_html=True)
            st.info("Redirigiendo al inicio...")
            st.switch_page("Inicio.py")
        
        return True  # Indicate callback was handled
    
    return False  # No callback to handle

# OAuth - Callback de Google
def handle_google_callback(code):
    """Handle Google OAuth callback"""
    try:
        try:
            google_config = st.secrets.get("google_oauth", {})
        except Exception:
            st.markdown(replace_emojis("❌ Error al acceder a la configuración de OAuth"), unsafe_allow_html=True)
            return False
            
        client_id = google_config.get("client_id")
        client_secret = google_config.get("client_secret")
        redirect_uri = google_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        # Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        
        response = requests.post(token_url, data=token_data)
        token_info = response.json()
        
        if 'access_token' in token_info:
            # Get user info
            user_info = get_google_user_info(token_info['access_token'])
            
            # Create or update user in local config
            username = create_oauth_user(user_info, "google")
            
            if username:
                st.markdown(f"{get_icon('✅', 20)} ¡Bienvenido, {user_info.get('name', 'Usuario')}!", unsafe_allow_html=True)
                st.markdown(replace_emojis("🔐 Sesión iniciada con Google"), unsafe_allow_html=True)
                return True
            else:
                st.markdown(replace_emojis("❌ Error al crear usuario OAuth"), unsafe_allow_html=True)
                return False
        else:
            # Mostrar detalles del error devuelto por Google para diagnóstico
            error = token_info.get("error", "desconocido")
            error_desc = token_info.get("error_description", "")
            st.markdown(replace_emojis("❌ Error al obtener token de acceso"), unsafe_allow_html=True)
            if error or error_desc:
                st.markdown(f"**Detalle del error:** `{error}` - {error_desc}")
            return False
            
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error en callback de Google: {str(e)}", unsafe_allow_html=True)
        return False

# OAuth - Callback de Microsoft
def handle_microsoft_callback(code):
    """Handle Microsoft OAuth callback"""
    try:
        try:
            microsoft_config = st.secrets.get("microsoft_oauth", {})
        except Exception:
            st.markdown(replace_emojis("❌ Error al acceder a la configuración de OAuth"), unsafe_allow_html=True)
            return False
            
        client_id = microsoft_config.get("client_id")
        client_secret = microsoft_config.get("client_secret")
        redirect_uri = microsoft_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        # Exchange code for token
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        
        response = requests.post(token_url, data=token_data)
        token_info = response.json()
        
        if 'access_token' in token_info:
            # Get user info
            user_info = get_microsoft_user_info(token_info['access_token'])
            
            # Create or update user in local config
            username = create_oauth_user(user_info, "microsoft")
            
            if username:
                st.markdown(f"{get_icon('✅', 20)} ¡Bienvenido, {user_info.get('displayName', 'Usuario')}!", unsafe_allow_html=True)
                st.markdown(replace_emojis("🔐 Sesión iniciada con Microsoft"), unsafe_allow_html=True)
                return True
            else:
                st.markdown(replace_emojis("❌ Error al crear usuario OAuth"), unsafe_allow_html=True)
                return False
        else:
            # Mostrar detalles del error devuelto por Microsoft para diagnóstico
            error = token_info.get("error", "desconocido")
            error_desc = token_info.get("error_description", "")
            st.markdown(replace_emojis("❌ Error al obtener token de acceso"), unsafe_allow_html=True)
            if error or error_desc:
                st.markdown(f"**Detalle del error:** `{error}` - {error_desc}")
            return False
            
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error en callback de Microsoft: {str(e)}", unsafe_allow_html=True)
        return False

# OAuth - Obtener Info de Usuario Google
def get_google_user_info(access_token):
    """Get user info from Google"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    return response.json()

# OAuth - Obtener Info de Usuario Microsoft
def get_microsoft_user_info(access_token):
    """Get user info from Microsoft"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()

# Usuario - Crear Usuario OAuth
def create_oauth_user(user_info, provider):
    """Create or update user in local config from OAuth info"""
    try:
        # For now, we'll create a simple user entry
        # In a real implementation, you'd want to save this to your database
        
        # Generate username from email
        email = user_info.get('email', user_info.get('mail', ''))
        username = email.split('@')[0] if email else f"{provider}_user_{secrets.token_hex(4)}"
        
        # Create a simple user entry for OAuth
        # This is a temporary solution - in production you'd want proper database integration
        oauth_user = {
            'username': username,
            'email': email,
            'first_name': user_info.get('given_name', user_info.get('name', '').split()[0] if user_info.get('name') else ''),
            'last_name': user_info.get('family_name', user_info.get('name', '').split()[-1] if user_info.get('name') else ''),
            'oauth_provider': provider,
            'oauth_id': user_info.get('id', '')
        }
        
        # Store in session state for now (temporary solution)
        st.session_state.oauth_user = oauth_user
        st.session_state.authenticated = True
        st.session_state.user = oauth_user
        
        return username
        
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error al crear usuario OAuth: {str(e)}", unsafe_allow_html=True)
        return None

if __name__ == "__main__":
    main()
