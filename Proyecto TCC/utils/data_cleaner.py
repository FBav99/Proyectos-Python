import streamlit as st
import pandas as pd
import numpy as np
import re
from typing import Dict, List, Any, Optional, Union
import unicodedata

class DataCleaner:
    """Clase para realizar limpieza automática de datos"""
    
    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.cleaned_df = df.copy()
        self.cleaning_history = []
        
    def add_to_history(self, operation: str, details: str):
        """Agregar operación al historial de limpieza"""
        self.cleaning_history.append({
            'operation': operation,
            'details': details,
            'timestamp': pd.Timestamp.now()
        })
    
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Obtener resumen de las operaciones de limpieza realizadas"""
        return {
            'total_operations': len(self.cleaning_history),
            'operations': self.cleaning_history,
            'original_shape': self.original_df.shape,
            'cleaned_shape': self.cleaned_df.shape,
            'rows_removed': self.original_df.shape[0] - self.cleaned_df.shape[0],
            'columns_removed': self.original_df.shape[1] - self.cleaned_df.shape[1]
        }
    
    def clean_whitespace(self, columns: Optional[List[str]] = None, 
                        remove_leading_trailing: bool = True,
                        normalize_spaces: bool = True,
                        remove_empty_strings: bool = True) -> pd.DataFrame:
        """
        Limpiar espacios en blanco en las columnas especificadas
        
        Args:
            columns: Lista de columnas a limpiar. Si es None, se aplica a todas las columnas de texto
            remove_leading_trailing: Eliminar espacios al inicio y final
            normalize_spaces: Normalizar múltiples espacios a uno solo
            remove_empty_strings: Eliminar cadenas vacías
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Aplicar limpieza de espacios
                if remove_leading_trailing:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.strip()
                
                if normalize_spaces:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.replace(r'\s+', ' ', regex=True)
                
                if remove_empty_strings:
                    # Reemplazar cadenas vacías con NaN
                    self.cleaned_df[col] = self.cleaned_df[col].replace(['', 'nan', 'None'], np.nan)
                
                # Contar cambios
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Limpieza de espacios en blanco",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def normalize_text_case(self, columns: Optional[List[str]] = None,
                           case_type: str = 'lower') -> pd.DataFrame:
        """
        Normalizar el caso del texto (mayúsculas/minúsculas)
        
        Args:
            columns: Lista de columnas a procesar
            case_type: 'lower', 'upper', 'title', 'capitalize'
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                if case_type == 'lower':
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.lower()
                elif case_type == 'upper':
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.upper()
                elif case_type == 'title':
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.title()
                elif case_type == 'capitalize':
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.capitalize()
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Normalización de caso a {case_type}",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def replace_values(self, columns: Optional[List[str]] = None,
                      replacements: Dict[str, Any] = None,
                      custom_replacements: Dict[str, Dict[str, str]] = None) -> pd.DataFrame:
        """
        Reemplazar valores en las columnas especificadas
        
        Args:
            columns: Lista de columnas a procesar
            replacements: Diccionario global de reemplazos {valor_original: valor_nuevo}
            custom_replacements: Diccionario específico por columna {columna: {valor_original: valor_nuevo}}
        """
        if columns is None:
            columns = self.cleaned_df.columns.tolist()
        
        changes_made = 0
        
        # Aplicar reemplazos globales
        if replacements:
            for col in columns:
                if col in self.cleaned_df.columns:
                    original_values = self.cleaned_df[col].copy()
                    self.cleaned_df[col] = self.cleaned_df[col].replace(replacements)
                    changes = (original_values != self.cleaned_df[col]).sum()
                    changes_made += changes
        
        # Aplicar reemplazos específicos por columna
        if custom_replacements:
            for col, col_replacements in custom_replacements.items():
                if col in self.cleaned_df.columns:
                    original_values = self.cleaned_df[col].copy()
                    self.cleaned_df[col] = self.cleaned_df[col].replace(col_replacements)
                    changes = (original_values != self.cleaned_df[col]).sum()
                    changes_made += changes
        
        self.add_to_history(
            "Reemplazo de valores",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def remove_special_characters(self, columns: Optional[List[str]] = None,
                                 keep_alphanumeric: bool = True,
                                 keep_spaces: bool = True,
                                 custom_chars: str = "") -> pd.DataFrame:
        """
        Remover caracteres especiales de las columnas de texto
        
        Args:
            columns: Lista de columnas a procesar
            keep_alphanumeric: Mantener letras y números
            keep_spaces: Mantener espacios
            custom_chars: Caracteres adicionales a mantener
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Construir patrón regex
                pattern = r'[^'
                if keep_alphanumeric:
                    pattern += r'a-zA-Z0-9'
                if keep_spaces:
                    pattern += r'\s'
                pattern += custom_chars + r']'
                
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.replace(pattern, '', regex=True)
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Remoción de caracteres especiales",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def normalize_accents(self, columns: Optional[List[str]] = None,
                         remove_accents: bool = True) -> pd.DataFrame:
        """
        Normalizar acentos en texto
        
        Args:
            columns: Lista de columnas a procesar
            remove_accents: Si True, remueve acentos. Si False, los normaliza
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                if remove_accents:
                    # Remover acentos
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: ''.join(c for c in unicodedata.normalize('NFD', x)
                                         if not unicodedata.combining(c))
                    )
                else:
                    # Normalizar acentos
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: unicodedata.normalize('NFC', x)
                    )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Normalización de acentos ({'removidos' if remove_accents else 'normalizados'})",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def standardize_phone_numbers(self, columns: Optional[List[str]] = None,
                                 format_type: str = 'international') -> pd.DataFrame:
        """
        Estandarizar números de teléfono
        
        Args:
            columns: Lista de columnas de números de teléfono
            format_type: 'international', 'national', 'simple'
        """
        if columns is None:
            # Intentar detectar columnas que podrían contener números de teléfono
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(phone_pattern, regex=True).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Limpiar y estandarizar números de teléfono
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                    lambda x: self._standardize_phone(x, format_type)
                )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Estandarización de números de teléfono ({format_type})",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def _standardize_phone(self, phone: str, format_type: str) -> str:
        """Función auxiliar para estandarizar un número de teléfono"""
        if pd.isna(phone) or phone == 'nan':
            return phone
        
        # Remover todos los caracteres no numéricos
        digits = re.sub(r'\D', '', str(phone))
        
        if len(digits) == 0:
            return phone
        
        if format_type == 'international':
            if len(digits) == 10:
                return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
            elif len(digits) == 11 and digits[0] == '1':
                return f"+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
            else:
                return f"+{digits}"
        elif format_type == 'national':
            if len(digits) == 10:
                return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            else:
                return digits
        else:  # simple
            return digits
    
    def standardize_emails(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Estandarizar direcciones de email
        """
        if columns is None:
            # Intentar detectar columnas que podrían contener emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(email_pattern, regex=True).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Estandarizar emails (minúsculas, sin espacios)
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.lower().str.strip()
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Estandarización de emails",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def remove_duplicates(self, subset: Optional[List[str]] = None,
                         keep: str = 'first') -> pd.DataFrame:
        """
        Remover filas duplicadas
        
        Args:
            subset: Columnas a considerar para identificar duplicados
            keep: 'first', 'last', False
        """
        original_shape = self.cleaned_df.shape
        
        self.cleaned_df = self.cleaned_df.drop_duplicates(subset=subset, keep=keep)
        
        rows_removed = original_shape[0] - self.cleaned_df.shape[0]
        
        self.add_to_history(
            "Remoción de duplicados",
            f"Filas removidas: {rows_removed}, Columnas consideradas: {subset or 'todas'}"
        )
        
        return self.cleaned_df
    
    def fill_missing_values(self, columns: Optional[List[str]] = None,
                           method: str = 'auto',
                           custom_values: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Llenar valores faltantes
        
        Args:
            columns: Lista de columnas a procesar
            method: 'auto', 'mean', 'median', 'mode', 'forward', 'backward'
            custom_values: Diccionario de valores personalizados por columna
        """
        if columns is None:
            columns = self.cleaned_df.columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns and self.cleaned_df[col].isnull().any():
                original_missing = self.cleaned_df[col].isnull().sum()
                
                if custom_values and col in custom_values:
                    # Usar valor personalizado
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(custom_values[col])
                elif method == 'auto':
                    # Detectar automáticamente el mejor método
                    if self.cleaned_df[col].dtype in ['int64', 'float64']:
                        self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].median())
                    else:
                        self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].mode().iloc[0] if not self.cleaned_df[col].mode().empty else 'Desconocido')
                elif method == 'mean' and self.cleaned_df[col].dtype in ['int64', 'float64']:
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].mean())
                elif method == 'median' and self.cleaned_df[col].dtype in ['int64', 'float64']:
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].median())
                elif method == 'mode':
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(self.cleaned_df[col].mode().iloc[0] if not self.cleaned_df[col].mode().empty else 'Desconocido')
                elif method == 'forward':
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(method='ffill')
                elif method == 'backward':
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(method='bfill')
                
                changes_made += original_missing
        
        self.add_to_history(
            f"Llenado de valores faltantes ({method})",
            f"Columnas: {columns}, Valores llenados: {changes_made}"
        )
        
        return self.cleaned_df
    
    def apply_auto_cleaning(self, cleaning_options: Dict[str, bool] = None) -> pd.DataFrame:
        """
        Aplicar limpieza automática basada en opciones predefinidas
        
        Args:
            cleaning_options: Diccionario con opciones de limpieza
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
            self.clean_whitespace()
        
        if cleaning_options.get('case_normalization', False):
            self.normalize_text_case(case_type='lower')
        
        if cleaning_options.get('special_characters', False):
            self.remove_special_characters()
        
        if cleaning_options.get('accents', False):
            self.normalize_accents()
        
        if cleaning_options.get('duplicates', False):
            self.remove_duplicates()
        
        if cleaning_options.get('missing_values', False):
            self.fill_missing_values()
        
        return self.cleaned_df
    
    def reset_to_original(self) -> pd.DataFrame:
        """Resetear a los datos originales"""
        self.cleaned_df = self.original_df.copy()
        self.cleaning_history = []
        return self.cleaned_df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Obtener los datos limpiados"""
        return self.cleaned_df.copy()


def create_data_cleaning_interface(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crear interfaz de Streamlit para limpieza de datos
    
    Args:
        df: DataFrame a limpiar
    
    Returns:
        DataFrame limpiado
    """
    st.markdown("## 🧹 Limpieza Automática de Datos")
    st.markdown("### Configura las opciones de limpieza para tus datos")
    
    # Inicializar limpiador
    cleaner = DataCleaner(df)
    
    # Opciones de limpieza automática
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
    
    # Aplicar limpieza automática
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
            
            # Aplicar limpiezas específicas
            if auto_phones:
                cleaner.standardize_phone_numbers()
            if auto_emails:
                cleaner.standardize_emails()
        
        st.success("✅ Limpieza automática completada!")
    
    # Limpieza manual avanzada
    st.markdown("### 🔧 Limpieza Manual Avanzada")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Texto", "🔄 Reemplazos", "📊 Datos", "📋 Historial"])
    
    with tab1:
        st.markdown("#### Limpieza de Texto")
        
        col1, col2 = st.columns(2)
        with col1:
            text_columns = st.multiselect(
                "Seleccionar columnas de texto",
                cleaner.cleaned_df.select_dtypes(include=['object']).columns.tolist(),
                default=cleaner.cleaned_df.select_dtypes(include=['object']).columns.tolist()[:3]
            )
            
            case_type = st.selectbox(
                "Tipo de normalización de caso",
                ['lower', 'upper', 'title', 'capitalize'],
                index=0
            )
        
        with col2:
            remove_accents = st.checkbox("Remover acentos")
            remove_special = st.checkbox("Remover caracteres especiales")
        
        if st.button("Aplicar Limpieza de Texto"):
            if text_columns:
                cleaner.normalize_text_case(text_columns, case_type)
                if remove_accents:
                    cleaner.normalize_accents(text_columns)
                if remove_special:
                    cleaner.remove_special_characters(text_columns)
                st.success("✅ Limpieza de texto aplicada!")
    
    with tab2:
        st.markdown("#### Reemplazo de Valores")
        
        # Reemplazos globales
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
        
        # Aplicar reemplazos
        if global_replacements and st.button("Aplicar Reemplazos"):
            cleaner.replace_values(replacements=global_replacements)
            st.success("✅ Reemplazos aplicados!")
    
    with tab3:
        st.markdown("#### Limpieza de Datos")
        
        col1, col2 = st.columns(2)
        with col1:
            # Manejo de duplicados
            st.markdown("**Duplicados:**")
            duplicate_subset = st.multiselect(
                "Columnas para identificar duplicados",
                cleaner.cleaned_df.columns.tolist()
            )
            keep_duplicates = st.selectbox("Mantener", ['first', 'last'], index=0)
            
            if st.button("Remover Duplicados"):
                cleaner.remove_duplicates(duplicate_subset, keep_duplicates)
                st.success("✅ Duplicados removidos!")
        
        with col2:
            # Manejo de valores faltantes
            st.markdown("**Valores Faltantes:**")
            missing_method = st.selectbox(
                "Método de llenado",
                ['auto', 'mean', 'median', 'mode', 'forward', 'backward'],
                index=0
            )
            
            if st.button("Llenar Valores Faltantes"):
                cleaner.fill_missing_values(method=missing_method)
                st.success("✅ Valores faltantes llenados!")
    
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
    
    # Comparación de datos
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
    
    # Botones de acción
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
