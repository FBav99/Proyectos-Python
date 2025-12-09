import pandas as pd
import io
from datetime import datetime

def export_data(df, filters_applied, metrics):
    """Crear funcionalidad de exportación"""
    buffer = io.BytesIO()
    
    # Archivo - Crear Archivo Excel con Multiples Hojas
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos_Filtrados', index=False)
        
        # Agregar hoja de resumen
        summary_df = pd.DataFrame([metrics])
        summary_df.to_excel(writer, sheet_name='Metricas_Resumen', index=False)
        
        # Agregar información de filtros
        filter_info = pd.DataFrame([filters_applied])
        filter_info.to_excel(writer, sheet_name='Filtros_Aplicados', index=False)
    
    buffer.seek(0)
    return buffer

def create_summary_report(df, filters_applied, metrics):
    """Crear reporte de resumen en formato texto"""
    summary_text = f"""
# Reporte Resumen de Análisis de Datos
Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Filtros Aplicados
{filters_applied if filters_applied else 'No se aplicaron filtros'}

## Métricas Clave
"""
    
    # Procesamiento - Agregar Metricas Disponibles de Forma Dinamica
    if 'total_value' in metrics:
        summary_text += f"- Valor Total: ${metrics['total_value']:,.2f}\n"
    
    if 'avg_value' in metrics:
        summary_text += f"- Valor Promedio: ${metrics['avg_value']:.2f}\n"
    
    if 'max_value' in metrics:
        summary_text += f"- Valor Máximo: ${metrics['max_value']:,.2f}\n"
    
    if 'min_value' in metrics:
        summary_text += f"- Valor Mínimo: ${metrics['min_value']:,.2f}\n"
    
    if 'total_value_2' in metrics:
        summary_text += f"- Valor Total 2: ${metrics['total_value_2']:,.2f}\n"
    
    if 'avg_value_2' in metrics:
        summary_text += f"- Valor Promedio 2: ${metrics['avg_value_2']:.2f}\n"
    
    if 'unique_categories' in metrics:
        summary_text += f"- Categorías Únicas: {metrics['unique_categories']}\n"
    
    if 'most_common_category' in metrics:
        summary_text += f"- Categoría Más Común: {metrics['most_common_category']}\n"
    
    if 'date_range_days' in metrics:
        summary_text += f"- Rango de Días: {metrics['date_range_days']} días\n"
    
    if 'monthly_growth' in metrics:
        summary_text += f"- Crecimiento Mensual: {metrics['monthly_growth']:.1f}%\n"
    
    if 'best_day' in metrics:
        summary_text += f"- Mejor Día: {metrics['best_day'].strftime('%Y-%m-%d')}\n"
    
    if 'best_day_value' in metrics:
        summary_text += f"- Valor del Mejor Día: ${metrics['best_day_value']:,.2f}\n"

    summary_text += f"""
## Resumen de Datos
- Total de Registros: {len(df):,}
- Total de Columnas: {len(df.columns)}
"""
    
    if 'Date' in df.columns:
        summary_text += f"- Rango de Fechas: {df['Date'].min().strftime('%Y-%m-%d')} hasta {df['Date'].max().strftime('%Y-%m-%d')}\n"
    
    return summary_text

def get_csv_data(df):
    """Obtener datos en formato CSV"""
    return df.to_csv(index=False) 