"""
🏆 ELITE THEME SYSTEM
Enterprise-grade design system with glassmorphism, animations, and micro-interactions
Inspired by: Apple, Microsoft Fluent Design, Google Material You, Stripe Dashboard
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import Tuple, Dict, Callable

class EliteTheme:
    """
    Elite design system - What the biggest firms in the world use
    Features: Glassmorphism, Neumorphism, Advanced gradients, Micro-animations
    """
    
    # 🎨 ELITE COLOR SYSTEM - Premium palette
    COLORS = {
        # Primary - Deep ocean blues with gradients
        'primary': '#0A66C2',           # LinkedIn blue
        'primary_light': '#1877F2',     # Facebook blue  
        'primary_dark': '#003A70',      # Navy
        'primary_gradient_start': '#667EEA',  # Purple-blue
        'primary_gradient_end': '#764BA2',    # Deep purple
        
        # Accent - Premium gold and purple
        'accent_gold': '#FFB800',       # Premium gold
        'accent_purple': '#9333EA',     # Royal purple
        'accent_teal': '#14B8A6',       # Modern teal
        'accent_pink': '#EC4899',       # Vibrant pink
        
        # Glassmorphism backgrounds
        'glass_bg': '#FFFFFF',          # Base glass
        'glass_bg_dark': '#1E1E1E',     # Dark glass
        'glass_overlay': '#F8F9FA',     # Light overlay (was semi-transparent)
        'glass_border': '#E8E8E8',      # Subtle border (was semi-transparent)
        
        # Surface elevations (Material Design inspired)
        'surface_0': '#FFFFFF',         # Ground level
        'surface_1': '#F8F9FA',         # 1dp elevation
        'surface_2': '#F1F3F5',         # 2dp elevation
        'surface_3': '#E9ECEF',         # 3dp elevation
        'surface_4': '#DEE2E6',         # 4dp elevation
        
        # Semantic colors
        'success': '#10B981',           # Green
        'success_light': '#D1FAE5',     # Light green bg
        'warning': '#F59E0B',           # Amber
        'warning_light': '#FEF3C7',     # Light amber bg
        'error': '#EF4444',             # Red
        'error_light': '#FEE2E2',       # Light red bg
        'info': '#3B82F6',              # Blue
        'info_light': '#DBEAFE',        # Light blue bg
        
        # Text hierarchy
        'text_primary': '#0F172A',      # Almost black
        'text_secondary': '#475569',    # Gray
        'text_tertiary': '#94A3B8',     # Light gray
        'text_disabled': '#CBD5E1',     # Very light gray
        'text_inverse': '#FFFFFF',      # White
        
        # Backgrounds
        'bg_primary': '#FFFFFF',        # White
        'bg_secondary': '#F8FAFC',      # Off-white
        'bg_tertiary': '#F1F5F9',       # Light gray
        'bg_dark': '#0F172A',           # Dark mode
        # Note: Tkinter doesn't support CSS gradients - removed gradient definitions
        
        # Borders
        'border_light': '#E2E8F0',      # Light border
        'border_medium': '#CBD5E1',     # Medium border
        'border_dark': '#94A3B8',       # Dark border
        'border_focus': '#3B82F6',      # Focus border
        
        # Shadows (for depth) - Note: tkinter doesn't support RGBA, these are for reference only
        'shadow_sm': '#E8E8E8',         # Small shadow (light gray)
        'shadow_md': '#D0D0D0',         # Medium shadow (medium gray)
        'shadow_lg': '#B8B8B8',         # Large shadow (darker gray)
        'shadow_xl': '#A0A0A0',         # Extra large shadow (darkest gray)
        
        # Status indicators
        'status_online': '#10B981',     # Green
        'status_busy': '#F59E0B',       # Amber
        'status_away': '#EF4444',       # Red
        'status_offline': '#6B7280',    # Gray
        
        # Chart colors (for data visualization)
        'chart_1': '#3B82F6',           # Blue
        'chart_2': '#8B5CF6',           # Purple
        'chart_3': '#EC4899',           # Pink
        'chart_4': '#10B981',           # Green
        'chart_5': '#F59E0B',           # Amber
        'chart_6': '#06B6D4',           # Cyan
        'chart_7': '#EF4444',           # Red
        'chart_8': '#6366F1',           # Indigo
    }
    
    # 🔤 PREMIUM TYPOGRAPHY SYSTEM
    FONTS = {
        # Headlines
        'display': ('SF Pro Display', 48, 'bold'),      # Large display text
        'h1': ('SF Pro Display', 36, 'bold'),           # Main headlines
        'h2': ('SF Pro Display', 28, 'bold'),           # Section headers
        'h3': ('SF Pro Display', 22, 'bold'),           # Subsection headers
        'h4': ('SF Pro Text', 18, 'bold'),              # Card titles
        'h5': ('SF Pro Text', 16, 'bold'),              # Small headers
        'h6': ('SF Pro Text', 14, 'bold'),              # Tiny headers
        
        # Body text
        'body_large': ('SF Pro Text', 16),              # Large body
        'body': ('SF Pro Text', 14),                    # Regular body
        'body_medium': ('SF Pro Text', 14, 'medium'),   # Medium weight body
        'body_bold': ('SF Pro Text', 14, 'bold'),       # Bold body
        'body_small': ('SF Pro Text', 12),              # Small body
        
        # Special
        'button': ('SF Pro Text', 14, 'bold'),          # Buttons
        'caption': ('SF Pro Text', 12),                 # Captions
        'overline': ('SF Pro Text', 10, 'bold'),        # Overline text
        'monospace': ('SF Mono', 13),                   # Code/data
        
        # Fallback (in case SF Pro not available)
        'fallback_display': ('Segoe UI', 48, 'bold'),
        'fallback_text': ('Segoe UI', 14),
        'fallback_button': ('Segoe UI', 14, 'bold'),
    }
    
    # 📏 PREMIUM SPACING SYSTEM (8px base)
    SPACING = {
        'xs': 4,      # Extra small
        'sm': 8,      # Small
        'md': 16,     # Medium
        'lg': 24,     # Large
        'xl': 32,     # Extra large
        '2xl': 48,    # 2X large
        '3xl': 64,    # 3X large
        '4xl': 96,    # 4X large
    }
    
    # 🎭 BORDER RADIUS SYSTEM
    RADIUS = {
        'none': 0,
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
        '2xl': 24,
        'full': 9999,
    }
    
    # 🎬 ANIMATION SYSTEM
    ANIMATIONS = {
        'duration_fast': 150,       # 150ms
        'duration_normal': 250,     # 250ms
        'duration_slow': 350,       # 350ms
        'easing_default': 'ease-in-out',
        'easing_spring': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    }
    
    # 💫 ELEVATION SYSTEM (z-index)
    ELEVATION = {
        'base': 0,
        'raised': 1,
        'overlay': 2,
        'dropdown': 3,
        'modal': 4,
        'popover': 5,
        'toast': 6,
        'tooltip': 7,
    }
    
    @classmethod
    def setup_elite_theme(cls):
        """Setup enterprise-grade theme with all premium styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== BASE CONFIGURATION =====
        style.configure('.',
            background=cls.COLORS['bg_secondary'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['body'],
            borderwidth=0,
            relief='flat'
        )
        
        # ===== ELITE BUTTON STYLES =====
        
        # Primary Elite Button (Gradient)
        style.configure('Elite.Primary.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['primary'],
            foreground=cls.COLORS['text_inverse'],
            borderwidth=0,
            focuscolor='',
            padding=(cls.SPACING['lg'], cls.SPACING['md']),
            relief='flat'
        )
        style.map('Elite.Primary.TButton',
            background=[
                ('active', cls.COLORS['primary_light']),
                ('pressed', cls.COLORS['primary_dark']),
                ('disabled', cls.COLORS['border_light'])
            ],
            foreground=[('disabled', cls.COLORS['text_disabled'])]
        )
        
        # Glass Button (Glassmorphism effect)
        style.configure('Elite.Glass.TButton',
            font=cls.FONTS['button'],
            background=cls.COLORS['glass_overlay'],
            foreground=cls.COLORS['text_primary'],
            borderwidth=1,
            focuscolor='',
            padding=(cls.SPACING['lg'], cls.SPACING['md']),
            relief='flat'
        )
        style.map('Elite.Glass.TButton',
            background=[('active', cls.COLORS['surface_1'])]
        )
        
        # Gradient Button
        style.configure('Elite.Gradient.TButton',
            font=cls.FONTS['button'],
            foreground=cls.COLORS['text_inverse'],
            borderwidth=0,
            focuscolor='',
            padding=(cls.SPACING['lg'], cls.SPACING['md']),
            relief='flat'
        )
        
        # Icon Button (Circular)
        style.configure('Elite.Icon.TButton',
            font=cls.FONTS['h5'],
            background=cls.COLORS['surface_1'],
            foreground=cls.COLORS['text_primary'],
            borderwidth=0,
            padding=(cls.SPACING['md'], cls.SPACING['md']),
            relief='flat'
        )
        style.map('Elite.Icon.TButton',
            background=[('active', cls.COLORS['surface_2'])]
        )
        
        # ===== PREMIUM ENTRY STYLES =====
        style.configure('Elite.TEntry',
            fieldbackground=cls.COLORS['surface_0'],
            background=cls.COLORS['surface_0'],
            foreground=cls.COLORS['text_primary'],
            borderwidth=2,
            relief='flat',
            padding=(cls.SPACING['md'], cls.SPACING['sm']),
            font=cls.FONTS['body']
        )
        style.map('Elite.TEntry',
            fieldbackground=[('focus', cls.COLORS['surface_0'])]
        )
        
        # ===== ELITE FRAME STYLES =====
        style.configure('Elite.TFrame',
            background=cls.COLORS['bg_secondary'],
            borderwidth=0,
            relief='flat'
        )
        
        # Glass Frame (Glassmorphism)
        style.configure('Elite.Glass.TFrame',
            background=cls.COLORS['glass_overlay'],
            borderwidth=1,
            relief='flat'
        )
        
        # Card Frame (Elevated)
        style.configure('Elite.Card.TFrame',
            background=cls.COLORS['surface_0'],
            borderwidth=0,
            relief='flat'
        )
        
        # ===== ELITE LABEL STYLES =====
        style.configure('Elite.TLabel',
            background=cls.COLORS['bg_secondary'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['body']
        )
        
        # Display (Hero text)
        style.configure('Elite.Display.TLabel',
            font=cls.FONTS['display'],
            foreground=cls.COLORS['primary'],
            background=cls.COLORS['bg_secondary']
        )
        
        # Headings
        for i in range(1, 7):
            style.configure(f'Elite.H{i}.TLabel',
                font=cls.FONTS[f'h{i}'],
                foreground=cls.COLORS['text_primary'],
                background=cls.COLORS['bg_secondary']
            )
        
        # Secondary text
        style.configure('Elite.Secondary.TLabel',
            font=cls.FONTS['body'],
            foreground=cls.COLORS['text_secondary'],
            background=cls.COLORS['bg_secondary']
        )
        
        # Caption
        style.configure('Elite.Caption.TLabel',
            font=cls.FONTS['caption'],
            foreground=cls.COLORS['text_tertiary'],
            background=cls.COLORS['bg_secondary']
        )
        
        # Badge labels
        for badge_type in ['success', 'warning', 'error', 'info']:
            style.configure(f'Elite.Badge.{badge_type.title()}.TLabel',
                font=cls.FONTS['caption'],
                foreground=cls.COLORS['text_inverse'],
                background=cls.COLORS[badge_type],
                padding=(cls.SPACING['sm'], cls.SPACING['xs']),
                relief='flat'
            )
        
        # ===== ELITE TREEVIEW (TABLE) STYLES =====
        style.configure('Elite.Treeview',
            background=cls.COLORS['surface_0'],
            foreground=cls.COLORS['text_primary'],
            fieldbackground=cls.COLORS['surface_0'],
            borderwidth=0,
            font=cls.FONTS['body'],
            rowheight=56  # Spacious rows
        )
        
        style.configure('Elite.Treeview.Heading',
            background=cls.COLORS['surface_1'],
            foreground=cls.COLORS['text_secondary'],
            borderwidth=0,
            font=cls.FONTS['button'],
            relief='flat',
            padding=(cls.SPACING['md'], cls.SPACING['sm'])
        )
        
        style.map('Elite.Treeview',
            background=[
                ('selected', cls.COLORS['primary']),
                ('active', cls.COLORS['surface_1'])
            ],
            foreground=[('selected', cls.COLORS['text_inverse'])]
        )
        
        style.map('Elite.Treeview.Heading',
            background=[('active', cls.COLORS['surface_2'])]
        )
        
        # ===== ELITE NOTEBOOK (TABS) STYLES =====
        style.configure('Elite.TNotebook',
            background=cls.COLORS['bg_secondary'],
            borderwidth=0,
            tabmargins=(0, 0, 0, 0)
        )
        
        style.configure('Elite.TNotebook.Tab',
            background=cls.COLORS['surface_1'],
            foreground=cls.COLORS['text_secondary'],
            padding=(cls.SPACING['xl'], cls.SPACING['md']),
            borderwidth=0,
            font=cls.FONTS['button']
        )
        
        style.map('Elite.TNotebook.Tab',
            background=[
                ('selected', cls.COLORS['surface_0']),
                ('active', cls.COLORS['surface_2'])
            ],
            foreground=[
                ('selected', cls.COLORS['primary']),
                ('active', cls.COLORS['text_primary'])
            ]
        )
        
        # ===== ELITE SCROLLBAR STYLES =====
        style.configure('Elite.Vertical.TScrollbar',
            background=cls.COLORS['border_light'],
            troughcolor=cls.COLORS['surface_1'],
            borderwidth=0,
            arrowsize=0,
            width=8
        )
        
        style.map('Elite.Vertical.TScrollbar',
            background=[('active', cls.COLORS['border_medium'])]
        )
        
        # ===== ELITE SEPARATOR STYLES =====
        style.configure('Elite.TSeparator',
            background=cls.COLORS['border_light']
        )
        
        # ===== ELITE PROGRESSBAR STYLES =====
        style.configure('Elite.TProgressbar',
            background=cls.COLORS['primary'],
            troughcolor=cls.COLORS['surface_2'],
            borderwidth=0,
            thickness=6
        )
        
        # Gradient progressbar
        style.configure('Elite.Gradient.TProgressbar',
            troughcolor=cls.COLORS['surface_2'],
            borderwidth=0,
            thickness=6
        )
    
    @classmethod
    def create_glass_card(cls, parent, **kwargs) -> tk.Frame:
        """Create a glassmorphism card with blur effect simulation"""
        card = tk.Frame(
            parent,
            bg=cls.COLORS['surface_0'],
            relief='flat',
            bd=0,
            **kwargs
        )
        
        # Simulate glass effect with border
        card.config(
            highlightbackground=cls.COLORS['glass_border'],
            highlightthickness=1
        )
        
        return card
    
    @classmethod
    def create_gradient_button(cls, parent, text, command, gradient_colors: Tuple[str, str], **kwargs) -> tk.Canvas:
        """Create a button with gradient background"""
        canvas = tk.Canvas(
            parent,
            height=48,
            bg=cls.COLORS['bg_secondary'],
            highlightthickness=0,
            **kwargs
        )
        
        # Create gradient (simplified - actual gradient would need PIL)
        start_color = gradient_colors[0]
        end_color = gradient_colors[1]
        
        # Create button rectangle
        btn_rect = canvas.create_rectangle(
            0, 0, 200, 48,
            fill=start_color,
            outline='',
            tags='button'
        )
        
        # Add text
        canvas.create_text(
            100, 24,
            text=text,
            fill=cls.COLORS['text_inverse'],
            font=cls.FONTS['button'],
            tags='button_text'
        )
        
        # Bind click event
        canvas.tag_bind('button', '<Button-1>', lambda e: command())
        canvas.tag_bind('button_text', '<Button-1>', lambda e: command())
        
        # Hover effects
        def on_enter(e):
            canvas.config(cursor='hand2')
            canvas.itemconfig(btn_rect, fill=end_color)
        
        def on_leave(e):
            canvas.config(cursor='')
            canvas.itemconfig(btn_rect, fill=start_color)
        
        canvas.tag_bind('button', '<Enter>', on_enter)
        canvas.tag_bind('button', '<Leave>', on_leave)
        canvas.tag_bind('button_text', '<Enter>', on_enter)
        canvas.tag_bind('button_text', '<Leave>', on_leave)
        
        return canvas
    
    @classmethod
    def create_metric_card(cls, parent, title: str, value: str, change: str = "", **kwargs) -> tk.Frame:
        """Create a KPI metric card"""
        card = cls.create_glass_card(parent, **kwargs)
        card.config(padx=cls.SPACING['lg'], pady=cls.SPACING['lg'])
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            bg=cls.COLORS['surface_0'],
            fg=cls.COLORS['text_secondary'],
            font=cls.FONTS['caption'],
            anchor='w'
        )
        title_label.pack(fill='x')
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            bg=cls.COLORS['surface_0'],
            fg=cls.COLORS['text_primary'],
            font=cls.FONTS['h2'],
            anchor='w'
        )
        value_label.pack(fill='x', pady=(cls.SPACING['xs'], 0))
        
        # Change indicator
        if change:
            change_color = cls.COLORS['success'] if '+' in change else cls.COLORS['error']
            change_label = tk.Label(
                card,
                text=change,
                bg=cls.COLORS['surface_0'],
                fg=change_color,
                font=cls.FONTS['caption'],
                anchor='w'
            )
            change_label.pack(fill='x', pady=(cls.SPACING['xs'], 0))
        
        return card
