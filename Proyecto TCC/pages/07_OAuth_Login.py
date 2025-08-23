import streamlit as st
import requests
import json
import os
from urllib.parse import urlencode, parse_qs, urlparse
import base64
import hashlib
import secrets
from core.auth_config import init_authentication, load_auth_config
from core.security import security_manager, secure_oauth_callback
import yaml

def generate_state():
    """Generate a random state parameter for OAuth security"""
    return secrets.token_urlsafe(32)

def generate_pkce():
    """Generate PKCE code verifier and challenge"""
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')
    return code_verifier, code_challenge

def main():
    """Página de login con OAuth (Google/Microsoft)"""
    st.set_page_config(
        page_title="OAuth Login - Google/Microsoft",
        page_icon="🌐",
        layout="wide"
    )
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4285f4 0%, #34a853 50%, #fbbc05 75%, #ea4335 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🌐 Iniciar Sesión con Proveedores Externos</h1>
        <p style="color: white; font-size: 1.1rem;">Usa tu cuenta de Google o Microsoft para acceder rápidamente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize authentication
    authenticator = init_authentication()
    
    # OAuth Configuration
    st.markdown("### 🔐 Opciones de Inicio de Sesión")
    
    # Check if OAuth is configured
    try:
        oauth_configured = st.secrets.get("oauth_configured", False)
    except Exception:
        oauth_configured = False
    
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
        authenticator.login()
        
        if st.session_state.get('authentication_status'):
            st.success("✅ Login exitoso!")
            st.rerun()
        elif st.session_state.get('authentication_status') == False:
            st.error('❌ Usuario/contraseña incorrectos')
    
    else:
        # OAuth is configured - show OAuth options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔵 Google OAuth")
            if st.button("🔵 Iniciar sesión con Google", use_container_width=True, type="primary"):
                handle_google_oauth()
        
        with col2:
            st.markdown("### 🔴 Microsoft OAuth")
            if st.button("🔴 Iniciar sesión con Microsoft", use_container_width=True, type="primary"):
                handle_microsoft_oauth()
        
        # Also show local login as option
        st.markdown("---")
        st.markdown("### 🔑 O usar login local")
        authenticator.login()
        
        if st.session_state.get('authentication_status'):
            st.success("✅ Login exitoso!")
            st.rerun()
        elif st.session_state.get('authentication_status') == False:
            st.error('❌ Usuario/contraseña incorrectos')
    
    # Handle OAuth callback
    handle_oauth_callback()
    
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

def handle_google_oauth():
    """Handle Google OAuth flow"""
    try:
        # Get OAuth config from secrets
        try:
            google_config = st.secrets.get("google_oauth", {})
        except Exception:
            st.error("❌ Error al acceder a la configuración de OAuth")
            st.info("Verifica que el archivo `.streamlit/secrets.toml` esté configurado correctamente")
            return
            
        client_id = google_config.get("client_id")
        client_secret = google_config.get("client_secret")
        redirect_uri = google_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        if not client_id or not client_secret:
            st.error("❌ Google OAuth no está configurado correctamente")
            st.info("Configura las credenciales de Google en `.streamlit/secrets.toml`")
            return
        
        # Generate OAuth parameters
        state = generate_state()
        code_verifier, code_challenge = generate_pkce()
        
        # Store in session state
        st.session_state.oauth_state = state
        st.session_state.oauth_code_verifier = code_verifier
        st.session_state.oauth_provider = "google"
        
        # Build authorization URL
        auth_params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
        
        # Redirect to Google
        st.markdown(f"""
        <script>
            window.open('{auth_url}', '_self');
        </script>
        """, unsafe_allow_html=True)
        
        st.info("🔄 Redirigiendo a Google...")
        
    except Exception as e:
        st.error(f"❌ Error en Google OAuth: {str(e)}")

def handle_microsoft_oauth():
    """Handle Microsoft OAuth flow"""
    try:
        # Get OAuth config from secrets
        try:
            microsoft_config = st.secrets.get("microsoft_oauth", {})
        except Exception:
            st.error("❌ Error al acceder a la configuración de OAuth")
            st.info("Verifica que el archivo `.streamlit/secrets.toml` esté configurado correctamente")
            return
            
        client_id = microsoft_config.get("client_id")
        client_secret = microsoft_config.get("client_secret")
        redirect_uri = microsoft_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        
        if not client_id or not client_secret:
            st.error("❌ Microsoft OAuth no está configurado correctamente")
            st.info("Configura las credenciales de Microsoft en `.streamlit/secrets.toml`")
            return
        
        # Generate OAuth parameters
        state = generate_state()
        code_verifier, code_challenge = generate_pkce()
        
        # Store in session state
        st.session_state.oauth_state = state
        st.session_state.oauth_code_verifier = code_verifier
        st.session_state.oauth_provider = "microsoft"
        
        # Build authorization URL
        auth_params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(auth_params)}"
        
        # Redirect to Microsoft
        st.markdown(f"""
        <script>
            window.open('{auth_url}', '_self');
        </script>
        """, unsafe_allow_html=True)
        
        st.info("🔄 Redirigiendo a Microsoft...")
        
    except Exception as e:
        st.error(f"❌ Error en Microsoft OAuth: {str(e)}")

def handle_oauth_callback():
    """Handle OAuth callback and token exchange"""
    # Check if we're in a callback
    query_params = st.query_params
    
    if 'code' in query_params and 'state' in query_params:
        code = query_params['code']
        state = query_params['state']
        
        # Secure OAuth callback validation
        stored_state = st.session_state.get('oauth_state')
        callback_valid, callback_msg = secure_oauth_callback(code, state, stored_state)
        
        if not callback_valid:
            st.error(f"❌ {callback_msg}")
            return
        
        provider = st.session_state.get('oauth_provider')
        
        if provider == "google":
            handle_google_callback(code)
        elif provider == "microsoft":
            handle_microsoft_callback(code)
        
        # Clear OAuth session state
        for key in ['oauth_state', 'oauth_code_verifier', 'oauth_provider']:
            if key in st.session_state:
                del st.session_state[key]

def handle_google_callback(code):
    """Handle Google OAuth callback"""
    try:
        try:
            google_config = st.secrets.get("google_oauth", {})
        except Exception:
            st.error("❌ Error al acceder a la configuración de OAuth")
            return
            
        client_id = google_config.get("client_id")
        client_secret = google_config.get("client_secret")
        redirect_uri = google_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        code_verifier = st.session_state.get('oauth_code_verifier')
        
        # Exchange code for token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code_verifier': code_verifier
        }
        
        response = requests.post(token_url, data=token_data)
        token_info = response.json()
        
        if 'access_token' in token_info:
            # Get user info
            user_info = get_google_user_info(token_info['access_token'])
            
            # Create or update user in local config
            create_oauth_user(user_info, "google")
            
            st.success(f"✅ ¡Bienvenido, {user_info.get('name', 'Usuario')}!")
            st.info("🔐 Sesión iniciada con Google")
            
            # Redirect to main page
            st.switch_page("Inicio.py")
        else:
            st.error("❌ Error al obtener token de acceso")
            
    except Exception as e:
        st.error(f"❌ Error en callback de Google: {str(e)}")

def handle_microsoft_callback(code):
    """Handle Microsoft OAuth callback"""
    try:
        try:
            microsoft_config = st.secrets.get("microsoft_oauth", {})
        except Exception:
            st.error("❌ Error al acceder a la configuración de OAuth")
            return
            
        client_id = microsoft_config.get("client_id")
        client_secret = microsoft_config.get("client_secret")
        redirect_uri = microsoft_config.get("redirect_uri", "http://localhost:8501/oauth_callback")
        code_verifier = st.session_state.get('oauth_code_verifier')
        
        # Exchange code for token
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code_verifier': code_verifier
        }
        
        response = requests.post(token_url, data=token_data)
        token_info = response.json()
        
        if 'access_token' in token_info:
            # Get user info
            user_info = get_microsoft_user_info(token_info['access_token'])
            
            # Create or update user in local config
            create_oauth_user(user_info, "microsoft")
            
            st.success(f"✅ ¡Bienvenido, {user_info.get('displayName', 'Usuario')}!")
            st.info("🔐 Sesión iniciada con Microsoft")
            
            # Redirect to main page
            st.switch_page("Inicio.py")
        else:
            st.error("❌ Error al obtener token de acceso")
            
    except Exception as e:
        st.error(f"❌ Error en callback de Microsoft: {str(e)}")

def get_google_user_info(access_token):
    """Get user info from Google"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    return response.json()

def get_microsoft_user_info(access_token):
    """Get user info from Microsoft"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()

def create_oauth_user(user_info, provider):
    """Create or update user in local config from OAuth info"""
    try:
        config = load_auth_config()
        
        # Generate username from email
        email = user_info.get('email', user_info.get('mail', ''))
        username = email.split('@')[0] if email else f"{provider}_user_{secrets.token_hex(4)}"
        
        # Ensure unique username
        counter = 1
        original_username = username
        while username in config['credentials']['usernames']:
            username = f"{original_username}_{counter}"
            counter += 1
        
        # Create user entry
        user_entry = {
            'email': email,
            'first_name': user_info.get('given_name', user_info.get('name', '').split()[0] if user_info.get('name') else ''),
            'last_name': user_info.get('family_name', user_info.get('name', '').split()[-1] if user_info.get('name') else ''),
            'password': secrets.token_hex(16),  # Random password for OAuth users
            'failed_login_attempts': 0,
            'logged_in': False,
            'oauth_provider': provider,
            'oauth_id': user_info.get('id', '')
        }
        
        config['credentials']['usernames'][username] = user_entry
        
        # Save updated config
        with open('config/config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        
        # Set session state for login
        st.session_state.authentication_status = True
        st.session_state.username = username
        st.session_state.name = f"{user_entry['first_name']} {user_entry['last_name']}".strip()
        
        return username
        
    except Exception as e:
        st.error(f"❌ Error al crear usuario OAuth: {str(e)}")
        return None

if __name__ == "__main__":
    main()
