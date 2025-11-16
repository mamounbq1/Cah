"""
Apple Modern Theme System
Professional, polished theme inspired by Apple's design language

This theme provides a complete styling system for all tkinter/ttk widgets
with support for light/dark modes, smooth transitions, and modern aesthetics.
"""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Optional, Callable, List

from .colors import ColorPalette, LIGHT_MODE, DARK_MODE, PRIMARY, SEMANTIC
from .typography import Typography, FONTS
from .spacing import (
    get_spacing, get_radius, COMPONENT_SIZES, BORDER_WIDTH,
    SEMANTIC_SPACING, SEMANTIC_RADIUS
)


class AppleModernTheme:
    """
    Complete modern theme system for the application
    
    Features:
    - Light/Dark mode support
    - Smooth transitions
    - Modern, clean aesthetics
    - Complete widget coverage
    - Accessibility compliant
    """
    
    def __init__(self, mode: str = 'light'):
        """
        Initialize theme
        
        Args:
            mode: 'light' or 'dark'
        """
        self.mode = mode
        self.colors = ColorPalette(mode)
        self.typography = Typography()
        
        # Theme change callbacks
        self._callbacks: List[Callable] = []
        
        # Cache for styled widgets
        self._style_cache: Dict[str, ttk.Style] = {}
    
    def setup(self, root: Optional[tk.Tk] = None) -> ttk.Style:
        """
        Setup and apply theme to the application
        
        Args:
            root: Root tkinter window
            
        Returns:
            Configured ttk.Style object
        """
        style = ttk.Style()
        
        # Use 'clam' as base theme (most customizable)
        try:
            style.theme_use('clam')
        except tk.TclError:
            # Fallback to default if clam not available
            pass
        
        # Configure all widget styles
        self._configure_root(style)
        self._configure_frames(style)
        self._configure_labels(style)
        self._configure_buttons(style)
        self._configure_entries(style)
        self._configure_text_widgets(style)
        self._configure_treeview(style)
        self._configure_notebook(style)
        self._configure_scrollbars(style)
        self._configure_progressbar(style)
        self._configure_scale(style)
        self._configure_checkbutton(style)
        self._configure_radiobutton(style)
        self._configure_combobox(style)
        self._configure_spinbox(style)
        self._configure_separator(style)
        self._configure_custom_styles(style)
        
        return style
    
    def _configure_root(self, style: ttk.Style) -> None:
        """Configure root/base styles"""
        style.configure('.',
            background=self.colors.get('background'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            borderwidth=0,
            relief='flat'
        )
    
    def _configure_frames(self, style: ttk.Style) -> None:
        """Configure frame styles"""
        # Standard frame
        style.configure('TFrame',
            background=self.colors.get('background'),
            borderwidth=0
        )
        
        # Card frame (elevated surface)
        style.configure('Card.TFrame',
            background=self.colors.get('surface'),
            borderwidth=0,
            relief='flat'
        )
        
        # Surface frame
        style.configure('Surface.TFrame',
            background=self.colors.get('surface'),
            borderwidth=0
        )
        
        # Secondary surface
        style.configure('SurfaceSecondary.TFrame',
            background=self.colors.get('surface_secondary'),
            borderwidth=0
        )
    
    def _configure_labels(self, style: ttk.Style) -> None:
        """Configure label styles"""
        # Default label
        style.configure('TLabel',
            background=self.colors.get('background'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            padding=get_spacing('xs')
        )
        
        # Display text
        style.configure('Display.TLabel',
            font=FONTS['display'],
            foreground=self.colors.get('text_primary')
        )
        
        # Headings
        for i in range(1, 7):
            style.configure(f'H{i}.TLabel',
                font=FONTS[f'h{i}'],
                foreground=self.colors.get('text_primary')
            )
        
        # Body variations
        style.configure('BodyLarge.TLabel',
            font=FONTS['body_large']
        )
        
        style.configure('BodySmall.TLabel',
            font=FONTS['body_small']
        )
        
        # Secondary text
        style.configure('Secondary.TLabel',
            foreground=self.colors.get('text_secondary')
        )
        
        # Caption
        style.configure('Caption.TLabel',
            font=FONTS['caption'],
            foreground=self.colors.get('text_secondary')
        )
        
        # Success/Warning/Error/Info labels
        for semantic_type in ['Success', 'Warning', 'Error', 'Info']:
            style.configure(f'{semantic_type}.TLabel',
                foreground=self.colors.get(semantic_type.lower())
            )
    
    def _configure_buttons(self, style: ttk.Style) -> None:
        """Configure button styles"""
        # Primary button (filled)
        style.configure('Primary.TButton',
            font=FONTS['button'],
            background=self.colors.get('blue'),
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(get_spacing('sm'), get_spacing('xs')),
            relief='flat'
        )
        style.map('Primary.TButton',
            background=[
                ('active', self.colors.get('blue_light')),
                ('pressed', self.colors.get('blue_dark')),
                ('disabled', self.colors.get('blue_ultra_light'))
            ],
            foreground=[
                ('disabled', self.colors.get('text_disabled'))
            ]
        )
        
        # Secondary button (outlined)
        style.configure('Secondary.TButton',
            font=FONTS['button'],
            background=self.colors.get('surface'),
            foreground=self.colors.get('blue'),
            borderwidth=BORDER_WIDTH['default'],
            bordercolor=self.colors.get('blue'),
            focuscolor='none',
            padding=(get_spacing('sm'), get_spacing('xs')),
            relief='solid'
        )
        style.map('Secondary.TButton',
            background=[
                ('active', self.colors.get('surface_hover')),
                ('pressed', self.colors.get('surface_pressed'))
            ]
        )
        
        # Ghost button (transparent)
        style.configure('Ghost.TButton',
            font=FONTS['button'],
            background=self.colors.get('background'),
            foreground=self.colors.get('text_primary'),
            borderwidth=0,
            focuscolor='none',
            padding=(get_spacing('sm'), get_spacing('xs')),
            relief='flat'
        )
        style.map('Ghost.TButton',
            background=[
                ('active', self.colors.get('surface')),
                ('pressed', self.colors.get('surface_hover'))
            ]
        )
        
        # Semantic buttons
        for semantic_type in ['Success', 'Warning', 'Error']:
            color_key = semantic_type.lower()
            style.configure(f'{semantic_type}.TButton',
                font=FONTS['button'],
                background=self.colors.get(color_key),
                foreground='white',
                borderwidth=0,
                focuscolor='none',
                padding=(get_spacing('sm'), get_spacing('xs'))
            )
            style.map(f'{semantic_type}.TButton',
                background=[
                    ('active', self.colors.get(f'{color_key}_light')),
                    ('pressed', self.colors.get(f'{color_key}_dark'))
                ]
            )
        
        # Small and large button variants
        style.configure('Small.TButton',
            padding=(get_spacing('xs'), get_spacing('xxs'))
        )
        
        style.configure('Large.TButton',
            font=FONTS['button_large'],
            padding=(get_spacing('md'), get_spacing('sm'))
        )
    
    def _configure_entries(self, style: ttk.Style) -> None:
        """Configure entry/input field styles"""
        style.configure('TEntry',
            font=FONTS['body'],
            fieldbackground=self.colors.get('surface'),
            foreground=self.colors.get('text_primary'),
            borderwidth=BORDER_WIDTH['default'],
            bordercolor=self.colors.get('border'),
            insertcolor=self.colors.get('text_primary'),
            selectbackground=self.colors.get('blue'),
            selectforeground='white',
            padding=get_spacing('xs')
        )
        style.map('TEntry',
            fieldbackground=[
                ('readonly', self.colors.get('surface_secondary')),
                ('disabled', self.colors.get('surface_secondary'))
            ],
            bordercolor=[
                ('focus', self.colors.get('border_focus')),
                ('invalid', self.colors.get('error'))
            ]
        )
    
    def _configure_text_widgets(self, style: ttk.Style) -> None:
        """Configure text widget styles"""
        # Note: Text widget is not a ttk widget, configured separately in components
        pass
    
    def _configure_treeview(self, style: ttk.Style) -> None:
        """Configure treeview/table styles"""
        style.configure('Treeview',
            background=self.colors.get('surface'),
            foreground=self.colors.get('text_primary'),
            fieldbackground=self.colors.get('surface'),
            font=FONTS['body'],
            borderwidth=0,
            relief='flat',
            rowheight=40  # Modern row height
        )
        
        style.configure('Treeview.Heading',
            background=self.colors.get('surface_secondary'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body_bold'],
            borderwidth=0,
            relief='flat'
        )
        
        style.map('Treeview',
            background=[
                ('selected', self.colors.get('blue')),
                ('alternate', self.colors.get('surface_secondary'))
            ],
            foreground=[
                ('selected', 'white')
            ]
        )
        
        style.map('Treeview.Heading',
            background=[
                ('active', self.colors.get('surface_hover'))
            ]
        )
    
    def _configure_notebook(self, style: ttk.Style) -> None:
        """Configure notebook/tab styles"""
        style.configure('TNotebook',
            background=self.colors.get('background'),
            borderwidth=0,
            tabmargins=(0, 0, 0, 0)
        )
        
        style.configure('TNotebook.Tab',
            background=self.colors.get('surface'),
            foreground=self.colors.get('text_secondary'),
            font=FONTS['body_medium'],
            padding=(get_spacing('sm'), get_spacing('xs')),
            borderwidth=0
        )
        
        style.map('TNotebook.Tab',
            background=[
                ('selected', self.colors.get('blue')),
                ('active', self.colors.get('surface_hover'))
            ],
            foreground=[
                ('selected', 'white'),
                ('active', self.colors.get('text_primary'))
            ],
            padding=[
                ('selected', (get_spacing('sm'), get_spacing('sm')))
            ]
        )
    
    def _configure_scrollbars(self, style: ttk.Style) -> None:
        """Configure scrollbar styles"""
        style.configure('TScrollbar',
            background=self.colors.get('gray_300'),
            troughcolor=self.colors.get('surface_secondary'),
            borderwidth=0,
            arrowsize=get_spacing('sm')
        )
        
        style.map('TScrollbar',
            background=[
                ('active', self.colors.get('gray_400')),
                ('pressed', self.colors.get('gray_500'))
            ]
        )
    
    def _configure_progressbar(self, style: ttk.Style) -> None:
        """Configure progressbar styles"""
        style.configure('TProgressbar',
            background=self.colors.get('blue'),
            troughcolor=self.colors.get('surface_secondary'),
            borderwidth=0,
            thickness=8
        )
    
    def _configure_scale(self, style: ttk.Style) -> None:
        """Configure scale/slider styles"""
        style.configure('TScale',
            background=self.colors.get('blue'),
            troughcolor=self.colors.get('surface_secondary'),
            borderwidth=0
        )
    
    def _configure_checkbutton(self, style: ttk.Style) -> None:
        """Configure checkbutton styles"""
        style.configure('TCheckbutton',
            background=self.colors.get('background'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            indicatorbackground=self.colors.get('surface'),
            indicatorforeground=self.colors.get('blue'),
            borderwidth=0
        )
    
    def _configure_radiobutton(self, style: ttk.Style) -> None:
        """Configure radiobutton styles"""
        style.configure('TRadiobutton',
            background=self.colors.get('background'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            indicatorbackground=self.colors.get('surface'),
            indicatorforeground=self.colors.get('blue'),
            borderwidth=0
        )
    
    def _configure_combobox(self, style: ttk.Style) -> None:
        """Configure combobox styles"""
        style.configure('TCombobox',
            fieldbackground=self.colors.get('surface'),
            background=self.colors.get('surface'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            borderwidth=BORDER_WIDTH['default'],
            arrowsize=get_spacing('sm')
        )
        
        style.map('TCombobox',
            fieldbackground=[
                ('readonly', self.colors.get('surface')),
                ('disabled', self.colors.get('surface_secondary'))
            ]
        )
    
    def _configure_spinbox(self, style: ttk.Style) -> None:
        """Configure spinbox styles"""
        style.configure('TSpinbox',
            fieldbackground=self.colors.get('surface'),
            background=self.colors.get('surface'),
            foreground=self.colors.get('text_primary'),
            font=FONTS['body'],
            borderwidth=BORDER_WIDTH['default'],
            arrowsize=get_spacing('sm')
        )
    
    def _configure_separator(self, style: ttk.Style) -> None:
        """Configure separator styles"""
        style.configure('TSeparator',
            background=self.colors.get('border')
        )
        
        style.configure('Vertical.TSeparator',
            background=self.colors.get('border')
        )
    
    def _configure_custom_styles(self, style: ttk.Style) -> None:
        """Configure custom application-specific styles"""
        # Header frame
        style.configure('Header.TFrame',
            background=self.colors.get('surface'),
            borderwidth=0
        )
        
        # Sidebar frame
        style.configure('Sidebar.TFrame',
            background=self.colors.get('surface_secondary'),
            borderwidth=0
        )
        
        # Content frame
        style.configure('Content.TFrame',
            background=self.colors.get('background'),
            borderwidth=0
        )
        
        # Card styles
        style.configure('ElevatedCard.TFrame',
            background=self.colors.get('surface'),
            borderwidth=0,
            relief='raised'
        )
        
        # Stats card label
        style.configure('StatsValue.TLabel',
            font=FONTS['display_small'],
            foreground=self.colors.get('text_primary')
        )
        
        style.configure('StatsLabel.TLabel',
            font=FONTS['caption'],
            foreground=self.colors.get('text_secondary')
        )
    
    def switch_mode(self, mode: str) -> None:
        """
        Switch between light and dark modes
        
        Args:
            mode: 'light' or 'dark'
        """
        self.mode = mode
        self.colors.switch_mode(mode)
        
        # Reapply all styles
        self.setup()
        
        # Notify callbacks
        for callback in self._callbacks:
            callback(mode)
    
    def register_callback(self, callback: Callable[[str], None]) -> None:
        """
        Register a callback for theme changes
        
        Args:
            callback: Function to call when theme changes
        """
        self._callbacks.append(callback)
    
    def toggle_mode(self) -> None:
        """Toggle between light and dark modes"""
        new_mode = 'dark' if self.mode == 'light' else 'light'
        self.switch_mode(new_mode)
    
    @property
    def is_dark_mode(self) -> bool:
        """Check if dark mode is active"""
        return self.mode == 'dark'


# Global theme instance
_theme: Optional[AppleModernTheme] = None


def get_theme() -> AppleModernTheme:
    """Get or create global theme instance"""
    global _theme
    if _theme is None:
        _theme = AppleModernTheme()
    return _theme


def setup_theme(root: Optional[tk.Tk] = None, mode: str = 'light') -> ttk.Style:
    """
    Setup and apply theme
    
    Args:
        root: Root window
        mode: 'light' or 'dark'
        
    Returns:
        Configured Style object
    """
    theme = get_theme()
    if theme.mode != mode:
        theme.switch_mode(mode)
    return theme.setup(root)


def switch_theme_mode(mode: str) -> None:
    """Switch theme mode"""
    get_theme().switch_mode(mode)


def toggle_theme_mode() -> None:
    """Toggle theme mode"""
    get_theme().toggle_mode()
