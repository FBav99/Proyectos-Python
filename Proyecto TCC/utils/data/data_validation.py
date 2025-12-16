# Nombre del Archivo: data_validation.py
# Descripción: Validación de datos y verificaciones de calidad para la plataforma de análisis de datos TCC - Maneja valores faltantes, duplicados, tipos de datos y análisis de calidad
# Autor: Fernando Bavera Villalba
# Fecha: 25/10/2025

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union

class DataValidation:
    """Validación de datos y verificaciones de calidad"""
    
    # Inicializacion - Inicializar Validacion de Datos
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    # Analisis - Analizar Valores Faltantes
    def analyze_missing_values(self) -> Dict[str, Any]:
        """Analizar valores faltantes en el conjunto de datos"""
        missing_info = {}
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            missing_percent = (missing_count / len(self.df)) * 100
            
            missing_info[col] = {
                'missing_count': missing_count,
                'missing_percent': missing_percent,
                'data_type': str(self.df[col].dtype),
                'unique_values': self.df[col].nunique()
            }
        
        return missing_info
    
    # Limpieza - Llenar Valores Faltantes
    def fill_missing_values(self, method: str = 'auto', 
                           columns: Optional[List[str]] = None,
                           custom_values: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Llenar valores faltantes usando varios métodos
        
        Args:
            method: 'auto', 'mean', 'median', 'mode', 'forward', 'backward', 'custom'
            columns: Lista de columnas a procesar
            custom_values: Diccionario de pares columna: valor para llenado personalizado
        """
        if columns is None:
            columns = self.df.columns.tolist()
        
        df_filled = self.df.copy()
        
        for col in columns:
            if col in df_filled.columns and df_filled[col].isnull().any():
                if method == 'auto':
                    # Auto-detect best method based on data type
                    if df_filled[col].dtype in ['int64', 'float64']:
                        fill_value = df_filled[col].median()
                    else:
                        fill_value = df_filled[col].mode().iloc[0] if not df_filled[col].mode().empty else 'Unknown'
                
                elif method == 'mean' and df_filled[col].dtype in ['int64', 'float64']:
                    fill_value = df_filled[col].mean()
                
                elif method == 'median' and df_filled[col].dtype in ['int64', 'float64']:
                    fill_value = df_filled[col].median()
                
                elif method == 'mode':
                    fill_value = df_filled[col].mode().iloc[0] if not df_filled[col].mode().empty else 'Unknown'
                
                elif method == 'forward':
                    df_filled[col] = df_filled[col].fillna(method='ffill')
                    continue
                
                elif method == 'backward':
                    df_filled[col] = df_filled[col].fillna(method='bfill')
                    continue
                
                elif method == 'custom' and custom_values and col in custom_values:
                    fill_value = custom_values[col]
                
                else:
                    fill_value = 'Unknown'
                
                df_filled[col] = df_filled[col].fillna(fill_value)
        
        return df_filled
    
    # Limpieza - Remover Duplicados
    def remove_duplicates(self, subset: Optional[List[str]] = None, 
                         keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows
        
        Args:
            subset: List of columns to consider for duplicates
            keep: 'first', 'last', or False (remove all duplicates)
        """
        df_no_duplicates = self.df.drop_duplicates(subset=subset, keep=keep)
        
        removed_count = len(self.df) - len(df_no_duplicates)
        
        return df_no_duplicates, removed_count
    
    # Analisis - Detectar Outliers
    def detect_outliers(self, columns: Optional[List[str]] = None, 
                       method: str = 'iqr', 
                       threshold: float = 1.5) -> Dict[str, Any]:
        """
        Detect outliers in numeric columns
        
        Args:
            columns: List of numeric columns to analyze
            method: 'iqr' (Interquartile Range) or 'zscore'
            threshold: Threshold for outlier detection
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers_info = {}
        
        for col in columns:
            if col in self.df.columns and self.df[col].dtype in ['int64', 'float64']:
                col_data = self.df[col].dropna()
                
                if method == 'iqr':
                    Q1 = col_data.quantile(0.25)
                    Q3 = col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    
                    outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                
                elif method == 'zscore':
                    z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
                    outliers = col_data[z_scores > threshold]
                
                else:
                    outliers = pd.Series(dtype=object)
                
                outliers_info[col] = {
                    'outlier_count': len(outliers),
                    'outlier_percent': (len(outliers) / len(col_data)) * 100,
                    'outlier_values': outliers.tolist(),
                    'lower_bound': lower_bound if method == 'iqr' else None,
                    'upper_bound': upper_bound if method == 'iqr' else None
                }
        
        return outliers_info
    
    # Analisis - Analizar Tipos de Datos
    def analyze_data_types(self) -> Dict[str, Any]:
        """Analyze data types and suggest optimizations"""
        type_info = {}
        
        for col in self.df.columns:
            current_dtype = str(self.df[col].dtype)
            memory_usage = self.df[col].memory_usage(deep=True)
            
            # Suggest optimizations
            suggestions = []
            
            if current_dtype == 'object':
                unique_ratio = self.df[col].nunique() / len(self.df)
                if unique_ratio < 0.5:
                    suggestions.append("Consider converting to category type")
            
            elif current_dtype == 'int64':
                if self.df[col].min() >= 0 and self.df[col].max() < 255:
                    suggestions.append("Consider converting to uint8")
                elif self.df[col].min() >= -32768 and self.df[col].max() < 32767:
                    suggestions.append("Consider converting to int16")
            
            elif current_dtype == 'float64':
                if self.df[col].dtype == 'float64' and not self.df[col].isnull().any():
                    suggestions.append("Consider converting to float32")
            
            type_info[col] = {
                'current_dtype': current_dtype,
                'memory_usage_bytes': memory_usage,
                'memory_usage_mb': memory_usage / 1024 / 1024,
                'suggestions': suggestions
            }
        
        return type_info
    
    # Validacion - Validar Calidad de Datos
    def validate_data_quality(self) -> Dict[str, Any]:
        """Comprehensive data quality validation"""
        quality_report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.analyze_missing_values(),
            'duplicates': {},
            'data_types': self.analyze_data_types(),
            'outliers': self.detect_outliers(),
            'quality_score': 0
        }
        
        # Check for duplicates
        _, duplicate_count = self.remove_duplicates()
        quality_report['duplicates'] = {
            'duplicate_rows': duplicate_count,
            'duplicate_percent': (duplicate_count / len(self.df)) * 100
        }
        
        # Calculate overall quality score
        quality_score = 100
        
        # Deduct points for missing values
        total_missing = sum(info['missing_count'] for info in quality_report['missing_values'].values())
        missing_penalty = min(30, (total_missing / (len(self.df) * len(self.df.columns))) * 100)
        quality_score -= missing_penalty
        
        # Deduct points for duplicates
        duplicate_penalty = min(20, quality_report['duplicates']['duplicate_percent'])
        quality_score -= duplicate_penalty
        
        # Deduct points for outliers (if too many)
        total_outliers = sum(info['outlier_count'] for info in quality_report['outliers'].values())
        outlier_penalty = min(15, (total_outliers / (len(self.df) * len(self.df.columns))) * 100)
        quality_score -= outlier_penalty
        
        quality_report['quality_score'] = max(0, quality_score)
        
        return quality_report
    
    # Sugerencias - Sugerir Acciones de Limpieza
    def suggest_cleaning_actions(self, quality_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest cleaning actions based on quality report"""
        suggestions = []
        
        # Missing values suggestions
        for col, info in quality_report['missing_values'].items():
            if info['missing_percent'] > 20:
                suggestions.append({
                    'type': 'missing_values',
                    'column': col,
                    'severity': 'high' if info['missing_percent'] > 50 else 'medium',
                    'description': f"Column '{col}' has {info['missing_percent']:.1f}% missing values",
                    'action': f"Consider filling missing values or removing column '{col}'"
                })
        
        # Duplicate suggestions
        if quality_report['duplicates']['duplicate_percent'] > 5:
            suggestions.append({
                'type': 'duplicates',
                'severity': 'medium',
                'description': f"Dataset has {quality_report['duplicates']['duplicate_percent']:.1f}% duplicate rows",
                'action': "Remove duplicate rows to improve data quality"
            })
        
        # Outlier suggestions
        for col, info in quality_report['outliers'].items():
            if info['outlier_percent'] > 10:
                suggestions.append({
                    'type': 'outliers',
                    'column': col,
                    'severity': 'medium',
                    'description': f"Column '{col}' has {info['outlier_percent']:.1f}% outliers",
                    'action': f"Investigate outliers in column '{col}' for data quality issues"
                })
        
        # Data type optimization suggestions
        for col, info in quality_report['data_types'].items():
            if info['suggestions']:
                suggestions.append({
                    'type': 'data_type_optimization',
                    'column': col,
                    'severity': 'low',
                    'description': f"Column '{col}' can be optimized",
                    'action': f"Apply suggestions: {', '.join(info['suggestions'])}"
                })
        
        return suggestions
    
    # Estadisticas - Obtener Estadisticas de Columnas
    def get_column_statistics(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get detailed statistics for columns"""
        if columns is None:
            columns = self.df.columns.tolist()
        
        stats = {}
        
        for col in columns:
            if col in self.df.columns:
                col_data = self.df[col].dropna()
                
                if col_data.dtype in ['int64', 'float64']:
                    stats[col] = {
                        'type': 'numeric',
                        'count': len(col_data),
                        'mean': col_data.mean(),
                        'median': col_data.median(),
                        'std': col_data.std(),
                        'min': col_data.min(),
                        'max': col_data.max(),
                        'q25': col_data.quantile(0.25),
                        'q75': col_data.quantile(0.75),
                        'skewness': col_data.skew(),
                        'kurtosis': col_data.kurtosis()
                    }
                else:
                    stats[col] = {
                        'type': 'categorical',
                        'count': len(col_data),
                        'unique_count': col_data.nunique(),
                        'most_common': col_data.value_counts().head(5).to_dict(),
                        'least_common': col_data.value_counts().tail(5).to_dict()
                    }
        
        return stats
