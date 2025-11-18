import io
import json
import textwrap
from datetime import datetime

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from core.dashboard_repository import (
    delete_dashboard,
    list_user_dashboards,
    upsert_dashboard,
)
from utils.ui.icon_system import get_icon, replace_emojis
from .dashboard_components import create_component_buttons, add_component_to_dashboard

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None

def _get_active_dataframe():
    """Return the DataFrame currently used in the dashboard context."""
    for key in ("cleaned_data", "uploaded_data", "sample_data"):
        df = st.session_state.get(key)
        if df is not None:
            return df
    return None

def create_dashboard_sidebar(df, show_component_controls=True):
    """Create the dashboard sidebar with all controls"""
    with st.sidebar:
        # Header with gradient background
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
            <h3 style="color: white; margin: 0; font-size: 1.2rem;">{get_icon("🎨", 20)} Dashboard Builder</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Construye tu dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ensure base state defaults exist
        st.session_state.setdefault('dashboard_name_input', "Mi Dashboard")
        st.session_state.setdefault('active_dashboard_id', None)
        st.session_state.setdefault('dashboards_cache_dirty', True)

        # Data info with better styling
        st.markdown(f"""
        <div style="background: rgba(0, 123, 255, 0.1); padding: 1rem; border-radius: 8px; 
                    border-left: 4px solid #007bff; margin-bottom: 1.5rem;">
            <h4 style="color: #007bff; margin: 0 0 0.5rem 0; font-size: 1rem;">{get_icon("📊", 18)} Información de Datos</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Filas:</strong> {len(df)}</p>
            <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>Columnas:</strong> {len(df.columns)}</p>
        </div>
        """, unsafe_allow_html=True)

        # Saved dashboards management
        user_id = st.session_state.get('auth_user_id')
        saved_dashboards = []
        if user_id:
            if 'cached_user_dashboards' not in st.session_state or st.session_state.get('dashboards_cache_dirty', True):
                st.session_state['cached_user_dashboards'] = list_user_dashboards(user_id)
                st.session_state['dashboards_cache_dirty'] = False
            saved_dashboards = st.session_state.get('cached_user_dashboards', [])

        if saved_dashboards:
            st.markdown(replace_emojis("#### 📁 Dashboards guardados"), unsafe_allow_html=True)
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
            replace_emojis("📝 Nombre del dashboard"),
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
        st.markdown(replace_emojis("#### 📤 Exportar"), unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 PDF", use_container_width=True):
                export_dashboard("PDF")
        
        with col2:
            if st.button("🖼️ Imagen", use_container_width=True):
                export_dashboard("Imagen")
        
        # Dashboard actions
        st.markdown(replace_emojis("#### 🔧 Acciones"), unsafe_allow_html=True)
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
        
        with st.expander(replace_emojis("🎯 Cómo usar el Dashboard Builder"), expanded=False):
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
        
        with st.expander(replace_emojis("📊 Tipos de Componentes"), expanded=False):
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
        st.markdown(replace_emojis("✅ Dashboard guardado en la base de datos."), unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error al guardar dashboard: {e}", unsafe_allow_html=True)

def export_dashboard(format_type):
    """Export dashboard"""
    if not st.session_state.dashboard_components:
        st.warning("No hay componentes para exportar")
        return

    try:
        dashboard_name = (st.session_state.get('dashboard_name_input') or "Mi Dashboard").strip() or "Mi Dashboard"
        components = st.session_state.get('dashboard_components', [])
        summary_lines = _build_component_summary(components, width=95)
        df = _get_active_dataframe()
        if df is None:
            st.warning("No hay datos activos para exportar el dashboard. Carga un dataset antes de exportar.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        format_upper = format_type.upper()

        if format_upper == "PDF":
            try:
                image_buffer, image_size = _generate_dashboard_image(dashboard_name, components, df)
            except ImportError as exc:
                st.error(str(exc))
                return

            try:
                pdf_buffer = _generate_dashboard_pdf(dashboard_name, summary_lines, image_buffer)
            except ImportError as exc:
                st.error(str(exc))
                return

            st.markdown(replace_emojis("✅ PDF generado. Usa los botones para descargar los archivos."), unsafe_allow_html=True)
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
                image_buffer, _ = _generate_dashboard_image(dashboard_name, components, df)
            except ImportError as exc:
                st.error(str(exc))
                return

            st.markdown(replace_emojis("✅ Imagen generada. Usa el botón para descargarla."), unsafe_allow_html=True)
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
        st.markdown(f"{get_icon("❌", 20)} Error al exportar dashboard: {e}", unsafe_allow_html=True)

def show_dashboard_info(df, *, show_divider=True, container_class=None):
    """Show dashboard information and statistics"""
    if show_divider:
        st.markdown("---")

    if container_class:
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)

    st.markdown(replace_emojis("### 📊 Información del Dashboard"), unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(replace_emojis("📋 Componentes"), len(st.session_state.dashboard_components))
    
    with col2:
        st.metric(replace_emojis("📊 Filas de Datos"), len(df))
    
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


def _prepare_layout_rows(components):
    """Return components grouped and ordered by layout row."""
    layout_rows = {}
    fallback_row_base = 1000

    for idx, component in enumerate(components):
        layout = component.get('layout') or {}
        row_key = layout.get('row')
        if row_key is None:
            row_key = fallback_row_base + idx
        order = layout.get('order', idx)
        col_span = layout.get('col_span', layout.get('width', 12))
        col_span = max(1, col_span)
        layout_rows.setdefault(row_key, []).append({
            'order': order,
            'col_span': col_span,
            'component': component
        })

    return [(row_key, sorted(items, key=lambda item: item['order'])) for row_key, items in sorted(layout_rows.items())]


def _calculate_metric_value(config, df, component_title):
    metric_type = config.get('metric_type', 'count')
    column = config.get('column')
    label = component_title or "Métrica"

    try:
        if metric_type == 'count':
            value = len(df)
            label = label or "Total de registros"
        elif metric_type in ['sum', 'mean', 'median', 'min', 'max']:
            if not column:
                raise ValueError("Selecciona una columna para la métrica.")
            if column not in df.columns:
                raise ValueError(f"La columna '{column}' no existe en el dataset.")
            series = df[column]
            if not np.issubdtype(series.dtype, np.number):
                raise ValueError(f"La columna '{column}' debe ser numérica para calcular esta métrica.")
            if metric_type == 'sum':
                value = series.sum()
                label = f"Suma de {column}"
            elif metric_type == 'mean':
                value = series.mean()
                label = f"Promedio de {column}"
            elif metric_type == 'median':
                value = series.median()
                label = f"Mediana de {column}"
            elif metric_type == 'min':
                value = series.min()
                label = f"Mínimo de {column}"
            elif metric_type == 'max':
                value = series.max()
                label = f"Máximo de {column}"
        else:
            raise ValueError(f"Tipo de métrica no válido: {metric_type}")
    except Exception as exc:
        raise ValueError(f"No se pudo calcular la métrica ({exc}).") from exc

    if isinstance(value, (int, np.integer)):
        formatted_value = f"{value:,}"
    elif isinstance(value, (float, np.floating)):
        formatted_value = f"{value:,.2f}"
    else:
        formatted_value = str(value)

    return label, formatted_value


def _create_card_base(width, body_height, fonts, title):
    padding = 28
    header_height = 54
    total_height = padding * 2 + header_height + body_height
    card = Image.new("RGB", (width, total_height), "#ffffff")
    draw = ImageDraw.Draw(card)

    # Outer card
    draw.rounded_rectangle((0, 0, width, total_height), radius=18, fill="#ffffff", outline="#e2e8f0", width=2)

    # Header
    header_box = (padding, padding, width - padding, padding + header_height)
    draw.rounded_rectangle(header_box, radius=12, fill="#f1f5f9")
    draw.text((padding + 12, padding + 12), title, font=fonts['subtitle'], fill="#1e293b")

    body_top = padding + header_height + 16
    return card, draw, body_top, padding


def _render_placeholder_card(width, body_height, fonts, title, message):
    card, draw, body_top, padding = _create_card_base(width, body_height, fonts, title)
    draw.text((padding, body_top), message, font=fonts['body'], fill="#dc2626")
    return card


def _render_metric_card(component, df, width, fonts):
    config = component.get('config', {})
    title = component.get('title') or replace_emojis("📈 Métrica")
    try:
        label, formatted_value = _calculate_metric_value(config, df, title)
    except ValueError as exc:
        return _render_placeholder_card(width, 120, fonts, title, str(exc))

    card, draw, body_top, padding = _create_card_base(width, 110, fonts, title)
    draw.text((padding, body_top), formatted_value, font=fonts['value'], fill="#0f172a")
    value_height = fonts['value'].getbbox(formatted_value)[3] - fonts['value'].getbbox(formatted_value)[1]
    draw.text((padding, body_top + value_height + 12), label, font=fonts['body'], fill="#475569")
    return card


def _build_plotly_figure(component_type, config, df):
    if component_type == replace_emojis("📊 Gráfico de Líneas"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        color_col = config.get('color_column')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        if x_col not in df.columns or y_col not in df.columns:
            raise ValueError("Las columnas seleccionadas no existen en el dataset.")
        fig = px.line(df, x=x_col, y=y_col, color=color_col)
    elif component_type == replace_emojis("📋 Gráfico de Barras"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        orientation = config.get('orientation', 'vertical')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        if x_col not in df.columns or y_col not in df.columns:
            raise ValueError("Las columnas seleccionadas no existen en el dataset.")
        if orientation == 'horizontal':
            fig = px.bar(df, y=x_col, x=y_col)
        else:
            fig = px.bar(df, x=x_col, y=y_col)
    elif component_type == "🥧 Gráfico Circular":
        values_col = config.get('values_column')
        names_col = config.get('names_column')
        if not values_col or not names_col:
            raise ValueError("Selecciona columnas de valores y nombres.")
        if values_col not in df.columns or names_col not in df.columns:
            raise ValueError("Las columnas seleccionadas no existen en el dataset.")
        pie_data = df.groupby(names_col)[values_col].sum().reset_index()
        fig = px.pie(pie_data, values=values_col, names=names_col)
    elif component_type == replace_emojis("📈 Gráfico de Área"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        color_col = config.get('color_column')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        fig = px.area(df, x=x_col, y=y_col, color=color_col)
    elif component_type == replace_emojis("📈 Gráfico de Dispersión"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        color_col = config.get('color_column')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
    elif component_type == replace_emojis("📊 Histograma"):
        column = config.get('column')
        bins = config.get('bins', 20)
        if not column:
            raise ValueError("Selecciona una columna para el histograma.")
        if column not in df.columns:
            raise ValueError("La columna seleccionada no existe en el dataset.")
        fig = px.histogram(df, x=column, nbins=bins)
    elif component_type == replace_emojis("📊 Box Plot"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        fig = px.box(df, x=x_col, y=y_col)
    elif component_type == replace_emojis("📈 Gráfico de Violín"):
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        if not x_col or not y_col:
            raise ValueError("Selecciona columnas X e Y para el gráfico.")
        fig = px.violin(df, x=x_col, y=y_col)
    elif component_type == replace_emojis("📊 Matriz de Correlación"):
        columns = config.get('columns', [])
        if len(columns) < 2:
            raise ValueError("Selecciona al menos dos columnas numéricas para la matriz de correlación.")
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise ValueError(f"Columnas inexistentes: {', '.join(missing)}.")
        corr_matrix = df[columns].corr()
        fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu")
    else:
        raise ValueError("Tipo de componente no soportado para exportación.")

    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=40),
        title=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


def _render_chart_card(component, df, width, fonts):
    chart_height = 350
    title = component.get('title') or component.get('type')
    try:
        fig = _build_plotly_figure(component.get('type'), component.get('config', {}), df)
    except ValueError as exc:
        return _render_placeholder_card(width, chart_height, fonts, title, str(exc))

    card, _, body_top, padding = _create_card_base(width, chart_height, fonts, title)
    chart_width = width - padding * 2

    try:
        chart_bytes = fig.to_image(format="png", width=chart_width, height=chart_height, scale=2)
    except ValueError as exc:
        if "kaleido" in str(exc).lower():
            raise ImportError("Se requiere la librería 'kaleido' para exportar los gráficos a PNG. Instálala con `pip install -U kaleido`.") from exc
        return _render_placeholder_card(width, chart_height, fonts, title, str(exc))
    except Exception as exc:
        return _render_placeholder_card(width, chart_height, fonts, title, str(exc))

    chart_image = Image.open(io.BytesIO(chart_bytes)).convert("RGB")
    card.paste(chart_image, (padding, body_top))
    return card


def _render_table_card(component, df, width, fonts):
    config = component.get('config', {})
    columns = config.get('columns') or df.columns.tolist()
    rows = config.get('rows', min(20, len(df)))
    title = component.get('title') or replace_emojis("📋 Tabla de Datos")

    if not columns:
        return _render_placeholder_card(width, 140, fonts, title, "Selecciona columnas para la tabla.")

    missing = [col for col in columns if col not in df.columns]
    if missing:
        return _render_placeholder_card(width, 140, fonts, title, f"Columnas inexistentes: {', '.join(missing)}.")

    table_df = df[columns].head(rows)
    visible_rows = min(len(table_df), 8)
    if visible_rows == 0:
        return _render_placeholder_card(width, 140, fonts, title, "No hay datos para mostrar en la tabla.")

    row_height = 34
    table_height = row_height * (visible_rows + 1)
    body_height = table_height + 40
    card, draw, body_top, padding = _create_card_base(width, body_height, fonts, title)

    table_width = width - padding * 2
    table_image = Image.new("RGB", (table_width, table_height), "white")
    table_draw = ImageDraw.Draw(table_image)

    col_count = len(columns)
    col_width = table_width // col_count if col_count else table_width

    header_bg = "#0f172a"
    text_color = "#1f2937"

    for idx, col in enumerate(columns):
        x0 = idx * col_width
        table_draw.rectangle((x0, 0, x0 + col_width, row_height), fill=header_bg)
        table_draw.text((x0 + 8, 8), str(col)[:22], font=fonts['body'], fill="#f8fafc")

    for row_idx in range(visible_rows):
        y0 = row_height * (row_idx + 1)
        if row_idx % 2 == 0:
            table_draw.rectangle((0, y0, table_width, y0 + row_height), fill="#f8fafc")
        for col_idx, col in enumerate(columns):
            x0 = col_idx * col_width
            value = table_df.iloc[row_idx][col]
            table_draw.text((x0 + 8, y0 + 8), str(value)[:22], font=fonts['body'], fill=text_color)

    card.paste(table_image, (padding, body_top))
    caption = f"Mostrando {visible_rows} de {len(df)} registros"
    draw.text((padding, body_top + table_height + 12), caption, font=fonts['caption'], fill="#475569")
    return card


def _render_component_card(component, df, width, fonts):
    component_type = component.get('type')
    try:
        if component_type == replace_emojis("📈 Métricas"):
            return _render_metric_card(component, df, width, fonts)
        elif component_type in {
            replace_emojis("📊 Gráfico de Líneas"),
            replace_emojis("📋 Gráfico de Barras"),
            "🥧 Gráfico Circular",
            replace_emojis("📈 Gráfico de Área"),
            replace_emojis("📈 Gráfico de Dispersión"),
            replace_emojis("📊 Histograma"),
            replace_emojis("📊 Box Plot"),
            replace_emojis("📈 Gráfico de Violín"),
            replace_emojis("📊 Matriz de Correlación"),
        }:
            return _render_chart_card(component, df, width, fonts)
        elif component_type == replace_emojis("📋 Tabla de Datos"):
            return _render_table_card(component, df, width, fonts)
    except ImportError:
        raise
    except Exception as exc:
        return _render_placeholder_card(width, 140, fonts, component.get('title') or component_type, str(exc))

    return _render_placeholder_card(width, 140, fonts, component.get('title') or component_type, "Este tipo de componente no se puede exportar todavía.")


def _generate_dashboard_image(dashboard_name, components, df):
    if Image is None or ImageDraw is None or ImageFont is None:
        raise ImportError("Pillow no está instalado. Instala con `pip install pillow` para exportar como imagen.")

    canvas_width = 1600
    margin = 48
    row_gap = 36
    column_gap = 24

    try:
        title_font = ImageFont.truetype("arial.ttf", 30)
        subtitle_font = ImageFont.truetype("arial.ttf", 22)
        body_font = ImageFont.truetype("arial.ttf", 18)
        value_font = ImageFont.truetype("arialbd.ttf", 36)
        caption_font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        title_font = subtitle_font = body_font = value_font = caption_font = ImageFont.load_default()

    fonts = {
        'title': title_font,
        'subtitle': subtitle_font,
        'body': body_font,
        'value': value_font,
        'caption': caption_font,
    }

    layout_rows = _prepare_layout_rows(components)

    rendered_rows = []
    max_content_height = 0

    for _, row_components in layout_rows:
        total_span = sum(item['col_span'] for item in row_components)
        span_units = max(total_span, 1)
        available_width = canvas_width - (2 * margin) - column_gap * (len(row_components) - 1)
        width_per_unit = available_width / span_units

        row_rendered = []
        row_height = 0
        x_cursor = margin

        for item in row_components:
            component_width = int(width_per_unit * item['col_span'])
            card_image = _render_component_card(item['component'], df, component_width, fonts)
            row_rendered.append((card_image, x_cursor))
            x_cursor += component_width + column_gap
            row_height = max(row_height, card_image.height)

        rendered_rows.append((row_rendered, row_height))
        max_content_height += row_height + row_gap

    title_height = title_font.getbbox("Ag")[3] - title_font.getbbox("Ag")[1]
    subtitle_height = subtitle_font.getbbox("Ag")[3] - subtitle_font.getbbox("Ag")[1]

    estimated_height = margin + title_height + subtitle_height + 32 + max_content_height + margin
    estimated_height = max(estimated_height, 600)

    image = Image.new("RGB", (canvas_width, estimated_height), "white")
    draw = ImageDraw.Draw(image)

    now_str = datetime.now().strftime('%d/%m/%Y %H:%M')
    draw.text((margin, margin), f"Dashboard: {dashboard_name}", fill="#111827", font=title_font)
    draw.text((margin, margin + title_height + 10), f"Generado: {now_str}", fill="#475569", font=subtitle_font)

    y_cursor = margin + title_height + subtitle_height + 32

    for row_rendered, row_height in rendered_rows:
        for card_image, x_pos in row_rendered:
            image.paste(card_image, (x_pos, y_cursor))
        y_cursor += row_height + row_gap

    final_height = max(y_cursor - row_gap + margin, 400)
    image = image.crop((0, 0, canvas_width, final_height))

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
