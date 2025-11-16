"""
Modern Theme Manager with Enhanced Styling
Provides a beautiful, modern UI with card layouts, gradients, and animations
"""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Tuple

class ModernTheme:
    """Modern theme with enhanced colors, fonts, and styles"""
    
    # Modern color palette
    COLORS = {
        # Primary colors - Modern blue gradient
        'primary': '#2563EB',       # Vibrant blue
        'primary_light': '#3B82F6', # Light blue
        'primary_dark': '#1E40AF',  # Dark blue
        'primary_hover': '#1D4ED8', # Hover blue
        
        # Secondary colors - Purple gradient
        'secondary': '#8B5CF6',     # Vibrant purple
        'secondary_light': '#A78BFA', # Light purple
        'secondary_dark': '#7C3AED', # Dark purple
        
        # Accent colors
        'accent': '#F59E0B',        # Amber
        'accent_light': '#FBBF24',  # Light amber
        'success': '#10B981',       # Green
        'warning': '#F59E0B',       # Orange
        'error': '#EF4444',         # Red
        'info': '#3B82F6',          # Blue
        
        # Background colors
        'background': '#F9FAFB',    # Very light gray
        'background_dark': '#F3F4F6', # Light gray
        'surface': '#FFFFFF',       # White
        'surface_hover': '#F3F4F6', # Hover gray
        
        # Text colors
        'text_primary': '#111827',  # Almost black
        'text_secondary': '#6B7280', # Medium gray
        'text_muted': '#9CA3AF',    # Light gray
        'text_white': '#FFFFFF',    # White text
        
        # Border colors
        'border': '#E5E7EB',        # Light border
        'border_focus': '#3B82F6',  # Focus border
        
        # Card colors
        'card_bg': '#FFFFFF',       # Card background
        'card_shadow': '#00000010', # Card shadow
        
        # Status colors
        'status_active': '#10B981',  # Active green
        'status_inactive': '#6B7280', # Inactive gray
        'status_warning': '#F59E0B',  # Warning amber
        'status_error': '#EF4444',    # Error red
    }
    
    # Modern font system
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),      # Large titles
        'heading': ('Segoe UI', 18, 'bold'),    # Section headers
        'subheading': ('Segoe UI', 14, 'bold'), # Subsection headers
        'body': ('Segoe UI', 11),               # Body text
        'body_bold': ('Segoe UI', 11, 'bold'),  # Bold body
        'small': ('Segoe UI', 9),               # Small text
        'small_bold': ('Segoe UI', 9, 'bold'),  # Small bold
        'button': ('Segoe UI', 10, 'bold'),     # Buttons
        'icon': ('Segoe UI', 16),               # Icon text
    }
    
    # Spacing system (8px base unit)
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
    }
    
    # Border radius
    RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
        'full': 9999,
    }
    
    @classmethod
    def setup_theme(cls):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== BASE STYLES =====
        style.configure('.',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['body'],
            borderwidth=0
        )
        
        # ===== FRAME STYLES =====
        style.configure('TFrame',
            background=cls.COLORS['background'],
            borderwidth=0
        )
        
        style.configure('Card.TFrame',
            background=cls.COLORS['card_bg'],
            relief='flat',
            borderwidth=1
        )
        
        style.configure('Surface.TFrame',
            background=cls.COLORS['surface'],
            relief='flat'
        )
        
        # ===== LABEL STYLES =====
        style.configure('TLabel',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['body']
        )
        
        style.configure('Title.TLabel',
            font=cls.FONTS['title'],
            foreground=cls.COLORS['primary'],
            background=cls.COLORS['background']
        )
        
        style.configure('Heading.TLabel',
            font=cls.FONTS['heading'],
            foreground=cls.COLORS['text_primary'],
            background=cls.COLORS['background']
        )
        
        style.configure('Subheading.TLabel',
            font=cls.FONTS['subheading'],
            foreground=cls.COLORS['text_primary'],
            background=cls.COLORS['background']
        )
        
        style.configure('Secondary.TLabel',
            font=cls.FONTS['body'],
            foreground=cls.COLORS['text_secondary'],
            background=cls.COLORS['background']
        )
        
        style.configure('Muted.TLabel',
            font=cls.FONTS['small'],
            foreground=cls.COLORS['text_muted'],
            background=cls.COLORS['background']
        )
        
        # Status labels
        style.configure('Success.TLabel',
            font=cls.FONTS['body_bold'],
            foreground=cls.COLORS['success'],
            background=cls.COLORS['background']
        )
        
        style.configure('Error.TLabel',
            font=cls.FONTS['body_bold'],
            foreground=cls.COLORS['error'],
            background=cls.COLORS['background']
        )
        
        style.configure('Warning.TLabel',
            font=cls.FONTS['body_bold'],
            foreground=cls.COLORS['warning'],
            background=cls.COLORS['background']
        )
        
        # ===== BUTTON STYLES =====
        # Primary button
        style.configure('Primary.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['primary'],
            foreground=cls.COLORS['text_white'],
            borderwidth=0,
            focuscolor='none',
            padding=(20, 12)
        )
        style.map('Primary.TButton',
            background=[('active', cls.COLORS['primary_hover']),
                       ('disabled', cls.COLORS['border'])],
            foreground=[('disabled', cls.COLORS['text_muted'])]
        )
        
        # Secondary button
        style.configure('Secondary.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['secondary'],
            foreground=cls.COLORS['text_white'],
            borderwidth=0,
            focuscolor='none',
            padding=(20, 12)
        )
        style.map('Secondary.TButton',
            background=[('active', cls.COLORS['secondary_dark'])]
        )
        
        # Success button
        style.configure('Success.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['success'],
            foreground=cls.COLORS['text_white'],
            borderwidth=0,
            focuscolor='none',
            padding=(20, 12)
        )
        style.map('Success.TButton',
            background=[('active', '#059669')]
        )
        
        # Danger button
        style.configure('Danger.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['error'],
            foreground=cls.COLORS['text_white'],
            borderwidth=0,
            focuscolor='none',
            padding=(20, 12)
        )
        style.map('Danger.TButton',
            background=[('active', '#DC2626')]
        )
        
        # Outline button
        style.configure('Outline.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['primary'],
            borderwidth=2,
            relief='solid',
            padding=(20, 12)
        )
        style.map('Outline.TButton',
            background=[('active', cls.COLORS['surface_hover'])]
        )
        
        # Icon button (small, rounded)
        style.configure('Icon.TButton',
            font=cls.FONTS['icon'],
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['primary'],
            borderwidth=0,
            padding=(8, 8)
        )
        style.map('Icon.TButton',
            background=[('active', cls.COLORS['surface_hover'])]
        )
        
        # ===== ENTRY STYLES =====
        style.configure('TEntry',
            fieldbackground=cls.COLORS['surface'],
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text_primary'],
            bordercolor=cls.COLORS['border'],
            lightcolor=cls.COLORS['border_focus'],
            darkcolor=cls.COLORS['border_focus'],
            borderwidth=2,
            relief='solid',
            padding=(12, 10),
            font=cls.FONTS['body']
        )
        style.map('TEntry',
            fieldbackground=[('focus', cls.COLORS['surface'])],
            bordercolor=[('focus', cls.COLORS['border_focus'])]
        )
        
        # ===== COMBOBOX STYLES =====
        style.configure('TCombobox',
            fieldbackground=cls.COLORS['surface'],
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text_primary'],
            bordercolor=cls.COLORS['border'],
            arrowcolor=cls.COLORS['primary'],
            borderwidth=2,
            relief='solid',
            padding=(12, 8),
            font=cls.FONTS['body']
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', cls.COLORS['surface'])],
            bordercolor=[('focus', cls.COLORS['border_focus'])]
        )
        
        # ===== NOTEBOOK (TABS) STYLES =====
        style.configure('TNotebook',
            background=cls.COLORS['background'],
            borderwidth=0,
            tabmargins=(0, 0, 0, 0)
        )
        
        style.configure('TNotebook.Tab',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text_secondary'],
            padding=(20, 12),
            borderwidth=0,
            font=cls.FONTS['body_bold']
        )
        style.map('TNotebook.Tab',
            background=[('selected', cls.COLORS['primary']),
                       ('active', cls.COLORS['surface_hover'])],
            foreground=[('selected', cls.COLORS['text_white']),
                       ('active', cls.COLORS['text_primary'])]
        )
        
        # ===== TREEVIEW STYLES =====
        style.configure('Treeview',
            background=cls.COLORS['surface'],
            foreground=cls.COLORS['text_primary'],
            fieldbackground=cls.COLORS['surface'],
            borderwidth=0,
            font=cls.FONTS['body'],
            rowheight=40
        )
        style.configure('Treeview.Heading',
            background=cls.COLORS['primary'],
            foreground=cls.COLORS['text_white'],
            borderwidth=0,
            font=cls.FONTS['body_bold'],
            relief='flat'
        )
        style.map('Treeview',
            background=[('selected', cls.COLORS['primary_light'])],
            foreground=[('selected', cls.COLORS['text_white'])]
        )
        style.map('Treeview.Heading',
            background=[('active', cls.COLORS['primary_hover'])]
        )
        
        # ===== SCROLLBAR STYLES =====
        style.configure('Vertical.TScrollbar',
            background=cls.COLORS['border'],
            troughcolor=cls.COLORS['background'],
            borderwidth=0,
            arrowsize=0,
            width=12
        )
        style.map('Vertical.TScrollbar',
            background=[('active', cls.COLORS['text_muted'])]
        )
        
        style.configure('Horizontal.TScrollbar',
            background=cls.COLORS['border'],
            troughcolor=cls.COLORS['background'],
            borderwidth=0,
            arrowsize=0,
            width=12
        )
        style.map('Horizontal.TScrollbar',
            background=[('active', cls.COLORS['text_muted'])]
        )
        
        # ===== SEPARATOR STYLES =====
        style.configure('TSeparator',
            background=cls.COLORS['border']
        )
        
        # ===== PROGRESSBAR STYLES =====
        style.configure('TProgressbar',
            background=cls.COLORS['primary'],
            troughcolor=cls.COLORS['background_dark'],
            borderwidth=0,
            thickness=8
        )
    
    @classmethod
    def create_card(cls, parent, title="", subtitle="", **kwargs) -> tk.Frame:
        """Create a modern card widget"""
        card = tk.Frame(
            parent,
            bg=cls.COLORS['card_bg'],
            relief='flat',
            bd=0,
            **kwargs
        )
        
        # Add subtle shadow effect with border
        card.config(
            highlightbackground=cls.COLORS['border'],
            highlightthickness=1
        )
        
        if title:
            title_label = tk.Label(
                card,
                text=title,
                bg=cls.COLORS['card_bg'],
                fg=cls.COLORS['text_primary'],
                font=cls.FONTS['subheading'],
                anchor='w'
            )
            title_label.pack(fill='x', padx=cls.SPACING['md'], pady=(cls.SPACING['md'], 0))
        
        if subtitle:
            subtitle_label = tk.Label(
                card,
                text=subtitle,
                bg=cls.COLORS['card_bg'],
                fg=cls.COLORS['text_secondary'],
                font=cls.FONTS['small'],
                anchor='w'
            )
            subtitle_label.pack(fill='x', padx=cls.SPACING['md'], pady=(cls.SPACING['xs'], 0))
        
        return card
    
    @classmethod
    def create_badge(cls, parent, text, color='primary') -> tk.Label:
        """Create a badge widget"""
        color_map = {
            'primary': cls.COLORS['primary'],
            'success': cls.COLORS['success'],
            'warning': cls.COLORS['warning'],
            'error': cls.COLORS['error'],
            'secondary': cls.COLORS['secondary']
        }
        
        badge = tk.Label(
            parent,
            text=text,
            bg=color_map.get(color, cls.COLORS['primary']),
            fg=cls.COLORS['text_white'],
            font=cls.FONTS['small_bold'],
            padx=cls.SPACING['sm'],
            pady=cls.SPACING['xs']
        )
        return badge
    
    @classmethod
    def create_icon_button(cls, parent, text, command, icon="", **kwargs) -> tk.Button:
        """Create an icon button"""
        full_text = f"{icon} {text}" if icon else text
        button = tk.Button(
            parent,
            text=full_text,
            command=command,
            bg=cls.COLORS['primary'],
            fg=cls.COLORS['text_white'],
            font=cls.FONTS['button'],
            bd=0,
            relief='flat',
            padx=cls.SPACING['md'],
            pady=cls.SPACING['sm'],
            cursor='hand2',
            **kwargs
        )
        
        # Hover effects
        def on_enter(e):
            button.config(bg=cls.COLORS['primary_hover'])
        
        def on_leave(e):
            button.config(bg=cls.COLORS['primary'])
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
