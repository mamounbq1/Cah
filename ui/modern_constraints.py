"""
Modern Constraint Management UI
Beautiful, creative interface with full CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional, Dict, Any
import sqlite3

from core.modern_theme import ModernTheme
from ui.modern_components import (
    ModernCard, ModernTable, ModernFormField, 
    ModernDialog, ModernSearchBar, ModernStatusBar
)
from core.config import DB_PATH


class ModernConstraintsFrame(tk.Frame):
    """Modern constraint management with tabbed interface"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=ModernTheme.COLORS['background'])
        self.controller = controller
        self.db_conn = sqlite3.connect(DB_PATH)
        self.db_cursor = self.db_conn.cursor()
        
        ModernTheme.setup_theme()
        self.create_ui()
    
    def create_ui(self):
        """Create the main UI"""
        # Header
        self.create_header()
        
        # Notebook for different constraint types
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=ModernTheme.SPACING['lg'], 
                          pady=ModernTheme.SPACING['md'])
        
        # Create tabs
        self.create_vacances_tab()
        self.create_holidays_tab()
        self.create_absences_tab()
        self.create_classes_tab()
        self.create_modules_tab()
        
        # Status bar
        self.status_bar = ModernStatusBar(self)
        self.status_bar.pack(fill='x', side='bottom')
    
    def create_header(self):
        """Create header with title and back button"""
        header = tk.Frame(self, bg=ModernTheme.COLORS['surface'], height=80)
        header.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        header.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            header,
            text="← Retour",
            command=lambda: self.controller.show_frame("HomeFrame"),
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['primary'],
            font=ModernTheme.FONTS['body_bold'],
            bd=0,
            relief='flat',
            cursor='hand2',
            padx=ModernTheme.SPACING['lg'],
            pady=ModernTheme.SPACING['md']
        )
        back_btn.pack(side='left')
        
        # Title
        title = tk.Label(
            header,
            text="Gestion des Contraintes",
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            font=ModernTheme.FONTS['heading']
        )
        title.pack(side='left', padx=ModernTheme.SPACING['lg'])
        
        # Subtitle
        subtitle = tk.Label(
            header,
            text="Gérez les vacances, jours fériés, absences, classes et modules",
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_secondary'],
            font=ModernTheme.FONTS['body']
        )
        subtitle.pack(side='left')
    
    def create_vacances_tab(self):
        """Create vacation management tab"""
        tab = VacancesManagementTab(self.notebook, self.db_conn)
        self.notebook.add(tab, text="🏖️  Vacances")
    
    def create_holidays_tab(self):
        """Create holidays management tab"""
        tab = HolidaysManagementTab(self.notebook, self.db_conn)
        self.notebook.add(tab, text="🎉  Jours Fériés")
    
    def create_absences_tab(self):
        """Create absences management tab"""
        tab = AbsencesManagementTab(self.notebook, self.db_conn)
        self.notebook.add(tab, text="📅  Absences")
    
    def create_classes_tab(self):
        """Create classes management tab"""
        tab = ClassesManagementTab(self.notebook, self.db_conn)
        self.notebook.add(tab, text="🎓  Classes")
    
    def create_modules_tab(self):
        """Create modules management tab"""
        tab = ModulesManagementTab(self.notebook, self.db_conn)
        self.notebook.add(tab, text="📚  Modules")


class BaseManagementTab(tk.Frame):
    """Base class for all management tabs with CRUD operations"""
    
    def __init__(self, parent, db_conn, title="", subtitle=""):
        super().__init__(parent, bg=ModernTheme.COLORS['background'])
        self.db_conn = db_conn
        self.db_cursor = db_conn.cursor()
        self.title = title
        self.subtitle = subtitle
        
        self.create_layout()
    
    def create_layout(self):
        """Create the standard layout"""
        # Main container with two columns
        main_container = tk.Frame(self, bg=ModernTheme.COLORS['background'])
        main_container.pack(fill='both', expand=True, padx=ModernTheme.SPACING['lg'], 
                           pady=ModernTheme.SPACING['lg'])
        
        # Left column - Form (40%)
        self.left_column = tk.Frame(main_container, bg=ModernTheme.COLORS['background'])
        self.left_column.pack(side='left', fill='both', expand=False, 
                             padx=(0, ModernTheme.SPACING['md']))
        self.left_column.config(width=400)
        
        # Right column - Table (60%)
        self.right_column = tk.Frame(main_container, bg=ModernTheme.COLORS['background'])
        self.right_column.pack(side='right', fill='both', expand=True)
        
        self.create_form_card()
        self.create_data_card()
    
    def create_form_card(self):
        """Create form card - to be overridden"""
        pass
    
    def create_data_card(self):
        """Create data display card - to be overridden"""
        pass
    
    def clear_form(self):
        """Clear form fields - to be overridden"""
        pass
    
    def validate_form(self) -> bool:
        """Validate form - to be overridden"""
        return True
    
    def save_data(self):
        """Save data - to be overridden"""
        pass
    
    def update_data(self):
        """Update data - to be overridden"""
        pass
    
    def delete_data(self):
        """Delete data - to be overridden"""
        pass
    
    def refresh_table(self):
        """Refresh table data - to be overridden"""
        pass


class VacancesManagementTab(BaseManagementTab):
    """Vacation management with full CRUD"""
    
    def __init__(self, parent, db_conn):
        super().__init__(parent, db_conn, "Vacances", "Gérez les périodes de vacances scolaires")
        self.edit_mode = False
        self.current_id = None
    
    def create_form_card(self):
        """Create vacation form"""
        card = ModernCard(self.left_column, title="➕ Ajouter une Vacance", 
                         subtitle="Remplissez les informations ci-dessous")
        card.pack(fill='both', expand=True)
        
        form_container = card.content_frame
        
        # Form fields
        self.label_field = ModernFormField(form_container, "Nom de la vacance", required=True)
        self.label_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.start_date_field = ModernFormField(form_container, "Date de début (YYYY-MM-DD)", required=True)
        self.start_date_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.end_date_field = ModernFormField(form_container, "Date de fin (YYYY-MM-DD)", required=True)
        self.end_date_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        # Buttons
        button_frame = tk.Frame(form_container, bg=ModernTheme.COLORS['card_bg'])
        button_frame.pack(fill='x', pady=(ModernTheme.SPACING['lg'], 0))
        
        self.save_btn = ttk.Button(
            button_frame,
            text="💾 Enregistrer",
            command=self.save_vacation,
            style='Success.TButton'
        )
        self.save_btn.pack(side='left', padx=(0, ModernTheme.SPACING['sm']))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🔄 Réinitialiser",
            command=self.clear_form,
            style='Outline.TButton'
        )
        self.clear_btn.pack(side='left')
    
    def create_data_card(self):
        """Create vacation data table"""
        card = ModernCard(self.right_column, title="📋 Liste des Vacances", 
                         subtitle="Cliquez sur une ligne pour modifier ou supprimer")
        card.pack(fill='both', expand=True)
        
        # Search bar
        search_frame = tk.Frame(card.content_frame, bg=ModernTheme.COLORS['card_bg'])
        search_frame.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.search_bar = ModernSearchBar(search_frame, placeholder="Rechercher une vacance...", 
                                         on_search=self.search_vacations)
        self.search_bar.pack(fill='x')
        
        # Table
        columns = [
            {'id': 'id', 'label': 'ID', 'width': 50},
            {'id': 'label', 'label': 'Nom', 'width': 200},
            {'id': 'start_date', 'label': 'Début', 'width': 120},
            {'id': 'end_date', 'label': 'Fin', 'width': 120},
        ]
        
        self.table = ModernTable(card.content_frame, columns)
        self.table.pack(fill='both', expand=True, pady=(0, ModernTheme.SPACING['md']))
        
        # Action buttons
        action_frame = tk.Frame(card.content_frame, bg=ModernTheme.COLORS['card_bg'])
        action_frame.pack(fill='x')
        
        ttk.Button(
            action_frame,
            text="✏️ Modifier",
            command=self.edit_vacation,
            style='Secondary.TButton'
        ).pack(side='left', padx=(0, ModernTheme.SPACING['sm']))
        
        ttk.Button(
            action_frame,
            text="🗑️ Supprimer",
            command=self.delete_vacation,
            style='Danger.TButton'
        ).pack(side='left')
        
        ttk.Button(
            action_frame,
            text="🔄 Actualiser",
            command=self.refresh_table,
            style='Outline.TButton'
        ).pack(side='right')
        
        self.refresh_table()
    
    def save_vacation(self):
        """Save or update vacation"""
        # Validate
        if not all([
            self.label_field.validate(),
            self.start_date_field.validate(),
            self.end_date_field.validate()
        ]):
            return
        
        label = self.label_field.get().strip()
        start_date = self.start_date_field.get().strip()
        end_date = self.end_date_field.get().strip()
        
        # Validate dates
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez YYYY-MM-DD")
            return
        
        try:
            if self.edit_mode and self.current_id:
                # Update
                self.db_cursor.execute(
                    "UPDATE vacances SET label=?, start_date=?, end_date=? WHERE id=?",
                    (label, start_date, end_date, self.current_id)
                )
                message = "Vacance modifiée avec succès!"
            else:
                # Insert
                self.db_cursor.execute(
                    "INSERT INTO vacances (label, start_date, end_date) VALUES (?, ?, ?)",
                    (label, start_date, end_date)
                )
                message = "Vacance ajoutée avec succès!"
            
            self.db_conn.commit()
            messagebox.showinfo("Succès", message)
            self.clear_form()
            self.refresh_table()
            
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur de base de données: {e}")
    
    def edit_vacation(self):
        """Edit selected vacation"""
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une vacance à modifier")
            return
        
        self.edit_mode = True
        self.current_id = selected[0]
        
        self.label_field.set(selected[1])
        self.start_date_field.set(selected[2])
        self.end_date_field.set(selected[3])
        
        self.save_btn.config(text="💾 Mettre à jour")
    
    def delete_vacation(self):
        """Delete selected vacation"""
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une vacance à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", 
                               f"Voulez-vous vraiment supprimer la vacance '{selected[1]}'?"):
            try:
                self.db_cursor.execute("DELETE FROM vacances WHERE id=?", (selected[0],))
                self.db_conn.commit()
                messagebox.showinfo("Succès", "Vacance supprimée avec succès!")
                self.refresh_table()
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur de base de données: {e}")
    
    def clear_form(self):
        """Clear form fields"""
        self.label_field.clear()
        self.start_date_field.clear()
        self.end_date_field.clear()
        self.edit_mode = False
        self.current_id = None
        self.save_btn.config(text="💾 Enregistrer")
    
    def refresh_table(self):
        """Refresh vacation table"""
        self.table.clear()
        self.db_cursor.execute("SELECT id, label, start_date, end_date FROM vacances ORDER BY start_date")
        for row in self.db_cursor.fetchall():
            self.table.insert(row)
    
    def search_vacations(self, query: str):
        """Search vacations"""
        self.table.clear()
        self.db_cursor.execute(
            "SELECT id, label, start_date, end_date FROM vacances WHERE label LIKE ? ORDER BY start_date",
            (f"%{query}%",)
        )
        for row in self.db_cursor.fetchall():
            self.table.insert(row)


class HolidaysManagementTab(BaseManagementTab):
    """Similar structure for holidays - simplified version"""
    
    def __init__(self, parent, db_conn):
        super().__init__(parent, db_conn)
        self.edit_mode = False
        self.current_id = None
    
    def create_form_card(self):
        card = ModernCard(self.left_column, title="➕ Ajouter un Jour Férié")
        card.pack(fill='both', expand=True)
        
        self.label_field = ModernFormField(card.content_frame, "Nom du jour férié", required=True)
        self.label_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.date_field = ModernFormField(card.content_frame, "Date (YYYY-MM-DD)", required=True)
        self.date_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        button_frame = tk.Frame(card.content_frame, bg=ModernTheme.COLORS['card_bg'])
        button_frame.pack(fill='x', pady=(ModernTheme.SPACING['lg'], 0))
        
        ttk.Button(button_frame, text="💾 Enregistrer", command=self.save_holiday,
                  style='Success.TButton').pack(side='left', padx=(0, ModernTheme.SPACING['sm']))
        ttk.Button(button_frame, text="🔄 Réinitialiser", command=self.clear_form,
                  style='Outline.TButton').pack(side='left')
    
    def create_data_card(self):
        card = ModernCard(self.right_column, title="📋 Liste des Jours Fériés")
        card.pack(fill='both', expand=True)
        
        columns = [
            {'id': 'id', 'label': 'ID', 'width': 50},
            {'id': 'label', 'label': 'Nom', 'width': 250},
            {'id': 'date', 'label': 'Date', 'width': 150}
        ]
        
        self.table = ModernTable(card.content_frame, columns)
        self.table.pack(fill='both', expand=True)
        
        self.refresh_table()
    
    def save_holiday(self):
        if not all([self.label_field.validate(), self.date_field.validate()]):
            return
        
        label = self.label_field.get().strip()
        date = self.date_field.get().strip()
        
        try:
            self.db_cursor.execute("INSERT INTO jours_feries (label, date) VALUES (?, ?)", (label, date))
            self.db_conn.commit()
            messagebox.showinfo("Succès", "Jour férié ajouté!")
            self.clear_form()
            self.refresh_table()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", str(e))
    
    def clear_form(self):
        self.label_field.clear()
        self.date_field.clear()
    
    def refresh_table(self):
        self.table.clear()
        self.db_cursor.execute("SELECT id, label, date FROM jours_feries ORDER BY date")
        for row in self.db_cursor.fetchall():
            self.table.insert(row)


# Similar classes for AbsencesManagementTab, ClassesManagementTab, and ModulesManagementTab
# Following the same pattern...

class AbsencesManagementTab(BaseManagementTab):
    """Absences management"""
    
    def __init__(self, parent, db_conn):
        super().__init__(parent, db_conn)
    
    def create_form_card(self):
        card = ModernCard(self.left_column, title="➕ Ajouter une Absence")
        card.pack(fill='both', expand=True)
        
        self.date_field = ModernFormField(card.content_frame, "Date (YYYY-MM-DD)", required=True)
        self.date_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.motif_field = ModernFormField(card.content_frame, "Motif", field_type='text', required=True)
        self.motif_field.pack(fill='both', expand=True, pady=(0, ModernTheme.SPACING['md']))
        
        ttk.Button(card.content_frame, text="💾 Enregistrer", command=self.save_absence,
                  style='Success.TButton').pack()
    
    def create_data_card(self):
        card = ModernCard(self.right_column, title="📋 Liste des Absences")
        card.pack(fill='both', expand=True)
        
        columns = [
            {'id': 'id', 'label': 'ID', 'width': 50},
            {'id': 'date', 'label': 'Date', 'width': 150},
            {'id': 'motif', 'label': 'Motif', 'width': 300}
        ]
        
        self.table = ModernTable(card.content_frame, columns)
        self.table.pack(fill='both', expand=True)
        self.refresh_table()
    
    def save_absence(self):
        if not all([self.date_field.validate(), self.motif_field.validate()]):
            return
        
        date = self.date_field.get().strip()
        motif = self.motif_field.get().strip()
        
        try:
            self.db_cursor.execute("INSERT INTO absences (date, motif) VALUES (?, ?)", (date, motif))
            self.db_conn.commit()
            messagebox.showinfo("Succès", "Absence ajoutée!")
            self.clear_form()
            self.refresh_table()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", str(e))
    
    def clear_form(self):
        self.date_field.clear()
        self.motif_field.clear()
    
    def refresh_table(self):
        self.table.clear()
        self.db_cursor.execute("SELECT id, date, motif FROM absences ORDER BY date DESC")
        for row in self.db_cursor.fetchall():
            self.table.insert(row)


class ClassesManagementTab(BaseManagementTab):
    """Classes management"""
    
    def __init__(self, parent, db_conn):
        super().__init__(parent, db_conn)
    
    def create_form_card(self):
        card = ModernCard(self.left_column, title="➕ Ajouter une Classe")
        card.pack(fill='both', expand=True)
        
        self.name_field = ModernFormField(card.content_frame, "Nom de la classe", required=True)
        self.name_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.level_field = ModernFormField(card.content_frame, "Niveau", required=True)
        self.level_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.year_field = ModernFormField(card.content_frame, "Année scolaire", required=True)
        self.year_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        ttk.Button(card.content_frame, text="💾 Enregistrer", command=self.save_class,
                  style='Success.TButton').pack()
    
    def create_data_card(self):
        card = ModernCard(self.right_column, title="📋 Liste des Classes")
        card.pack(fill='both', expand=True)
        
        columns = [
            {'id': 'id', 'label': 'ID', 'width': 50},
            {'id': 'name', 'label': 'Nom', 'width': 150},
            {'id': 'level', 'label': 'Niveau', 'width': 150},
            {'id': 'year', 'label': 'Année', 'width': 150}
        ]
        
        self.table = ModernTable(card.content_frame, columns)
        self.table.pack(fill='both', expand=True)
        self.refresh_table()
    
    def save_class(self):
        if not all([self.name_field.validate(), self.level_field.validate(), self.year_field.validate()]):
            return
        
        name = self.name_field.get().strip()
        level = self.level_field.get().strip()
        year = self.year_field.get().strip()
        
        try:
            self.db_cursor.execute("INSERT INTO classes (name, level, school_year) VALUES (?, ?, ?)", 
                                  (name, level, year))
            self.db_conn.commit()
            messagebox.showinfo("Succès", "Classe ajoutée!")
            self.clear_form()
            self.refresh_table()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", str(e))
    
    def clear_form(self):
        self.name_field.clear()
        self.level_field.clear()
        self.year_field.clear()
    
    def refresh_table(self):
        self.table.clear()
        self.db_cursor.execute("SELECT id, name, level, school_year FROM classes")
        for row in self.db_cursor.fetchall():
            self.table.insert(row)


class ModulesManagementTab(BaseManagementTab):
    """Modules management"""
    
    def __init__(self, parent, db_conn):
        super().__init__(parent, db_conn)
    
    def create_form_card(self):
        card = ModernCard(self.left_column, title="➕ Ajouter un Module")
        card.pack(fill='both', expand=True)
        
        self.name_field = ModernFormField(card.content_frame, "Nom du module", required=True)
        self.name_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        self.code_field = ModernFormField(card.content_frame, "Code", required=True)
        self.code_field.pack(fill='x', pady=(0, ModernTheme.SPACING['md']))
        
        ttk.Button(card.content_frame, text="💾 Enregistrer", command=self.save_module,
                  style='Success.TButton').pack()
    
    def create_data_card(self):
        card = ModernCard(self.right_column, title="📋 Liste des Modules")
        card.pack(fill='both', expand=True)
        
        # Note: This requires a modules table which may not exist
        # Creating a placeholder
        info_label = tk.Label(
            card.content_frame,
            text="Fonctionnalité en cours de développement\nLa table 'modules' sera créée automatiquement",
            bg=ModernTheme.COLORS['card_bg'],
            fg=ModernTheme.COLORS['text_secondary'],
            font=ModernTheme.FONTS['body'],
            justify='center'
        )
        info_label.pack(expand=True)
    
    def save_module(self):
        messagebox.showinfo("Info", "Fonctionnalité en cours de développement")
    
    def clear_form(self):
        self.name_field.clear()
        self.code_field.clear()
    
    def refresh_table(self):
        pass
