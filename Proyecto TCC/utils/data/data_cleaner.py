from utils.ui.icon_system import get_icon, replace_emojis
"""
Data cleaning service for TCC Data Analysis Platform
Main orchestrator for data cleaning, validation, and quality operations
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from .data_cleaning_ops import DataCleaningOperations
from .data_validation import DataValidation

class DataCleaner:
    """Main data cleaning orchestrator"""
    
    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.cleaned_df = df.copy()
        self.cleaning_ops = DataCleaningOperations(df)
        self.validation = DataValidation(df)
        self.cleaning_history = []
    
    def add_to_history(self, operation: str, details: str):
        """Add operation to cleaning history"""
        self.cleaning_history.append({
            'operation': operation,
            'details': details,
            'timestamp': pd.Timestamp.now()
        })
    
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Get summary of cleaning operations performed"""
        return {
            'total_operations': len(self.cleaning_history),
            'operations': self.cleaning_history,
            'original_shape': self.original_df.shape,
            'cleaned_shape': self.cleaned_df.shape,
            'rows_removed': self.original_df.shape[0] - self.cleaned_df.shape[0],
            'columns_removed': self.original_df.shape[1] - self.cleaned_df.shape[1]
        }
    
    def apply_auto_cleaning(self, cleaning_options: Dict[str, bool] = None) -> pd.DataFrame:
        """
        Apply automatic cleaning based on predefined options
        
        Args:
            cleaning_options: Dictionary with cleaning options
        """
        if cleaning_options is None:
            cleaning_options = {
                'whitespace': True,
                'case_normalization': True,
                'special_characters': False,
                'accents': False,
                'duplicates': True,
                'missing_values': True
            }
        
        # Start with current cleaned_df
        current_df = self.cleaned_df.copy()
        
        if cleaning_options.get('whitespace', False):
            # Update cleaning_ops with current data
            self.cleaning_ops.cleaned_df = current_df.copy()
            current_df = self.cleaning_ops.clean_whitespace()
            self.add_to_history("Auto whitespace cleaning", "Applied to all text columns")
        
        if cleaning_options.get('case_normalization', False):
            # Update cleaning_ops with current data
            self.cleaning_ops.cleaned_df = current_df.copy()
            current_df = self.cleaning_ops.normalize_text_case(case_type='lower')
            self.add_to_history("Auto case normalization", "Applied to all text columns")
        
        if cleaning_options.get('special_characters', False):
            # Update cleaning_ops with current data
            self.cleaning_ops.cleaned_df = current_df.copy()
            current_df = self.cleaning_ops.remove_special_characters()
            self.add_to_history("Auto special character removal", "Applied to all text columns")
        
        if cleaning_options.get('accents', False):
            # Update cleaning_ops with current data
            self.cleaning_ops.cleaned_df = current_df.copy()
            current_df = self.cleaning_ops.normalize_accents()
            self.add_to_history("Auto accent normalization", "Applied to all text columns")
        
        if cleaning_options.get('duplicates', False):
            # Update validation with current data
            self.validation.df = current_df.copy()
            current_df, removed_count = self.validation.remove_duplicates()
            self.add_to_history("Auto duplicate removal", f"Removed {removed_count} duplicate rows")
        
        if cleaning_options.get('missing_values', False):
            # Update validation with current data
            self.validation.df = current_df.copy()
            current_df = self.validation.fill_missing_values(method='auto')
            self.add_to_history("Auto missing value filling", "Applied auto-fill method")
        
        # Update all components with final result
        self.cleaned_df = current_df.copy()
        self.cleaning_ops.cleaned_df = current_df.copy()
        
        return self.cleaned_df
    
    def reset_to_original(self) -> pd.DataFrame:
        """Reset to original data"""
        self.cleaned_df = self.original_df.copy()
        self.cleaning_ops.cleaned_df = self.original_df.copy()
        self.validation.df = self.original_df.copy()
        self.cleaning_history = []
        return self.cleaned_df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Get cleaned data"""
        return self.cleaned_df.copy()
    
    def get_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report"""
        return self.validation.validate_data_quality()
    
    def get_cleaning_suggestions(self) -> List[Dict[str, Any]]:
        """Get suggestions for cleaning actions"""
        quality_report = self.get_quality_report()
        return self.validation.suggest_cleaning_actions(quality_report)


def create_data_cleaning_interface(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Streamlit interface for data cleaning
    
    Args:
        df: DataFrame to clean
    
    Returns:
        Cleaned DataFrame
    """
    # Initialize cleaner
    cleaner = DataCleaner(df)
    
    # Store cleaner in session state to persist across reruns
    if 'data_cleaner' not in st.session_state:
        st.session_state.data_cleaner = cleaner
    else:
        # Update the cleaner with current data if it changed
        if not st.session_state.data_cleaner.original_df.equals(df):
            st.session_state.data_cleaner = cleaner
    
    # Use the session state cleaner
    cleaner = st.session_state.data_cleaner
    
    # Main header with data overview
    st.markdown("## 🧹 Limpieza de Datos")
    
    # Quick data overview
    quality_report = cleaner.get_quality_report()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(replace_emojis("📊 Calidad"), f"{quality_report['quality_score']:.1f}%")
    with col2:
        st.metric(replace_emojis("📈 Filas"), quality_report['total_rows'])
    with col3:
        st.metric("🏷️ Columnas", quality_report['total_columns'])
    with col4:
        missing_count = sum(info['missing_count'] for info in quality_report['missing_values'].values())
        st.metric(replace_emojis("❌ Faltantes"), missing_count)
    
    st.markdown("---")
    
    # Main cleaning interface with better organization
    tab1, tab2, tab3, tab4 = st.tabs([replace_emojis("🚀 Limpieza Rápida"), "🔧 Limpieza Avanzada", "📊 Análisis", "📋 Historial"])
    
    with tab1:
        st.markdown(replace_emojis("### 🚀 Limpieza Rápida"), unsafe_allow_html=True)
        st.markdown("Limpieza automática con configuraciones predefinidas")
        
        # Quick cleaning presets
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(replace_emojis("#### 🎯 Presets de Limpieza"), unsafe_allow_html=True)
            
            if st.button("🧹 Limpieza Básica", use_container_width=True, type="primary"):
                with st.spinner("Aplicando limpieza básica..."):
                    cleaning_options = {
                        'whitespace': True,
                        'case_normalization': True,
                        'duplicates': True,
                        'missing_values': True,
                        'special_characters': False,
                        'accents': False
                    }
                    cleaner.apply_auto_cleaning(cleaning_options)
                    # Update session state cleaner
                    st.session_state.data_cleaner = cleaner
                    st.markdown(replace_emojis("✅ Limpieza básica completada!"), unsafe_allow_html=True)
                    st.rerun()
            
            if st.button("🔧 Limpieza Completa", use_container_width=True):
                    cleaning_options = {
                        'whitespace': True,
                        'case_normalization': True,
                        'special_characters': True,
                        'accents': True,
                        'duplicates': True,
                        'missing_values': True
                    }
                    cleaner.apply_auto_cleaning(cleaning_options)
                    
                    # Apply specific cleanings
                    cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                    cleaner.cleaned_df = cleaner.cleaning_ops.standardize_phone_numbers()
                    cleaner.cleaned_df = cleaner.cleaning_ops.standardize_emails()
                    
                    # Update session state cleaner
                    st.session_state.data_cleaner = cleaner
                    st.markdown(replace_emojis("✅ Limpieza completa finalizada!"), unsafe_allow_html=True)
                    st.rerun()
    
    with col2:
            st.markdown("#### ⚙️ Opciones Personalizadas")
            
            # Collapsible advanced options
            with st.expander(replace_emojis("🔧 Configuración Avanzada")):
                auto_whitespace = st.checkbox("🧹 Limpiar espacios", value=True)
                auto_case = st.checkbox(replace_emojis("📝 Normalizar capitalización"), value=True)
                auto_duplicates = st.checkbox(replace_emojis("🔄 Remover duplicados"), value=True)
                auto_missing = st.checkbox(replace_emojis("❌ Llenar faltantes"), value=True)
                auto_special_chars = st.checkbox(replace_emojis("🔤 Remover caracteres especiales"), value=False)
                auto_accents = st.checkbox("🌍 Normalizar acentos", value=False)
                auto_phones = st.checkbox("📞 Estandarizar teléfonos", value=False)
                auto_emails = st.checkbox("📧 Estandarizar emails", value=False)
                auto_dates = st.checkbox(replace_emojis("📅 Estandarizar fechas"), value=False)
                
                # Advanced options
                if auto_case:
                    auto_case_type = st.selectbox(
                        "Tipo de normalización:",
                        ["lower", "upper", "title", "capitalize"],
                        format_func=lambda x: {
                            "lower": "Minúsculas",
                            "upper": "MAYÚSCULAS", 
                            "title": "Título",
                            "capitalize": "Primera Mayúscula"
                        }[x],
                        key="auto_case_type"
                    )
                
                if auto_phones:
                    auto_phone_format = st.selectbox(
                        "Formato de teléfono:",
                        ["paraguay", "international", "national", "simple"],
                        format_func=lambda x: {
                            "paraguay": "Paraguay (+595 9xx xxxxxx)",
                            "international": "Internacional",
                            "national": "Nacional",
                            "simple": "Simple"
                        }[x],
                        key="auto_phone_format"
                    )
                
                if auto_dates:
                    auto_date_format = st.selectbox(
                        "Formato de fecha:",
                        ["dd/mm/yyyy", "yyyy-mm-dd", "mm/dd/yyyy", "dd-mm-yyyy"],
                        format_func=lambda x: {
                            "dd/mm/yyyy": "DD/MM/YYYY (Recomendado)",
                            "yyyy-mm-dd": "YYYY-MM-DD (ISO)",
                            "mm/dd/yyyy": "MM/DD/YYYY (US)",
                            "dd-mm-yyyy": "DD-MM-YYYY"
                        }[x],
                        key="auto_date_format"
                    )
                
                if st.button("🚀 Aplicar Configuración Personalizada", type="secondary"):
                    with st.spinner("Aplicando limpieza personalizada..."):
                        cleaning_options = {
                            'whitespace': auto_whitespace,
                            'case_normalization': auto_case,
                            'special_characters': auto_special_chars,
                            'accents': auto_accents,
                            'duplicates': auto_duplicates,
                            'missing_values': auto_missing
                        }
                        
                        cleaner.apply_auto_cleaning(cleaning_options)
                        
                        # Apply specific cleanings with custom options
                        if auto_phones:
                            cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                            cleaner.cleaned_df = cleaner.cleaning_ops.standardize_phone_numbers(format_type=auto_phone_format)
                        
                        if auto_emails:
                            cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                            cleaner.cleaned_df = cleaner.cleaning_ops.standardize_emails()
                        
                        if auto_dates:
                            cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                            cleaner.cleaned_df = cleaner.cleaning_ops.standardize_dates(format_type=auto_date_format)
                        
                        # Update session state cleaner
                        st.session_state.data_cleaner = cleaner
                        st.markdown(replace_emojis("✅ Limpieza personalizada completada!"), unsafe_allow_html=True)
                        st.rerun()
    
    with tab2:
        st.markdown(replace_emojis("### 🔧 Limpieza Avanzada"), unsafe_allow_html=True)
        st.markdown("Control granular sobre cada operación de limpieza")
        
        # Initialize global_replacements in session state if not exists
        if 'global_replacements' not in st.session_state:
            st.session_state.global_replacements = {}
        
        # Organized manual cleaning sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🧹 Limpieza de Texto")
            
            # Column selection
            st.markdown("**Seleccionar columnas:**")
            all_columns = cleaner.cleaned_df.columns.tolist()
            text_columns = cleaner.cleaned_df.select_dtypes(include=['object']).columns.tolist()
            
            col_selection = st.selectbox(
                "Aplicar a:",
                ["Todas las columnas de texto", "Columna específica", "Múltiples columnas"],
                key="col_selection"
            )
            
            selected_columns = None
            if col_selection == "Columna específica":
                selected_columns = [st.selectbox("Seleccionar columna:", text_columns, key="single_col")]
            elif col_selection == "Múltiples columnas":
                selected_columns = st.multiselect("Seleccionar columnas:", text_columns, key="multi_col")
            
            # Text cleaning operations
            text_ops = st.container()
            with text_ops:
                if st.button("🧹 Limpiar Espacios", use_container_width=True):
                    cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                    result_df = cleaner.cleaning_ops.clean_whitespace(columns=selected_columns)
                    cleaner.cleaned_df = result_df.copy()
                    st.session_state.data_cleaner = cleaner
                    st.markdown(replace_emojis("✅ Espacios limpiados!"), unsafe_allow_html=True)
                    st.rerun()
                
                # Enhanced case normalization
                st.markdown("**Normalización de capitalización:**")
                case_type = st.selectbox(
                    "Tipo de normalización:",
                    ["lower", "upper", "title", "capitalize"],
                    format_func=lambda x: {
                        "lower": "Minúsculas (lower)",
                        "upper": "MAYÚSCULAS (upper)", 
                        "title": "Título (Title Case)",
                        "capitalize": "Primera Mayúscula (Capitalize)"
                    }[x],
                    key="case_type"
                )
                
                if st.button("📝 Normalizar Capitalización", use_container_width=True):
                    st.rerun()
                
                if st.button("🔤 Remover Caracteres Especiales", use_container_width=True):
                    st.rerun()
                
                if st.button("🌍 Normalizar Acentos", use_container_width=True):
                    cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                    result_df = cleaner.cleaning_ops.normalize_accents(columns=selected_columns)
                    cleaner.cleaned_df = result_df.copy()
                    st.session_state.data_cleaner = cleaner
                    st.markdown(replace_emojis("✅ Acentos normalizados!"), unsafe_allow_html=True)
                    st.rerun()
                
                # Data preview button
                st.markdown("---")
                if st.button("👁️ Vista Previa de Datos", use_container_width=True, type="secondary"):
                    st.markdown(replace_emojis("### 📊 Vista Previa de Datos Limpiados"), unsafe_allow_html=True)
                    st.dataframe(cleaner.cleaned_df.head(10), use_container_width=True)
                    
                    # Show some basic stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(replace_emojis("📊 Filas"), len(cleaner.cleaned_df))
                    with col2:
                        st.metric(replace_emojis("📋 Columnas"), len(cleaner.cleaned_df.columns))
                    with col3:
                        missing_count = cleaner.cleaned_df.isnull().sum().sum()
                        st.metric(replace_emojis("❌ Valores Faltantes"), missing_count)
        
        with col2:
            st.markdown("#### 📞 Estandarización")
            
            # Phone number standardization options
            st.markdown("**Estandarización de teléfonos:**")
            phone_format = st.selectbox(
                "Formato de teléfono:",
                ["paraguay", "international", "national", "simple"],
                format_func=lambda x: {
                    "paraguay": "Paraguay (+595 9xx xxxxxx)",
                    "international": "Internacional (+1-555-123-4567)",
                    "national": "Nacional ((555) 123-4567)",
                    "simple": "Simple (5551234567)"
                }[x],
                key="phone_format"
            )
            
            if st.button("📞 Estandarizar Teléfonos", use_container_width=True):
                cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                result_df = cleaner.cleaning_ops.standardize_phone_numbers(format_type=phone_format)
                cleaner.cleaned_df = result_df.copy()
                st.session_state.data_cleaner = cleaner
                st.markdown(replace_emojis("✅ Teléfonos estandarizados!"), unsafe_allow_html=True)
                st.rerun()
            
            if st.button("📧 Estandarizar Emails", use_container_width=True):
                cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                result_df = cleaner.cleaning_ops.standardize_emails()
                cleaner.cleaned_df = result_df.copy()
                st.session_state.data_cleaner = cleaner
                st.markdown(replace_emojis("✅ Emails estandarizados!"), unsafe_allow_html=True)
                st.rerun()
            
            # Date standardization options
            st.markdown("**Estandarización de fechas:**")
            date_format = st.selectbox(
                "Formato de fecha:",
                ["dd/mm/yyyy", "yyyy-mm-dd", "mm/dd/yyyy", "dd-mm-yyyy"],
                format_func=lambda x: {
                    "dd/mm/yyyy": "DD/MM/YYYY (Recomendado)",
                    "yyyy-mm-dd": "YYYY-MM-DD (ISO)",
                    "mm/dd/yyyy": "MM/DD/YYYY (US)",
                    "dd-mm-yyyy": "DD-MM-YYYY"
                }[x],
                key="date_format"
            )
            
            if st.button("📅 Estandarizar Fechas", use_container_width=True):
                st.rerun()
            
            # Data preview button for standardization section
            st.markdown("---")
            if st.button("👁️ Vista Previa", use_container_width=True, type="secondary"):
                st.markdown(replace_emojis("### 📊 Vista Previa de Datos Estandarizados"), unsafe_allow_html=True)
                st.dataframe(cleaner.cleaned_df.head(10), use_container_width=True)
        
        # Global value replacements in a separate section
        st.markdown("---")
        st.markdown(replace_emojis("#### 🔄 Reemplazos Globales"), unsafe_allow_html=True)
        
        # Column selection for replacements
        st.markdown("**Aplicar reemplazos a:**")
        replacement_scope = st.selectbox(
            "Alcance:",
            ["Todas las columnas", "Solo columnas de texto", "Columna específica"],
            key="replacement_scope"
        )
        
        replacement_columns = None
        if replacement_scope == "Solo columnas de texto":
            replacement_columns = text_columns
        elif replacement_scope == "Columna específica":
            replacement_columns = [st.selectbox("Seleccionar columna:", all_columns, key="replacement_col")]
        
        # Display current replacements in a cleaner way
        if st.session_state.global_replacements:
            st.markdown("**Reemplazos configurados:**")
            for old_val, new_val in st.session_state.global_replacements.items():
                st.write(f"• `{old_val}` → `{new_val}`")
            st.markdown("")
        
        # Replacement input in a cleaner layout
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            old_value = st.text_input("Valor a reemplazar", key="old_value_input", placeholder="ej: null, N/A, etc.")
        with col2:
            new_value = st.text_input("Nuevo valor", key="new_value_input", placeholder="ej: '', Unknown, etc.")
        with col3:
            st.markdown("")  # Spacer
            if st.button("➕ Agregar", use_container_width=True) and old_value and new_value:
                st.session_state.global_replacements[old_value] = new_value
                st.markdown(f"{get_icon("✅", 20)} Reemplazo agregado!", unsafe_allow_html=True)
                st.rerun()
        
        # Action buttons for replacements
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.global_replacements and st.button("🚀 Aplicar Reemplazos", type="primary"):
                cleaner.cleaning_ops.cleaned_df = cleaner.cleaned_df.copy()
                result_df = cleaner.cleaning_ops.replace_values(
                    replacements=st.session_state.global_replacements,
                    columns=replacement_columns
                )
                cleaner.cleaned_df = result_df.copy()
                st.session_state.data_cleaner = cleaner
                st.markdown(replace_emojis("✅ Reemplazos aplicados!"), unsafe_allow_html=True)
                st.rerun()
        
        with col2:
            if st.button("🗑️ Limpiar Reemplazos", use_container_width=True):
                st.session_state.global_replacements = {}
                st.markdown(replace_emojis("✅ Reemplazos limpiados!"), unsafe_allow_html=True)
                st.rerun()
    
    with tab3:
        st.markdown(replace_emojis("### 📊 Análisis de Calidad"), unsafe_allow_html=True)
        st.markdown("Insights detallados sobre la calidad de tus datos")
        
        # Data quality metrics in a cleaner layout
        quality_report = cleaner.get_quality_report()
        
        # Main quality metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(replace_emojis("📊 Calidad General"), f"{quality_report['quality_score']:.1f}%")
        with col2:
            missing_count = sum(info['missing_count'] for info in quality_report['missing_values'].values())
            st.metric(replace_emojis("❌ Valores Faltantes"), missing_count)
        with col3:
            st.metric(replace_emojis("🔄 Duplicados"), quality_report['duplicates']['duplicate_rows'])
        with col4:
            outlier_count = sum(info['outlier_count'] for info in quality_report['outliers'].values())
            st.metric(replace_emojis("📈 Outliers"), outlier_count)
        
        st.markdown("---")
        
        # Detailed analysis sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(replace_emojis("#### 📋 Valores Faltantes por Columna"), unsafe_allow_html=True)
            missing_data = pd.DataFrame(quality_report['missing_values']).T
            missing_data['missing_percent'] = pd.to_numeric(missing_data['missing_percent'], errors='coerce').round(2)
            
            # Show only columns with missing values
            missing_cols = missing_data[missing_data['missing_count'] > 0]
            if not missing_cols.empty:
                st.dataframe(missing_cols[['missing_count', 'missing_percent', 'data_type']], use_container_width=True)
            else:
                st.markdown(replace_emojis("✅ No hay valores faltantes en el dataset"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(replace_emojis("#### 🔄 Análisis de Duplicados"), unsafe_allow_html=True)
            duplicate_info = quality_report['duplicates']
            if duplicate_info['duplicate_rows'] > 0:
                st.warning(f"⚠️ Se encontraron {duplicate_info['duplicate_rows']} filas duplicadas ({duplicate_info['duplicate_percent']:.2f}%)")
            else:
                st.markdown(replace_emojis("✅ No se encontraron duplicados"), unsafe_allow_html=True)
        
        # Cleaning suggestions in a cleaner format
        suggestions = cleaner.get_cleaning_suggestions()
        if suggestions:
            st.markdown("---")
            st.markdown(replace_emojis("#### 💡 Sugerencias de Limpieza"), unsafe_allow_html=True)
            
            # Group suggestions by severity
            high_priority = [s for s in suggestions if s.get('severity') == 'high']
            medium_priority = [s for s in suggestions if s.get('severity') == 'medium']
            low_priority = [s for s in suggestions if s.get('severity') == 'low']
            
            if high_priority:
                st.markdown("**🔴 Alta Prioridad:**")
                for suggestion in high_priority:
                    st.markdown(f"• **{suggestion['description']}**")
                    st.markdown(f"  *{suggestion['action']}*")
            
            if medium_priority:
                st.markdown("**🟡 Prioridad Media:**")
                for suggestion in medium_priority:
                    st.markdown(f"• **{suggestion['description']}**")
                    st.markdown(f"  *{suggestion['action']}*")
            
            if low_priority:
                st.markdown("**🟢 Baja Prioridad:**")
                for suggestion in low_priority:
                    st.markdown(f"• **{suggestion['description']}**")
                    st.markdown(f"  *{suggestion['action']}*")
        else:
            st.markdown(replace_emojis("✅ No se encontraron problemas de calidad significativos"), unsafe_allow_html=True)
    
    with tab4:
        st.markdown(replace_emojis("### 📋 Historial y Control"), unsafe_allow_html=True)
        st.markdown("Seguimiento de operaciones y control de datos")
        
        summary = cleaner.get_cleaning_summary()
        
        # Summary metrics in a cleaner layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(replace_emojis("🔧 Operaciones Realizadas"), summary['total_operations'])
        with col2:
            st.metric("📉 Filas Removidas", summary['rows_removed'])
        with col3:
            st.metric("🗑️ Columnas Removidas", summary['columns_removed'])
        
        st.markdown("---")
        
        # Operations history
        if summary['operations']:
            st.markdown(replace_emojis("#### 📝 Historial de Operaciones"), unsafe_allow_html=True)
            for i, op in enumerate(summary['operations'], 1):
                with st.expander(f"{i}. {op['operation']}", expanded=False):
                    st.markdown(f"**Detalles:** {op['details']}")
                    st.markdown(f"**Timestamp:** {op['timestamp']}")
        else:
            st.markdown(replace_emojis("📝 No se han realizado operaciones de limpieza aún."), unsafe_allow_html=True)
        
        # Reset section
        st.markdown("---")
        st.markdown(replace_emojis("#### 🔄 Control de Datos"), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Resetear a Datos Originales", type="secondary"):
                cleaner.reset_to_original()
                # Clear global replacements
                if 'global_replacements' in st.session_state:
                    st.session_state.global_replacements = {}
                st.markdown(replace_emojis("✅ Datos reseteados a estado original!"), unsafe_allow_html=True)
                st.rerun()
        
        with col2:
            if st.button("💾 Guardar Estado Actual", use_container_width=True):
                # Store current state in session
                st.session_state.saved_cleaned_data = cleaner.cleaned_df.copy()
                st.markdown(replace_emojis("✅ Estado actual guardado!"), unsafe_allow_html=True)
                st.rerun()
    
    # Action buttons for using cleaned data
    st.markdown("---")
    st.markdown(replace_emojis("### 🎯 Acciones con Datos Limpiados"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Usar Datos Limpiados", type="primary", use_container_width=True):
            st.session_state.cleaned_data = cleaner.get_cleaned_data()
            st.session_state.data_quality_completed = True
            st.success("¡Datos limpiados cargados exitosamente!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Resetear a Originales", use_container_width=True):
            st.rerun()
    
    return cleaner.get_cleaned_data()
