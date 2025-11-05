import streamlit as st
from core.auth_service import auth_service
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling
from core.database import db_manager
from utils.ui import auth_ui
import re

# Import init_sidebar - using module import for better compatibility
init_sidebar = auth_ui.init_sidebar

# Configure error handling at module level
configure_streamlit_error_handling()

# Ensure database is initialized before using it
from core.database import ensure_database_initialized
try:
    ensure_database_initialized()
except Exception as e:
    # Error will be shown when page loads
    pass

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@safe_main
def main():
    """Página de recuperación de contraseña con verificación de email y cambio de email"""
    st.set_page_config(
        page_title="Recuperar Contraseña",
        page_icon="🔑",
        layout="wide"
    )
    
    # Initialize sidebar with user info (always visible)
    init_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🔑 Recuperar Contraseña</h1>
        <p style="color: white; font-size: 1.1rem;">Recupera tu contraseña o actualiza tu email de forma segura</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab selection for different recovery options
    tab1, tab2 = st.tabs(["🔑 Recuperar Contraseña", "📧 Cambiar Email"])
    
    with tab1:
        st.markdown("### 🔐 Recuperar Contraseña")
        st.info("""
        **Proceso de recuperación:**
        1. Ingresa tu nombre de usuario
        2. Verifica tu email (debe coincidir con el registrado)
        3. Recibe tu nueva contraseña
        """)
        
        # Password recovery form
        with st.form("password_recovery_form", clear_on_submit=False):
            username = st.text_input(
                "Nombre de Usuario",
                placeholder="Ingresa tu nombre de usuario",
                help="Ingresa el nombre de usuario de tu cuenta"
            )
            
            submitted = st.form_submit_button("🔑 Continuar", type="primary", use_container_width=True)
            
            if submitted:
                if not username:
                    st.session_state.recovery_error = "❌ Por favor ingresa tu nombre de usuario"
                    st.rerun()
                else:
                    # Check if user exists and get email
                    username_sanitized = username.strip()
                    with db_manager.get_connection() as conn:
                        cursor = conn.execute("""
                            SELECT id, username, email, first_name, last_name 
                            FROM users 
                            WHERE username = ? AND is_active = 1
                        """, (username_sanitized,))
                        user = cursor.fetchone()
                    
                    if user:
                        # Store user info for email verification step
                        st.session_state.recovery_user = {
                            'id': user['id'],
                            'username': user['username'],
                            'email': user['email'],
                            'first_name': user['first_name'],
                            'last_name': user['last_name']
                        }
                        st.session_state.recovery_step = 'verify_email'
                        st.rerun()
                    else:
                        st.session_state.recovery_error = '❌ Usuario no encontrado o cuenta inactiva'
                        st.rerun()
        
        # Email verification step (2FA-like)
        if st.session_state.get('recovery_step') == 'verify_email' and st.session_state.get('recovery_user'):
            user_info = st.session_state.recovery_user
            st.markdown("---")
            st.markdown("### 🔒 Verificación de Seguridad")
            st.warning(f"""
            **Verificación requerida:**
            
            Para tu seguridad, necesitamos verificar que eres el dueño de esta cuenta.
            
            **Usuario:** {user_info['username']}
            **Email registrado:** {user_info['email'][:3]}***@***{user_info['email'].split('@')[1] if '@' in user_info['email'] else ''}
            """)
            
            with st.form("email_verification_form"):
                verification_email = st.text_input(
                    "Confirma tu email completo",
                    placeholder="tu@email.com",
                    help="Ingresa el email completo registrado en tu cuenta"
                )
                
                verify_submitted = st.form_submit_button("✅ Verificar y Recuperar", type="primary", use_container_width=True)
                
                if verify_submitted:
                    if not verification_email:
                        st.error("❌ Por favor ingresa tu email")
                    elif verification_email.lower().strip() != user_info['email'].lower().strip():
                        st.error("❌ El email no coincide con el registrado. Por favor verifica e intenta nuevamente.")
                        st.info("💡 Si no recuerdas tu email, puedes usar la opción 'Cambiar Email' después de iniciar sesión")
                    else:
                        # Email verified - proceed with password recovery
                        success, recovered_username, email, new_password = auth_service.forgot_password(user_info['username'])
                        
                        if success:
                            st.session_state.recovery_success = True
                            st.session_state.recovery_data = {
                                'username': recovered_username,
                                'email': email,
                                'password': new_password
                            }
                            # Clear recovery step
                            if 'recovery_step' in st.session_state:
                                del st.session_state.recovery_step
                            if 'recovery_user' in st.session_state:
                                del st.session_state.recovery_user
                            st.rerun()
                        else:
                            st.error("❌ Error al generar la nueva contraseña")
        
        # Show success message
        if st.session_state.get('recovery_success', False):
            recovery_data = st.session_state.get('recovery_data', {})
            st.markdown("---")
            st.success('✅ Nueva contraseña generada exitosamente!')
            st.info(f'👤 Usuario: {recovery_data.get("username", "")}')
            st.info(f'📧 Email: {recovery_data.get("email", "")}')
            st.warning(f'🔑 Nueva contraseña: **{recovery_data.get("password", "")}**')
            
            st.markdown("""
            ### ⚠️ Importante:
            - **Guarda esta contraseña en un lugar seguro**
            - **Cámbiala después de iniciar sesión**
            - **Esta contraseña es temporal**
            """)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("🏠 Ir al Inicio", type="primary", use_container_width=True):
                    if 'recovery_success' in st.session_state:
                        del st.session_state.recovery_success
                    if 'recovery_data' in st.session_state:
                        del st.session_state.recovery_data
                    st.switch_page("Inicio.py")
        
        # Show error if any
        if st.session_state.get('recovery_error'):
            st.error(st.session_state.recovery_error)
            del st.session_state.recovery_error
    
    with tab2:
        st.markdown("### 📧 Cambiar Email")
        st.info("""
        **Para cambiar tu email:**
        1. Debes estar autenticado (iniciar sesión primero)
        2. Ingresa tu nuevo email
        3. Confirma el cambio
        """)
        
        # Check if user is authenticated
        from core.auth_service import get_current_user
        current_user = get_current_user()
        
        if not current_user:
            st.warning("⚠️ Debes iniciar sesión para cambiar tu email")
            if st.button("🔐 Ir a Iniciar Sesión", type="primary", use_container_width=True):
                st.switch_page("Inicio.py")
        else:
            st.success(f"✅ Autenticado como: **@{current_user['username']}**")
            st.info(f"📧 Email actual: **{current_user['email']}**")
            
            with st.form("change_email_form", clear_on_submit=False):
                new_email = st.text_input(
                    "Nuevo Email",
                    placeholder="nuevo@email.com",
                    help="Ingresa tu nuevo email"
                )
                
                confirm_new_email = st.text_input(
                    "Confirmar Nuevo Email",
                    placeholder="nuevo@email.com",
                    help="Confirma tu nuevo email"
                )
                
                submitted = st.form_submit_button("📧 Cambiar Email", type="primary", use_container_width=True)
                
                if submitted:
                    if not new_email or not confirm_new_email:
                        st.error("❌ Por favor completa ambos campos")
                    elif new_email != confirm_new_email:
                        st.error("❌ Los emails no coinciden")
                    elif not validate_email(new_email):
                        st.error("❌ Formato de email inválido")
                    elif new_email.lower().strip() == current_user['email'].lower().strip():
                        st.warning("⚠️ Este es tu email actual. No se requiere cambio.")
                    else:
                        # Update email
                        success, message = auth_service.update_email(current_user['id'], new_email)
                        
                        if success:
                            st.success(f"✅ {message}")
                            st.info(f"📧 Tu nuevo email es: **{new_email}**")
                            st.info("🔄 Por favor, inicia sesión nuevamente para actualizar tu sesión")
                            
                            # Clear form by rerunning
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
    
    # Navigation
    st.markdown("---")
    st.markdown("### 🔗 Navegación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("🔐 Iniciar Sesión", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col3:
        if st.button("📝 Crear Cuenta", use_container_width=True):
            st.switch_page("pages/05_Registro.py")

if __name__ == "__main__":
    main()
