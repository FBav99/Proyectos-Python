"""
Emoji to Icon Converter
Herramienta para reemplazar emojis en el código por llamadas al sistema de iconos PNG
"""
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import ast
import json

class EmojiToIconConverter:
    """Convierte emojis en el código a llamadas al sistema de iconos"""
    
    def __init__(self, project_root: str = None):
        """Inicializar el convertidor"""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = Path(project_root)
        self.python_files = []
        self.replacements_made = []
        
        # Importar el sistema de iconos para verificar qué iconos existen
        try:
            import sys
            import os
            # Asegurar que el directorio del proyecto esté en el path
            project_root = Path(__file__).parent.parent.parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            
            from utils.ui.icon_system import icon_system
            self.icon_system = icon_system
            # Verificar que el directorio de iconos existe
            icons_dir = project_root / "assets" / "images" / "icons"
            if not icons_dir.exists():
                # Intentar con ruta relativa
                icons_dir = Path("assets/images/icons")
            self.icon_system.icons_dir = icons_dir
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el sistema de iconos: {e}")
            self.icon_system = None
    
    def find_python_files(self, exclude_dirs: List[str] = None) -> List[Path]:
        """Encontrar todos los archivos Python en el proyecto"""
        if exclude_dirs is None:
            exclude_dirs = ['__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules']
        
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        self.python_files = python_files
        return python_files
    
    def find_emojis_in_code(self, content: str) -> List[Tuple[str, int, str]]:
        """
        Encontrar todos los emojis en el código con su contexto
        Returns: Lista de (emoji, posición, contexto)
        """
        emojis_found = []
        
        # Patrón para encontrar emojis
        emoji_pattern = r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+'
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(emoji_pattern, line)
            for match in matches:
                emoji = match.group()
                start_pos = match.start()
                end_pos = match.end()
                
                # Determinar contexto
                before = line[:start_pos].strip()
                after = line[end_pos:].strip()
                
                context = self._determine_context(before, after, line)
                
                emojis_found.append((emoji, line_num, context))
        
        return emojis_found
    
    def _determine_context(self, before: str, after: str, full_line: str) -> str:
        """Determinar el contexto donde se usa el emoji"""
        line_lower = full_line.lower()
        
        if 'page_icon' in line_lower:
            return 'page_icon'
        elif 'st.markdown' in line_lower or 'markdown' in line_lower:
            return 'markdown'
        elif 'st.title' in line_lower or 'st.header' in line_lower or 'st.subheader' in line_lower:
            return 'title'
        elif 'st.success' in line_lower or 'st.error' in line_lower or 'st.warning' in line_lower or 'st.info' in line_lower:
            return 'message'
        elif 'f"' in line_lower or "f'" in line_lower:
            return 'fstring'
        elif '"' in line_lower or "'" in line_lower:
            return 'string'
        else:
            return 'other'
    
    def icon_exists(self, emoji: str) -> bool:
        """Verificar si existe un icono PNG para el emoji"""
        if self.icon_system:
            return self.icon_system.icon_exists(emoji)
        return False
    
    def convert_page_icon(self, emoji: str) -> str:
        """Convertir emoji en page_icon a uso del sistema de iconos"""
        if self.icon_exists(emoji):
            return f'get_icon("{emoji}", 20)'
        return f'"{emoji}"'  # Mantener emoji si no hay icono PNG
    
    def convert_string_emoji(self, line: str, emoji: str, context: str) -> str:
        """Convertir emoji en string a uso del sistema de iconos"""
        if not self.icon_exists(emoji):
            return line  # No cambiar si no hay icono PNG
        
        # Para page_icon, usar get_icon directamente
        if context == 'page_icon':
            # Reemplazar page_icon="emoji" por page_icon=get_icon("emoji", 20)
            pattern = rf'page_icon\s*=\s*["\']{re.escape(emoji)}["\']'
            replacement = f'page_icon={self.convert_page_icon(emoji)}'
            return re.sub(pattern, replacement, line)
        
        # Para markdown y strings, usar replace_emojis o get_icon
        elif context in ['markdown', 'fstring', 'string', 'title', 'message']:
            # Si es un f-string o string simple, envolver con replace_emojis
            if 'f"' in line or "f'" in line:
                # Para f-strings, necesitamos un enfoque diferente
                # Reemplazar el emoji directamente por la llamada a get_icon
                icon_call = f'{{get_icon("{emoji}", 20)}}'
                return line.replace(emoji, icon_call)
            else:
                # Para strings normales, usar replace_emojis()
                # Necesitamos envolver el string completo
                return self._wrap_string_with_replace_emojis(line, emoji)
        
        return line
    
    def _wrap_string_with_replace_emojis(self, line: str, emoji: str) -> str:
        """Envolver un string con replace_emojis()"""
        # Buscar el string que contiene el emoji
        # Patrón para encontrar strings que contengan el emoji
        pattern = rf'(["\'])([^"\']*{re.escape(emoji)}[^"\']*)\1'
        
        def replace_func(match):
            quote = match.group(1)
            string_content = match.group(2)
            # Verificar si ya está envuelto
            if 'replace_emojis' in line[:match.start()]:
                return match.group(0)
            return f'replace_emojis({quote}{string_content}{quote})'
        
        return re.sub(pattern, replace_func, line)
    
    def convert_file(self, file_path: Path, dry_run: bool = True) -> Tuple[int, List[str]]:
        """Convertir emojis en un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes = []
            lines = content.split('\n')
            new_lines = []
            
            # Verificar si necesita importar get_icon o replace_emojis
            needs_icon_import = False
            has_icon_import = 'from utils.ui.icon_system import' in content or 'import utils.ui.icon_system' in content
            
            for line_num, line in enumerate(lines, 1):
                original_line = line
                emojis = re.findall(r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', line)
                
                if emojis:
                    for emoji in emojis:
                        if self.icon_exists(emoji):
                            context = self._determine_context('', '', line)
                            line = self.convert_string_emoji(line, emoji, context)
                            if line != original_line:
                                needs_icon_import = True
                                changes.append(f"Línea {line_num}: {emoji} -> get_icon()")
                
                new_lines.append(line)
            
            # Agregar import si es necesario
            if needs_icon_import and not has_icon_import and not dry_run:
                # Encontrar dónde agregar el import (después de otros imports)
                import_lines = []
                other_lines = []
                in_imports = True
                
                for i, line in enumerate(new_lines):
                    if in_imports and (line.startswith('import ') or line.startswith('from ')):
                        import_lines.append(line)
                    elif line.strip() == '' and in_imports:
                        import_lines.append(line)
                    else:
                        in_imports = False
                        other_lines.append(line)
                
                # Agregar import después de los otros imports
                import_lines.append('from utils.ui.icon_system import get_icon, replace_emojis')
                new_lines = import_lines + other_lines
            
            new_content = '\n'.join(new_lines)
            
            if not dry_run and new_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.replacements_made.append((str(file_path.relative_to(self.project_root)), len(changes)))
            
            return len(changes), changes
            
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            return 0, []
    
    def convert_all_files(self, dry_run: bool = True):
        """Convertir emojis en todos los archivos"""
        total_changes = 0
        files_modified = 0
        
        for file_path in self.python_files:
            # Saltar el archivo del convertidor mismo
            if 'emoji_to_icon_converter' in str(file_path):
                continue
            
            changes_count, changes = self.convert_file(file_path, dry_run)
            if changes_count > 0:
                total_changes += changes_count
                files_modified += 1
                if dry_run:
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"\n[DRY RUN] {rel_path}:")
                    for change in changes[:5]:  # Mostrar máximo 5 cambios
                        # Usar repr para evitar problemas de codificación con emojis
                        safe_change = change.encode('ascii', 'replace').decode('ascii')
                        print(f"  - {safe_change}")
                    if len(changes) > 5:
                        print(f"  ... y {len(changes) - 5} cambios más")
        
        mode = "DRY RUN" if dry_run else "CONVERTIDO"
        print(f"\n{mode}: {total_changes} cambios en {files_modified} archivos")
        
        return total_changes, files_modified
    
    def generate_conversion_report(self, output_file: str = "emoji_conversion_report.json"):
        """Generar reporte de conversión"""
        report = {
            'files_analyzed': len(self.python_files),
            'emojis_found': {},
            'conversion_status': {}
        }
        
        for file_path in self.python_files:
            if 'emoji_to_icon_converter' in str(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                emojis = self.find_emojis_in_code(content)
                if emojis:
                    rel_path = str(file_path.relative_to(self.project_root))
                    report['conversion_status'][rel_path] = {
                        'total_emojis': len(emojis),
                        'emojis': {}
                    }
                    
                    for emoji, line_num, context in emojis:
                        if emoji not in report['emojis_found']:
                            report['emojis_found'][emoji] = {
                                'count': 0,
                                'has_icon': self.icon_exists(emoji),
                                'locations': []
                            }
                        
                        report['emojis_found'][emoji]['count'] += 1
                        report['emojis_found'][emoji]['locations'].append({
                            'file': rel_path,
                            'line': line_num,
                            'context': context
                        })
                        
                        if emoji not in report['conversion_status'][rel_path]['emojis']:
                            report['conversion_status'][rel_path]['emojis'][emoji] = []
                        report['conversion_status'][rel_path]['emojis'][emoji].append({
                            'line': line_num,
                            'context': context,
                            'can_convert': self.icon_exists(emoji)
                        })
            except Exception as e:
                print(f"Error analizando {file_path}: {e}")
        
        # Guardar reporte
        report_path = self.project_root / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nReporte generado: {report_path}")
        return report


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convertir emojis a iconos PNG en el proyecto')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Solo mostrar cambios sin aplicarlos (default)')
    parser.add_argument('--apply', action='store_true', help='Aplicar cambios (sin esto solo hace dry-run)')
    parser.add_argument('--report', action='store_true', help='Generar reporte de conversión')
    
    args = parser.parse_args()
    
    converter = EmojiToIconConverter()
    converter.find_python_files()
    
    if args.report:
        report = converter.generate_conversion_report()
        print(f"\nTotal de archivos analizados: {report['files_analyzed']}")
        print(f"Total de emojis únicos encontrados: {len(report['emojis_found'])}")
        
        emojis_with_icons = sum(1 for e in report['emojis_found'].values() if e['has_icon'])
        print(f"Emojis con iconos PNG disponibles: {emojis_with_icons}")
        print(f"Emojis sin iconos PNG: {len(report['emojis_found']) - emojis_with_icons}")
    
    if not args.report:
        dry_run = not args.apply
        if dry_run:
            print("=== MODO DRY RUN - No se realizarán cambios ===")
            print("Usa --apply para aplicar los cambios\n")
        
        converter.convert_all_files(dry_run=dry_run)
        
        if not dry_run:
            print("\n✅ Conversión completada")
            print("⚠️  Revisa los archivos modificados y prueba la aplicación")
        else:
            print("\n💡 Ejecuta con --apply para aplicar los cambios")


if __name__ == "__main__":
    main()

