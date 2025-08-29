import streamlit as st
from core.auth_service import login_user, logout_user, get_current_user

def show_login_form():
    """Display the login form for unauthenticated users"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🔐 Iniciar Sesión</h1>
        <p style="color: white; font-size: 1.1rem;">Accede a tu cuenta para continuar</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
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
            st.success("✅ ¡Inicio de sesión exitoso!")
            st.rerun()
        else:
            st.error(f"❌ {message}")
    
    # Add additional options
    st.markdown("---")
    st.markdown("### 🔐 ¿Necesitas ayuda?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Crear Nueva Cuenta", type="primary", use_container_width=True):
            st.switch_page("pages/05_Registro.py")
    with col2:
        if st.button("🔑 ¿Olvidaste tu contraseña?", use_container_width=True):
            st.switch_page("pages/06_Recuperar_Password.py")
    with col3:
        if st.button("🌐 Login con Google/Microsoft", use_container_width=True):
            st.switch_page("pages/07_OAuth_Login.py")

def show_user_sidebar(current_user):
    """Display user information and logout button in sidebar"""
    with st.sidebar:
        st.markdown("### 👤 Usuario")
        name = f"{current_user['first_name']} {current_user['last_name']}"
        st.write(f"**{name}**")
        st.write(f"@{current_user['username']}")
        
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            logout_user()
            st.rerun()
    
    return name

def handle_authentication():
    """Handle authentication flow and return user info if authenticated"""
    current_user = get_current_user()
    
    if not current_user:
        show_login_form()
        return None, None
    
    # User is authenticated - show logout button
    username = current_user['username']
    name = show_user_sidebar(current_user)
    
    return current_user, name
