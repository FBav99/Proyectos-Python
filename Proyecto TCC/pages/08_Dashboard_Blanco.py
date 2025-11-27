import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from utils.ui.icon_system import get_icon, replace_emojis
# Importar módulos personalizados
from core.config import setup_page_config, apply_custom_css
from core.auth_service import get_current_user, require_auth
from data.sample_datasets import get_sample_datasets
from core.dashboard_repository import list_user_dashboards, delete_dashboard
from utils.analysis import (
    calculate_metrics, 
    calculate_growth_metrics, 
    calculate_performance_insights,
    create_time_series_chart, 
    create_category_analysis, 
    create_regional_analysis,
    create_correlation_matrix,
    create_custom_calculation_charts,
    apply_custom_calculations,
    apply_all_filters
)
from utils.ui import (
    create_sidebar_controls,
    create_custom_calculations_ui,
    display_metrics_dashboard,
    display_custom_calculations_metrics,
    display_export_section,
    display_error, 
    safe_execute
)

# Import new dashboard modules
from utils.dashboard import (
    configure_component,
    render_dashboard,
    create_dashboard_sidebar,
    show_dashboard_info,
    add_component_to_dashboard,
    create_component_buttons,
    get_default_config,
)
from utils.ui import auth_ui
init_sidebar = auth_ui.init_sidebar
from core.streamlit_error_handler import safe_main, configure_streamlit_error_handling

# Configure error handling
configure_streamlit_error_handling()

DASHBOARD_CUSTOM_CSS = """
<style>
.dashboard-setup-card{
    background: var(--secondary-background-color);
    padding: 1.5rem 2rem;
    border-radius: 20px;
    margin-top: 1.5rem;
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 20px 38px rgba(15,23,42,0.08);
}
.dashboard-section-divider{
    width: 100%;
    height: 1px;
    margin: 1.75rem 0;
    background: linear-gradient(90deg, rgba(148,163,184,0), rgba(148,163,184,0.35), rgba(148,163,184,0));
}
.dashboard-subtle-divider{
    width: 100%;
    height: 1px;
    margin: 1.25rem 0;
    background: linear-gradient(90deg, rgba(148,163,184,0), rgba(148,163,184,0.2), rgba(148,163,184,0));
}
.dashboard-builder-card{
    background: var(--background-color);
    border: 1px dashed rgba(148,163,184,0.4);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
}
.dashboard-info-card{
    background: var(--secondary-background-color);
    padding: 1.5rem;
    border-radius: 18px;
    margin: 1.5rem 0;
    box-shadow: 0 16px 30px rgba(15,23,42,0.08);
    border: 1px solid rgba(148,163,184,0.18);
}
.dashboard-canvas{
    background: var(--background-color);
    padding: 2rem;
    border-radius: 20px;
    margin-top: 1.5rem;
    box-shadow: 0 24px 45px rgba(15,23,42,0.12);
    border: 1px solid rgba(148,163,184,0.16);
}
.dashboard-canvas > div[data-testid="stVerticalBlock"]{
    padding-top: 0;
}
</style>
"""


# Archivo - Cargar DataFrame Subido
def load_uploaded_dataframe(uploaded_file):
    """Carga un archivo subido por el usuario y devuelve un DataFrame."""
    from utils.data.data_handling import load_excel_with_sheet_selection
    
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    df = load_excel_with_sheet_selection(uploaded_file, key_prefix="dashboard_blank")
    return df if df is not None else pd.DataFrame()


# Analisis - Analizar Columnas del Dataset
def analyze_dataset_columns(df):
    """Analiza columnas del dataset y las organiza según su uso recomendado."""
    id_columns = [col for col in df.columns if 'id' in col.lower()]

    numeric_non_id = []
    numeric_id = []
    for col in df.select_dtypes(include=[np.number]).columns.tolist():
        if col in id_columns:
            numeric_id.append(col)
        else:
            numeric_non_id.append(col)

    categorical_non_id = []
    categorical_id = []
    for col in df.select_dtypes(include=['object', 'category']).columns.tolist():
        if col in id_columns:
            categorical_id.append(col)
        else:
            categorical_non_id.append(col)

    datetime_cols = [
        col for col in df.columns
        if pd.api.types.is_datetime64_any_dtype(df[col])
    ]

    # Fallback: if we have ID columns that aren't captured above, add them accordingly
    for col in id_columns:
        if col not in numeric_non_id + numeric_id and pd.api.types.is_numeric_dtype(df[col]):
            numeric_id.append(col)
        if col not in categorical_non_id + categorical_id and df[col].dtype == object:
            categorical_id.append(col)

    ordered_numeric = numeric_non_id + numeric_id
    ordered_categorical = categorical_non_id + categorical_id

    return {
        'id': id_columns,
        'numeric': ordered_numeric,
        'numeric_without_id': numeric_non_id,
        'categorical': ordered_categorical,
        'categorical_without_id': categorical_non_id,
        'datetime': datetime_cols,
    }


# UI - Seleccionar Datos del Dashboard
def select_dashboard_data():
    """Gestiona la selección de datos para el dashboard y devuelve el DataFrame activo."""
    st.markdown("### 📂 Selecciona o carga tus datos")
    st.caption("Puedes subir tus propios datos o practicar con un dataset de ejemplo sin abandonar esta página.")

    render_saved_dashboards_panel()

    col_upload, col_samples = st.columns(2)

    with col_upload:
        st.markdown(replace_emojis("#### 📤 Subir datos"), unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Elige un archivo CSV o Excel",
            type=['csv', 'xlsx', 'xls'],
            key="dashboard_blank_uploader",
            help="Los datos se guardarán en tu sesión para que puedas construir el dashboard de inmediato."
        )

        if uploaded_file is not None:
            try:
                df = load_uploaded_dataframe(uploaded_file)
                st.session_state.cleaned_data = df
                st.session_state.uploaded_data = df
                st.session_state.sample_data = None
                st.session_state.dashboard_data_label = uploaded_file.name
                st.success(f"Archivo `{uploaded_file.name}` cargado correctamente.")
                with st.expander("👀 Vista previa (primeras 10 filas)", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
            except Exception as exc:
                st.error(f"No se pudo cargar el archivo. Detalle: {exc}")

    with col_samples:
        st.markdown(replace_emojis("#### 📊 Datasets de ejemplo"), unsafe_allow_html=True)
        sample_datasets = get_sample_datasets()
        sample_names = list(sample_datasets.keys())

        if sample_names:
            default_index = 0
            if 'dashboard_selected_sample' in st.session_state:
                try:
                    default_index = sample_names.index(st.session_state.dashboard_selected_sample)
                except ValueError:
                    default_index = 0

            selected_sample = st.selectbox(
                "Selecciona un dataset",
                sample_names,
                index=default_index,
                key="dashboard_blank_sample_selector"
            )

            sample_info = sample_datasets[selected_sample]
            st.write(sample_info['description'])
            st.markdown(f"**Nivel sugerido:** {sample_info['difficulty']}")

            with st.expander("👀 Vista previa (primeras 10 filas)"):
                st.dataframe(sample_info['data'].head(10), use_container_width=True)

            if st.button("Usar este dataset de ejemplo", key="dashboard_use_sample", use_container_width=True):
                dataset_df = sample_info['data']
                st.session_state.sample_data = dataset_df
                st.session_state.cleaned_data = dataset_df
                st.session_state.uploaded_data = dataset_df
                st.session_state.dashboard_data_label = f"Ejemplo: {selected_sample}"
                st.session_state.dashboard_selected_sample = selected_sample
                st.success(f"Ahora estás usando `{selected_sample}`.")
                st.rerun()
        else:
            st.info("No hay datasets de ejemplo disponibles en este momento.")

    current_df = None
    if 'cleaned_data' in st.session_state and st.session_state.cleaned_data is not None:
        current_df = st.session_state.cleaned_data
    elif 'sample_data' in st.session_state and st.session_state.sample_data is not None:
        current_df = st.session_state.sample_data

    if current_df is not None:
        label = st.session_state.get('dashboard_data_label', 'Datos cargados')
        st.markdown("---")
        st.markdown(f"#### {get_icon("✅", 20)} Datos en uso: `{label}`")
        st.caption(f"{len(current_df)} filas · {len(current_df.columns)} columnas")
    else:
        st.warning("Carga un archivo o elige un dataset de ejemplo para comenzar.")

    return current_df


# Cache - Obtener Dashboards del Usuario
def get_cached_user_dashboards():
    """Retorna dashboards guardados para el usuario autenticado utilizando caché local."""
    user_id = st.session_state.get('auth_user_id')
    if not user_id:
        return []

    if st.session_state.get('dashboards_cache_dirty', True) or 'cached_user_dashboards' not in st.session_state:
        st.session_state['cached_user_dashboards'] = list_user_dashboards(user_id)
        st.session_state['dashboards_cache_dirty'] = False

    return st.session_state.get('cached_user_dashboards', [])


# UI - Mostrar Panel de Dashboards Guardados
def render_saved_dashboards_panel():
    """Muestra un panel con dashboards guardados antes de seleccionar los datos."""
    user_id = st.session_state.get('auth_user_id')
    if not user_id:
        return

    saved_dashboards = get_cached_user_dashboards()

    with st.expander(replace_emojis("📁 Dashboards guardados"), expanded=False):
        if not saved_dashboards:
            st.info("No tienes dashboards guardados todavía. Puedes guardar uno desde la barra lateral.")
            return

        for dashboard in saved_dashboards:
            with st.container():
                dataset_label = dashboard.get("dataset_info", {}).get("label") or "Dataset no especificado"
                st.markdown(f"**{dashboard['dashboard_name']}**")
                updated_at = dashboard.get('updated_at') or dashboard.get('created_at')
                if updated_at:
                    st.caption(f"Última actualización: {updated_at}")
                st.caption(f"Dataset original: `{dataset_label}`")

                col_load, col_delete = st.columns([2, 1])
                with col_load:
                    if st.button("📂 Cargar en el constructor", key=f"main_load_dashboard_{dashboard['id']}", use_container_width=True):
                        components = dashboard.get('config', {}).get('components', [])
                        st.session_state.dashboard_components = components
                        st.session_state.dashboard_component_counter = len(components)
                        st.session_state.active_dashboard_id = dashboard['id']
                        st.session_state.dashboard_name_input = dashboard['dashboard_name']
                        dataset_label = dashboard.get("dataset_info", {}).get("label")
                        if dataset_label:
                            st.session_state.dashboard_data_label = dataset_label
                        st.session_state.editing_component = None
                        st.session_state.dashboard_template_gallery_expanded = False
                        st.session_state.dashboard_selected_template_key = None
                        st.session_state.dashboard_selected_template_title = dashboard['dashboard_name']
                        if dataset_label:
                            st.info(f"Dashboard cargado. Selecciona un dataset (por ejemplo `{dataset_label}`) para visualizarlo.")
                        else:
                            st.success("Dashboard cargado. Selecciona tu fuente de datos para visualizarlo.")
                        st.rerun()

                with col_delete:
                    if st.button("🗑️ Eliminar", key=f"main_delete_dashboard_{dashboard['id']}", use_container_width=True):
                        delete_dashboard(dashboard['id'], user_id)
                        st.session_state['dashboards_cache_dirty'] = True
                        st.success("Dashboard eliminado.")
                        st.rerun()


# UI - Controles Rapidos de Construccion
def render_inline_builder_controls(df):
    """Renderiza controles rápidos para agregar componentes sin depender del sidebar."""
    st.markdown("### 🧱 Construye tu dashboard")
    st.caption("Agrega componentes frecuentes desde aquí y utiliza el panel lateral para ajustes avanzados.")

    quick_components = [
        {
            "label": replace_emojis("📊 Métrica KPI"),
            "type": replace_emojis("📈 Métricas"),
            "description": "Resalta un indicador clave.",
        },
        {
            "label": replace_emojis("📈 Línea"),
            "type": replace_emojis("📊 Gráfico de Líneas"),
            "description": "Muestra tendencias en el tiempo.",
        },
        {
            "label": replace_emojis("📋 Barras"),
            "type": replace_emojis("📋 Gráfico de Barras"),
            "description": "Compara categorías rápidamente.",
        },
        {
            "label": "🥧 Circular",
            "type": "🥧 Gráfico Circular",
            "description": "Visualiza proporciones.",
        },
        {
            "label": replace_emojis("📈 Área"),
            "type": replace_emojis("📈 Gráfico de Área"),
            "description": "Destaca acumulados y evolución.",
        },
        {
            "label": replace_emojis("📋 Tabla"),
            "type": replace_emojis("📋 Tabla de Datos"),
            "description": "Explora datos detallados.",
        },
    ]

    cols = st.columns(3)
    selected_type = None
    for idx, component in enumerate(quick_components):
        col = cols[idx % len(cols)]
        with col:
            if st.button(
                component["label"],
                key=f"quick_component_{idx}",
                help=component["description"],
                use_container_width=True,
            ):
                selected_type = component["type"]

    with st.expander("Ver más componentes y análisis", expanded=False):
        advanced_type = create_component_buttons(key_prefix="inline_", expand_all=True)
        if advanced_type:
            selected_type = advanced_type

    if selected_type:
        if add_component_to_dashboard(selected_type, df):
            st.rerun()


# Plantilla - Construir Componente de Plantilla
def build_component_template(component_type, df, *, title=None, layout=None, overrides=None):
    """Crea un componente listo para usarse dentro de una plantilla."""
    config = get_default_config(component_type, df) or {}
    if overrides:
        config.update({k: v for k, v in overrides.items() if v is not None})

    return {
        'id': None,
        'type': component_type,
        'title': title or f"{component_type}",
        'config': config,
        'layout': layout or {}
    }


# Plantilla - Construir Plantilla Ejecutiva
def build_executive_template(df):
    """Crea una plantilla con KPIs superiores y visualizaciones principales."""
    columns_info = analyze_dataset_columns(df)
    numeric_cols = columns_info['numeric']
    id_columns = columns_info['id']
    date_cols = columns_info['datetime']
    categorical_cols = columns_info['categorical']

    first_numeric = numeric_cols[0] if numeric_cols else None
    second_numeric = numeric_cols[1] if len(numeric_cols) > 1 else first_numeric
    date_col = date_cols[0] if date_cols else None
    if date_col is None and id_columns:
        date_col = id_columns[0]
    if date_col is None and df.columns.tolist():
        date_col = df.columns.tolist()[0]

    sum_overrides = {'metric_type': 'sum', 'column': first_numeric} if first_numeric else {'metric_type': 'count'}
    mean_overrides = {'metric_type': 'mean', 'column': second_numeric} if second_numeric else {'metric_type': 'count'}
    line_overrides = {}
    if first_numeric:
        line_overrides['y_column'] = first_numeric
    if date_col:
        line_overrides['x_column'] = date_col
    bar_overrides = {}
    if categorical_cols:
        bar_overrides['x_column'] = categorical_cols[0]
    elif id_columns:
        bar_overrides['x_column'] = id_columns[0]
    if first_numeric:
        bar_overrides['y_column'] = first_numeric

    components = [
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Registros totales",
            layout={'row': 1, 'order': 1, 'col_span': 4},
            overrides={'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Suma principal",
            layout={'row': 1, 'order': 2, 'col_span': 4},
            overrides=sum_overrides
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Promedio principal",
            layout={'row': 1, 'order': 3, 'col_span': 4},
            overrides=mean_overrides
        ),
        build_component_template(
            replace_emojis("📊 Gráfico de Líneas"),
            df,
            title="Tendencia principal",
            layout={'row': 2, 'order': 1, 'col_span': 8},
            overrides=line_overrides
        ),
        build_component_template(
            replace_emojis("📋 Gráfico de Barras"),
            df,
            title="Top categorías",
            layout={'row': 2, 'order': 2, 'col_span': 4},
            overrides=bar_overrides
        ),
        build_component_template(
            replace_emojis("📋 Tabla de Datos"),
            df,
            title="Detalle de registros",
            layout={'row': 3, 'order': 1, 'col_span': 12},
            overrides={'rows': min(20, len(df))}
        ),
    ]

    return components


# Plantilla - Construir Plantilla de Rendimiento
def build_performance_template(df):
    """Plantilla enfocada en rendimiento con correlaciones y comparativas."""
    columns_info = analyze_dataset_columns(df)
    numeric_cols = columns_info['numeric']
    categorical_cols = columns_info['categorical']
    id_columns = columns_info['id']
    date_cols = columns_info['datetime']

    first_numeric = numeric_cols[0] if numeric_cols else None
    second_numeric = numeric_cols[1] if len(numeric_cols) > 1 else first_numeric
    category_col = categorical_cols[0] if categorical_cols else None
    date_col = date_cols[0] if date_cols else None
    if date_col is None and id_columns:
        date_col = id_columns[0]
    if date_col is None and df.columns.tolist():
        date_col = df.columns.tolist()[0]

    line_overrides = {}
    if first_numeric:
        line_overrides['y_column'] = first_numeric
    if date_col:
        line_overrides['x_column'] = date_col

    bar_overrides = {}
    if category_col:
        bar_overrides['x_column'] = category_col
    if first_numeric:
        bar_overrides['y_column'] = first_numeric

    components = [
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Valor máximo",
            layout={'row': 1, 'order': 1, 'col_span': 3},
            overrides={'metric_type': 'max', 'column': first_numeric} if first_numeric else {'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Valor mínimo",
            layout={'row': 1, 'order': 2, 'col_span': 3},
            overrides={'metric_type': 'min', 'column': first_numeric} if first_numeric else {'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Mediana",
            layout={'row': 1, 'order': 3, 'col_span': 3},
            overrides={'metric_type': 'median', 'column': first_numeric} if first_numeric else {'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Promedio secundario",
            layout={'row': 1, 'order': 4, 'col_span': 3},
            overrides={'metric_type': 'mean', 'column': second_numeric} if second_numeric else {'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📊 Gráfico de Líneas"),
            df,
            title="Evolución temporal",
            layout={'row': 2, 'order': 1, 'col_span': 6},
            overrides=line_overrides
        ),
        build_component_template(
            replace_emojis("📊 Gráfico de Barras"),
            df,
            title="Comparativa por categoría",
            layout={'row': 2, 'order': 2, 'col_span': 6},
            overrides=bar_overrides
        ),
        build_component_template(
            replace_emojis("📊 Matriz de Correlación"),
            df,
            title="Relaciones entre variables",
            layout={'row': 3, 'order': 1, 'col_span': 6},
            overrides={'columns': numeric_cols[:min(5, len(numeric_cols))]} if len(numeric_cols) >= 2 else {}
        ),
        build_component_template(
            replace_emojis("📋 Tabla de Datos"),
            df,
            title="Detalle filtrable",
            layout={'row': 3, 'order': 2, 'col_span': 6},
            overrides={'rows': min(15, len(df))}
        ),
    ]
    return components


# Plantilla - Construir Plantilla Operativa
def build_operations_template(df):
    """Plantilla con enfoque operativo y análisis de distribución."""
    columns_info = analyze_dataset_columns(df)
    numeric_cols = columns_info['numeric']
    categorical_cols = columns_info['categorical']
    id_columns = columns_info['id']

    first_numeric = numeric_cols[0] if numeric_cols else None
    second_numeric = numeric_cols[1] if len(numeric_cols) > 1 else first_numeric
    category_col = categorical_cols[0] if categorical_cols else None
    if category_col is None and id_columns:
        category_col = id_columns[0]

    hist_overrides = {'column': first_numeric} if first_numeric else {}
    box_overrides = {}
    if category_col:
        box_overrides['x_column'] = category_col
    if first_numeric:
        box_overrides['y_column'] = first_numeric

    components = [
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Total de filas limpias",
            layout={'row': 1, 'order': 1, 'col_span': 4},
            overrides={'metric_type': 'count'}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Suma principal",
            layout={'row': 1, 'order': 2, 'col_span': 4},
            overrides={'metric_type': 'sum', 'column': first_numeric}
        ),
        build_component_template(
            replace_emojis("📈 Métricas"),
            df,
            title="Promedio operativo",
            layout={'row': 1, 'order': 3, 'col_span': 4},
            overrides={'metric_type': 'mean', 'column': second_numeric}
        ),
        build_component_template(
            replace_emojis("📊 Histograma"),
            df,
            title="Distribución principal",
            layout={'row': 2, 'order': 1, 'col_span': 6},
            overrides=hist_overrides
        ),
        build_component_template(
            replace_emojis("📊 Box Plot"),
            df,
            title="Outliers por categoría",
            layout={'row': 2, 'order': 2, 'col_span': 6},
            overrides=box_overrides
        ),
        build_component_template(
            replace_emojis("📋 Tabla de Datos"),
            df,
            title="Registro detallado",
            layout={'row': 3, 'order': 1, 'col_span': 12},
            overrides={'rows': min(25, len(df))}
        ),
    ]
    return components


# Cache - Obtener Plantillas de Dashboard
@st.cache_resource
def get_dashboard_templates(df):
    """Retorna la configuración de plantillas disponibles.
    
    Uses cache_resource because the return value contains functions (builders)
    which are not pickle-serializable for cache_data.
    """
    return [
        {
            "key": "executive_overview",
            "title": replace_emojis("🎯 Resumen Ejecutivo"),
            "description": "Disposición tipo Power BI con KPIs en la parte superior y visualizaciones clave en la zona central.",
            "recommended_dataset": "E-commerce",
            "builder": build_executive_template,
        },
        {
            "key": "performance_insights",
            "title": replace_emojis("📈 Rendimiento y correlaciones"),
            "description": "Analiza tendencias, comparativas por categoría y relaciones entre variables numéricas.",
            "recommended_dataset": "Finance",
            "builder": build_performance_template,
        },
        {
            "key": "operations_monitor",
            "title": "⚙️ Monitor Operativo",
            "description": "Ideal para revisar distribuciones, detectar outliers y consultar operaciones recientes.",
            "recommended_dataset": "Dataset Sucio (Limpieza)",
            "builder": build_operations_template,
        },
    ]


# Estado - Limpiar Layout del Dashboard
def clear_dashboard_layout():
    """Reinicia el dashboard a un lienzo en blanco."""
    st.session_state.dashboard_components = []
    st.session_state.dashboard_component_counter = 0
    st.session_state.editing_component = None
    st.session_state.active_dashboard_id = None
    st.session_state.dashboard_name_input = "Mi Dashboard"
    st.session_state.dashboard_selected_template_key = None
    st.session_state.dashboard_selected_template_title = None
    st.session_state.dashboard_template_gallery_expanded = True
    st.session_state.dashboards_cache_dirty = True


# Plantilla - Aplicar Plantilla al Dashboard
def apply_dashboard_template(template_config, df, *, data_label=None, force_rerun=False):
    """Aplica una plantilla al dashboard actual."""
    components = template_config["builder"](df)
    for idx, component in enumerate(components):
        component['id'] = idx
    st.session_state.dashboard_components = components
    st.session_state.dashboard_component_counter = len(components)
    st.session_state.editing_component = None
    st.session_state.dashboard_selected_template_key = template_config.get("key")
    st.session_state.dashboard_selected_template_title = template_config.get("title")
    st.session_state.dashboard_template_gallery_expanded = False
    if data_label:
        st.session_state.dashboard_data_label = data_label
    if force_rerun:
        st.rerun()


# UI - Mostrar Galeria de Plantillas
def render_template_gallery(df, *, show_header=True):
    """Muestra las plantillas disponibles y opciones para aplicarlas."""
    if show_header:
        st.markdown("### 📐 Plantillas guiadas")
        st.caption("Estas plantillas cargan un dataset de ejemplo para que explores la disposición. Puedes limpiar la plantilla y reutilizarla con tus propios datos en cualquier momento.")

    sample_datasets = get_sample_datasets()
    templates = get_dashboard_templates(df)

    for template in templates:
        st.markdown(f"#### {template['title']}")
        st.write(template['description'])
        recommended_dataset = template.get("recommended_dataset")
        if recommended_dataset:
            st.caption(f"Plantilla optimizada con el dataset de ejemplo: `{recommended_dataset}`.")

        col_apply, col_example, col_clear = st.columns(3)

        with col_apply:
            if st.button("Aplicar con mis datos", key=f"apply_{template['key']}", use_container_width=True):
                apply_dashboard_template(template, df, data_label=st.session_state.get('dashboard_data_label'))
                st.rerun()

        with col_example:
            if recommended_dataset and recommended_dataset in sample_datasets:
                if st.button("Probar con datos de ejemplo", key=f"example_{template['key']}", use_container_width=True):
                    dataset_df = sample_datasets[recommended_dataset]['data']
                    st.session_state.sample_data = dataset_df
                    st.session_state.cleaned_data = dataset_df
                    st.session_state.uploaded_data = dataset_df
                    st.session_state.dashboard_data_label = f"Ejemplo: {recommended_dataset}"
                    apply_dashboard_template(template, dataset_df, data_label=st.session_state.dashboard_data_label, force_rerun=True)
            else:
                st.button("Dataset no disponible", key=f"example_disabled_{template['key']}", disabled=True, use_container_width=True)

        with col_clear:
            if st.button("🧹 Limpiar plantilla", key=f"clear_{template['key']}", use_container_width=True):
                st.session_state.dashboard_selected_template_key = None
                st.session_state.dashboard_selected_template_title = None
                st.session_state.dashboard_template_gallery_expanded = True
                clear_dashboard_layout()
                st.rerun()

        st.markdown("---")

# Principal - Dashboard en Blanco
@safe_main
def main():
    """Dashboard en Blanco - Construcción Manual"""
    # Configurar página
    st.set_page_config(
        page_title="Dashboard en Blanco - Construcción Manual",
        page_icon=get_icon("🎨", 20),
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_css()
    
    # Initialize sidebar with user info (always visible)
    current_user = init_sidebar()
    if not current_user:
        st.error("Por favor inicia sesión para acceder a esta página.")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Volver al Inicio", use_container_width=True):
                st.switch_page("Inicio.py")
        with col2:
            if st.button("🔐 Iniciar Sesión", use_container_width=True):
                st.switch_page("Inicio.py")
        st.stop()
    
    username = current_user['username']
    name = f"{current_user['first_name']} {current_user['last_name']}"
    st.session_state.setdefault('dashboards_cache_dirty', True)
    st.session_state.setdefault('cached_user_dashboards', [])
    
    # Header
    st.markdown(f'<h1 class="main-header">{get_icon("🎨", 20)} Dashboard en Blanco</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; color: #666; font-size: 1.1rem;">Construye tu dashboard personalizado, <strong>{name}</strong></p>', unsafe_allow_html=True)
    
    # Initialize dashboard components in session state
    if 'dashboard_components' not in st.session_state:
        st.session_state.dashboard_components = []
    if 'dashboard_component_counter' not in st.session_state:
        if st.session_state.dashboard_components:
            max_id = max(component.get('id', 0) for component in st.session_state.dashboard_components)
            st.session_state.dashboard_component_counter = max_id + 1
        else:
            st.session_state.dashboard_component_counter = 0
    if 'dashboard_template_gallery_expanded' not in st.session_state:
        st.session_state.dashboard_template_gallery_expanded = True
    if 'dashboard_selected_template_key' not in st.session_state:
        st.session_state.dashboard_selected_template_key = None
    if 'dashboard_selected_template_title' not in st.session_state:
        st.session_state.dashboard_selected_template_title = None

    st.markdown(DASHBOARD_CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown('<div class="dashboard-setup-card">', unsafe_allow_html=True)

    # Data selection controls
    df = select_dashboard_data()
    if df is None:
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="dashboard-section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-builder-card">', unsafe_allow_html=True)
    st.markdown("#### 🧰 Opciones de construcción")

    builder_mode = st.radio(
        "Modo de construcción",
        ("Lienzo en blanco", "Plantillas guiadas"),
        index=0 if st.session_state.get("dashboard_builder_mode", "Lienzo en blanco") == "Lienzo en blanco" else 1,
        horizontal=True,
        key="dashboard_builder_mode"
    )

    if builder_mode == "Plantillas guiadas":
        toggle_label = "Ocultar plantillas" if st.session_state.dashboard_template_gallery_expanded else "Mostrar plantillas"
        col_toggle, col_status = st.columns([1, 3])
        with col_toggle:
            if st.button(toggle_label, key="toggle_templates"):
                st.session_state.dashboard_template_gallery_expanded = not st.session_state.dashboard_template_gallery_expanded
                st.rerun()
        with col_status:
            active_template = st.session_state.get("dashboard_selected_template_title")
            if active_template:
                st.markdown(f"**Plantilla activa:** `{active_template}`")
            else:
                st.caption("Selecciona una plantilla preconfigurada para comenzar rápidamente.")

        if st.session_state.dashboard_template_gallery_expanded:
            render_template_gallery(df, show_header=False)
    else:
        render_inline_builder_controls(df)
        st.markdown('<div class="dashboard-subtle-divider"></div>', unsafe_allow_html=True)
        if st.session_state.dashboard_components:
            if st.button("🧹 Limpiar dashboard", key="clear_dashboard_manual"):
                clear_dashboard_layout()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # close builder card
    st.markdown('</div>', unsafe_allow_html=True)  # close setup card

    show_dashboard_info(df, show_divider=False, container_class="dashboard-info-card")

    # Create sidebar
    create_dashboard_sidebar(df, show_component_controls=(builder_mode == "Lienzo en blanco"))

    # Main content area
    
    # Component configuration section
    if st.session_state.get('editing_component') is not None:
        editing_id = st.session_state.editing_component
        component = next((c for c in st.session_state.dashboard_components if c['id'] == editing_id), None)
        
        if component:
            st.markdown(f"### ⚙️ Configurando: {component['title']}")
            configure_component(component, df)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Guardar Configuración", type="primary", use_container_width=True):
                    st.session_state.editing_component = None
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.session_state.editing_component = None
        else:
            st.session_state.editing_component = None
    
    # Dashboard info
    st.markdown("### 🎛️ Vista del dashboard")
    st.markdown('<div class="dashboard-canvas">', unsafe_allow_html=True)
    render_dashboard(df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer navigation
    st.markdown("---")
    st.markdown("### 🧭 Navegación Rápida")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.switch_page("Inicio.py")
    
    with col2:
        if st.button("📊 Ver Métricas", use_container_width=True):
            st.switch_page("pages/03_Nivel_3_Metricas.py")
    
    with col3:
        if st.button("🚀 Nivel Avanzado", use_container_width=True):
            st.switch_page("pages/04_Nivel_4_Avanzado.py")
    
    with col4:
        if st.button("❓ Ayuda", use_container_width=True):
            st.switch_page("pages/00_Ayuda.py")

if __name__ == "__main__":
    main()
