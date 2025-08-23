import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os
from core.auth_config import init_authentication, load_auth_config

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
    
    # Initialize authentication
    authenticator = init_authentication()
    
    # Create registration form
    st.markdown("### 🔐 Crear Nueva Cuenta")
    
    try:
        # Use the register_user method from Streamlit-Authenticator
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            location='main',
            fields={
                'Form name': 'Registro de Usuario',
                'First name': 'Nombre',
                'Last name': 'Apellido',
                'Email': 'Correo Electrónico',
                'Username': 'Nombre de Usuario',
                'Password': 'Contraseña',
                'Repeat password': 'Repetir Contraseña',
                'Register': 'Registrarse'
            },
            captcha=True,  # Enable CAPTCHA for security
            clear_on_submit=True
        )
        
        if email_of_registered_user:
            st.success('✅ Usuario registrado exitosamente!')
            st.info(f'📧 Email: {email_of_registered_user}')
            st.info(f'👤 Usuario: {username_of_registered_user}')
            st.info(f'👨‍💼 Nombre: {name_of_registered_user}')
            
            # Update the config file
            config = load_auth_config()
            with open('config/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            
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
                    
    except Exception as e:
        st.error(f'❌ Error durante el registro: {str(e)}')
    
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
