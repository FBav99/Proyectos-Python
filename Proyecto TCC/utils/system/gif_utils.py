import streamlit as st
import os
from pathlib import Path

from utils.ui.icon_system import get_icon, replace_emojis
def display_gif(gif_path, caption="", width=None, use_container_width=True):
    """
    Display a GIF in Streamlit with proper error handling
    
    Args:
        gif_path (str): Path to the GIF file
        caption (str): Caption to display below the GIF
        width (int): Width of the GIF in pixels (optional)
        use_container_width (bool): Whether to use container width
    """
    try:
        # Check if file exists
        if not os.path.exists(gif_path):
            st.warning(f"⚠️ GIF no encontrado: {gif_path}")
            st.markdown(replace_emojis("📹 Si estas viendo esto, significa que el GIF no esta disponible."), unsafe_allow_html=True)
            return False
        
        # Display the GIF
        if width:
            st.image(gif_path, caption=caption, width=width)
        else:
            st.image(gif_path, caption=caption, use_container_width=use_container_width)
        
        return True
        
    except Exception as e:
        st.markdown(f"{get_icon("❌", 20)} Error al cargar el GIF: {str(e)}", unsafe_allow_html=True)
        return False

def get_gif_path(nivel, gif_name):
    """
    Get the path to a GIF file based on level and name
    
    Args:
        nivel (str): Level number (e.g., "nivel1", "nivel2")
        gif_name (str): Name of the GIF file (without extension)
    
    Returns:
        str: Full path to the GIF file
    """
    base_path = Path("assets/gifs")
    gif_path = base_path / nivel / f"{gif_name}.gif"
    return str(gif_path)

def create_gif_placeholder(nivel, gif_name, description=""):
    """
    Create a placeholder for a GIF that hasn't been created yet
    
    Args:
        nivel (str): Level number
        gif_name (str): Name of the GIF
        description (str): Description of what the GIF should show
    """
    # UI - Intentar Mostrar GIF Placeholder usando Funcion de Imagen de Streamlit
    try:
        # Using a reliable placeholder GIF
        placeholder_url = "https://media1.tenor.com/m/Ta7yC7OAADkAAAAd/fernet-branca.gif"
        
        # Create a styled container with the GIF inside
        st.markdown(f"""
        <div style="background: #f0f2f6; border: 2px dashed #ccc; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
            <h3 style="color: #666; margin-bottom: 0.5rem; text-align: center;">📹 GIF Demostración</h3>
            <p style="color: #888; margin-bottom: 0.5rem; text-align: center; font-size: 0.9rem;">
                <strong>Archivo:</strong> {nivel}/{gif_name}.gif
            </p>
            <p style="color: #666; font-style: italic; text-align: center; margin-bottom: 1rem; font-size: 0.9rem;">
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the GIF inside the container
        st.image(placeholder_url, caption="🎬 Placeholder GIF - Demostración", use_container_width=True)
        
        # Add footer note
        st.markdown(f"""
        <div style="text-align: center; margin-top: 0.5rem;">
            <p style="color: #999; font-size: 0.8rem;">
                💡 Si estas viendo esto, significa que el GIF correspondiente no esta disponible.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        # Fallback if GIF fails to load
        st.markdown(f"""
        <div style="background: #f0f2f6; border: 2px dashed #ccc; border-radius: 10px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <h3 style="color: #666; margin-bottom: 1rem;">📹 GIF Demostración</h3>
            <p style="color: #888; margin-bottom: 1rem;">
                <strong>Archivo:</strong> {nivel}/{gif_name}.gif
            </p>
            <p style="color: #666; font-style: italic;">
                {description}
            </p>
            <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">
                💡 Sube el archivo GIF correspondiente en assets/gifs/{nivel}/ para ver la demostración real
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(replace_emojis("📹 Placeholder para GIF de demostración"), unsafe_allow_html=True)
        st.caption("El GIF real se mostrará cuando subas el archivo correspondiente")

def display_gif_with_fallback(nivel, gif_name, description="", caption="", width=None):
    """
    Display a GIF with fallback to placeholder if not found
    
    Args:
        nivel (str): Level number
        gif_name (str): Name of the GIF file
        description (str): Description for placeholder
        caption (str): Caption for the GIF
        width (int): Width of the GIF
    """
    gif_path = get_gif_path(nivel, gif_name)
    
    if os.path.exists(gif_path):
        display_gif(gif_path, caption, width)
    else:
        create_gif_placeholder(nivel, gif_name, description)

# Predefined GIF configurations for each level
# NOTA: Usamos emojis directos aquí, replace_emojis() se aplica cuando se usa
GIF_CONFIGS = {
    "nivel1": {
        "preparacion_csv": {
            "description": "Demostración de cómo preparar un archivo CSV con la estructura correcta",
            "caption": "📋 Preparación de Archivo CSV"
        },
        "carga_archivo": {
            "description": "Proceso de carga de archivo en la aplicación Streamlit",
            "caption": "📤 Carga de Archivo en Streamlit"
        }
    },
    "nivel2": {
        "filtros_fecha": {
            "description": "Aplicación de filtros de fecha para analizar períodos específicos",
            "caption": "📅 Filtros de Fecha"
        },
        "filtros_categoria": {
            "description": "Uso de filtros de categoría para segmentar datos",
            "caption": "🏷️ Filtros de Categoría"
        },
        "filtros_numericos": {
            "description": "Aplicación de filtros numéricos con deslizadores",
            "caption": "📊 Filtros Numéricos"
        }
    },
    "nivel3": {
        "interpretacion_metricas": {
            "description": "Interpretación de métricas y KPIs del dashboard",
            "caption": "📈 Interpretación de Métricas"
        },
        "analisis_categoria": {
            "description": "Análisis detallado por categorías y regiones",
            "caption": "📊 Análisis por Categoría"
        }
    },
    "nivel4": {
        "calculos_personalizados": {
            "description": "Creación de cálculos personalizados avanzados",
            "caption": "🧮 Cálculos Personalizados"
        },
        "visualizaciones": {
            "description": "Generación de visualizaciones interactivas",
            "caption": "📊 Visualizaciones Avanzadas"
        }
    }
}

def display_level_gif(nivel, gif_name, width=None):
    """
    Display a GIF for a specific level with predefined configuration
    
    Args:
        nivel (str): Level number (e.g., "nivel1")
        gif_name (str): Name of the GIF
        width (int): Width of the GIF
    """
    if nivel in GIF_CONFIGS and gif_name in GIF_CONFIGS[nivel]:
        config = GIF_CONFIGS[nivel][gif_name]
        display_gif_with_fallback(
            nivel, 
            gif_name, 
            config["description"], 
            replace_emojis(config["caption"]), 
            width
        )
    else:
        st.warning(f"⚠️ Configuración no encontrada para {nivel}/{gif_name}")
