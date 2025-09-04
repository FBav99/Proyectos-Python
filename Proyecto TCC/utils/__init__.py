"""
Main utilities package for TCC Data Analysis Platform
Provides organized access to all utility modules
"""

# Import from all subpackages
from .dashboard import *
from .data import *
from .learning import *
from .ui import *
from .analysis import *
from .system import *

# Legacy imports for backward compatibility
from .learning import learning_progress
from .learning import level_components
from .learning import level_data
from .learning import level_styles

__all__ = [
    # Dashboard utilities
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
    
    # Data utilities
    'DataCleaner',
    'create_data_cleaning_interface',
    'DataCleaningOperations',
    'DataValidation',
    'show_upload_section',
    'show_examples_section',
    'get_current_data',
    
    # Learning utilities
    'create_step_card',
    'create_info_box',
    'load_level_styles',
    'get_level_progress',
    'create_sample_data',
    'analyze_uploaded_data',
    'show_user_profile_section',
    'show_progress_reset_button',
    'save_level_progress',
    'create_help_header',
    'create_learning_levels_section',
    'create_dashboard_blanco_section',
    'create_visualization_guide',
    'create_common_scenarios',
    'create_troubleshooting_section',
    'create_quick_reference',
    'create_learning_resources',
    'create_navigation_section',
    
    # UI utilities
    'create_navigation_header',
    'create_footer',
    'show_login_form',
    'show_registration_form',
    'handle_authentication',
    'get_current_user',
    'show_header',
    'show_quick_start_section',
    'should_show_main_content',
    'clear_selected_template',
    'create_sidebar_controls',
    'create_file_uploader',
    'create_column_selector',
    'create_filter_controls',
    'create_chart_type_selector',
    'create_color_picker',
    'create_title_input',
    'create_legend_toggle',
    'create_axis_labels_input',
    'create_grid_toggle',
    'create_tooltip_toggle',
    'create_custom_calculations_ui',
    'display_metrics_dashboard',
    'display_custom_calculations_metrics',
    'display_export_section',
    'handle_authentication_error',
    'display_error',
    'safe_execute',
    'log_error',
    
    # Analysis utilities
    'create_chart',
    'create_metric_card',
    'apply_filters',
    'calculate_statistics',
    'calculate_metrics',
    'calculate_growth_metrics',
    'calculate_performance_insights',
    'create_time_series_chart',
    'create_bar_chart',
    'create_pie_chart',
    'create_line_chart',
    'create_scatter_plot',
    'create_histogram',
    'create_box_plot',
    'create_correlation_matrix',
    'create_category_analysis',
    'create_regional_analysis',
    'create_custom_calculation_charts',
    'apply_custom_calculations',
    'apply_all_filters',
    
    # System utilities
    'export_data',
    'get_csv_data',
    'create_summary_report',
    'create_gif',
    'save_gif',
    'display_level_gif'
]
