"""
Dashboard utilities package for TCC Data Analysis Platform
"""

from .dashboard_components import *
from .dashboard_renderer import *
from .dashboard_sidebar import *
from .dashboard_templates import *

__all__ = [
    'create_component_buttons',
    'add_component_to_dashboard',
    'get_default_config',
    'configure_component',
    'render_dashboard',
    'render_component',
    'display_metric',
    'display_line_chart',
    'display_bar_chart',
    'display_pie_chart',
    'display_area_chart',
    'display_scatter_plot',
    'display_histogram',
    'display_box_plot',
    'display_violin_plot',
    'display_correlation_matrix',
    'display_data_table',
    'create_dashboard_sidebar',
    'save_dashboard',
    'export_dashboard',
    'show_dashboard_info',
    'show_dashboard_selection'
]
