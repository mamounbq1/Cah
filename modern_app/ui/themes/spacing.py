"""
Spacing and Layout System
8px grid system with semantic naming
"""

from typing import Dict, Tuple


# Base unit (8px grid system)
BASE_UNIT = 8

# Spacing Scale
SPACING = {
    'none': 0,
    'xxs': BASE_UNIT * 0.5,    # 4px
    'xs': BASE_UNIT * 1,        # 8px
    'sm': BASE_UNIT * 2,        # 16px
    'md': BASE_UNIT * 3,        # 24px
    'lg': BASE_UNIT * 4,        # 32px
    'xl': BASE_UNIT * 5,        # 40px
    'xxl': BASE_UNIT * 6,       # 48px
    'xxxl': BASE_UNIT * 8,      # 64px
}

# Semantic Spacing Names
SEMANTIC_SPACING = {
    # Padding
    'padding_button': SPACING['sm'],                    # 16px
    'padding_card': SPACING['md'],                      # 24px
    'padding_section': SPACING['lg'],                   # 32px
    'padding_page': SPACING['xl'],                      # 40px
    
    # Margins
    'margin_component': SPACING['xs'],                  # 8px
    'margin_element': SPACING['sm'],                    # 16px
    'margin_section': SPACING['md'],                    # 24px
    'margin_page': SPACING['lg'],                       # 32px
    
    # Gaps (for flex/grid layouts)
    'gap_tight': SPACING['xxs'],                        # 4px
    'gap_default': SPACING['xs'],                       # 8px
    'gap_relaxed': SPACING['sm'],                       # 16px
    'gap_loose': SPACING['md'],                         # 24px
}

# Border Radius
RADIUS = {
    'none': 0,
    'xs': 2,
    'sm': 4,
    'md': 8,
    'lg': 12,
    'xl': 16,
    'xxl': 20,
    'full': 9999,  # Fully rounded
}

# Semantic Border Radius
SEMANTIC_RADIUS = {
    'button': RADIUS['md'],                             # 8px
    'input': RADIUS['md'],                              # 8px
    'card': RADIUS['lg'],                               # 12px
    'modal': RADIUS['xl'],                              # 16px
    'badge': RADIUS['full'],                            # Full rounding
    'avatar': RADIUS['full'],                           # Full rounding
}

# Border Width
BORDER_WIDTH = {
    'none': 0,
    'thin': 1,
    'default': 2,
    'thick': 3,
    'heavy': 4,
}

# Shadows (for elevation)
SHADOWS = {
    'none': {
        'offset': (0, 0),
        'blur': 0,
        'spread': 0,
        'opacity': 0,
    },
    'xs': {
        'offset': (0, 1),
        'blur': 2,
        'spread': 0,
        'opacity': 0.05,
    },
    'sm': {
        'offset': (0, 2),
        'blur': 4,
        'spread': 0,
        'opacity': 0.1,
    },
    'md': {
        'offset': (0, 4),
        'blur': 8,
        'spread': 0,
        'opacity': 0.1,
    },
    'lg': {
        'offset': (0, 8),
        'blur': 16,
        'spread': 0,
        'opacity': 0.15,
    },
    'xl': {
        'offset': (0, 12),
        'blur': 24,
        'spread': 0,
        'opacity': 0.2,
    },
    'xxl': {
        'offset': (0, 16),
        'blur': 32,
        'spread': 0,
        'opacity': 0.25,
    },
}

# Z-index layers
Z_INDEX = {
    'base': 0,
    'dropdown': 100,
    'sticky': 200,
    'fixed': 300,
    'modal_backdrop': 400,
    'modal': 500,
    'popover': 600,
    'tooltip': 700,
    'notification': 800,
}

# Component Sizes
COMPONENT_SIZES = {
    'button': {
        'small': {'height': 32, 'padding_x': 12, 'padding_y': 6},
        'medium': {'height': 40, 'padding_x': 16, 'padding_y': 10},
        'large': {'height': 48, 'padding_x': 24, 'padding_y': 14},
    },
    'input': {
        'small': {'height': 32, 'padding_x': 12, 'padding_y': 6},
        'medium': {'height': 40, 'padding_x': 12, 'padding_y': 10},
        'large': {'height': 48, 'padding_x': 16, 'padding_y': 14},
    },
    'avatar': {
        'xs': 24,
        'sm': 32,
        'md': 40,
        'lg': 48,
        'xl': 64,
        'xxl': 96,
    },
    'icon': {
        'xs': 12,
        'sm': 16,
        'md': 20,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
    },
}

# Breakpoints (for responsive design reference)
BREAKPOINTS = {
    'xs': 480,
    'sm': 640,
    'md': 768,
    'lg': 1024,
    'xl': 1280,
    'xxl': 1536,
}

# Container Max Widths
CONTAINER_MAX_WIDTH = {
    'sm': 640,
    'md': 768,
    'lg': 1024,
    'xl': 1280,
    'full': '100%',
}


class SpacingSystem:
    """Spacing system manager"""
    
    def __init__(self):
        """Initialize spacing system"""
        self.base_unit = BASE_UNIT
        self._spacing = SPACING.copy()
        self._radius = RADIUS.copy()
    
    def get_spacing(self, size: str) -> int:
        """
        Get spacing value
        
        Args:
            size: Spacing size name
            
        Returns:
            Spacing value in pixels
        """
        return self._spacing.get(size, self._spacing['md'])
    
    def get_radius(self, size: str) -> int:
        """
        Get border radius value
        
        Args:
            size: Radius size name
            
        Returns:
            Radius value in pixels
        """
        return self._radius.get(size, self._radius['md'])
    
    def get_padding(self, *sizes: str) -> Tuple[int, ...]:
        """
        Get padding tuple for tkinter
        
        Args:
            *sizes: Size names (1-4 values like CSS)
            
        Returns:
            Padding tuple
        """
        if len(sizes) == 1:
            p = self.get_spacing(sizes[0])
            return (p, p, p, p)
        elif len(sizes) == 2:
            py = self.get_spacing(sizes[0])
            px = self.get_spacing(sizes[1])
            return (px, py, px, py)
        elif len(sizes) == 3:
            pt = self.get_spacing(sizes[0])
            px = self.get_spacing(sizes[1])
            pb = self.get_spacing(sizes[2])
            return (px, pt, px, pb)
        elif len(sizes) == 4:
            return tuple(self.get_spacing(s) for s in sizes)
        else:
            return (16, 16, 16, 16)  # Default medium
    
    def scale(self, multiplier: float) -> None:
        """
        Scale all spacing values
        
        Args:
            multiplier: Scaling factor
        """
        self.base_unit = int(BASE_UNIT * multiplier)
        for key in self._spacing:
            self._spacing[key] = int(SPACING[key] * multiplier)
        for key in self._radius:
            if self._radius[key] != 9999:  # Don't scale 'full'
                self._radius[key] = int(RADIUS[key] * multiplier)


# Global spacing instance
_spacing_system = SpacingSystem()


def get_spacing(size: str) -> int:
    """Get spacing value"""
    return _spacing_system.get_spacing(size)


def get_radius(size: str) -> int:
    """Get border radius value"""
    return _spacing_system.get_radius(size)


def get_padding(*sizes: str) -> Tuple[int, ...]:
    """Get padding tuple"""
    return _spacing_system.get_padding(*sizes)


def scale_spacing(multiplier: float) -> None:
    """Scale all spacing"""
    _spacing_system.scale(multiplier)


def get_spacing_system() -> SpacingSystem:
    """Get global spacing system"""
    return _spacing_system
