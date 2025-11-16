"""
Modern Apple-Inspired Color Palette
Professional color system for the School Management application
"""

from typing import Dict


# Primary Brand Colors - iOS Blue
PRIMARY = {
    'blue': '#007AFF',          # Main brand color
    'blue_dark': '#0051D5',     # Pressed state
    'blue_light': '#4DA1FF',    # Hover state
    'blue_ultra_light': '#B3D7FF',  # Disabled state
}

# Neutral Grays - iOS System Grays
NEUTRAL = {
    'black': '#000000',
    'gray_900': '#1C1C1E',      # Almost black
    'gray_800': '#2C2C2E',      # Dark gray
    'gray_700': '#3A3A3C',      # Medium-dark gray
    'gray_600': '#48484A',      # Medium gray
    'gray_500': '#636366',      # Base gray
    'gray_400': '#8E8E93',      # Light-medium gray
    'gray_300': '#AEAEB2',      # Light gray
    'gray_200': '#C7C7CC',      # Very light gray
    'gray_100': '#D1D1D6',      # Ultra light gray
    'gray_50': '#E5E5EA',       # Near white
    'white': '#FFFFFF',
}

# Semantic Colors
SEMANTIC = {
    'success': '#34C759',       # iOS Green
    'success_dark': '#248A3D',
    'success_light': '#81E89E',
    
    'warning': '#FF9500',       # iOS Orange
    'warning_dark': '#C76900',
    'warning_light': '#FFBB66',
    
    'error': '#FF3B30',         # iOS Red
    'error_dark': '#C4221A',
    'error_light': '#FF8F8A',
    
    'info': '#5AC8FA',          # iOS Teal
    'info_dark': '#2A9FC9',
    'info_light': '#A3E3FD',
}

# Additional Accent Colors
ACCENTS = {
    'purple': '#AF52DE',
    'pink': '#FF2D55',
    'indigo': '#5856D6',
    'teal': '#5AC8FA',
    'yellow': '#FFCC00',
    'orange': '#FF9500',
}

# Light Mode Theme
LIGHT_MODE = {
    # Backgrounds
    'background': '#F2F2F7',            # iOS background gray
    'background_secondary': '#E5E5EA',   # Slightly darker
    
    # Surfaces (cards, panels)
    'surface': '#FFFFFF',               # Pure white
    'surface_secondary': '#F9F9F9',     # Off-white
    'surface_hover': '#F5F5F5',         # Hover state
    'surface_pressed': '#EFEFEF',       # Pressed state
    
    # Text
    'text_primary': '#000000',          # Pure black
    'text_secondary': '#8E8E93',        # Gray text
    'text_tertiary': '#AEAEB2',         # Light gray text
    'text_disabled': '#C7C7CC',         # Disabled text
    'text_inverse': '#FFFFFF',          # Text on dark backgrounds
    
    # Borders
    'border': '#C6C6C8',                # Default border
    'border_light': '#E5E5EA',          # Light border
    'border_focus': '#007AFF',          # Focus border
    
    # Shadows
    'shadow': 'rgba(0, 0, 0, 0.1)',
    'shadow_hover': 'rgba(0, 0, 0, 0.15)',
    'shadow_elevated': 'rgba(0, 0, 0, 0.2)',
    
    # Overlays
    'overlay': 'rgba(0, 0, 0, 0.3)',
    'overlay_light': 'rgba(0, 0, 0, 0.15)',
}

# Dark Mode Theme
DARK_MODE = {
    # Backgrounds
    'background': '#000000',            # Pure black
    'background_secondary': '#1C1C1E',  # Elevated black
    
    # Surfaces
    'surface': '#1C1C1E',               # Elevated surface
    'surface_secondary': '#2C2C2E',     # More elevated
    'surface_hover': '#3A3A3C',         # Hover state
    'surface_pressed': '#48484A',       # Pressed state
    
    # Text
    'text_primary': '#FFFFFF',          # Pure white
    'text_secondary': '#8E8E93',        # Gray text (same as light!)
    'text_tertiary': '#636366',         # Darker gray
    'text_disabled': '#48484A',         # Disabled text
    'text_inverse': '#000000',          # Text on light backgrounds
    
    # Borders
    'border': '#38383A',                # Default border
    'border_light': '#2C2C2E',          # Light border
    'border_focus': '#007AFF',          # Focus border (same as light!)
    
    # Shadows
    'shadow': 'rgba(0, 0, 0, 0.3)',
    'shadow_hover': 'rgba(0, 0, 0, 0.4)',
    'shadow_elevated': 'rgba(0, 0, 0, 0.5)',
    
    # Overlays
    'overlay': 'rgba(0, 0, 0, 0.6)',
    'overlay_light': 'rgba(0, 0, 0, 0.4)',
}


class ColorPalette:
    """
    Centralized color management with theme support
    """
    
    def __init__(self, mode: str = 'light'):
        """
        Initialize color palette
        
        Args:
            mode: 'light' or 'dark'
        """
        self.mode = mode
        self._colors = {}
        self._load_colors()
    
    def _load_colors(self) -> None:
        """Load colors based on current mode"""
        base_theme = LIGHT_MODE if self.mode == 'light' else DARK_MODE
        
        self._colors = {
            **PRIMARY,
            **NEUTRAL,
            **SEMANTIC,
            **ACCENTS,
            **base_theme,
        }
    
    def get(self, color_name: str, fallback: str = '#000000') -> str:
        """
        Get color by name
        
        Args:
            color_name: Name of the color
            fallback: Fallback color if not found
            
        Returns:
            Hex color string
        """
        return self._colors.get(color_name, fallback)
    
    def switch_mode(self, mode: str) -> None:
        """
        Switch between light and dark mode
        
        Args:
            mode: 'light' or 'dark'
        """
        self.mode = mode
        self._load_colors()
    
    def get_all(self) -> Dict[str, str]:
        """Get all colors"""
        return self._colors.copy()
    
    @property
    def is_dark_mode(self) -> bool:
        """Check if dark mode is active"""
        return self.mode == 'dark'


# Global palette instance
_palette = ColorPalette('light')


def get_color(name: str, fallback: str = '#000000') -> str:
    """Convenience function to get color"""
    return _palette.get(name, fallback)


def switch_theme(mode: str) -> None:
    """Convenience function to switch theme"""
    _palette.switch_mode(mode)


def get_palette() -> ColorPalette:
    """Get the global palette instance"""
    return _palette
