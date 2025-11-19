"""
Icon Standardizer Tool
Herramienta para reemplazar emojis en bulk con un sistema de iconos estandarizado
"""
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple
import json

class IconStandardizer:
    """Sistema para estandarizar y reemplazar iconos en el proyecto"""
    
    # Mapeo estandarizado de iconos por categoría
    # NOTA: Estos son emojis directos, no llamadas a replace_emojis() porque
    # este diccionario se evalúa en tiempo de importación
    STANDARD_ICONS = {
        # Niveles de Aprendizaje
        'nivel0': '🌟',  # Introducción
        'nivel1': '📚',  # Básico
        'nivel2': '🔍',  # Filtros
        'nivel3': '📊',  # Métricas
        'nivel4': '🚀',  # Avanzado
        
        # Navegación y UI
        'inicio': '🏠',
        'ayuda': '❓',
        'dashboard': '📊',
        'configuracion': '⚙️',
        'usuario': '👤',
        'cerrar_sesion': '🚪',
        
        # Acciones
        'agregar': '➕',
        'eliminar': '🗑️',
        'editar': '📝',
        'guardar': '💾',
        'exportar': '📤',
        'importar': '📥',
        'buscar': '🔍',
        'filtrar': '🔽',
        'actualizar': '🔄',
        'descargar': '⬇️',
        'subir': '⬆️',
        
        # Estados y Feedback
        'exito': '✅',
        'error': '❌',
        'advertencia': '⚠️',
        'informacion': 'ℹ️',
        'cargando': '⏳',
        'completado': '✔️',
        'pendiente': '⏸️',
        
        # Datos y Análisis
        'datos': '📊',
        'grafico': '📈',
        'tabla': '📋',
        'metricas': '📊',
        'calculo': '🧮',
        'estadisticas': '📉',
        'tendencias': '📈',
        
        # Seguridad y Autenticación
        'seguridad': '🔐',
        'bloqueado': '🔒',
        'desbloqueado': '🔓',
        'autenticacion': '🔑',
        'oauth': '🌐',
        
        # Documentación y Contenido
        'documento': '📄',
        'documentacion': '📚',
        'libro': '📖',
        'nota': '📝',
        'archivo': '📁',
        'carpeta': '📂',
        
        # Multimedia
        'video': '🎥',
        'imagen': '🖼️',
        'gif': '🎬',
        'audio': '🔊',
        
        # Sistema
        'configuracion': '⚙️',
        'herramientas': '🔧',
        'ajustes': '🎛️',
        'menu': '☰',
        'cerrar': '✖️',
        'abrir': '➕',
        
        # Progreso y Logros
        'progreso': '📊',
        'logro': '🏆',
        'medalla': '🥇',
        'estrella': '⭐',
        'objetivo': '🎯',
        
        # Comunicación
        'mensaje': '💬',
        'notificacion': '🔔',
        'correo': '📧',
        'compartir': '🔗',
        
        # Tiempo
        'calendario': '📅',
        'reloj': '🕐',
        'historial': '📜',
        
        # Otros
        'idea': '💡',
        'fuego': '🔥',
        'corazon': '❤️',
        'me_gusta': '👍',
        'no_me_gusta': '👎',
        'pregunta': '❓',
        'respuesta': '💬',
        'ayuda': '❓',
        'soporte': '🆘',
    }
    
    # Mapeo de emojis comunes a nombres estandarizados
    # NOTA: Estos son emojis directos como claves
    EMOJI_TO_STANDARD = {
        '📚': 'nivel1',
        '🔍': 'nivel2',
        '📊': 'nivel3',
        '🚀': 'nivel4',
        '🌟': 'nivel0',
        '🏠': 'inicio',
        '❓': 'ayuda',
        '➕': 'agregar',
        '🗑️': 'eliminar',
        '📝': 'editar',
        '💾': 'guardar',
        '📤': 'exportar',
        '📥': 'importar',
        '🔄': 'actualizar',
        '✅': 'exito',
        '❌': 'error',
        '⚠️': 'advertencia',
        'ℹ️': 'informacion',
        '⏳': 'cargando',
        '🔐': 'seguridad',
        '🔒': 'bloqueado',
        '🔓': 'desbloqueado',
        '🔑': 'autenticacion',
        '🌐': 'oauth',
        '📄': 'documento',
        '📁': 'archivo',
        '📂': 'carpeta',
        '🎥': 'video',
        '⚙️': 'configuracion',
        '🔧': 'herramientas',
        '🏆': 'logro',
        '⭐': 'estrella',
        '🎯': 'objetivo',
        '📅': 'calendario',
        '💡': 'idea',
        '📋': 'tabla',
        '🧮': 'calculo',
        '📈': 'grafico',
        '📉': 'estadisticas',
    }
    
    def __init__(self, project_root: str = None):
        """Inicializar el estandarizador de iconos"""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = Path(project_root)
        self.python_files = []
        self.replacements_made = []
        
    def find_python_files(self, exclude_dirs: List[str] = None) -> List[Path]:
        """Encontrar todos los archivos Python en el proyecto"""
        if exclude_dirs is None:
            exclude_dirs = ['__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules']
        
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Excluir directorios
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        self.python_files = python_files
        return python_files
    
    def analyze_icon_usage(self) -> Dict[str, List[Tuple[str, int]]]:
        """Analizar el uso de iconos en el proyecto"""
        usage = {}
        
        for file_path in self.python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        # Buscar emojis en la línea
                        emojis = re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', line)
                        for emoji in emojis:
                            if emoji not in usage:
                                usage[emoji] = []
                            usage[emoji].append((str(file_path.relative_to(self.project_root)), line_num))
            except Exception as e:
                print(f"Error leyendo {file_path}: {e}")
        
        return usage
    
    def generate_replacement_report(self, output_file: str = "icon_replacement_report.json"):
        """Generar un reporte de reemplazos propuestos"""
        usage = self.analyze_icon_usage()
        report = {
            'total_files': len(self.python_files),
            'icons_found': {},
            'suggested_replacements': {},
            'unmapped_emojis': []
        }
        
        for emoji, locations in usage.items():
            report['icons_found'][emoji] = {
                'count': len(locations),
                'locations': locations[:10]  # Limitar a 10 para el reporte
            }
            
            # Sugerir reemplazo estandarizado
            if emoji in self.EMOJI_TO_STANDARD:
                standard_name = self.EMOJI_TO_STANDARD[emoji]
                standard_emoji = self.STANDARD_ICONS.get(standard_name, emoji)
                report['suggested_replacements'][emoji] = {
                    'standard_name': standard_name,
                    'standard_emoji': standard_emoji,
                    'should_replace': emoji != standard_emoji
                }
            else:
                report['unmapped_emojis'].append(emoji)
        
        # Guardar reporte
        report_path = self.project_root / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Reporte generado: {report_path}")
        return report
    
    def replace_in_file(self, file_path: Path, replacements: Dict[str, str], dry_run: bool = True) -> int:
        """Reemplazar iconos en un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_count = 0
            
            for old_emoji, new_emoji in replacements.items():
                if old_emoji in content:
                    count = content.count(old_emoji)
                    content = content.replace(old_emoji, new_emoji)
                    replacements_count += count
            
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.replacements_made.append((str(file_path.relative_to(self.project_root)), replacements_count))
            
            return replacements_count
            
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            return 0
    
    def standardize_icons(self, replacements: Dict[str, str] = None, dry_run: bool = True):
        """Estandarizar iconos en todo el proyecto"""
        if replacements is None:
            # Generar reemplazos automáticos basados en el mapeo
            replacements = {}
            for emoji, standard_name in self.EMOJI_TO_STANDARD.items():
                standard_emoji = self.STANDARD_ICONS.get(standard_name, emoji)
                if emoji != standard_emoji:
                    replacements[emoji] = standard_emoji
        
        total_replacements = 0
        files_modified = 0
        
        for file_path in self.python_files:
            count = self.replace_in_file(file_path, replacements, dry_run)
            if count > 0:
                total_replacements += count
                files_modified += 1
                if dry_run:
                    print(f"[DRY RUN] {file_path.relative_to(self.project_root)}: {count} reemplazos")
        
        mode = "DRY RUN" if dry_run else "ACTUALIZADO"
        print(f"\n{mode}: {total_replacements} reemplazos en {files_modified} archivos")
        
        return total_replacements, files_modified
    
    def create_icon_constants_file(self, output_file: str = "utils/ui/icon_constants.py"):
        """Crear un archivo con constantes de iconos estandarizados"""
        content = '''"""
Icon Constants - Iconos estandarizados del proyecto
Usar estas constantes en lugar de emojis directos para mantener consistencia
"""
from utils.ui.icon_system import get_icon

# Niveles de Aprendizaje
ICON_NIVEL_0 = replace_emojis("🌟")
ICON_NIVEL_1 = replace_emojis("📚")
ICON_NIVEL_2 = replace_emojis("🔍")
ICON_NIVEL_3 = replace_emojis("📊")
ICON_NIVEL_4 = replace_emojis("🚀")

# Navegación
ICON_INICIO = "🏠"
ICON_AYUDA = "❓"
ICON_DASHBOARD = replace_emojis("📊")
ICON_CONFIGURACION = "⚙️"
ICON_USUARIO = replace_emojis("👤")

# Acciones
ICON_AGREGAR = "➕"
ICON_ELIMINAR = "🗑️"
ICON_EDITAR = replace_emojis("📝")
ICON_GUARDAR = "💾"
ICON_EXPORTAR = replace_emojis("📤")
ICON_IMPORTAR = "📥"
ICON_BUSCAR = replace_emojis("🔍")
ICON_ACTUALIZAR = replace_emojis("🔄")

# Estados
ICON_EXITO = replace_emojis("✅")
ICON_ERROR = replace_emojis("❌")
ICON_ADVERTENCIA = "⚠️"
ICON_INFORMACION = "ℹ️"
ICON_CARGANDO = "⏳"

# Seguridad
ICON_SEGURIDAD = replace_emojis("🔐")
ICON_BLOQUEADO = replace_emojis("🔒")
ICON_DESBLOQUEADO = "🔓"
ICON_AUTENTICACION = "🔑"
ICON_OAUTH = "🌐"

# Datos
ICON_DATOS = replace_emojis("📊")
ICON_GRAFICO = replace_emojis("📈")
ICON_TABLA = replace_emojis("📋")
ICON_METRICAS = replace_emojis("📊")
ICON_CALCULO = replace_emojis("🧮")

# Documentación
ICON_DOCUMENTO = replace_emojis("📄")
ICON_DOCUMENTACION = replace_emojis("📚")
ICON_ARCHIVO = replace_emojis("📁")

# Sistema
ICON_CONFIGURACION = "⚙️"
ICON_HERRAMIENTAS = replace_emojis("🔧")
ICON_MENU = "☰"

# Progreso
ICON_PROGRESO = replace_emojis("📊")
ICON_LOGRO = replace_emojis("🏆")
ICON_ESTRELLA = "⭐"
ICON_OBJETIVO = replace_emojis("🎯")

# Tiempo
ICON_CALENDARIO = replace_emojis("📅")

# Otros
ICON_IDEA = replace_emojis("💡")
ICON_PREGUNTA = "❓"

def get_standard_icon(icon_name: str, size: int = 20) -> str:
    """
    Obtener un icono estandarizado por nombre
    
    Args:
        icon_name: Nombre del icono (ej: 'nivel1', 'inicio', 'exito')
        size: Tamaño del icono en píxeles
    
    Returns:
        HTML img tag o emoji como fallback
    """
    icon_map = {
        'nivel0': ICON_NIVEL_0,
        'nivel1': ICON_NIVEL_1,
        'nivel2': ICON_NIVEL_2,
        'nivel3': ICON_NIVEL_3,
        'nivel4': ICON_NIVEL_4,
        'inicio': ICON_INICIO,
        'ayuda': ICON_AYUDA,
        'dashboard': ICON_DASHBOARD,
        'configuracion': ICON_CONFIGURACION,
        'usuario': ICON_USUARIO,
        'agregar': ICON_AGREGAR,
        'eliminar': ICON_ELIMINAR,
        'editar': ICON_EDITAR,
        'guardar': ICON_GUARDAR,
        'exportar': ICON_EXPORTAR,
        'importar': ICON_IMPORTAR,
        'buscar': ICON_BUSCAR,
        'actualizar': ICON_ACTUALIZAR,
        'exito': ICON_EXITO,
        'error': ICON_ERROR,
        'advertencia': ICON_ADVERTENCIA,
        'informacion': ICON_INFORMACION,
        'cargando': ICON_CARGANDO,
        'seguridad': ICON_SEGURIDAD,
        'bloqueado': ICON_BLOQUEADO,
        'desbloqueado': ICON_DESBLOQUEADO,
        'autenticacion': ICON_AUTENTICACION,
        'oauth': ICON_OAUTH,
        'datos': ICON_DATOS,
        'grafico': ICON_GRAFICO,
        'tabla': ICON_TABLA,
        'metricas': ICON_METRICAS,
        'calculo': ICON_CALCULO,
        'documento': ICON_DOCUMENTO,
        'documentacion': ICON_DOCUMENTACION,
        'archivo': ICON_ARCHIVO,
        'herramientas': ICON_HERRAMIENTAS,
        'progreso': ICON_PROGRESO,
        'logro': ICON_LOGRO,
        'estrella': ICON_ESTRELLA,
        'objetivo': ICON_OBJETIVO,
        'calendario': ICON_CALENDARIO,
        'idea': ICON_IDEA,
        'pregunta': ICON_PREGUNTA,
    }
    
    emoji = icon_map.get(icon_name.lower())
    if emoji:
        return get_icon(emoji, size)
    return icon_name  # Fallback
'''
        
        output_path = self.project_root / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Archivo de constantes creado: {output_path}")
        return output_path


def main():
    """Función principal para ejecutar el estandarizador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Estandarizar iconos en el proyecto')
    parser.add_argument('--dry-run', action='store_true', help='Solo mostrar cambios sin aplicarlos')
    parser.add_argument('--analyze', action='store_true', help='Solo analizar uso de iconos')
    parser.add_argument('--report', action='store_true', help='Generar reporte de iconos')
    parser.add_argument('--create-constants', action='store_true', help='Crear archivo de constantes')
    
    args = parser.parse_args()
    
    standardizer = IconStandardizer()
    standardizer.find_python_files()
    
    if args.analyze or args.report:
        report = standardizer.generate_replacement_report()
        print(f"\nTotal de archivos analizados: {report['total_files']}")
        print(f"Total de iconos únicos encontrados: {len(report['icons_found'])}")
        print(f"Emojis sin mapeo: {len(report['unmapped_emojis'])}")
        
        if args.report:
            print("\nReporte guardado en: icon_replacement_report.json")
    
    if args.create_constants:
        standardizer.create_icon_constants_file()
    
    if not args.analyze and not args.report and not args.create_constants:
        # Ejecutar estandarización
        dry_run = args.dry_run
        if dry_run:
            print("=== MODO DRY RUN - No se realizarán cambios ===")
        
        standardizer.standardize_icons(dry_run=dry_run)
        
        if not dry_run:
            print(replace_emojis("\n✅ Estandarización completada"))
        else:
            print(replace_emojis("\n💡 Ejecuta sin --dry-run para aplicar los cambios"))


if __name__ == "__main__":
    main()

