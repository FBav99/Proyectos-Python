import io
import json
import textwrap
from datetime import datetime

import streamlit as st
from core.dashboard_repository import (
    delete_dashboard,
    list_user_dashboards,
    upsert_dashboard,
)
from .dashboard_components import create_component_buttons, add_component_to_dashboard

def create_dashboard_sidebar(df, show_component_controls=True):
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
        
        # Ensure base state defaults exist
        st.session_state.setdefault('dashboard_name_input', "Mi Dashboard")
        st.session_state.setdefault('active_dashboard_id', None)
        st.session_state.setdefault('dashboards_cache_dirty', True)

        # Data info with better styling
        st.markdown("""
        <div style="background: rgba(0, 123, 255, 0.1); padding: 1rem; border-radius: 8px; 
                    border-left: 4px solid #007bff; margin-bottom: 1.5rem;">
            <h4 style="color: #007bff; margin: 0 0 0.5rem 0; font-size: 1rem;">📊 Información de Datos</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Filas:</strong> {}</p>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Columnas:</strong> {}</p>
        </div>
        """.format(len(df), len(df.columns)), unsafe_allow_html=True)

        # Saved dashboards management
        user_id = st.session_state.get('auth_user_id')
        saved_dashboards = []
        if user_id:
            if 'cached_user_dashboards' not in st.session_state or st.session_state.get('dashboards_cache_dirty', True):
                st.session_state['cached_user_dashboards'] = list_user_dashboards(user_id)
                st.session_state['dashboards_cache_dirty'] = False
            saved_dashboards = st.session_state.get('cached_user_dashboards', [])

        if saved_dashboards:
            st.markdown("#### 📁 Dashboards guardados")
            options = {"➕ Nuevo dashboard": None}
            for dashboard in saved_dashboards:
                dataset_label = dashboard.get("dataset_info", {}).get("label") or "Dataset no especificado"
                label = f"{dashboard['dashboard_name']} · {_format_timestamp(dashboard.get('updated_at'))} · {dataset_label}"
                options[label] = dashboard

            selection = st.selectbox(
                "Selecciona un dashboard previamente guardado",
                list(options.keys()),
                key="dashboard_saved_selector"
            )
            selected_dashboard = options.get(selection)

            if selected_dashboard:
                col_load, col_delete = st.columns([2, 1])
                with col_load:
                    if st.button("📂 Cargar dashboard", use_container_width=True, key="load_saved_dashboard"):
                        components = selected_dashboard.get('config', {}).get('components', [])
                        st.session_state.dashboard_components = components
                        st.session_state.dashboard_component_counter = len(components)
                        st.session_state.active_dashboard_id = selected_dashboard['id']
                        st.session_state.dashboard_name_input = selected_dashboard['dashboard_name']
                        st.session_state.editing_component = None
                        dataset_label = selected_dashboard.get("dataset_info", {}).get("label")
                        if dataset_label:
                            st.session_state.dashboard_data_label = dataset_label
                            st.info(f"Dashboard cargado. Fuente de datos previamente usada: `{dataset_label}`. Selecciona tu dataset actual para continuar.")
                        else:
                            st.success("Dashboard cargado correctamente desde la base de datos.")
                        st.rerun()
                with col_delete:
                    if st.button("🗑️ Eliminar", use_container_width=True, key="delete_saved_dashboard"):
                        delete_dashboard(selected_dashboard['id'], user_id)
                        st.session_state['dashboards_cache_dirty'] = True
                        st.session_state.active_dashboard_id = None
                        st.success("Dashboard eliminado permanentemente.")
                        st.rerun()

            st.markdown("---")

        st.text_input(
            "📝 Nombre del dashboard",
            value=st.session_state.dashboard_name_input,
            key="dashboard_name_input",
            help="Define el título que verás al guardar o exportar tu dashboard."
        )

        if show_component_controls:
            # Component creation section
            component_type = create_component_buttons()

            # Add component if button was clicked
            if component_type:
                if add_component_to_dashboard(component_type, df):
                    st.rerun()
        
        # Dashboard management section
        st.markdown("---")
        st.markdown("### 🛠️ Gestión del Dashboard")

        dashboard_name_preview = st.session_state.get('dashboard_name_input', 'Mi Dashboard')
        st.caption(f"Guardado como: **{dashboard_name_preview}**")
        
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
                st.session_state.dashboard_component_counter = 0
                st.session_state.active_dashboard_id = None
                st.session_state.dashboard_name_input = "Mi Dashboard"
                st.rerun()
        
        with col2:
            if st.button("📋 Limpiar", use_container_width=True):
                st.session_state.dashboard_components = []
                st.session_state.dashboard_component_counter = 0
                st.session_state.active_dashboard_id = None
                st.session_state.dashboard_name_input = "Mi Dashboard"
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

        with st.expander("🧪 Insights y Analisis Avanzados", expanded=False):
            st.markdown("""
            Estas ideas estarán disponibles en futuras versiones:

            - **SPLY (Same Period Last Year):** compara períodos iguales año contra año para resaltar estacionalidad.
            - **YoY / QoQ / MoM:** analiza variaciones porcentuales entre intervalos consecutivos para encontrar tendencias.
            - **Insights automáticos:** resúmenes en lenguaje natural sobre hallazgos destacados (picos, caídas, outliers).
            - **Alertas inteligentes:** recomendaciones rápidas basadas en reglas configurables o métricas críticas.

            ¿Quieres dar feedback o priorizar alguna? ¡Cuéntanos desde la sección de ayuda! 😊
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
        user_id = st.session_state.get('auth_user_id')
        if not user_id:
            st.warning("Debes iniciar sesión para guardar tu dashboard.")
            return

        components = st.session_state.get('dashboard_components', [])
        if not components:
            st.warning("Agrega al menos un componente antes de guardar.")
            return

        dashboard_name = (st.session_state.get('dashboard_name_input') or "Mi Dashboard").strip() or "Mi Dashboard"
        dashboard_id = st.session_state.get('active_dashboard_id')
        dataset_label = st.session_state.get('dashboard_data_label')
        dataset_info = None
        if dataset_label:
            dataset_info = {
                "label": dataset_label,
                "noted_at": datetime.now().isoformat()
            }

        saved_id = upsert_dashboard(
            user_id=user_id,
            dashboard_name=dashboard_name,
            components=components,
            dashboard_id=dashboard_id,
            is_public=False,
            dataset_info=dataset_info,
        )

        st.session_state['active_dashboard_id'] = saved_id
        st.session_state['dashboards_cache_dirty'] = True
        st.success("✅ Dashboard guardado en la base de datos.")
    except Exception as e:
        st.error(f"❌ Error al guardar dashboard: {e}")

def export_dashboard(format_type):
    """Export dashboard"""
    if not st.session_state.dashboard_components:
        st.warning("No hay componentes para exportar")
        return

    try:
        dashboard_name = (st.session_state.get('dashboard_name_input') or "Mi Dashboard").strip() or "Mi Dashboard"
        components = st.session_state.get('dashboard_components', [])
        summary_lines = _build_component_summary(components, width=95)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        format_upper = format_type.upper()

        if format_upper == "PDF":
            try:
                image_buffer, image_size = _generate_dashboard_image(dashboard_name, summary_lines)
            except ImportError as exc:
                st.error(str(exc))
                return

            try:
                pdf_buffer = _generate_dashboard_pdf(dashboard_name, summary_lines, image_buffer)
            except ImportError as exc:
                st.error(str(exc))
                return

            st.success("✅ PDF generado. Usa los botones para descargar los archivos.")
            st.download_button(
                "⬇️ Descargar PDF",
                pdf_buffer,
                file_name=f"{dashboard_name}_{timestamp}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"dashboard_pdf_{timestamp}"
            )
            image_buffer.seek(0)
            st.download_button(
                "⬇️ Descargar PNG",
                image_buffer,
                file_name=f"{dashboard_name}_{timestamp}.png",
                mime="image/png",
                use_container_width=True,
                key=f"dashboard_png_{timestamp}_from_pdf"
            )
            return

        if format_upper in {"IMAGEN", "IMÁGEN", "PNG"}:
            try:
                image_buffer, _ = _generate_dashboard_image(dashboard_name, summary_lines)
            except ImportError as exc:
                st.error(str(exc))
                return

            st.success("✅ Imagen generada. Usa el botón para descargarla.")
            st.download_button(
                "⬇️ Descargar PNG",
                image_buffer,
                file_name=f"{dashboard_name}_{timestamp}.png",
                mime="image/png",
                use_container_width=True,
                key=f"dashboard_png_{timestamp}"
            )
            return

        st.warning("Formato de exportación no reconocido.")
    except Exception as e:
        st.error(f"❌ Error al exportar dashboard: {e}")

def show_dashboard_info(df, *, show_divider=True, container_class=None):
    """Show dashboard information and statistics"""
    if show_divider:
        st.markdown("---")

    if container_class:
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)

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
            st.metric("📦 Estado", "Vacío")

    if container_class:
        st.markdown("</div>", unsafe_allow_html=True)


def _format_timestamp(value):
    if not value:
        return "sin fecha"
    try:
        return datetime.fromisoformat(str(value)).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(value)


def _build_component_summary(components, width=90):
    lines = []
    for idx, component in enumerate(components, 1):
        title = component.get('title') or component.get('type') or f"Componente {idx}"
        lines.append(f"{idx}. {title} ({component.get('type', 'tipo desconocido')})")
        config = component.get('config', {})
        for key, value in config.items():
            if key == "title":
                continue
            formatted_value = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
            wrapped_lines = textwrap.wrap(formatted_value, width=width)
            if not wrapped_lines:
                continue
            lines.append(f"   - {key}: {wrapped_lines[0]}")
            for continuation in wrapped_lines[1:]:
                lines.append(f"     {continuation}")
        lines.append("")
    return lines or ["Sin componentes disponibles."]


def _generate_dashboard_image(dashboard_name, summary_lines):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise ImportError("Pillow no está instalado. Instala con `pip install pillow` para exportar como imagen.") from exc

    padding = 48
    content_width = 1104
    image_width = content_width + padding * 2

    # Load fonts (fallback to default)
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
        body_font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    line_height = body_font.getbbox("Ag")[3] - body_font.getbbox("Ag")[1] + 4
    subtitle_height = subtitle_font.getbbox("Ag")[3] - subtitle_font.getbbox("Ag")[1]
    title_height = title_font.getbbox("Ag")[3] - title_font.getbbox("Ag")[1]

    content_height = padding + title_height + 8 + subtitle_height + 20 + len(summary_lines) * line_height + padding
    image_height = max(content_height, 400)

    image = Image.new("RGB", (image_width, image_height), color="white")
    draw = ImageDraw.Draw(image)

    now_str = datetime.now().strftime('%d/%m/%Y %H:%M')
    draw.text((padding, padding), f"Dashboard: {dashboard_name}", fill="black", font=title_font)
    draw.text((padding, padding + title_height + 8), f"Generado: {now_str}", fill="#555555", font=subtitle_font)

    y_cursor = padding + title_height + subtitle_height + 24
    for line in summary_lines:
        draw.text((padding, y_cursor), line, fill="black", font=body_font)
        y_cursor += line_height

    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer, image.size


def _generate_dashboard_pdf(dashboard_name, summary_lines, image_buffer):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise ImportError("Reportlab no está instalado. Instala con `pip install reportlab` para exportar a PDF.") from exc

    page_width, page_height = letter
    margin = 0.75 * inch
    now_str = datetime.now().strftime('%d/%m/%Y %H:%M')

    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    text_object = pdf.beginText()
    text_object.setTextOrigin(margin, page_height - margin)
    text_object.setFont("Helvetica-Bold", 16)
    text_object.textLine(f"Dashboard: {dashboard_name}")
    text_object.setFont("Helvetica", 11)
    text_object.textLine(f"Generado: {now_str}")
    pdf.drawText(text_object)

    image_buffer.seek(0)
    image_reader = ImageReader(image_buffer)
    img_width, img_height = image_reader.getSize()

    available_width = page_width - 2 * margin
    scale = min(available_width / img_width, 1.0)
    draw_width = img_width * scale
    draw_height = img_height * scale
    image_x = (page_width - draw_width) / 2
    image_y = text_object.getY() - draw_height - 0.5 * inch

    if image_y < margin:
        pdf.showPage()
        image_y = page_height - margin - draw_height

    pdf.drawImage(
        image_reader,
        image_x,
        image_y,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask='auto'
    )

    pdf.showPage()
    text_object = pdf.beginText()
    text_object.setTextOrigin(margin, page_height - margin)
    text_object.setFont("Helvetica-Bold", 12)
    text_object.textLine("Resumen de componentes")
    text_object.setFont("Helvetica", 10)

    for line in summary_lines:
        if text_object.getY() <= margin:
            pdf.drawText(text_object)
            pdf.showPage()
            text_object = pdf.beginText()
            text_object.setTextOrigin(margin, page_height - margin)
            text_object.setFont("Helvetica", 10)
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer
