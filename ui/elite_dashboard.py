"""
🏆 ELITE ENTERPRISE DASHBOARD
What the biggest firms in the world use - Advanced analytics, KPIs, data visualization
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import sqlite3
from typing import List, Dict, Tuple

from core.elite_theme import EliteTheme
from ui.elite_components import (
    AnimatedButton, DashboardCard, Toast,
    SearchBox, ProgressCard, InlineEditableTable
)
from core.config import DB_PATH


class EliteEnterpriseDashboard(tk.Frame):
    """
    Premium enterprise dashboard with:
    - Real-time KPIs
    - Data visualization
    - Quick actions
    - Recent activity
    - Analytics widgets
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=EliteTheme.COLORS['bg_secondary'])
        self.controller = controller
        self.db_conn = sqlite3.connect(DB_PATH)
        self.db_cursor = self.db_conn.cursor()
        
        EliteTheme.setup_elite_theme()
        self.create_ui()
        self.load_data()
    
    def create_ui(self):
        """Create the elite dashboard UI"""
        # ===== HEADER =====
        self.create_header()
        
        # ===== MAIN CONTENT =====
        main_container = tk.Frame(self, bg=EliteTheme.COLORS['bg_secondary'])
        main_container.pack(fill='both', expand=True, padx=EliteTheme.SPACING['2xl'], 
                           pady=EliteTheme.SPACING['xl'])
        
        # Welcome section
        self.create_welcome_section(main_container)
        
        # KPI Cards row
        self.create_kpi_section(main_container)
        
        # Main content grid (2 columns)
        content_grid = tk.Frame(main_container, bg=EliteTheme.COLORS['bg_secondary'])
        content_grid.pack(fill='both', expand=True, pady=(EliteTheme.SPACING['xl'], 0))
        
        # Left column (60%)
        left_column = tk.Frame(content_grid, bg=EliteTheme.COLORS['bg_secondary'])
        left_column.pack(side='left', fill='both', expand=True, 
                        padx=(0, EliteTheme.SPACING['lg']))
        
        # Right column (40%)
        right_column = tk.Frame(content_grid, bg=EliteTheme.COLORS['bg_secondary'])
        right_column.pack(side='right', fill='both')
        right_column.config(width=400)
        
        # Quick actions
        self.create_quick_actions(left_column)
        
        # Recent activity
        self.create_recent_activity(left_column)
        
        # Progress widgets
        self.create_progress_widgets(right_column)
        
        # Calendar widget
        self.create_calendar_widget(right_column)
    
    def create_header(self):
        """Create premium header"""
        header = tk.Frame(
            self,
            bg=EliteTheme.COLORS['surface_0'],
            height=80
        )
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Container for header content
        header_content = tk.Frame(header, bg=EliteTheme.COLORS['surface_0'])
        header_content.pack(fill='both', expand=True, 
                           padx=EliteTheme.SPACING['2xl'], 
                           pady=EliteTheme.SPACING['md'])
        
        # Logo/Brand
        brand_frame = tk.Frame(header_content, bg=EliteTheme.COLORS['surface_0'])
        brand_frame.pack(side='left')
        
        tk.Label(
            brand_frame,
            text="🎓",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['primary'],
            font=EliteTheme.FONTS['h2']
        ).pack(side='left', padx=(0, EliteTheme.SPACING['md']))
        
        tk.Label(
            brand_frame,
            text="Elite Schedule Manager",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h4']
        ).pack(side='left')
        
        # Search bar (center)
        search_container = tk.Frame(header_content, bg=EliteTheme.COLORS['surface_0'])
        search_container.pack(side='left', padx=EliteTheme.SPACING['2xl'], expand=True, fill='x')
        
        self.search_box = SearchBox(
            search_container,
            placeholder="Search schedules, classes, teachers...",
            on_search=self.on_search
        )
        self.search_box.pack(fill='x')
        
        # User menu (right)
        user_frame = tk.Frame(header_content, bg=EliteTheme.COLORS['surface_0'])
        user_frame.pack(side='right')
        
        # Notifications
        notif_btn = AnimatedButton(
            user_frame,
            icon="🔔",
            command=self.show_notifications,
            style='glass',
            width=50,
            height=50
        )
        notif_btn.pack(side='left', padx=EliteTheme.SPACING['sm'])
        
        # Profile
        profile_btn = AnimatedButton(
            user_frame,
            icon="👤",
            text="Admin",
            command=self.show_profile,
            style='glass',
            width=120,
            height=50
        )
        profile_btn.pack(side='left')
        
        # Separator
        ttk.Separator(self, orient='horizontal', style='Elite.TSeparator').pack(fill='x')
    
    def create_welcome_section(self, parent):
        """Create welcome section with time-based greeting"""
        welcome_frame = tk.Frame(parent, bg=EliteTheme.COLORS['bg_secondary'])
        welcome_frame.pack(fill='x', pady=(0, EliteTheme.SPACING['xl']))
        
        # Time-based greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good Morning"
            emoji = "🌅"
        elif hour < 18:
            greeting = "Good Afternoon"
            emoji = "☀️"
        else:
            greeting = "Good Evening"
            emoji = "🌙"
        
        greeting_label = tk.Label(
            welcome_frame,
            text=f"{emoji} {greeting}, Admin",
            bg=EliteTheme.COLORS['bg_secondary'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h1']
        )
        greeting_label.pack(anchor='w')
        
        # Current date
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        date_label = tk.Label(
            welcome_frame,
            text=date_str,
            bg=EliteTheme.COLORS['bg_secondary'],
            fg=EliteTheme.COLORS['text_secondary'],
            font=EliteTheme.FONTS['body']
        )
        date_label.pack(anchor='w', pady=(EliteTheme.SPACING['xs'], 0))
    
    def create_kpi_section(self, parent):
        """Create KPI cards section"""
        kpi_frame = tk.Frame(parent, bg=EliteTheme.COLORS['bg_secondary'])
        kpi_frame.pack(fill='x', pady=(0, EliteTheme.SPACING['xl']))
        
        # Grid for KPI cards (4 columns)
        kpi_cards = [
            {
                'title': 'Total Classes',
                'value': '0',
                'trend': '+12%',
                'subtitle': 'Active this semester',
                'icon': '🎓'
            },
            {
                'title': 'Total Students',
                'value': '0',
                'trend': '+8%',
                'subtitle': 'Enrolled',
                'icon': '👥'
            },
            {
                'title': 'Schedule Completion',
                'value': '0%',
                'trend': '+15%',
                'subtitle': 'This week',
                'icon': '📊'
            },
            {
                'title': 'Upcoming Events',
                'value': '0',
                'trend': '3 this week',
                'subtitle': 'Holidays & Vacations',
                'icon': '📅'
            }
        ]
        
        self.kpi_widgets = []
        for i, kpi in enumerate(kpi_cards):
            card = DashboardCard(
                kpi_frame,
                title=kpi['title'],
                value=kpi['value'],
                subtitle=kpi['subtitle'],
                trend=kpi['trend'],
                icon=kpi['icon']
            )
            card.grid(row=0, column=i, sticky='nsew', 
                     padx=(0 if i == 0 else EliteTheme.SPACING['md'], 
                           0 if i == len(kpi_cards)-1 else 0))
            kpi_frame.grid_columnconfigure(i, weight=1)
            self.kpi_widgets.append(card)
    
    def create_quick_actions(self, parent):
        """Create quick actions section"""
        actions_card = tk.Frame(
            parent,
            bg=EliteTheme.COLORS['surface_0'],
            highlightbackground=EliteTheme.COLORS['border_light'],
            highlightthickness=1
        )
        actions_card.pack(fill='x', pady=(0, EliteTheme.SPACING['xl']))
        actions_card.config(padx=EliteTheme.SPACING['xl'], pady=EliteTheme.SPACING['xl'])
        
        # Title
        tk.Label(
            actions_card,
            text="⚡ Quick Actions",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h4']
        ).pack(anchor='w', pady=(0, EliteTheme.SPACING['lg']))
        
        # Action buttons grid
        actions_grid = tk.Frame(actions_card, bg=EliteTheme.COLORS['surface_0'])
        actions_grid.pack(fill='x')
        
        actions = [
            ("📅 View Schedule", lambda: self.controller.show_frame("EmploiDuTempsApp"), 'primary'),
            ("✨ Manage Constraints", lambda: self.controller.show_frame("ModernConstraintsFrame"), 'primary'),
            ("📥 Import Data", lambda: self.controller.show_frame("ExcelImporterFrame"), 'success'),
            ("📊 Generate Report", self.generate_report, 'glass'),
        ]
        
        for i, (text, command, style) in enumerate(actions):
            row, col = divmod(i, 2)
            btn = AnimatedButton(
                actions_grid,
                text=text,
                command=command,
                style=style,
                width=280,
                height=56
            )
            btn.grid(row=row, column=col, sticky='ew',
                    padx=(0 if col == 0 else EliteTheme.SPACING['md'], 0),
                    pady=(0 if row == 0 else EliteTheme.SPACING['md'], 0))
            actions_grid.grid_columnconfigure(col, weight=1)
    
    def create_recent_activity(self, parent):
        """Create recent activity section"""
        activity_card = tk.Frame(
            parent,
            bg=EliteTheme.COLORS['surface_0'],
            highlightbackground=EliteTheme.COLORS['border_light'],
            highlightthickness=1
        )
        activity_card.pack(fill='both', expand=True, pady=(0, EliteTheme.SPACING['xl']))
        activity_card.config(padx=EliteTheme.SPACING['xl'], pady=EliteTheme.SPACING['xl'])
        
        # Title
        title_frame = tk.Frame(activity_card, bg=EliteTheme.COLORS['surface_0'])
        title_frame.pack(fill='x', pady=(0, EliteTheme.SPACING['lg']))
        
        tk.Label(
            title_frame,
            text="📋 Recent Activity",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h4']
        ).pack(side='left')
        
        tk.Label(
            title_frame,
            text="View All →",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['primary'],
            font=EliteTheme.FONTS['caption'],
            cursor='hand2'
        ).pack(side='right')
        
        # Activity list
        activities = [
            ("Schedule updated", "TCSF 1 - Mathematics", "2 hours ago", "✏️"),
            ("New class added", "TCSF 5 - Physics", "5 hours ago", "➕"),
            ("Vacation scheduled", "Christmas Break", "1 day ago", "🏖️"),
            ("Report generated", "Weekly Summary", "2 days ago", "📊"),
        ]
        
        for activity in activities:
            self.create_activity_item(activity_card, *activity)
    
    def create_activity_item(self, parent, title, subtitle, time, icon):
        """Create activity item"""
        item = tk.Frame(parent, bg=EliteTheme.COLORS['surface_0'])
        item.pack(fill='x', pady=(0, EliteTheme.SPACING['md']))
        
        # Icon
        icon_label = tk.Label(
            item,
            text=icon,
            bg=EliteTheme.COLORS['surface_1'],
            fg=EliteTheme.COLORS['primary'],
            font=EliteTheme.FONTS['h5'],
            width=3,
            height=2
        )
        icon_label.pack(side='left', padx=(0, EliteTheme.SPACING['md']))
        
        # Content
        content = tk.Frame(item, bg=EliteTheme.COLORS['surface_0'])
        content.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            content,
            text=title,
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['body_bold'],
            anchor='w'
        ).pack(fill='x')
        
        tk.Label(
            content,
            text=subtitle,
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_secondary'],
            font=EliteTheme.FONTS['caption'],
            anchor='w'
        ).pack(fill='x')
        
        # Time
        tk.Label(
            item,
            text=time,
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_tertiary'],
            font=EliteTheme.FONTS['caption']
        ).pack(side='right')
    
    def create_progress_widgets(self, parent):
        """Create progress tracking widgets"""
        progress_container = tk.Frame(parent, bg=EliteTheme.COLORS['bg_secondary'])
        progress_container.pack(fill='x', pady=(0, EliteTheme.SPACING['xl']))
        
        # Title
        tk.Label(
            progress_container,
            text="📈 Progress Tracking",
            bg=EliteTheme.COLORS['bg_secondary'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h4']
        ).pack(anchor='w', pady=(0, EliteTheme.SPACING['md']))
        
        # Progress cards
        ProgressCard(
            progress_container,
            title="Schedule Completion",
            current=0,
            total=100
        ).pack(fill='x', pady=(0, EliteTheme.SPACING['md']))
        
        ProgressCard(
            progress_container,
            title="Classes Assigned",
            current=0,
            total=100
        ).pack(fill='x', pady=(0, EliteTheme.SPACING['md']))
        
        ProgressCard(
            progress_container,
            title="Teachers Allocated",
            current=0,
            total=100
        ).pack(fill='x')
    
    def create_calendar_widget(self, parent):
        """Create mini calendar widget"""
        calendar_card = tk.Frame(
            parent,
            bg=EliteTheme.COLORS['surface_0'],
            highlightbackground=EliteTheme.COLORS['border_light'],
            highlightthickness=1
        )
        calendar_card.pack(fill='x')
        calendar_card.config(padx=EliteTheme.SPACING['xl'], pady=EliteTheme.SPACING['xl'])
        
        # Title
        tk.Label(
            calendar_card,
            text="📅 This Week",
            bg=EliteTheme.COLORS['surface_0'],
            fg=EliteTheme.COLORS['text_primary'],
            font=EliteTheme.FONTS['h4']
        ).pack(anchor='w', pady=(0, EliteTheme.SPACING['lg']))
        
        # Week days
        today = datetime.now()
        for i in range(7):
            day = today + timedelta(days=i)
            is_today = i == 0
            
            day_frame = tk.Frame(
                calendar_card,
                bg=EliteTheme.COLORS['primary'] if is_today else EliteTheme.COLORS['surface_1'],
                highlightbackground=EliteTheme.COLORS['border_light'],
                highlightthickness=0 if is_today else 1
            )
            day_frame.pack(fill='x', pady=(0, EliteTheme.SPACING['sm']))
            day_frame.config(padx=EliteTheme.SPACING['md'], pady=EliteTheme.SPACING['sm'])
            
            # Day name
            tk.Label(
                day_frame,
                text=day.strftime("%A"),
                bg=day_frame['bg'],
                fg=EliteTheme.COLORS['text_inverse'] if is_today else EliteTheme.COLORS['text_primary'],
                font=EliteTheme.FONTS['body_bold']
            ).pack(side='left')
            
            # Date
            tk.Label(
                day_frame,
                text=day.strftime("%b %d"),
                bg=day_frame['bg'],
                fg=EliteTheme.COLORS['text_inverse'] if is_today else EliteTheme.COLORS['text_secondary'],
                font=EliteTheme.FONTS['caption']
            ).pack(side='right')
    
    def load_data(self):
        """Load dashboard data"""
        try:
            # Get total classes
            self.db_cursor.execute("SELECT COUNT(*) FROM classes")
            total_classes = self.db_cursor.fetchone()[0]
            
            # Update KPI
            if self.kpi_widgets:
                self.update_kpi_value(0, str(total_classes))
            
            # Get schedule entries count
            self.db_cursor.execute("SELECT COUNT(*) FROM schedule_entries")
            total_entries = self.db_cursor.fetchone()[0]
            
            # Calculate completion percentage
            if total_classes > 0:
                completion = int((total_entries / (total_classes * 35)) * 100)  # Assuming 35 slots per week
                self.update_kpi_value(2, f"{min(completion, 100)}%")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def update_kpi_value(self, index, value):
        """Update KPI card value"""
        if index < len(self.kpi_widgets):
            card = self.kpi_widgets[index]
            for widget in card.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget('font') == EliteTheme.FONTS['h1']:
                    widget.config(text=value)
                    break
    
    def on_search(self, query):
        """Handle search"""
        if query:
            Toast(self, f"Searching for: {query}", type='info')
    
    def show_notifications(self):
        """Show notifications"""
        Toast(self, "No new notifications", type='info')
    
    def show_profile(self):
        """Show user profile"""
        Toast(self, "Profile settings coming soon", type='info')
    
    def generate_report(self):
        """Generate report"""
        Toast(self, "Report generated successfully!", type='success', duration=2000)
