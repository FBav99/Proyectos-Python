import streamlit as st
from core.auth_service import auth_service

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
    
    # Create password recovery form
    st.markdown("### 🔐 Recuperar Contraseña")
    
    # Password recovery form
    with st.form("password_recovery_form", clear_on_submit=True):
        username = st.text_input(
            "Nombre de Usuario",
            placeholder="Ingresa tu nombre de usuario",
            help="Ingresa el nombre de usuario de tu cuenta"
        )
        
        submitted = st.form_submit_button("🔑 Recuperar Contraseña", type="primary", use_container_width=True)
        
        if submitted:
            if not username:
                st.error("❌ Por favor ingresa tu nombre de usuario")
            else:
                # Use database auth service for password recovery
                success, recovered_username, email, new_password = auth_service.forgot_password(username)
                
                if success and recovered_username:
                    st.success('✅ Nueva contraseña generada exitosamente!')
                    st.info(f'👤 Usuario: {recovered_username}')
                    st.info(f'📧 Email: {email}')
                    st.warning(f'🔑 Nueva contraseña: **{new_password}**')
                    
                    st.markdown("""
                    ### ⚠️ Importante:
                    - **Guarda esta contraseña en un lugar seguro**
                    - **Cámbiala después de iniciar sesión**
                    - **Esta contraseña es temporal**
                    - **Los cambios se guardan permanentemente en la base de datos**
                    """)
                    
                    st.markdown("---")
                    st.markdown("### 🎉 ¡Contraseña Recuperada!")
                    st.markdown("""
                    Tu nueva contraseña ha sido generada y guardada en la base de datos. Ahora puedes:
                    
                    - 🔐 **Iniciar sesión** con tu usuario y la nueva contraseña
                    - 🔒 **Cambiar la contraseña** desde tu perfil después de iniciar sesión
                    - 📚 **Continuar con tu aprendizaje**
                    """)
                    
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        if st.button("🏠 Ir al Inicio", type="primary", use_container_width=True):
                            st.switch_page("Inicio.py")
                else:
                    st.error('❌ Usuario no encontrado')
                    st.info("Verifica que el nombre de usuario sea correcto y que tu cuenta esté activa")
    
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
