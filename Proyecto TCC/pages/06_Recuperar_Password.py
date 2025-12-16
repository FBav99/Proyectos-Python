# Nombre del Archivo: 06_Recuperar_Password.py
# Descripción: Página para recuperar contraseña de usuario
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
from core.auth_service import auth_service
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling
from core.database import db_manager
from utils.ui import auth_ui
import re

from utils.ui.icon_system import get_icon, replace_emojis
# Importacion - Importar init_sidebar usando importación de módulo para mejor compatibilidad
init_sidebar = auth_ui.init_sidebar

# Configuracion - Configurar manejo de errores a nivel de módulo
configure_streamlit_error_handling()

# Inicializacion - Asegurar que la base de datos esté inicializada antes de usarla
from core.database import ensure_database_initialized
try:
    ensure_database_initialized()
except Exception as e:
    # Manejo de Errores - Se mostrará cuando la página cargue
    pass

# Validacion - Formato de Email
def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Validacion - Fortaleza de Contraseña
def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, "Contraseña válida"

# Principal - Recuperacion de Contraseña
@safe_main
def main():
    """Página de recuperación de contraseña con verificación de email y cambio de email"""
    st.set_page_config(
        page_title="Recuperar Contraseña",
        page_icon="🔑",
        layout="wide"
    )
    
    # UI - Inicializar Sidebar con Info de Usuario
    init_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🔑 Recuperar Contraseña</h1>
        <p style="color: white; font-size: 1.1rem;">Recupera tu contraseña o actualiza tu email y contraseña de forma segura</p>
    </div>
    """, unsafe_allow_html=True)
    
    # UI - Seleccion de Tabs para Opciones de Recuperacion
    tab1, tab2, tab3 = st.tabs(["🔑 Recuperar Contraseña", "📧 Cambiar Email", replace_emojis("🔐 Cambiar Contraseña")])
    
    with tab1:
        st.markdown(replace_emojis("### 🔐 Recuperar Contraseña"), unsafe_allow_html=True)
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
                    st.session_state.recovery_error = replace_emojis("❌ Por favor ingresa tu nombre de usuario")
                    st.rerun()
                else:
                    # Check if user exists and get email
                    username_sanitized = username.strip()
                    with db_manager.get_connection() as conn:
                        active_literal = db_manager.get_boolean_literal(True)
                        cursor = conn.execute(f"""
                            SELECT id, username, email, first_name, last_name 
                            FROM users 
                            WHERE username = ? AND is_active = {active_literal}
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
                        st.session_state.recovery_error = replace_emojis('❌ Usuario no encontrado o cuenta inactiva')
                        st.rerun()
        
        # Email verification step (2FA-like)
        if st.session_state.get('recovery_step') == 'verify_email' and st.session_state.get('recovery_user'):
            user_info = st.session_state.recovery_user
            st.markdown("---")
            st.markdown(replace_emojis("### 🔒 Verificación de Seguridad"), unsafe_allow_html=True)
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
                
                verify_submitted = st.form_submit_button(replace_emojis("✅ Verificar y Recuperar"), type="primary", use_container_width=True)
                
                if verify_submitted:
                    if not verification_email:
                        st.markdown(replace_emojis("❌ Por favor ingresa tu email"), unsafe_allow_html=True)
                    elif verification_email.lower().strip() != user_info['email'].lower().strip():
                        st.markdown(replace_emojis("❌ El email no coincide con el registrado. Por favor verifica e intenta nuevamente."), unsafe_allow_html=True)
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
                            st.markdown(replace_emojis("❌ Error al generar la nueva contraseña"), unsafe_allow_html=True)
        
        # Show success message
        if st.session_state.get('recovery_success', False):
            recovery_data = st.session_state.get('recovery_data', {})
            st.markdown("---")
            st.markdown(replace_emojis('✅ Nueva contraseña generada exitosamente!'), unsafe_allow_html=True)
            st.markdown(f'{get_icon("👤", 20)} Usuario: {recovery_data.get("username", "")}', unsafe_allow_html=True)
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
            st.markdown(f"{get_icon('✅', 20)} Autenticado como: **@{current_user['username']}**", unsafe_allow_html=True)
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
                        st.markdown(replace_emojis("❌ Por favor completa ambos campos"), unsafe_allow_html=True)
                    elif new_email != confirm_new_email:
                        st.markdown(replace_emojis("❌ Los emails no coinciden"), unsafe_allow_html=True)
                    elif not validate_email(new_email):
                        st.markdown(replace_emojis("❌ Formato de email inválido"), unsafe_allow_html=True)
                    elif new_email.lower().strip() == current_user['email'].lower().strip():
                        st.warning("⚠️ Este es tu email actual. No se requiere cambio.")
                    else:
                        # Update email
                        success, message = auth_service.update_email(current_user['id'], new_email)
                        
                        if success:
                            st.markdown(f"{get_icon("✅", 20)} {message}", unsafe_allow_html=True)
                            st.info(f"📧 Tu nuevo email es: **{new_email}**")
                            st.markdown(replace_emojis("🔄 Por favor, inicia sesión nuevamente para actualizar tu sesión"), unsafe_allow_html=True)
                            
                            # Clear form by rerunning
                            st.rerun()
                        else:
                            st.markdown(f"{get_icon("❌", 20)} {message}", unsafe_allow_html=True)
    
    with tab3:
        st.markdown(replace_emojis("### 🔐 Cambiar Contraseña"), unsafe_allow_html=True)
        st.info("""
        **Para cambiar tu contraseña:**
        1. Debes estar autenticado (iniciar sesión primero)
        2. Ingresa tu contraseña actual
        3. Ingresa y confirma tu nueva contraseña
        4. Confirma el cambio
        """)
        
        # Check if user is authenticated
        from core.auth_service import get_current_user
        current_user = get_current_user()
        
        if not current_user:
            st.warning("⚠️ Debes iniciar sesión para cambiar tu contraseña")
            if st.button("🔐 Ir a Iniciar Sesión", type="primary", use_container_width=True):
                st.switch_page("Inicio.py")
        else:
            st.markdown(f"{get_icon('✅', 20)} Autenticado como: **@{current_user['username']}**", unsafe_allow_html=True)
            
            # Password requirements help text
            password_help = "La contraseña debe tener: mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
            
            with st.form("change_password_form", clear_on_submit=False):
                current_password = st.text_input(
                    "Contraseña Actual",
                    type="password",
                    placeholder="••••••••",
                    help="Ingresa tu contraseña actual"
                )
                
                new_password = st.text_input(
                    "Nueva Contraseña",
                    type="password",
                    placeholder="••••••••",
                    help=password_help
                )
                
                confirm_new_password = st.text_input(
                    "Confirmar Nueva Contraseña",
                    type="password",
                    placeholder="••••••••",
                    help="Confirma tu nueva contraseña"
                )
                
                # Password strength indicator
                if new_password:
                    is_valid, message = validate_password(new_password)
                    if is_valid:
                        st.markdown(f"{get_icon("✅", 20)} {message}", unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ {message}")
                        st.info("""
                        **Requisitos de contraseña:**
                        - Mínimo 8 caracteres
                        - Al menos una letra mayúscula (A-Z)
                        - Al menos una letra minúscula (a-z)
                        - Al menos un número (0-9)
                        """)
                
                submitted = st.form_submit_button(replace_emojis("🔐 Cambiar Contraseña"), type="primary", use_container_width=True)
                
                if submitted:
                    if not current_password or not new_password or not confirm_new_password:
                        st.markdown(replace_emojis("❌ Por favor completa todos los campos"), unsafe_allow_html=True)
                    elif new_password != confirm_new_password:
                        st.markdown(replace_emojis("❌ Las contraseñas nuevas no coinciden"), unsafe_allow_html=True)
                    else:
                        # Validate password strength
                        is_valid, message = validate_password(new_password)
                        if not is_valid:
                            st.markdown(f"{get_icon("❌", 20)} {message}", unsafe_allow_html=True)
                        else:
                            # Update password
                            success, message = auth_service.update_password(
                                current_user['id'],
                                current_password,
                                new_password
                            )
                            
                            if success:
                                st.markdown(f"{get_icon("✅", 20)} {message}", unsafe_allow_html=True)
                                st.markdown(replace_emojis("🔄 Por favor, inicia sesión nuevamente con tu nueva contraseña"), unsafe_allow_html=True)
                                
                                # Clear form by rerunning
                                st.rerun()
                            else:
                                st.markdown(f"{get_icon("❌", 20)} {message}", unsafe_allow_html=True)
    
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
