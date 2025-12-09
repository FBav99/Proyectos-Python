"""
Icon System for replacing emojis with PNG images
"""
import streamlit as st
import os
from pathlib import Path

class IconSystem:
    """System for managing and displaying icons instead of emojis"""
    
    def __init__(self):
        self.icons_dir = Path("assets/images/icons")
        self.emoji_to_icon = {
            # Navigation & Levels
            "🌟": "star.png",
            "🎯": "target.png", 
            "📚": "book.png",
            "🔍": "search.png",
            "📊": "chart.png",
            "🚀": "rocket.png",
            
            # Data Types
            "📈": "trending_up.png",
            "🔢": "numbers.png",
            "🔤": "text.png",
            "📅": "calendar.png",
            "💰": "money.png",
            
            # Actions
            "💡": "lightbulb.png",
            "📝": "edit.png",
            "🎮": "game.png",
            "🎉": "celebration.png",
            "📋": "clipboard.png",
            
            # Status
            "✅": "check.png",
            "⏳": "loading.png",
            "🔐": "lock.png",
            "❌": "error.png",
            
            # UI Elements
            "📁": "folder.png",
            "📄": "document.png",
            "🎥": "video.png",
            "📹": "camera.png",
            "🔄": "refresh.png",
            "🔒": "locked.png",
            "👤": "user.png",
            "🎓": "graduation.png",
            "🏗️": "construction.png",
            "📢": "announcement.png",
            "🔧": "settings.png",
            "📤": "upload.png",
            "🎨": "palette.png",
            "🧮": "calculator.png",
            "🤝": "handshake.png",
            "🏆": "trophy.png"
        }
        self._path_cache = {}
        self._exists_cache = {}
    
    def get_icon_path(self, emoji: str) -> str:
        """Get the path to the icon file for a given emoji"""
        if emoji in self._path_cache:
            return self._path_cache[emoji]
        if emoji in self.emoji_to_icon:
            path = str(self.icons_dir / self.emoji_to_icon[emoji])
        else:
            path = None
        self._path_cache[emoji] = path
        return path
    
    def icon_exists(self, emoji: str) -> bool:
        """Check if an icon file exists for the given emoji"""
        if emoji in self._exists_cache:
            return self._exists_cache[emoji]
        icon_path = self.get_icon_path(emoji)
        exists = bool(icon_path and os.path.exists(icon_path))
        self._exists_cache[emoji] = exists
        return exists
    
    def display_icon(self, emoji: str, size: int = 20, alt_text: str = None) -> str:
        """
        Display an icon instead of emoji
        Returns HTML img tag or fallback to emoji if icon doesn't exist
        """
        if self.icon_exists(emoji):
            icon_path = self.get_icon_path(emoji)
            # Convert Windows backslashes to forward slashes for web URLs
            icon_path = icon_path.replace('\\', '/') if icon_path else None
            alt = alt_text or emoji
            return f'<img src="{icon_path}" alt="{alt}" width="{size}" height="{size}" style="vertical-align: middle; margin-right: 4px;">'
        else:
            # Fallback to emoji if icon doesn't exist
            return emoji
    
    def replace_emojis_in_text(self, text: str, size: int = 20) -> str:
        """Replace all emojis in text with icon images"""
        result = text
        for emoji, icon_file in self.emoji_to_icon.items():
            if emoji in result and self.icon_exists(emoji):
                icon_html = self.display_icon(emoji, size)
                result = result.replace(emoji, icon_html)
        return result

# Global instance
icon_system = IconSystem()

def get_icon(emoji: str, size: int = 20, alt_text: str = None) -> str:
    """Convenience function to get an icon"""
    return icon_system.display_icon(emoji, size, alt_text)

def replace_emojis(text: str, size: int = 20) -> str:
    """Convenience function to replace emojis in text"""
    return icon_system.replace_emojis_in_text(text, size)

def get_emoji_only(text: str) -> str:
    """
    Extract emojis from text without converting to HTML
    Use this for component labels (st.button, st.text_input, etc.) that don't support HTML
    """
    # Procesamiento - Retornar Texto Tal Como Esta (Emojis se Mostraran Nativamente)
    # Nota: Placeholder para Logica Futura si se Necesita
    return text
