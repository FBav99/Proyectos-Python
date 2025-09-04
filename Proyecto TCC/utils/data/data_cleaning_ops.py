"""
Data cleaning operations for TCC Data Analysis Platform
Handles text cleaning, normalization, and standardization
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import unicodedata
from typing import Dict, List, Any, Optional, Union

class DataCleaningOperations:
    """Core data cleaning operations"""
    
    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.cleaned_df = df.copy()
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
    
    def clean_whitespace(self, columns: Optional[List[str]] = None, 
                        remove_leading_trailing: bool = True,
                        normalize_spaces: bool = True,
                        remove_empty_strings: bool = True) -> pd.DataFrame:
        """
        Clean whitespace in specified columns
        
        Args:
            columns: List of columns to clean. If None, applies to all text columns
            remove_leading_trailing: Remove leading and trailing spaces
            normalize_spaces: Normalize multiple spaces to single space
            remove_empty_strings: Remove empty strings
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Apply whitespace cleaning
                if remove_leading_trailing:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.strip()
                
                if normalize_spaces:
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).str.replace(r'\s+', ' ', regex=True)
                
                if remove_empty_strings:
                    # Replace empty strings with NaN
                    self.cleaned_df[col] = self.cleaned_df[col].replace(['', 'nan', 'None'], np.nan)
                
                # Count changes
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Whitespace cleaning",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def normalize_text_case(self, columns: Optional[List[str]] = None,
                           case_type: str = 'lower') -> pd.DataFrame:
        """
        Normalize text case (uppercase/lowercase)
        
        Args:
            columns: List of columns to process
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
            f"Text case normalization ({case_type})",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def remove_special_characters(self, columns: Optional[List[str]] = None,
                                keep_alphanumeric: bool = True,
                                keep_spaces: bool = True,
                                keep_punctuation: bool = False) -> pd.DataFrame:
        """
        Remove special characters from text columns
        
        Args:
            columns: List of columns to process
            keep_alphanumeric: Keep letters and numbers
            keep_spaces: Keep spaces
            keep_punctuation: Keep punctuation marks
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Build regex pattern
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
            "Special characters removal",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def normalize_accents(self, columns: Optional[List[str]] = None,
                         remove_accents: bool = True) -> pd.DataFrame:
        """
        Normalize accents in text
        
        Args:
            columns: List of columns to process
            remove_accents: If True, removes accents. If False, normalizes them
        """
        if columns is None:
            columns = self.cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                if remove_accents:
                    # Remove accents
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: ''.join(c for c in unicodedata.normalize('NFD', x)
                                         if not unicodedata.combining(c))
                    )
                else:
                    # Normalize accents
                    self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                        lambda x: unicodedata.normalize('NFC', x)
                    )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Accent normalization ({'removed' if remove_accents else 'normalized'})",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def standardize_phone_numbers(self, columns: Optional[List[str]] = None,
                                 format_type: str = 'international') -> pd.DataFrame:
        """
        Standardize phone numbers
        
        Args:
            columns: List of phone number columns
            format_type: 'international', 'national', 'simple'
        """
        if columns is None:
            # Try to detect columns that might contain phone numbers
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(phone_pattern, regex=True).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Clean and standardize phone numbers
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                    lambda x: self._standardize_phone(x, format_type)
                )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            f"Phone number standardization ({format_type})",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def _standardize_phone(self, phone: str, format_type: str) -> str:
        """Helper function to standardize a phone number"""
        if pd.isna(phone) or phone == 'nan':
            return phone
        
        # Remove all non-numeric characters
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
        Standardize email addresses
        
        Args:
            columns: List of email columns
        """
        if columns is None:
            # Try to detect email columns
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            columns = []
            for col in self.cleaned_df.select_dtypes(include=['object']).columns:
                if self.cleaned_df[col].astype(str).str.contains(email_pattern, regex=True).any():
                    columns.append(col)
        
        changes_made = 0
        
        for col in columns:
            if col in self.cleaned_df.columns:
                original_values = self.cleaned_df[col].copy()
                
                # Clean and standardize emails
                self.cleaned_df[col] = self.cleaned_df[col].astype(str).apply(
                    lambda x: self._standardize_email(x)
                )
                
                changes = (original_values != self.cleaned_df[col]).sum()
                changes_made += changes
        
        self.add_to_history(
            "Email standardization",
            f"Columns: {columns}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def _standardize_email(self, email: str) -> str:
        """Helper function to standardize an email"""
        if pd.isna(email) or email == 'nan':
            return email
        
        email = str(email).strip().lower()
        
        # Remove extra spaces and normalize
        email = re.sub(r'\s+', '', email)
        
        return email
    
    def replace_values(self, replacements: Dict[str, str], 
                      columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Replace specific values in the dataset
        
        Args:
            replacements: Dictionary of old_value: new_value pairs
            columns: List of columns to apply replacements to
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
            "Value replacements",
            f"Columns: {columns}, Replacements: {len(replacements)}, Changes made: {changes_made}"
        )
        
        return self.cleaned_df
    
    def reset_to_original(self) -> pd.DataFrame:
        """Reset to original data"""
        self.cleaned_df = self.original_df.copy()
        self.cleaning_history = []
        return self.cleaned_df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Get cleaned data"""
        return self.cleaned_df.copy()
