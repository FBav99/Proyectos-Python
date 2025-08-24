import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os
from core.auth_config import init_authentication, load_auth_config

def main():
    """Página de recuperación de contraseña"""
    st.set_page_config(
        page_title="Recuperar Contraseña",
        page_icon="🔑",
        layout="wide"
    )
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 1rem;">🔑 Recuperar Contraseña</h1>
        <p style="color: white; font-size: 1.1rem;">Ingresa tu nombre de usuario para generar una nueva contraseña</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize authentication
    authenticator = init_authentication()
    
    # Create password recovery form
    st.markdown("### 🔐 Recuperar Contraseña")
    
    try:
        # Use the forgot_password method from Streamlit-Authenticator
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(
            location='main',
            fields={
                'Form name': 'Recuperar Contraseña',
                'Username': 'Nombre de Usuario',
                'Captcha': 'Captcha',
                'Submit': 'Recuperar Contraseña'
            },
            captcha=True,  # Enable CAPTCHA for security
            clear_on_submit=True
        )
        
        if username_of_forgotten_password:
            st.success('✅ Nueva contraseña generada exitosamente!')
            st.info(f'👤 Usuario: {username_of_forgotten_password}')
            st.info(f'📧 Email: {email_of_forgotten_password}')
            st.warning(f'🔑 Nueva contraseña: {new_random_password}')
            
            st.markdown("""
            ### ⚠️ Importante:
            - **Guarda esta contraseña en un lugar seguro**
            - **Cámbiala después de iniciar sesión**
            - **Esta contraseña es temporal**
            """)
            
            # Update the config file
            config = load_auth_config()
            with open('config/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            
            st.markdown("---")
            st.markdown("### 🎉 ¡Contraseña Recuperada!")
            st.markdown("""
            Tu nueva contraseña ha sido generada. Ahora puedes:
            
            - 🔐 **Iniciar sesión** con tu usuario y la nueva contraseña
            - 🔒 **Cambiar la contraseña** desde tu perfil
            - 📚 **Continuar con tu aprendizaje**
            """)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("🏠 Ir al Inicio", type="primary", use_container_width=True):
                    st.switch_page("Inicio.py")
                    
        elif username_of_forgotten_password == False:
            st.error('❌ Usuario no encontrado')
            st.info("Verifica que el nombre de usuario sea correcto")
                    
    except Exception as e:
        st.error(f'❌ Error durante la recuperación: {str(e)}')
    
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
