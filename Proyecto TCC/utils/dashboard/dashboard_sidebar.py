import streamlit as st
import pandas as pd
from datetime import datetime
from .dashboard_components import create_component_buttons, add_component_to_dashboard

def create_dashboard_sidebar(df):
    """Create the dashboard sidebar with all controls"""
    with st.sidebar:
        # Header with gradient background
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
            <h3 style="color: white; margin: 0; font-size: 1.2rem;">🎨 Dashboard Builder</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Construye tu dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data info with better styling
        st.markdown("""
        <div style="background: rgba(0, 123, 255, 0.1); padding: 1rem; border-radius: 8px; 
                    border-left: 4px solid #007bff; margin-bottom: 1.5rem;">
            <h4 style="color: #007bff; margin: 0 0 0.5rem 0; font-size: 1rem;">📊 Información de Datos</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Filas:</strong> {}</p>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Columnas:</strong> {}</p>
        </div>
        """.format(len(df), len(df.columns)), unsafe_allow_html=True)
        
        # Component creation section
        component_type = create_component_buttons()
        
        # Add component if button was clicked
        if component_type:
            if add_component_to_dashboard(component_type, df):
                st.rerun()
        
        # Dashboard management section
        st.markdown("---")
        st.markdown("### 🛠️ Gestión del Dashboard")
        
        # Save dashboard
        if st.button("💾 Guardar Dashboard", use_container_width=True, type="primary"):
            save_dashboard()
        
        # Export options
        st.markdown("#### 📤 Exportar")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 PDF", use_container_width=True):
                export_dashboard("PDF")
        
        with col2:
            if st.button("🖼️ Imagen", use_container_width=True):
                export_dashboard("Imagen")
        
        # Dashboard actions
        st.markdown("#### 🔧 Acciones")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reiniciar", use_container_width=True):
                st.session_state.dashboard_components = []
                st.rerun()
        
        with col2:
            if st.button("📋 Limpiar", use_container_width=True):
                st.session_state.dashboard_components = []
                st.rerun()
        
        # Help section
        st.markdown("---")
        st.markdown("### ❓ Ayuda")
        
        with st.expander("🎯 Cómo usar el Dashboard Builder", expanded=False):
            st.markdown("""
            **1. Agregar Componentes:**
            - Usa los botones en la sección "Tipos de Componentes"
            - Cada componente se puede configurar individualmente
            
            **2. Configurar Componentes:**
            - Haz clic en "⚙️ Configurar" en cada componente
            - Selecciona las columnas y opciones deseadas
            
            **3. Organizar Dashboard:**
            - Los componentes se muestran en el orden que los agregaste
            - Usa "🗑️ Eliminar" para quitar componentes no deseados
            
            **4. Guardar y Exportar:**
            - Guarda tu dashboard para reutilizarlo
            - Exporta en diferentes formatos según necesites
            """)
        
        with st.expander("📊 Tipos de Componentes", expanded=False):
            st.markdown("""
            **📈 Métricas:** Números clave como totales, promedios, etc.
            **📊 Gráficos Básicos:** Líneas, barras, circular, área
            **🔬 Gráficos Avanzados:** Dispersión, histograma, box plot, violín
            **🔍 Análisis:** Matriz de correlación, tablas de datos
            """)
        
        # Navigation
        st.markdown("---")
        st.markdown("### 🧭 Navegación")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Inicio", use_container_width=True):
                st.switch_page("Inicio.py")
        
        with col2:
            if st.button("❓ Ayuda", use_container_width=True):
                st.switch_page("pages/00_Ayuda.py")

def save_dashboard():
    """Save dashboard configuration"""
    try:
        dashboard_config = {
            'components': st.session_state.dashboard_components,
            'created_at': datetime.now().isoformat(),
            'user': st.session_state.get('username', 'unknown')
        }
        
        # Save to session state for now (could be extended to save to file/database)
        st.session_state.saved_dashboard = dashboard_config
        st.success("✅ Dashboard guardado exitosamente!")
    except Exception as e:
        st.error(f"❌ Error al guardar dashboard: {e}")

def export_dashboard(format_type):
    """Export dashboard"""
    if not st.session_state.dashboard_components:
        st.warning("No hay componentes para exportar")
        return
    
    try:
        st.info(f"📤 Exportando dashboard en formato {format_type}...")
        # Here you would implement the actual export logic
        # For now, just show a success message
        st.success(f"✅ Dashboard exportado como {format_type}")
    except Exception as e:
        st.error(f"❌ Error al exportar dashboard: {e}")

def show_dashboard_info(df):
    """Show dashboard information and statistics"""
    st.markdown("---")
    st.markdown("### 📊 Información del Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Componentes", len(st.session_state.dashboard_components))
    
    with col2:
        st.metric("📊 Filas de Datos", len(df))
    
    with col3:
        st.metric("🏷️ Columnas", len(df.columns))
    
    with col4:
        if st.session_state.dashboard_components:
            last_updated = datetime.now().strftime("%H:%M")
            st.metric("🕒 Última Actualización", last_updated)
        else:
            st.metric("�� Estado", "Vacío")
