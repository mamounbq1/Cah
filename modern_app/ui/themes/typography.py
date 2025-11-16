"""
Modern Typography System
Apple/Microsoft-inspired font hierarchy with SF Pro fallbacks
"""

from typing import Tuple, Dict, List


# Font Families with Fallbacks
FONT_FAMILIES = {
    'display': 'SF Pro Display',        # For large headings
    'text': 'SF Pro Text',              # For body text
    'mono': 'SF Mono',                  # For code/monospace
    'system': 'Segoe UI',               # Windows fallback
    'fallback': 'Helvetica Neue',      # Universal fallback
}

# Build fallback chain
def get_font_family(primary: str) -> str:
    """Get font family with complete fallback chain"""
    families = [
        FONT_FAMILIES.get(primary, primary),
        FONT_FAMILIES['system'],
        FONT_FAMILIES['fallback'],
        'Arial',
        'sans-serif'
    ]
    return ', '.join(families)


# Font Weights
FONT_WEIGHTS = {
    'thin': 100,
    'light': 300,
    'regular': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700,
    'heavy': 800,
    'black': 900,
}

# Tkinter doesn't support numeric weights, so we map them
TK_WEIGHTS = {
    'thin': 'normal',
    'light': 'normal',
    'regular': 'normal',
    'medium': 'normal',
    'semibold': 'bold',
    'bold': 'bold',
    'heavy': 'bold',
    'black': 'bold',
}


class FontStyle:
    """Represents a complete font style specification"""
    
    def __init__(
        self,
        family: str,
        size: int,
        weight: str = 'regular',
        line_height: float = 1.5
    ):
        """
        Initialize font style
        
        Args:
            family: Font family name
            size: Font size in points
            weight: Font weight name
            line_height: Line height multiplier
        """
        self.family = family
        self.size = size
        self.weight = weight
        self.line_height = line_height
    
    def to_tkinter(self) -> Tuple[str, int, str]:
        """
        Convert to tkinter font format
        
        Returns:
            (family, size, weight) tuple
        """
        tk_weight = TK_WEIGHTS.get(self.weight, 'normal')
        return (FONT_FAMILIES.get(self.family, self.family), self.size, tk_weight)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'family': self.family,
            'size': self.size,
            'weight': self.weight,
            'line_height': self.line_height,
        }


# Typography Scale - iOS/macOS inspired
TYPOGRAPHY = {
    # Display styles (48-64px) - Hero sections
    'display_large': FontStyle('display', 64, 'bold', 1.2),
    'display': FontStyle('display', 48, 'bold', 1.2),
    'display_small': FontStyle('display', 40, 'bold', 1.3),
    
    # Headings (20-36px)
    'h1': FontStyle('display', 36, 'bold', 1.3),
    'h2': FontStyle('display', 28, 'bold', 1.3),
    'h3': FontStyle('display', 24, 'semibold', 1.4),
    'h4': FontStyle('text', 20, 'semibold', 1.4),
    'h5': FontStyle('text', 18, 'semibold', 1.4),
    'h6': FontStyle('text', 16, 'semibold', 1.4),
    
    # Body text (13-17px)
    'body_large': FontStyle('text', 17, 'regular', 1.5),
    'body': FontStyle('text', 15, 'regular', 1.5),
    'body_medium': FontStyle('text', 15, 'medium', 1.5),
    'body_bold': FontStyle('text', 15, 'semibold', 1.5),
    'body_small': FontStyle('text', 13, 'regular', 1.5),
    
    # Specialized
    'button': FontStyle('text', 15, 'semibold', 1.0),
    'button_large': FontStyle('text', 17, 'semibold', 1.0),
    'button_small': FontStyle('text', 13, 'semibold', 1.0),
    
    'caption': FontStyle('text', 12, 'regular', 1.4),
    'caption_bold': FontStyle('text', 12, 'semibold', 1.4),
    'caption_small': FontStyle('text', 11, 'regular', 1.3),
    
    'label': FontStyle('text', 14, 'medium', 1.0),
    'label_small': FontStyle('text', 12, 'medium', 1.0),
    
    # Monospace
    'code': FontStyle('mono', 13, 'regular', 1.6),
    'code_large': FontStyle('mono', 15, 'regular', 1.6),
    'code_small': FontStyle('mono', 11, 'regular', 1.6),
}


class Typography:
    """
    Typography system manager
    """
    
    def __init__(self):
        """Initialize typography system"""
        self._styles = TYPOGRAPHY.copy()
    
    def get(self, style_name: str) -> FontStyle:
        """
        Get font style by name
        
        Args:
            style_name: Name of the typography style
            
        Returns:
            FontStyle instance
            
        Raises:
            KeyError: If style name not found
        """
        if style_name not in self._styles:
            # Fallback to body style
            return self._styles['body']
        return self._styles[style_name]
    
    def get_tk_font(self, style_name: str) -> Tuple[str, int, str]:
        """
        Get tkinter font tuple
        
        Args:
            style_name: Name of the typography style
            
        Returns:
            (family, size, weight) tuple for tkinter
        """
        style = self.get(style_name)
        return style.to_tkinter()
    
    def add_custom_style(
        self,
        name: str,
        family: str,
        size: int,
        weight: str = 'regular',
        line_height: float = 1.5
    ) -> None:
        """
        Add a custom typography style
        
        Args:
            name: Style name
            family: Font family
            size: Font size
            weight: Font weight
            line_height: Line height multiplier
        """
        self._styles[name] = FontStyle(family, size, weight, line_height)
    
    def get_all_styles(self) -> Dict[str, FontStyle]:
        """Get all typography styles"""
        return self._styles.copy()
    
    def scale_sizes(self, multiplier: float) -> None:
        """
        Scale all font sizes by a multiplier
        Useful for accessibility/zoom
        
        Args:
            multiplier: Size multiplier (e.g., 1.2 for 20% larger)
        """
        for style in self._styles.values():
            style.size = int(style.size * multiplier)


# Global typography instance
_typography = Typography()


def get_font(style_name: str) -> Tuple[str, int, str]:
    """
    Convenience function to get tkinter font
    
    Args:
        style_name: Typography style name
        
    Returns:
        (family, size, weight) tuple
    """
    return _typography.get_tk_font(style_name)


def get_font_style(style_name: str) -> FontStyle:
    """
    Get FontStyle object
    
    Args:
        style_name: Typography style name
        
    Returns:
        FontStyle instance
    """
    return _typography.get(style_name)


def scale_typography(multiplier: float) -> None:
    """
    Scale all typography sizes
    
    Args:
        multiplier: Size multiplier
    """
    _typography.scale_sizes(multiplier)


def get_typography() -> Typography:
    """Get global typography instance"""
    return _typography


# Export commonly used font tuples for convenience
FONTS = {
    name: _typography.get_tk_font(name)
    for name in TYPOGRAPHY.keys()
}
