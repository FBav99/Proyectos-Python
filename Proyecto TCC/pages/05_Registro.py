import streamlit as st
import re
from core.auth_service import auth_service
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

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

@safe_main
def main():
    """Página de registro de usuarios"""
    st.set_page_config(
        page_title="Registro - Crear Cuenta",
        page_icon="📝",
        layout="wide"
    )
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">📝 Registro de Usuario</h1>
        <p style="color: white; font-size: 1.1rem;">Crea tu cuenta para acceder al sistema de análisis de datos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create registration form
    st.markdown("### 🔐 Crear Nueva Cuenta")
    
    # Password requirements tooltip text
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
                st.success(f"✅ {message}")
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
            validation_messages.append("❌ Formato de email inválido")
        
        # Username validation
        if username:
            if len(username) < 3:
                validation_messages.append("❌ El nombre de usuario debe tener al menos 3 caracteres")
            elif not username.isalnum():
                validation_messages.append("❌ El nombre de usuario solo puede contener letras y números")
        
        # Show validation messages if any
        if validation_messages:
            for msg in validation_messages:
                st.warning(msg)
        
        submitted = st.form_submit_button("📝 Registrarse", type="primary", use_container_width=True)
        
        if submitted:
            # Validate all fields
            if not all([first_name, last_name, email, username, password, confirm_password]):
                st.error("❌ Todos los campos son obligatorios")
                return
            
            if not validate_email(email):
                st.error("❌ Formato de email inválido")
                return
            
            is_valid, message = validate_password(password)
            if not is_valid:
                st.error(f"❌ {message}")
                return
            
            if password != confirm_password:
                st.error("❌ Las contraseñas no coinciden")
                return
            
            if len(username) < 3:
                st.error("❌ El nombre de usuario debe tener al menos 3 caracteres")
                return
            
            if not username.isalnum():
                st.error("❌ El nombre de usuario solo puede contener letras y números")
                return
            
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
                    st.success('✅ Usuario registrado exitosamente!')
                    st.info(f'📧 Email: {email}')
                    st.info(f'👤 Usuario: {username}')
                    st.info(f'👨‍💼 Nombre: {first_name} {last_name}')
                    
                    st.markdown("---")
                    st.markdown("### 🎉 ¡Registro Completado!")
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
                            st.switch_page("Inicio.py")
                else:
                    st.error(f'❌ Error durante el registro: {message}')
                    # Don't clear form on error - data is preserved
                    
            except Exception as e:
                st.error(f'❌ Error durante el registro: {str(e)}')
                # The error is already sanitized by auth_service
    
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
