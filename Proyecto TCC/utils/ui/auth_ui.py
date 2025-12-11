import streamlit as st
from core.auth_service import login_user, logout_user, get_current_user as db_get_current_user

from utils.ui.icon_system import get_icon, replace_emojis
HIDDEN_NAVIGATION_PATTERNS = [
    "pages/99_Survey",
    "pages/99_Admin",
    "/99_Survey",
    "/99_Admin",
    "99_Survey_",
    "99_Admin_",
]


# UI - Ocultar Entradas Restringidas del Sidebar
def hide_restricted_sidebar_entries():
    """Inject CSS rules to hide restricted pages from the sidebar navigation."""
    if not HIDDEN_NAVIGATION_PATTERNS:
        return

    selectors = []
    for pattern in HIDDEN_NAVIGATION_PATTERNS:
        selectors.append(f'section[data-testid="stSidebar"] a[href*="{pattern}"]')
        selectors.append(f'section[data-testid="stSidebar"] li a[href*="{pattern}"]')
        selectors.append(f'section[data-testid="stSidebar"] button[href*="{pattern}"]')
    combined_selector = ", ".join(selectors)
    css_rules = f"{combined_selector} {{ display: none !important; }}"
    st.markdown(f"<style>{css_rules}</style>", unsafe_allow_html=True)

    scripts = """
    <script>
    const __dashboardHiddenKeywords = ["encuesta", "survey", "admin database", "admin backup", "admin"];
    const __hideRestrictedNav = () => {
        const doc = window.parent?.document || document;
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) { return; }
        const links = sidebar.querySelectorAll('a, button');
        links.forEach(link => {
            const text = (link.innerText || "").trim().toLowerCase();
            const href = (link.getAttribute("href") || "").toLowerCase();
            if (__dashboardHiddenKeywords.some(keyword => text.includes(keyword) || href.includes(keyword))) {
                link.style.display = "none";
                if (link.parentElement && link.parentElement.tagName === "LI") {
                    link.parentElement.style.display = "none";
                }
            }
        });
    };
    const __sidebarObserver = new MutationObserver(() => __hideRestrictedNav());
    __sidebarObserver.observe(window.parent?.document?.body || document.body, { childList: true, subtree: true });
    setInterval(__hideRestrictedNav, 800);
    window.addEventListener("load", __hideRestrictedNav);
    __hideRestrictedNav();
    </script>
    """
    st.markdown(scripts, unsafe_allow_html=True)


# UI - Mostrar Formulario de Login
def show_login_form():
    """Display the login form for unauthenticated users"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">{get_icon("🔐", 28)} Iniciar Sesión</h1>
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
            st.markdown(replace_emojis("✅ ¡Inicio de sesión exitoso!"), unsafe_allow_html=True)
            st.rerun()
        else:
            st.markdown(f"{get_icon("❌", 20)} {message}", unsafe_allow_html=True)
    
    # UI - Agregar Opciones Adicionales
    st.markdown("---")
    st.markdown(replace_emojis("### 🔐 ¿Necesitas ayuda?"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Crear Nueva Cuenta", type="primary", use_container_width=True):
            st.switch_page("pages/05_Registro.py")
    with col2:
        if st.button("🔑 ¿Olvidaste tu contraseña?", use_container_width=True):
            st.switch_page("pages/06_Recuperar_Password.py")
    with col3:
        if st.button("🌐 Login con Google/Microsoft", use_container_width=True):
            st.switch_page("pages/07_Inicio_de_Sesion_con_Google.py")

# UI - Mostrar Sidebar de Usuario
def show_user_sidebar(current_user=None):
    """Display user information and logout button in sidebar - Always shows username prominently"""
    hide_restricted_sidebar_entries()
    with st.sidebar:
        st.markdown(replace_emojis("### 👤 Usuario"), unsafe_allow_html=True)
        st.markdown("---")
        
        if current_user:
            # Persist authenticated user info in session state for cross-page utilities
            st.session_state['auth_user'] = current_user
            st.session_state['auth_user_id'] = current_user.get('id')
            st.session_state['auth_username'] = current_user.get('username')
            st.session_state['auth_user_full_name'] = f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}".strip()

            # Handle both database users and OAuth users
            if 'oauth_provider' in current_user:
                # OAuth user
                name = f"{current_user['first_name']} {current_user['last_name']}"
                username = current_user['username']
                provider = current_user['oauth_provider'].title()
                
                # Show username prominently
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                    <h3 style="color: white; margin: 0;">@{username}</h3>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{name}</p>
                    <p style="color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem;">{get_icon("🔐", 16)} {provider}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Database user
                name = f"{current_user['first_name']} {current_user['last_name']}"
                username = current_user['username']
                
                # Show username prominently with green background to indicate active session
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                            padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                    <h3 style="color: white; margin: 0;">@{username}</h3>
                    <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{name}</p>
                    <p style="color: white; margin: 0.3rem 0 0 0; font-size: 0.8rem;">{get_icon("✅", 16)} Sesión activa</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Botón para repetir el tour de onboarding (solo usuarios de BD)
            if 'oauth_provider' not in current_user:
                # Check onboarding status to show appropriate button text
                from core.database import DatabaseManager
                from utils.ui.onboarding import check_onboarding_status
                
                if '_db_manager' not in st.session_state:
                    st.session_state._db_manager = DatabaseManager()
                db_manager = st.session_state._db_manager
                user_id = current_user.get('id')
                
                onboarding_completed = False
                if user_id:
                    try:
                        onboarding_completed = check_onboarding_status(user_id, db_manager)
                    except:
                        pass  # If check fails, assume not completed
                
                button_text = "🔄 Repetir Tour de Introducción" if onboarding_completed else "🎯 Ver Tour de Introducción"
                button_help = " (Ya completado - puedes repetirlo)" if onboarding_completed else ""
                
                if st.button(button_text, use_container_width=True, key="repeat_onboarding", help=f"Tour guiado que explica las funcionalidades principales de la plataforma{button_help}"):
                    # Reset onboarding state to start from beginning
                    st.session_state.show_onboarding = True
                    st.session_state.onboarding_step = 0
                    st.session_state.onboarding_active = True
                    # Clear any cached onboarding status to force re-check
                    check_onboarding_status.clear()
                    st.rerun()
                st.markdown("---")
            
            if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
                logout_user()
                st.rerun()
            
            return name
        else:
            # Clear cached auth info
            st.session_state.pop('auth_user', None)
            st.session_state.pop('auth_user_id', None)
            st.session_state.pop('auth_username', None)
            st.session_state.pop('auth_user_full_name', None)
            # Not authenticated - show login prompt with clear indication
            st.markdown(f"""
            <div style="background: #f0f0f0; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center; border: 2px solid #ff6b6b;">
                <p style="color: #666; margin: 0; font-weight: bold;">{get_icon("⚠️", 16)} No autenticado</p>
                <p style="color: #999; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{get_icon("👤", 16)} Usuario: Invitado</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🔐 Iniciar Sesión", type="primary", use_container_width=True):
                st.switch_page("Inicio.py")
            return None

# Consulta - Obtener Usuario Actual
def get_current_user():
    """Get current authenticated user (handles both database and OAuth users)"""
    # Validacion - Verificar Usuario OAuth en Session State
    if st.session_state.get('authenticated') and st.session_state.get('oauth_user'):
        return st.session_state.oauth_user
    
    # Consulta - Obtener Usuario de Base de Datos
    return db_get_current_user()

# Inicializacion - Inicializar Sidebar
def init_sidebar():
    """Initialize sidebar with user info on all pages - Call this at the start of every page"""
    current_user = get_current_user()
    show_user_sidebar(current_user)
    return current_user

# Autenticacion - Manejar Flujo de Autenticacion
def handle_authentication():
    """Handle authentication flow and return user info if authenticated"""
    current_user = get_current_user()
    
    # UI - Mostrar Sidebar con Nombre de Usuario (Incluso si No Autenticado)
    name = show_user_sidebar(current_user)
    
    if not current_user:
        show_login_form()
        return None, None
    
    # Validacion - Usuario Autenticado
    return current_user, name
