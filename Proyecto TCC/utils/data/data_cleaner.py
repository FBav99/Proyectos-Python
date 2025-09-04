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
        
        if cleaning_options.get('whitespace', False):
            self.cleaned_df = self.cleaning_ops.clean_whitespace()
            self.add_to_history("Auto whitespace cleaning", "Applied to all text columns")
        
        if cleaning_options.get('case_normalization', False):
            self.cleaned_df = self.cleaning_ops.normalize_text_case(case_type='lower')
            self.add_to_history("Auto case normalization", "Applied to all text columns")
        
        if cleaning_options.get('special_characters', False):
            self.cleaned_df = self.cleaning_ops.remove_special_characters()
            self.add_to_history("Auto special character removal", "Applied to all text columns")
        
        if cleaning_options.get('accents', False):
            self.cleaned_df = self.cleaning_ops.normalize_accents()
            self.add_to_history("Auto accent normalization", "Applied to all text columns")
        
        if cleaning_options.get('duplicates', False):
            self.cleaned_df, removed_count = self.validation.remove_duplicates()
            self.add_to_history("Auto duplicate removal", f"Removed {removed_count} duplicate rows")
        
        if cleaning_options.get('missing_values', False):
            self.cleaned_df = self.validation.fill_missing_values(method='auto')
            self.add_to_history("Auto missing value filling", "Applied auto-fill method")
        
        return self.cleaned_df
    
    def reset_to_original(self) -> pd.DataFrame:
        """Reset to original data"""
        self.cleaned_df = self.original_df.copy()
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
    st.markdown("## 🧹 Limpieza Automática de Datos")
    st.markdown("### Configura las opciones de limpieza para tus datos")
    
    # Initialize cleaner
    cleaner = DataCleaner(df)
    
    # Automatic cleaning options
    st.markdown("### ⚙️ Opciones de Limpieza Automática")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_whitespace = st.checkbox("🧹 Limpiar espacios en blanco", value=True)
        auto_case = st.checkbox("📝 Normalizar mayúsculas/minúsculas", value=True)
        auto_duplicates = st.checkbox("🔄 Remover duplicados", value=True)
        auto_missing = st.checkbox("❌ Llenar valores faltantes", value=True)
    
    with col2:
        auto_special_chars = st.checkbox("🔤 Remover caracteres especiales", value=False)
        auto_accents = st.checkbox("🌍 Normalizar acentos", value=False)
        auto_phones = st.checkbox("📞 Estandarizar teléfonos", value=False)
        auto_emails = st.checkbox("📧 Estandarizar emails", value=False)
    
    # Apply automatic cleaning
    if st.button("🚀 Aplicar Limpieza Automática", type="primary"):
        with st.spinner("Aplicando limpieza automática..."):
            cleaning_options = {
                'whitespace': auto_whitespace,
                'case_normalization': auto_case,
                'special_characters': auto_special_chars,
                'accents': auto_accents,
                'duplicates': auto_duplicates,
                'missing_values': auto_missing
            }
            
            cleaner.apply_auto_cleaning(cleaning_options)
            
            # Apply specific cleanings
            if auto_phones:
                cleaner.cleaned_df = cleaner.cleaning_ops.standardize_phone_numbers()
                cleaner.add_to_history("Phone standardization", "Applied to detected phone columns")
            
            if auto_emails:
                cleaner.cleaned_df = cleaner.cleaning_ops.standardize_emails()
                cleaner.add_to_history("Email standardization", "Applied to detected email columns")
            
            st.success("✅ Limpieza automática completada!")
    
    # Create tabs for different cleaning operations
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Análisis", "🧹 Limpieza Manual", "📊 Calidad", "📋 Historial"])
    
    with tab1:
        st.markdown("#### Análisis de Datos")
        
        # Data quality report
        quality_report = cleaner.get_quality_report()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Calidad General", f"{quality_report['quality_score']:.1f}%")
        with col2:
            st.metric("📈 Filas", quality_report['total_rows'])
        with col3:
            st.metric("🏷️ Columnas", quality_report['total_columns'])
        
        # Missing values analysis
        st.markdown("**Valores Faltantes:**")
        missing_data = pd.DataFrame(quality_report['missing_values']).T
        missing_data['missing_percent'] = missing_data['missing_percent'].round(2)
        st.dataframe(missing_data[['missing_count', 'missing_percent', 'data_type']])
        
        # Duplicates analysis
        st.markdown("**Duplicados:**")
        duplicate_info = quality_report['duplicates']
        st.metric("Filas duplicadas", duplicate_info['duplicate_rows'])
        st.metric("Porcentaje duplicados", f"{duplicate_info['duplicate_percent']:.2f}%")
    
    with tab2:
        st.markdown("#### Limpieza Manual")
        
        # Manual cleaning options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Limpieza de Texto:**")
            if st.button("🧹 Limpiar Espacios"):
                cleaner.cleaned_df = cleaner.cleaning_ops.clean_whitespace()
                st.success("✅ Espacios limpiados!")
            
            if st.button("📝 Normalizar Caso"):
                cleaner.cleaned_df = cleaner.cleaning_ops.normalize_text_case()
                st.success("✅ Caso normalizado!")
            
            if st.button("🔤 Remover Caracteres Especiales"):
                cleaner.cleaned_df = cleaner.cleaning_ops.remove_special_characters()
                st.success("✅ Caracteres especiales removidos!")
        
        with col2:
            st.markdown("**Estandarización:**")
            if st.button("📞 Estandarizar Teléfonos"):
                cleaner.cleaned_df = cleaner.cleaning_ops.standardize_phone_numbers()
                st.success("✅ Teléfonos estandarizados!")
            
            if st.button("📧 Estandarizar Emails"):
                cleaner.cleaned_df = cleaner.cleaning_ops.standardize_emails()
                st.success("✅ Emails estandarizados!")
            
            if st.button("🌍 Normalizar Acentos"):
                cleaner.cleaned_df = cleaner.cleaning_ops.normalize_accents()
                st.success("✅ Acentos normalizados!")
        
        # Global value replacements
        st.markdown("**Reemplazos Globales:**")
        global_replacements = {}
        
        col1, col2 = st.columns(2)
        with col1:
            old_value = st.text_input("Valor a reemplazar")
        with col2:
            new_value = st.text_input("Nuevo valor")
        
        if st.button("Agregar Reemplazo Global") and old_value and new_value:
            global_replacements[old_value] = new_value
            st.success(f"✅ Reemplazo agregado: '{old_value}' → '{new_value}'")
        
        # Apply replacements
        if global_replacements and st.button("Aplicar Reemplazos"):
            cleaner.cleaned_df = cleaner.cleaning_ops.replace_values(replacements=global_replacements)
            st.success("✅ Reemplazos aplicados!")
    
    with tab3:
        st.markdown("#### Calidad de Datos")
        
        # Data quality metrics
        quality_report = cleaner.get_quality_report()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Calidad", f"{quality_report['quality_score']:.1f}%")
        with col2:
            st.metric("❌ Faltantes", sum(info['missing_count'] for info in quality_report['missing_values'].values()))
        with col3:
            st.metric("🔄 Duplicados", quality_report['duplicates']['duplicate_rows'])
        with col4:
            st.metric("📈 Outliers", sum(info['outlier_count'] for info in quality_report['outliers'].values()))
        
        # Cleaning suggestions
        suggestions = cleaner.get_cleaning_suggestions()
        if suggestions:
            st.markdown("**💡 Sugerencias de Limpieza:**")
            for i, suggestion in enumerate(suggestions, 1):
                severity_color = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                st.markdown(f"{i}. {severity_color.get(suggestion['severity'], '⚪')} **{suggestion['description']}**")
                st.markdown(f"   *{suggestion['action']}*")
    
    with tab4:
        st.markdown("#### Historial de Limpieza")
        
        summary = cleaner.get_cleaning_summary()
        
        st.metric("Operaciones realizadas", summary['total_operations'])
        st.metric("Filas removidas", summary['rows_removed'])
        st.metric("Columnas removidas", summary['columns_removed'])
        
        if summary['operations']:
            st.markdown("**Detalle de operaciones:**")
            for i, op in enumerate(summary['operations'], 1):
                st.markdown(f"{i}. **{op['operation']}** - {op['details']}")
    
    # Data comparison
    st.markdown("### 📊 Comparación de Datos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📈 Datos Originales**")
        st.metric("Filas", len(df))
        st.metric("Columnas", len(df.columns))
        st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    with col2:
        st.markdown("**🧹 Datos Limpiados**")
        st.metric("Filas", len(cleaner.cleaned_df))
        st.metric("Columnas", len(cleaner.cleaned_df.columns))
        st.metric("Memoria", f"{cleaner.cleaned_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    with col3:
        st.markdown("**📉 Cambios**")
        st.metric("Filas removidas", len(df) - len(cleaner.cleaned_df))
        st.metric("Columnas removidas", len(df.columns) - len(cleaner.cleaned_df.columns))
        st.metric("Operaciones", summary['total_operations'])
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Usar Datos Limpiados", type="primary"):
            st.session_state.cleaned_data = cleaner.get_cleaned_data()
            st.session_state.data_quality_completed = True
            st.success("¡Datos limpiados cargados exitosamente!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Resetear a Originales"):
            cleaner.reset_to_original()
            st.success("¡Datos reseteados a originales!")
            st.rerun()
    
    with col3:
        if st.button("📤 Subir Nuevo Archivo"):
            st.session_state.data_quality_completed = False
            st.rerun()
    
    return cleaner.get_cleaned_data()
