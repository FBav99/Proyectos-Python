import pandas as pd
import io
from datetime import datetime

def export_data(df, filters_applied, metrics):
    """Crear funcionalidad de exportación"""
    buffer = io.BytesIO()
    
    # Crear archivo Excel con múltiples hojas
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
- Ingresos Totales: ${metrics['total_revenue']:,.2f}
- Pedidos Totales: {metrics['total_orders']:,}
- Valor Promedio de Pedido: ${metrics['avg_order_value']:.2f}
- Ganancia Total: ${metrics['total_profit']:,.2f}
- Margen de Ganancia: {metrics['profit_margin']:.1f}%
- Calificación Promedio: {metrics['avg_rating']:.2f}/5.0

## Resumen de Datos
- Total de Registros: {len(df):,}
"""
    
    if 'Date' in df.columns:
        summary_text += f"- Rango de Fechas: {df['Date'].min().strftime('%Y-%m-%d')} hasta {df['Date'].max().strftime('%Y-%m-%d')}\n"
    
    return summary_text

def get_csv_data(df):
    """Obtener datos en formato CSV"""
    return df.to_csv(index=False) 