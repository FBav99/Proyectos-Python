import streamlit as st
import re
from core.auth_service import auth_service, login_user
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

from utils.ui.icon_system import get_icon, replace_emojis
# Import init_sidebar - using absolute import path
from utils.ui import auth_ui
init_sidebar = auth_ui.init_sidebar

# Configure error handling
configure_streamlit_error_handling()

# Ensure database is initialized before using it
from core.database import ensure_database_initialized
try:
    ensure_database_initialized()
except Exception as e:
    st.error(f"Error initializing database: {e}")
    st.stop()

# Validacion - Formato de Email
def validate_email(email):
    """Validate email format"""
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

# Principal - Registro de Usuarios
@safe_main
def main():
    """Página de registro de usuarios"""
    st.set_page_config(
        page_title="Registro - Crear Cuenta",
        page_icon=get_icon("📝", 20),
        layout="wide"
    )
    
    # UI - Inicializar Sidebar con Info de Usuario
    init_sidebar()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">{get_icon("📝", 28)} Registro de Usuario</h1>
        <p style="color: white; font-size: 1.1rem;">Crea tu cuenta para acceder al sistema de análisis de datos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # UI - Crear Formulario de Registro
    st.markdown(replace_emojis("### 🔐 Crear Nueva Cuenta"), unsafe_allow_html=True)
    
    # UI - Texto de Ayuda para Requisitos de Contraseña
    password_help = "La contraseña debe tener: mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número"
    
    with st.form("registration_form", clear_on_submit=False):
        # First row: Name fields (left to right)
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Nombre", placeholder="Tu nombre", key="first_name")
        with col2:
            last_name = st.text_input("Apellido", placeholder="Tu apellido", key="last_name")
        
        # Second row: Email and Username (left to right)
        col3, col4 = st.columns(2)
        with col3:
            email = st.text_input("Correo Electrónico", placeholder="tu@email.com", key="email")
        with col4:
            username = st.text_input("Nombre de Usuario", placeholder="usuario123", key="username")
        
        # Third row: Password fields (left to right)
        col5, col6 = st.columns(2)
        with col5:
            password = st.text_input(
                "Contraseña", 
                type="password", 
                placeholder="••••••••",
                help=password_help,
                key="password"
            )
        with col6:
            confirm_password = st.text_input(
                "Confirmar Contraseña", 
                type="password", 
                placeholder="••••••••",
                key="confirm_password"
            )
        
        # Password strength indicator (outside columns, doesn't reset)
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.markdown(f"{get_icon('✅', 20)} {message}", unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ {message}")
                # Show detailed requirements
                st.info("""
                **Requisitos de contraseña:**
                - Mínimo 8 caracteres
                - Al menos una letra mayúscula (A-Z)
                - Al menos una letra minúscula (a-z)
                - Al menos un número (0-9)
                """)
        
        # Real-time validation messages (shown below form, don't reset)
        validation_messages = []
        
        # Email validation
        if email and not validate_email(email):
            validation_messages.append(replace_emojis("❌ Formato de email inválido"))
        
        # Username validation
        if username:
            if len(username) < 3:
                validation_messages.append(replace_emojis("❌ El nombre de usuario debe tener al menos 3 caracteres"))
            elif not username.isalnum():
                validation_messages.append(replace_emojis("❌ El nombre de usuario solo puede contener letras y números"))
        
        # Show validation messages if any
        if validation_messages:
            for msg in validation_messages:
                st.warning(msg)
        
        submitted = st.form_submit_button("📝 Registrarse", type="primary", use_container_width=True)
        
        if submitted:
            # Validate all fields
            validation_error = None
            
            if not all([first_name, last_name, email, username, password, confirm_password]):
                validation_error = replace_emojis("❌ Todos los campos son obligatorios")
            elif not validate_email(email):
                validation_error = replace_emojis("❌ Formato de email inválido")
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    validation_error = f"{get_icon("❌", 20)} {message}"
                elif password != confirm_password:
                    validation_error = replace_emojis("❌ Las contraseñas no coinciden")
                elif len(username) < 3:
                    validation_error = replace_emojis("❌ El nombre de usuario debe tener al menos 3 caracteres")
                elif not username.isalnum():
                    validation_error = replace_emojis("❌ El nombre de usuario solo puede contener letras y números")
            
            if validation_error:
                # Store error in session state to show outside form
                st.session_state.registration_error = validation_error
                st.rerun()
            else:
                # Attempt registration
                try:
                    success, message = auth_service.register_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    if success:
                        login_success, login_message = login_user(username, password)
                        if login_success:
                            st.session_state.pop('registration_error', None)
                            st.session_state.pop('registration_success', None)
                            st.session_state.registration_welcome = {
                                'username': username,
                                'first_name': first_name
                            }
                            st.switch_page("Inicio.py")
                        else:
                            st.session_state.registration_success = True
                            st.session_state.registered_user = {
                                'email': email,
                                'username': username,
                                'first_name': first_name,
                                'last_name': last_name
                            }
                            st.session_state.registration_error = f'{get_icon("❌", 20)} Registro exitoso pero el inicio de sesión automático falló: {login_message}'
                            st.rerun()
                    else:
                        st.session_state.registration_error = f'{get_icon("❌", 20)} Error durante el registro: {message}'
                        st.rerun()
                        
                except Exception as e:
                    st.session_state.registration_error = f'{get_icon("❌", 20)} Error durante el registro: {str(e)}'
                    st.rerun()
    
    # UI - Mostrar Mensajes de Error fuera del Formulario
    if 'registration_error' in st.session_state and st.session_state.registration_error:
        st.error(st.session_state.registration_error)
        # Clear error after showing
        del st.session_state.registration_error
    
    # UI - Mostrar Mensaje de Exito fuera del Formulario
    if st.session_state.get('registration_success', False):
        user_info = st.session_state.get('registered_user', {})
        st.markdown(replace_emojis('✅ Usuario registrado exitosamente!'), unsafe_allow_html=True)
        st.info(f'📧 Email: {user_info.get("email", "")}')
        st.markdown(f'{get_icon("👤", 20)} Usuario: {user_info.get("username", "")}', unsafe_allow_html=True)
        st.info(f'👨‍💼 Nombre: {user_info.get("first_name", "")} {user_info.get("last_name", "")}')
        
        st.markdown("---")
        st.markdown(replace_emojis("### 🎉 ¡Registro Completado!"), unsafe_allow_html=True)
        st.markdown("""
        Tu cuenta ha sido creada exitosamente. Ahora puedes:
        
        - 🔐 **Iniciar sesión** con tu nuevo usuario y contraseña
        - 📚 **Acceder a todos los niveles** de aprendizaje
        - 📊 **Crear dashboards** personalizados
        - 💾 **Guardar tu progreso** automáticamente
        """)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🏠 Ir al Inicio", type="primary", use_container_width=True):
                # Clear registration success state
                if 'registration_success' in st.session_state:
                    del st.session_state.registration_success
                if 'registered_user' in st.session_state:
                    del st.session_state.registered_user
                st.switch_page("Inicio.py")
    
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
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

if __name__ == "__main__":
    main()
