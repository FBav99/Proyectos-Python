# Nombre del Archivo: data_cleaning_ops.py
# Descripción: Operaciones de limpieza de datos para la plataforma de análisis de datos TCC - Maneja limpieza de texto, normalización y estandarización
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import pandas as pd
import numpy as np
import re
import unicodedata
from typing import Dict, List, Any, Optional, Union

# ============================================================================
# CLASE DE OPERACIONES DE LIMPIEZA DE DATOS
# ============================================================================

class DataCleaningOperations:
    """Operaciones principales de limpieza de datos"""
    
    # Inicializacion - Inicializar Operaciones de Limpieza
    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.cleaned_df = df.copy()
        self.cleaning_history = []
    
    # Historial - Agregar Operacion al Historial
    def add_to_history(self, operation: str, details: str):
        """Agregar operación al historial de limpieza"""
        self.cleaning_history.append({
            'operation': operation,
            'details': details,
            'timestamp': pd.Timestamp.now()
        })
    
    # Consulta - Obtener Resumen de Limpieza
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Obtener resumen de operaciones de limpieza realizadas"""
        return {
            'total_operations': len(self.cleaning_history),
            'operations': self.cleaning_history,
            'original_shape': self.original_df.shape,
            'cleaned_shape': self.cleaned_df.shape,
            'rows_removed': self.original_df.shape[0] - self.cleaned_df.shape[0],
            'columns_removed': self.original_df.shape[1] - self.cleaned_df.shape[1]
        }
    
    # Limpieza - Limpiar Espacios en Blanco
    def clean_whitespace(self, columns: Optional[List[str]] = None, 
                        remove_leading_trailing: bool = True,
                        normalize_spaces: bool = True,
                        remove_empty_strings: bool = True) -> pd.DataFrame:
        """
        Limpiar espacios en blanco en columnas especificadas
        
        Args:
            columns: Lista de columnas a limpiar. Si es None, aplica a todas las columnas de texto
            remove_leading_trailing: Eliminar espacios al inicio y final
            normalize_spaces: Normalizar múltiples espacios a un solo espacio
            remove_empty_strings: Eliminar cadenas vacías
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Limpieza - Aplicar Limpieza de Espacios en Blanco
                if remove_leading_trailing:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.strip()
                
                if normalize_spaces:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.replace(r'\s+', ' ', regex=True)
                
                if remove_empty_strings:
                    # Conversion - Reemplazar Cadenas Vacías con NaN
                    self.cleaned_df[col] = self.cleaned_df[col].replace(['', 'nan', 'None', 'null', 'N/A'], np.nan)
                
                # Calculo - Contar Cambios Realizados
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Limpieza de espacios en blanco",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Limpieza - Normalizar Mayusculas y Minusculas
    def normalize_text_case(self, columns: Optional[List[str]] = None,
                           case_type: str = 'lower') -> pd.DataFrame:
        """
        Normalizar mayúsculas y minúsculas en texto
        
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
            f"Normalización de mayúsculas/minúsculas ({case_type})",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Limpieza - Remover Caracteres Especiales
    def remove_special_characters(self, columns: Optional[List[str]] = None,
                                keep_alphanumeric: bool = True,
                                keep_spaces: bool = True,
                                keep_punctuation: bool = False) -> pd.DataFrame:
        """
        Remover caracteres especiales de columnas de texto
        
        Args:
            columns: Lista de columnas a procesar
            keep_alphanumeric: Mantener letras y números
            keep_spaces: Mantener espacios
            keep_punctuation: Mantener signos de puntuación
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Procesamiento - Construir Patrón de Expresión Regular
                pattern = r'[^'
                if keep_alphanumeric:
                    pattern += r'a-zA-Z0-9'
                if keep_spaces:
                    pattern += r'\s'
                if keep_punctuation:
                    pattern += r'.,!?;:()[]{}"\'-'
                pattern += r']'
                
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.replace(pattern, '', regex=True)
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Eliminación de caracteres especiales",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Limpieza - Normalizar Acentos
    def normalize_accents(self, columns: Optional[List[str]] = None,
                         remove_accents: bool = True) -> pd.DataFrame:
        """
        Normalizar acentos en texto
        
        Args:
            columns: Lista de columnas a procesar
            remove_accents: Si es True, elimina acentos. Si es False, los normaliza
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                if remove_accents:
                    # Limpieza - Eliminar Acentos
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: ''.join(c for c in unicodedata.normalize('NFD', x)
                                         if not unicodedata.combining(c))
                    )
                else:
                    # Limpieza - Normalizar Acentos
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: unicodedata.normalize('NFC', x)
                    )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Normalización de acentos ({'eliminados' if remove_accents else 'normalizados'})",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Limpieza - Estandarizar Numeros de Telefono
    def standardize_phone_numbers(self, columns: Optional[List[str]] = None,
                                 format_type: str = 'international') -> pd.DataFrame:
        """
        Estandarizar números de teléfono
        
        Args:
            columns: Lista de columnas de números de teléfono
            format_type: 'international', 'national', 'simple', 'paraguay'
        """
        if columns is None:
            # Consulta - Intentar Detectar Columnas que Puedan Contener Números de Teléfono
            # Nota: Usar grupos no capturadores para evitar advertencias
            phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(phone_pattern, regex=True, na=False).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Limpieza - Limpiar y Estandarizar Números de Teléfono
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
    
    # Utilidad - Estandarizar Telefono Interno
    def _standardize_phone(self, phone: str, format_type: str) -> str:
        """Función auxiliar para estandarizar un número de teléfono"""
        if pd.isna(phone) or phone == 'nan':
            return phone
        
        # Limpieza - Eliminar Todos los Caracteres No Numéricos
        digits = re.sub(r'\D', '', str(phone))
        
        if len(digits) == 0:
            return phone
        
        if format_type == 'paraguay':
            # Paraguay format: +595 9xx xxxxxx
            if len(digits) == 9 and digits[0] == '9':
                return f"+595 {digits[0]}{digits[1]}{digits[2]} {digits[3:]}"
            elif len(digits) == 12 and digits[:3] == '595':
                return f"+{digits[:3]} {digits[3:6]} {digits[6:]}"
            elif len(digits) == 11 and digits[:2] == '59':
                return f"+{digits[:3]} {digits[3:6]} {digits[6:]}"
            else:
                return f"+595 {digits}" if len(digits) <= 9 else f"+{digits}"
        elif format_type == 'international':
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
    
    # Limpieza - Estandarizar Emails
    def standardize_emails(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Estandarizar direcciones de correo electrónico
        
        Args:
            columns: Lista de columnas de correo electrónico
        """
        if columns is None:
            # Consulta - Intentar Detectar Columnas de Correo Electrónico
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(email_pattern, regex=True, na=False).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Limpieza - Limpiar y Estandarizar Correos Electrónicos
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                    lambda x: self._standardize_email(x)
                )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Estandarización de correos electrónicos",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Utilidad - Estandarizar Email Interno
    def _standardize_email(self, email: str) -> str:
        """Función auxiliar para estandarizar un correo electrónico"""
        if pd.isna(email) or email == 'nan':
            return email
        
        email = str(email).strip().lower()
        
        # Limpieza - Eliminar Espacios Extra y Normalizar
        email = re.sub(r'\s+', '', email)
        
        return email
    
    # Limpieza - Estandarizar Fechas
    def standardize_dates(self, columns: Optional[List[str]] = None,
                         format_type: str = 'dd/mm/yyyy') -> pd.DataFrame:
        """
        Estandarizar formatos de fecha
        
        Args:
            columns: Lista de columnas de fecha
            format_type: 'dd/mm/yyyy', 'yyyy-mm-dd', 'mm/dd/yyyy', 'dd-mm-yyyy'
        """
        if columns is None:
            # Consulta - Intentar Detectar Columnas de Fecha
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object', 'datetime64']).columns:
                # Validacion - Verificar si la Columna Contiene Patrones Similares a Fechas
                sample_values = self.cleaned_df[col].dropna().astype(str).head(10)
                if any(self._is_date_like(val) for val in sample_values):
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Conversion - Convertir a Fecha Primero, Luego Formatear
                try:
                    # Conversion - Intentar Parsear como Fecha con Inferencia de Formato
                    self.cleaned_df[col] = pd.to_datetime(self.cleaned_df[col], errors='coerce')
                    
                    # Conversion - Formatear Según Formato Especificado
                    if format_type == 'dd/mm/yyyy':
                        self.cleaned_df[col] = self.cleaned_df[col].dt.strftime('%d/%m/%Y')
                    elif format_type == 'yyyy-mm-dd':
                        self.cleaned_df[col] = self.cleaned_df[col].dt.strftime('%Y-%m-%d')
                    elif format_type == 'mm/dd/yyyy':
                        self.cleaned_df[col] = self.cleaned_df[col].dt.strftime('%m/%d/%Y')
                    elif format_type == 'dd-mm-yyyy':
                        self.cleaned_df[col] = self.cleaned_df[col].dt.strftime('%d-%m-%Y')
                    
                    # Conversion - Reemplazar NaT con Valores Originales que No Pudieron Ser Parseados
                    self.cleaned_df[col] = self.cleaned_df[col].fillna(original_values)
                    
                except Exception:
                    # Manejo - Si la Conversión Falla, Mantener Valores Originales
                    self.cleaned_df[col] = original_values
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Estandarización de fechas ({format_type})",
            f"Columnas: {columns}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Validacion - Verificar si es Fecha
    def _is_date_like(self, value: str) -> bool:
        """Verificar si una cadena parece ser una fecha"""
        if pd.isna(value) or value == 'nan':
            return False
        
        value = str(value).strip()
        
        # Procesamiento - Patrones Comunes de Fecha
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # dd/mm/yyyy or dd-mm-yyyy
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',    # yyyy/mm/dd or yyyy-mm-dd
            r'\d{1,2}\s+\w+\s+\d{4}',          # dd Month yyyy
            r'\w+\s+\d{1,2},?\s+\d{4}',        # Month dd, yyyy
        ]
        
        for pattern in date_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        
        return False
    
    # Limpieza - Reemplazar Valores
    def replace_values(self, replacements: Dict[str, str], 
                      columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Reemplazar valores específicos en el conjunto de datos
        
        Args:
            replacements: Diccionario de pares valor_anterior: valor_nuevo
            columns: Lista de columnas a las que aplicar los reemplazos
        """
        if columns is None:
            columns = self.cleaned_df.columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                for old_val, new_val in replacements.items():
                    self.cleaned_df[col] = self.cleaned_df[col].replace(old_val, new_val)
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Reemplazo de valores",
            f"Columnas: {columns}, Reemplazos: {len(replacements)}, Cambios realizados: {changes_made}"
        )
        
        return self.cleaned_df
    
    # Limpieza - Resetear a Datos Originales
    def reset_to_original(self) -> pd.DataFrame:
        """Resetear a datos originales"""
        self.cleaned_df = self.original_df.copy()
        self.cleaning_history = []
        return self.cleaned_df
    
    # Consulta - Obtener Datos Limpiados
    def get_cleaned_data(self) -> pd.DataFrame:
        """Obtener datos limpiados"""
        return self.cleaned_df.copy()
