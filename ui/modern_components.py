"""
Modern UI Components Library
Reusable components for building beautiful interfaces
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, List, Dict, Any
from core.modern_theme import ModernTheme


class ModernCard(tk.Frame):
    """A beautiful card component with shadow and hover effects"""
    
    def __init__(self, parent, title="", subtitle="", **kwargs):
        super().__init__(
            parent,
            bg=ModernTheme.COLORS['card_bg'],
            relief='flat',
            bd=0,
            highlightbackground=ModernTheme.COLORS['border'],
            highlightthickness=1,
            **kwargs
        )
        
        self.title_text = title
        self.subtitle_text = subtitle
        
        if title or subtitle:
            self.header_frame = tk.Frame(self, bg=ModernTheme.COLORS['card_bg'])
            self.header_frame.pack(fill='x', padx=ModernTheme.SPACING['md'], 
                                  pady=(ModernTheme.SPACING['md'], ModernTheme.SPACING['sm']))
            
            if title:
                self.title_label = tk.Label(
                    self.header_frame,
                    text=title,
                    bg=ModernTheme.COLORS['card_bg'],
                    fg=ModernTheme.COLORS['text_primary'],
                    font=ModernTheme.FONTS['subheading'],
                    anchor='w'
                )
                self.title_label.pack(fill='x')
            
            if subtitle:
                self.subtitle_label = tk.Label(
                    self.header_frame,
                    text=subtitle,
                    bg=ModernTheme.COLORS['card_bg'],
                    fg=ModernTheme.COLORS['text_secondary'],
                    font=ModernTheme.FONTS['small'],
                    anchor='w'
                )
                self.subtitle_label.pack(fill='x', pady=(ModernTheme.SPACING['xs'], 0))
        
        # Content area
        self.content_frame = tk.Frame(self, bg=ModernTheme.COLORS['card_bg'])
        self.content_frame.pack(fill='both', expand=True, 
                               padx=ModernTheme.SPACING['md'], 
                               pady=(0, ModernTheme.SPACING['md']))
    
    def add_action_button(self, text, command, style='primary'):
        """Add an action button to the card footer"""
        if not hasattr(self, 'footer_frame'):
            ttk.Separator(self, orient='horizontal').pack(fill='x', pady=ModernTheme.SPACING['sm'])
            self.footer_frame = tk.Frame(self, bg=ModernTheme.COLORS['card_bg'])
            self.footer_frame.pack(fill='x', padx=ModernTheme.SPACING['md'], 
                                  pady=(0, ModernTheme.SPACING['md']))
        
        style_map = {
            'primary': 'Primary.TButton',
            'secondary': 'Secondary.TButton',
            'success': 'Success.TButton',
            'danger': 'Danger.TButton',
            'outline': 'Outline.TButton'
        }
        
        button = ttk.Button(
            self.footer_frame,
            text=text,
            command=command,
            style=style_map.get(style, 'Primary.TButton')
        )
        button.pack(side='right', padx=(ModernTheme.SPACING['sm'], 0))
        return button


class ModernTable(ttk.Frame):
    """A modern table/grid component with CRUD operations"""
    
    def __init__(self, parent, columns: List[Dict[str, Any]], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.columns = columns  # [{'id': 'name', 'label': 'Name', 'width': 200}, ...]
        self.data = []
        self.selected_item = None
        
        # Create table
        self.create_table()
    
    def create_table(self):
        """Create the table structure"""
        # Container with scrollbars
        container = tk.Frame(self, bg=ModernTheme.COLORS['surface'])
        container.pack(fill='both', expand=True)
        
        # Treeview
        column_ids = [col['id'] for col in self.columns]
        self.tree = ttk.Treeview(
            container,
            columns=column_ids,
            show='headings',
            selectmode='browse'
        )
        
        # Configure columns
        for col in self.columns:
            self.tree.heading(col['id'], text=col['label'])
            self.tree.column(col['id'], width=col.get('width', 150), anchor=col.get('anchor', 'w'))
        
        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def on_select(self, event):
        """Handle row selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_item = item['values']
    
    def insert(self, values: tuple):
        """Insert a new row"""
        self.tree.insert('', 'end', values=values)
        self.data.append(values)
    
    def update_selected(self, values: tuple):
        """Update the selected row"""
        selection = self.tree.selection()
        if selection:
            self.tree.item(selection[0], values=values)
            return True
        return False
    
    def delete_selected(self):
        """Delete the selected row"""
        selection = self.tree.selection()
        if selection:
            self.tree.delete(selection[0])
            return True
        return False
    
    def clear(self):
        """Clear all rows"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data.clear()
    
    def get_selected(self) -> Optional[tuple]:
        """Get the selected row data"""
        return self.selected_item


class ModernFormField(tk.Frame):
    """A modern form field with label and validation"""
    
    def __init__(self, parent, label, field_type='entry', options=None, required=False, **kwargs):
        super().__init__(parent, bg=ModernTheme.COLORS['background'])
        
        self.label_text = label
        self.required = required
        self.field_type = field_type
        self.options = options or []
        
        # Label
        label_frame = tk.Frame(self, bg=ModernTheme.COLORS['background'])
        label_frame.pack(fill='x', pady=(0, ModernTheme.SPACING['xs']))
        
        label_widget = tk.Label(
            label_frame,
            text=label + (' *' if required else ''),
            bg=ModernTheme.COLORS['background'],
            fg=ModernTheme.COLORS['text_primary'],
            font=ModernTheme.FONTS['body_bold'],
            anchor='w'
        )
        label_widget.pack(side='left')
        
        # Field
        if field_type == 'entry':
            self.widget = ttk.Entry(self, **kwargs)
        elif field_type == 'text':
            text_frame = tk.Frame(self, bg=ModernTheme.COLORS['surface'])
            text_frame.pack(fill='both', expand=True)
            
            self.widget = tk.Text(
                text_frame,
                height=4,
                bg=ModernTheme.COLORS['surface'],
                fg=ModernTheme.COLORS['text_primary'],
                font=ModernTheme.FONTS['body'],
                relief='solid',
                borderwidth=2,
                bd=2
            )
            self.widget.pack(side='left', fill='both', expand=True)
            
            scrollbar = ttk.Scrollbar(text_frame, command=self.widget.yview)
            scrollbar.pack(side='right', fill='y')
            self.widget.config(yscrollcommand=scrollbar.set)
        elif field_type == 'combobox':
            self.widget = ttk.Combobox(self, values=self.options, state='readonly', **kwargs)
            if self.options:
                self.widget.current(0)
        elif field_type == 'date':
            self.widget = ttk.Entry(self, **kwargs)
            # Add date picker icon/button here if needed
        else:
            self.widget = ttk.Entry(self, **kwargs)
        
        if field_type != 'text':
            self.widget.pack(fill='x')
        
        # Error label
        self.error_label = tk.Label(
            self,
            text="",
            bg=ModernTheme.COLORS['background'],
            fg=ModernTheme.COLORS['error'],
            font=ModernTheme.FONTS['small'],
            anchor='w'
        )
        self.error_label.pack(fill='x', pady=(ModernTheme.SPACING['xs'], 0))
    
    def get(self) -> str:
        """Get field value"""
        if self.field_type == 'text':
            return self.widget.get('1.0', 'end-1c')
        return self.widget.get()
    
    def set(self, value: str):
        """Set field value"""
        if self.field_type == 'text':
            self.widget.delete('1.0', 'end')
            self.widget.insert('1.0', value)
        else:
            self.widget.delete(0, 'end')
            self.widget.insert(0, value)
    
    def clear(self):
        """Clear field value"""
        if self.field_type == 'text':
            self.widget.delete('1.0', 'end')
        else:
            self.widget.delete(0, 'end')
    
    def validate(self) -> bool:
        """Validate field"""
        value = self.get().strip()
        
        if self.required and not value:
            self.show_error(f"{self.label_text} est requis")
            return False
        
        self.clear_error()
        return True
    
    def show_error(self, message: str):
        """Show error message"""
        self.error_label.config(text=message)
        self.widget.config(style='Error.TEntry' if self.field_type != 'text' else '')
    
    def clear_error(self):
        """Clear error message"""
        self.error_label.config(text="")


class ModernDialog(tk.Toplevel):
    """A modern dialog window"""
    
    def __init__(self, parent, title="Dialog", width=500, height=400):
        super().__init__(parent)
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.configure(bg=ModernTheme.COLORS['background'])
        self.resizable(False, False)
        
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Content frame
        self.content = tk.Frame(
            self,
            bg=ModernTheme.COLORS['background'],
            padx=ModernTheme.SPACING['lg'],
            pady=ModernTheme.SPACING['lg']
        )
        self.content.pack(fill='both', expand=True)
        
        self.result = None
    
    def add_button_bar(self, buttons: List[Dict[str, Any]]):
        """Add button bar at the bottom"""
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=(ModernTheme.SPACING['md'], 0))
        
        button_frame = tk.Frame(
            self,
            bg=ModernTheme.COLORS['background'],
            padx=ModernTheme.SPACING['lg'],
            pady=ModernTheme.SPACING['md']
        )
        button_frame.pack(fill='x')
        
        for btn in buttons:
            button = ttk.Button(
                button_frame,
                text=btn.get('text', 'Button'),
                command=btn.get('command'),
                style=btn.get('style', 'Primary.TButton')
            )
            button.pack(side='right', padx=(ModernTheme.SPACING['sm'], 0))


class ModernSearchBar(tk.Frame):
    """A modern search bar with icon"""
    
    def __init__(self, parent, placeholder="Search...", on_search: Callable = None, **kwargs):
        super().__init__(parent, bg=ModernTheme.COLORS['background'])
        
        self.on_search = on_search
        
        # Search icon
        icon_label = tk.Label(
            self,
            text="🔍",
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_muted'],
            font=ModernTheme.FONTS['body'],
            padx=ModernTheme.SPACING['sm']
        )
        icon_label.pack(side='left')
        
        # Entry
        self.entry = ttk.Entry(self, **kwargs)
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.insert(0, placeholder)
        self.entry.config(foreground=ModernTheme.COLORS['text_muted'])
        
        # Placeholder handling
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyRelease>', self.on_key_release)
        
        self.placeholder = placeholder
        self.has_placeholder = True
    
    def on_focus_in(self, event):
        if self.has_placeholder:
            self.entry.delete(0, 'end')
            self.entry.config(foreground=ModernTheme.COLORS['text_primary'])
            self.has_placeholder = False
    
    def on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(foreground=ModernTheme.COLORS['text_muted'])
            self.has_placeholder = True
    
    def on_key_release(self, event):
        if self.on_search and not self.has_placeholder:
            self.on_search(self.entry.get())
    
    def get(self) -> str:
        if self.has_placeholder:
            return ""
        return self.entry.get()


class ModernStatusBar(tk.Frame):
    """A modern status bar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=ModernTheme.COLORS['surface'],
            relief='flat',
            bd=0,
            highlightbackground=ModernTheme.COLORS['border'],
            highlightthickness=1,
            **kwargs
        )
        
        self.label = tk.Label(
            self,
            text="Ready",
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_secondary'],
            font=ModernTheme.FONTS['small'],
            anchor='w',
            padx=ModernTheme.SPACING['md'],
            pady=ModernTheme.SPACING['sm']
        )
        self.label.pack(fill='both')
    
    def set_status(self, text: str, status_type='info'):
        """Set status text with color"""
        color_map = {
            'info': ModernTheme.COLORS['text_secondary'],
            'success': ModernTheme.COLORS['success'],
            'warning': ModernTheme.COLORS['warning'],
            'error': ModernTheme.COLORS['error']
        }
        
        self.label.config(
            text=text,
            fg=color_map.get(status_type, ModernTheme.COLORS['text_secondary'])
        )
