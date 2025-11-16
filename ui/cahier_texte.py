from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import sys
import os
import logging
from datetime import datetime, timedelta
from core.db_manager import DatabaseManager
from services.course_distribution import CourseDistributionManager
from core.constants import (
    MORNING_SLOTS, AFTERNOON_SLOTS, DAYS,
    get_school_year, format_week_text, get_week_dates
)
from services.pdf_generator import generate_pdf
from services.test import generate_pdf_grouped

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='cahier_texte.log'
)

class CahierTextFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.db = DatabaseManager()
        self.course_distributor = CourseDistributionManager("data/cahier_texte.db")
        
        self.cells = {}           # Dictionnaire pour les cellules du tableau
        self.unsaved_changes = False
        self.vacation_cells = {}  # Pour stocker les cellules fusionnées (vacations, holidays, absences)
        self.morning_slots = MORNING_SLOTS
        self.afternoon_slots = AFTERNOON_SLOTS
        self.columns = DAYS
        
        try:
            self.db.setup_database()
            self.db.initialize_basic_data(self.columns, self.morning_slots, self.afternoon_slots)
            self.setup_ui()
            self._create_cell_menu()
        except Exception as e:
            logging.error(f"Initialization error: {e}")
            raise

    def setup_ui(self):
        nav_frame = ttk.Frame(self, padding="10") 
        nav_frame.pack(fill='x', pady=(0, 10))
        
        back_button = ttk.Button(
            nav_frame,
            text="Retour au tableau de bord",
            command=lambda: self.controller.show_frame("HomeFrame")
        )
        back_button.pack(side='left', padx=5)
        
        week_frame = ttk.Frame(nav_frame)
        week_frame.pack(side='left', expand=True, padx=20)
        
        ttk.Label(week_frame, text="Semaine:", style='Body.TLabel').pack(side='left', padx=5)
        
        self.week_var = tk.StringVar()
        weeks = self._get_school_year_weeks()
        self.week_selector = ttk.Combobox(
            week_frame,
            textvariable=self.week_var,
            values=weeks,
            state="readonly",
            width=30,
            style='Combo.TCombobox'
        )
        self.week_selector.pack(side='left', padx=5)
        self.week_selector.bind('<<ComboboxSelected>>', self._on_week_change)
        
        action_frame = ttk.Frame(nav_frame)
        action_frame.pack(side='right')
        
        buttons = [
            ("Recharger", self.reload_schedule),
            ("Sauvegarder", self.save_schedule),
            ("Imprimer PDF", self.print_pdf_choice)
        ]
        for text, command in buttons:
            ttk.Button(
                action_frame,
                text=text,
                command=command,
                style='Action.TButton'
            ).pack(side='left', padx=5)

        # Scrollable container
        grid_container = ttk.Frame(self)
        grid_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(grid_container)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(grid_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig('win', width=e.width-4))
        self.canvas.addtag_all('win')
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            
        for i in range(len(self.columns) + 1):
            self.main_frame.grid_columnconfigure(i, weight=1)
        
        self._create_header_row()
        self._create_schedule_grid()
        
        # Configure scroll region after content is added
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        current_week = datetime.now().isocalendar()[1]
        for i, week in enumerate(weeks):
            if str(current_week) in week:
                self.week_selector.current(i)
                break





    def print_pdf_choice(self):
        """Opens a dialog that lets the user choose which PDF design to use via graphical previews with hover effects."""
        # Create the Toplevel window with the main window as parent
        choice_window = tk.Toplevel(self.winfo_toplevel())
        choice_window.title("Choisissez le design d'impression PDF")
        choice_window.geometry("600x400")  # Increased size for better presentation
        choice_window.configure(bg="#f5f5f7")  # Light gray background
        choice_window.transient(self.winfo_toplevel())
        choice_window.grab_set()

        # Create a style for modern-looking widgets
        style = ttk.Style()
        style.configure("Modern.TLabel",
                    font=("Helvetica", 14),
                    background="#f5f5f7",
                    foreground="#1d1d1f")

        # Header label with modern styling
        header_label = ttk.Label(
            choice_window,
            text="Sélectionnez le design d'impression PDF",
            style="Modern.TLabel"
        )
        header_label.pack(pady=20)

        # Create a frame to hold the design preview canvases
        previews_frame = tk.Frame(choice_window, bg="#f5f5f7")
        previews_frame.pack(pady=20)

        # Function to create shadow effect
        def create_shadow(canvas, x1, y1, x2, y2, shadow_width=3):
            # Create multiple rectangles with decreasing opacity for shadow effect
            for i in range(shadow_width):
                opacity = 0.1 - (i * 0.02)
                shadow_color = f"#{int(0 * 255):02x}{int(0 * 255):02x}{int(0 * 255):02x}"
                canvas.create_rectangle(
                    x1 + i, y1 + i, x2 + i, y2 + i,
                    fill="", outline=shadow_color,
                    stipple="gray50"
                )

        # ---------- Standard PDF Preview ----------
        standard_frame = tk.Frame(previews_frame, bg="#f5f5f7")
        standard_frame.grid(row=0, column=0, padx=30)
        
        standard_canvas = tk.Canvas(standard_frame, width=220, height=220, bg="white",
                                highlightthickness=0)
        standard_canvas.pack()
        
        # Add shadow before drawing the main content
        create_shadow(standard_canvas, 12, 12, 208, 208)
        
        # Main content rectangle with rounded corners
        standard_canvas.create_rectangle(10, 10, 210, 210, fill="white", outline="#e1e1e1",
                                    width=2)
        # Header with gradient effect
        standard_canvas.create_rectangle(10, 10, 210, 40, fill="#007AFF", outline="")
        standard_canvas.create_text(50, 25, text="Horaire", font=("Helvetica", 10, "bold"),
                                fill="white")
        standard_canvas.create_text(130, 25, text="Lundi", font=("Helvetica", 10, "bold"),
                                fill="white")
        
        # Data rows with alternating backgrounds
        standard_canvas.create_rectangle(10, 40, 210, 80, fill="#f8f8f8", outline="#e1e1e1")
        standard_canvas.create_text(50, 60, text="08:00", font=("Helvetica", 10))
        standard_canvas.create_text(130, 60, text="Math", font=("Helvetica", 10))
        
        standard_canvas.create_rectangle(10, 80, 210, 120, fill="white", outline="#e1e1e1")
        standard_canvas.create_text(50, 100, text="09:00", font=("Helvetica", 10))
        standard_canvas.create_text(130, 100, text="Phys", font=("Helvetica", 10))
        
        standard_label = tk.Label(standard_frame, text="PDF Standard",
                                font=("Helvetica", 12, "bold"), bg="#f5f5f7", fg="#1d1d1f")
        standard_label.pack(pady=10)

        # ---------- Grouped PDF Preview ----------
        grouped_frame = tk.Frame(previews_frame, bg="#f5f5f7")
        grouped_frame.grid(row=0, column=1, padx=30)
        
        grouped_canvas = tk.Canvas(grouped_frame, width=220, height=220, bg="white",
                                highlightthickness=0)
        grouped_canvas.pack()
        
        # Add shadow
        create_shadow(grouped_canvas, 12, 12, 208, 208)
        
        # Main content rectangle
        grouped_canvas.create_rectangle(10, 10, 210, 210, fill="white", outline="#e1e1e1",
                                    width=2)
        # Header with gradient
        grouped_canvas.create_rectangle(10, 10, 210, 40, fill="#FF2D55", outline="")
        grouped_canvas.create_text(110, 25, text="TCSF1", font=("Helvetica", 12, "bold"),
                                fill="white")
        
        # Schedule entries with modern styling
        grouped_canvas.create_rectangle(10, 40, 210, 70, fill="#f8f8f8", outline="#e1e1e1")
        grouped_canvas.create_text(40, 55, text="Lundi", font=("Helvetica", 9))
        grouped_canvas.create_text(110, 55, text="08:00-09:30", font=("Helvetica", 9))
        grouped_canvas.create_text(170, 55, text="Math", font=("Helvetica", 9, "bold"))
        
        grouped_canvas.create_rectangle(10, 70, 210, 100, fill="white", outline="#e1e1e1")
        grouped_canvas.create_text(40, 85, text="Mardi", font=("Helvetica", 9))
        grouped_canvas.create_text(110, 85, text="09:00-10:30", font=("Helvetica", 9))
        grouped_canvas.create_text(170, 85, text="Phys", font=("Helvetica", 9, "bold"))
        
        grouped_label = tk.Label(grouped_frame, text="PDF Groupé",
                            font=("Helvetica", 12, "bold"), bg="#f5f5f7", fg="#1d1d1f")
        grouped_label.pack(pady=10)

        # ---------- Enhanced Hover Effects ----------
        def on_enter(event):
            widget = event.widget
            # Create elevation effect
            widget.configure(bg="#fafafa")
            # Scale up effect
            widget.scale("all", 110, 110, 1.02, 1.02)
            # Brighten colors
            items = widget.find_all()
            for item in items:
                if widget.type(item) == "rectangle":
                    current_fill = widget.itemcget(item, "fill")
                    if current_fill == "#007AFF":
                        widget.itemconfig(item, fill="#1e90ff")
                    elif current_fill == "#FF2D55":
                        widget.itemconfig(item, fill="#ff4d79")

        def on_leave(event):
            widget = event.widget
            # Remove elevation effect
            widget.configure(bg="white")
            # Scale back to normal
            widget.scale("all", 110, 110, 1/1.02, 1/1.02)
            # Restore original colors
            items = widget.find_all()
            for item in items:
                if widget.type(item) == "rectangle":
                    current_fill = widget.itemcget(item, "fill")
                    if current_fill == "#1e90ff":
                        widget.itemconfig(item, fill="#007AFF")
                    elif current_fill == "#ff4d79":
                        widget.itemconfig(item, fill="#FF2D55")

        standard_canvas.bind("<Enter>", on_enter)
        standard_canvas.bind("<Leave>", on_leave)
        grouped_canvas.bind("<Enter>", on_enter)
        grouped_canvas.bind("<Leave>", on_leave)

        # ---------- Click Events ----------
        def select_standard(event):
            choice_window.destroy()
            self.print_to_pdf()

        def select_grouped(event):
            choice_window.destroy()
            self.print_to_pdf_grouped()

        standard_canvas.bind("<Button-1>", select_standard)
        grouped_canvas.bind("<Button-1>", select_grouped)

        # Add a subtle info text at the bottom
        info_label = tk.Label(
            choice_window,
            text="Cliquez sur un design pour sélectionner",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#f5f5f7"
        )
        info_label.pack(pady=10)























































    def _get_school_year_weeks(self):
        school_start, school_end = get_school_year()
        vacations = self.db.get_vacations()
        vacations = [(datetime.strptime(start, '%Y-%m-%d'),
                      datetime.strptime(end, '%Y-%m-%d'),
                      desc) for start, end, desc in vacations]
        weeks = []
        current_date = school_start
        while current_date <= school_end:
            week_start = current_date - timedelta(days=current_date.weekday())
            week_end = week_start + timedelta(days=5)
            vacation_text = ""
            for vac_start, vac_end, vac_desc in vacations:
                if week_start <= vac_end and week_end >= vac_start:
                    vacation_text = f" ({vac_desc})"
                    break
            weeks.append(format_week_text(week_start, vacation_text))
            current_date += timedelta(days=7)
        return weeks

    def _clear_existing_cells(self):
        for cell in self.cells.values():
            if isinstance(cell, tuple):
                for widget in cell:
                    if widget:
                        widget.destroy()
            elif cell:
                cell.destroy()
        self.cells.clear()
        for cell in self.vacation_cells.values():
            cell.destroy()
        self.vacation_cells.clear()

    def _create_header_row(self):
        for col, text in enumerate(["Horaire"] + self.columns):
            label = ttk.Label(
                self.main_frame,
                text=text,
                style='Header.TLabel'
            )
            label.grid(row=1, column=col, sticky='nsew', padx=1, pady=1)



    def _create_schedule_grid(self):
        self._clear_existing_cells()
        schedule_entries = self.db.get_schedule_entries()
        selected_week = self.week_selector.get()
        
        try:
            week_start = datetime.strptime(selected_week.split("du ")[1].split(" au")[0], "%d/%m/%Y")
        except Exception as e:
            logging.error("Error parsing week: " + str(e))
            messagebox.showerror("Erreur", "Erreur lors de la création de la grille")
            return

        dates = get_week_dates(week_start, self.columns)
        event_days = {}
        
        # Check for events (vacation, holiday, absence) on each day
        for day, date_str in dates.items():
            event_type, event_msg = self.db.check_events(date_str)
            if event_type:
                event_days[self.columns.index(day) + 1] = (event_type, event_msg)
        
        # Create regular grid first
        class_schedule = {}
        for day_id, time_slot_id, class_name in schedule_entries:
            class_schedule[(day_id, time_slot_id)] = class_name

        # Create all rows and cells
        current_row = 2
        for horaire in self.morning_slots:
            self._create_row(current_row, horaire, class_schedule)
            current_row += 1

        # Add separator
        separator = ttk.Frame(self.main_frame, style='Separator.TFrame')
        separator.grid(row=current_row, column=0, columnspan=len(self.columns) + 1, sticky='ew', pady=5)
        current_row += 1

        for horaire in self.afternoon_slots:
            self._create_row(current_row, horaire, class_schedule)
            current_row += 1

        # Now handle vacation days by hiding affected cells
        for col in event_days.keys():
            for key in list(self.cells.keys()):
                if key[1] == col:
                    cell = self.cells[key]
                    if isinstance(cell, tuple):
                        text_widget, placeholder, class_label = cell
                        for widget in (text_widget, placeholder, class_label):
                            if widget:
                                widget.grid_remove()
                    else:
                        cell.grid_remove()

        # Create merged vacation cells last
        self._create_merged_vacation_cells(event_days)




    def _create_merged_vacation_cells(self, event_days):
        total_rows = len(self.morning_slots) + 2 + len(self.afternoon_slots)
        for col, (event_type, event_msg) in event_days.items():
            if event_type == 'vacation':
                bg_color = self.controller.colors['vacation_bg'] if hasattr(self.controller, 'colors') else "#FFC0CB"
            elif event_type == 'holiday':
                bg_color = self.controller.colors['holiday_bg'] if hasattr(self.controller, 'colors') else "#ADD8E6"
            elif event_type == 'absence':
                bg_color = self.controller.colors['absence_bg'] if hasattr(self.controller, 'colors') else "#90EE90"
            else:
                bg_color = self.controller.colors.get('default_bg', "#ffffff")
            
            event_frame = tk.Frame(
                self.main_frame,
                bg=bg_color,
                relief="solid",
                borderwidth=2
            )
            event_frame.grid(
                row=2,
                column=col,
                rowspan=total_rows - 1,
                sticky='nsew',
                padx=1, pady=1
            )
            
            event_label = tk.Label(
                event_frame,
                text=event_msg,
                font=("Arial", 11, "bold"),
                fg=self.controller.colors['cell_fg'] if hasattr(self.controller, 'colors') else "#000000",
                bg=bg_color,
                wraplength=150,
                justify='center'
            )
            event_label.pack(expand=True, fill='both')
            self.vacation_cells[(col, col)] = event_frame


    def _create_row(self, row, horaire, class_schedule):
        time_label = ttk.Label(
            self.main_frame,
            text=horaire,
            style='Time.TLabel'
        )
        time_label.grid(row=row, column=0, sticky='nsew', padx=1, pady=1)
        
        for col in range(len(self.columns)):
            cell_frame = ttk.Frame(
                self.main_frame,
                style='Cell.TFrame'
            )
            cell_frame.grid(row=row, column=col + 1, sticky='nsew', padx=1, pady=1)
            cell_frame.grid_rowconfigure(1, weight=1)
            cell_frame.grid_columnconfigure(0, weight=1)

            time_slot_id = self._get_time_slot_id(horaire)
            class_name = None
            for entry in self.db.get_schedule_entries():
                if entry[0] == col + 1 and entry[1] == time_slot_id:
                    class_name = entry[2]
                    break

            if class_name:
                # Existing code for cells with class names
                class_label = ttk.Label(
                    cell_frame,
                    text=class_name,
                    style='Cell.TLabel'
                )
                class_label.grid(row=0, column=0, sticky='nsew')
                
                container_frame = ttk.Frame(cell_frame)
                container_frame.grid(row=1, column=0, sticky='nsew', pady=1)
                container_frame.grid_columnconfigure(0, weight=1)
                container_frame.grid_rowconfigure(0, weight=1)
                
                text_widget = tk.Text(
                    container_frame,
                    wrap=tk.WORD,
                    height=3,
                    width=15
                )
                text_widget.grid(row=0, column=0, sticky='nsew')
                text_widget.grid_remove()
                
                placeholder = ttk.Label(
                    container_frame,
                    text="Cliquez pour éditer",
                    style='Empty.TLabel'
                )
                placeholder.grid(row=0, column=0, sticky='nsew')
                
                self.cells[(row, col + 1)] = (text_widget, placeholder, class_label)
                
                for widget in (cell_frame, class_label, placeholder):
                    widget.bind('<Button-1>', lambda e, r=row, c=col+1: self._on_cell_click(r, c))
                    widget.bind('<Button-3>', lambda e, r=row, c=col+1: self._show_cell_menu(e, r, c))
                text_widget.bind('<FocusOut>', lambda e, r=row, c=col+1: self._on_cell_focus_out(r, c))
                text_widget.bind('<KeyRelease>', lambda e: self._on_cell_change())
            else:
                # Empty cell case
                empty_label = ttk.Label(
                    cell_frame,
                    text="",
                    style='Empty.TLabel'
                )
                empty_label.grid(row=0, column=0, sticky='nsew', rowspan=2)
                
                # Make cell interactive
                empty_label.bind('<Button-1>', lambda e, r=row, c=col+1: self._on_cell_click(r, c))
                empty_label.bind('<Button-3>', lambda e, r=row, c=col+1: self._show_cell_menu(e, r, c))
                
                self.cells[(row, col + 1)] = cell_frame
    
    
 
    def _distribute_ma_table_values(self, week_number):
        try:
            selected_week = self.week_selector.get()
            week_start = datetime.strptime(selected_week.split("du ")[1].split(" au")[0], "%d/%m/%Y")
            week_end = week_start + timedelta(days=5)
            logging.info(f"Distributing courses for week {week_number}...")
            distribution = self.course_distributor.distribute_courses(week_number, week_start, week_end)
            logging.info(f"Distribution: {distribution}")
            for group, slots in distribution.items():
                for day_id, time_slot_id, course_id in slots:
                    course_value = self.db._fetch_course_value_by_id(course_id)
                    if not course_value:
                        logging.warning(f"No course_value found for course_id: {course_id}")
                        continue
                    row = self._get_row_from_time_slot(time_slot_id)
                    col = day_id
                    logging.info(f"Assigning course value {course_value} to row {row}, col {col}")
                    if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
                        text_widget, placeholder, class_label = self.cells[(row, col)]
                        if text_widget:
                            text_widget.delete('1.0', tk.END)
                            text_widget.insert('1.0', course_value)
                            text_widget.grid()
                            placeholder.grid_remove()
                            class_label.config(cursor="hand2")
                            class_label.bind('<Button-1>', lambda e, r=row, c=col: self._show_cell_menu(e, r, c))
        except Exception as e:
            logging.error(f"Error distributing ma_table values: {e}")
            messagebox.showerror("Error", f"Failed to distribute values: {e}")

    def _on_cell_change(self):
        self.unsaved_changes = True

    def _on_cell_click(self, row, col):
        if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
            text_widget, placeholder, _ = self.cells[(row, col)]
            if text_widget:
                placeholder.grid_remove()
                text_widget.grid()
                text_widget.focus_set()

    def _on_cell_focus_out(self, row, col):
        if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
            text_widget, placeholder, _ = self.cells[(row, col)]
            if text_widget and not text_widget.get('1.0', tk.END).strip():
                text_widget.grid_remove()
                placeholder.grid()

    def _on_week_change(self, event=None):
        if self.unsaved_changes:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before switching weeks?",
                icon="warning"
            )
            if response is None:
                return
            elif response:
                self.save_schedule()
        self.reload_schedule()
        self.unsaved_changes = False

    def reload_schedule(self):
        try:
            selected_week = self.week_selector.get()
            week_start = datetime.strptime(selected_week.split("du ")[1].split(" au")[0], "%d/%m/%Y")
            dates = get_week_dates(week_start, self.columns)
            if not dates:
                messagebox.showerror("Error", "Failed to parse week dates")
                return
            week_number = int(selected_week.split("Semaine ")[1].split(" -")[0])
            self._create_schedule_grid()
            self.db.cursor.execute("""
                SELECT cell_row, cell_col, value
                FROM schedule_data
                WHERE week_number = ?
            """, (week_number,))
            saved_data = self.db.cursor.fetchall()
            if saved_data:
                self._load_saved_data(saved_data)
            else:
                self._distribute_ma_table_values(week_number)
        except Exception as e:
            logging.error(f"Error reloading schedule: {e}")
            messagebox.showerror("Error", f"Failed to reload schedule: {e}")

    def _load_saved_data(self, saved_data):
        for row, col, value in saved_data:
            if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
                text_widget, placeholder, _ = self.cells[(row, col)]
                if text_widget:
                    text_widget.delete('1.0', tk.END)
                    text_widget.insert('1.0', value)
                    text_widget.grid()
                    placeholder.grid_remove()
                    cell_frame = text_widget.master
                    cell_frame.bind('<Button-3>', lambda e, r=row, c=col: self._show_cell_menu(e, r, c))
                    placeholder.bind('<Button-1>', lambda e, r=row, c=col: self._show_cell_menu(e, r, c))
                    text_widget.bind('<FocusOut>', lambda e, r=row, c=col: self._on_cell_focus_out(r, c))
                    text_widget.bind('<KeyRelease>', lambda e: self._on_cell_change())

    def _get_row_from_time_slot(self, time_slot_id):
        if time_slot_id <= len(self.morning_slots):
            return 2 + time_slot_id - 1
        else:
            return 2 + len(self.morning_slots) + 1 + (time_slot_id - len(self.morning_slots) - 1)

    def _handle_control(self):
        if hasattr(self, 'current_cell'):
            row, col = self.current_cell
            if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
                control_window = tk.Toplevel(self.main_frame)
                control_window.title("Control Options")
                control_window.geometry("300x250")
                frame = ttk.Frame(control_window, padding="10")
                frame.pack(fill='both', expand=True)
                ttk.Label(frame, text="Select Control Type:", font=("Arial", 11, "bold")).pack(pady=(0, 10))
                controls = [
                    "Contrôle écrit",
                    "Contrôle oral",
                    "Quiz",
                    "Evaluation pratique",
                    "Devoir maison",
                    "Projet"
                ]
                selected_control = tk.StringVar()
                selected_control.set(controls[0])
                for control in controls:
                    ttk.Radiobutton(frame, text=control, variable=selected_control, value=control).pack(anchor='w', pady=2)
                ttk.Label(frame, text="Additional Notes:", font=("Arial", 10)).pack(pady=(10, 5), anchor='w')
                notes_entry = tk.Text(frame, height=3, width=30)
                notes_entry.pack(fill='x', pady=(0, 10))
                def apply_control():
                    control_type = selected_control.get()
                    notes = notes_entry.get('1.0', tk.END).strip()
                    text_widget, placeholder, _ = self.cells[self.current_cell]
                    if text_widget:
                        content = f"CONTROL: {control_type}"
                        if notes:
                            content += f"\nNotes: {notes}"
                        text_widget.delete('1.0', tk.END)
                        text_widget.insert('1.0', content)
                        text_widget.grid()
                        placeholder.grid_remove()
                        self.unsaved_changes = True
                    control_window.destroy()
                button_frame = ttk.Frame(frame)
                button_frame.pack(fill='x', pady=(10, 0))
                ttk.Button(button_frame, text="Apply", command=apply_control).pack(side='left', padx=5)
                ttk.Button(button_frame, text="Cancel", command=control_window.destroy).pack(side='left')

    def _handle_custom_content(self):
        if hasattr(self, 'current_cell'):
            row, col = self.current_cell
            if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
                text_widget, placeholder, _ = self.cells[(row, col)]
                if text_widget:
                    text_widget.delete('1.0', tk.END)
                    text_widget.grid()
                    placeholder.grid_remove()
                    text_widget.focus_set()

    def save_schedule(self):
        try:
            week_text = self.week_selector.get()
            week_number = int(week_text.split("Semaine ")[1].split(" -")[0])
            year = int(week_text.split("/")[-1].strip())
            course_progress = {}
            for (row, col), cell in self.cells.items():
                if isinstance(cell, tuple):
                    text_widget, _, class_label = cell
                    if text_widget and text_widget.winfo_ismapped():
                        content = text_widget.get('1.0', tk.END).strip()
                        if content:
                            self.db.cursor.execute("""
                                DELETE FROM schedule_data 
                                WHERE week_number = ? AND cell_row = ? AND cell_col = ? AND year = ?
                            """, (week_number, row, col, year))
                            self.db.cursor.execute("""
                                INSERT INTO schedule_data (week_number, cell_row, cell_col, value, year)
                                VALUES (?, ?, ?, ?, ?)
                            """, (week_number, row, col, content, year))
                            self.db.cursor.execute("""
                                SELECT id FROM ma_table WHERE valeur = ?
                            """, (content,))
                            result = self.db.cursor.fetchone()
                            if result:
                                cours_id = result[0]
                                class_name = class_label.cget('text')
                                if class_name:
                                    self.db.cursor.execute("""
                                        SELECT id FROM classes WHERE name = ?
                                    """, (class_name,))
                                    result = self.db.cursor.fetchone()
                                    if result:
                                        class_id = result[0]
                                        course_progress[class_id] = max(cours_id, course_progress.get(class_id, 0))
            for class_id, last_course in course_progress.items():
                self.db.cursor.execute("""
                    DELETE FROM class_course_progress
                    WHERE class_id = ? AND last_week = ? AND year = ?
                """, (class_id, week_number, year))
                self.db.cursor.execute("""
                    INSERT INTO class_course_progress (class_id, last_course_id, last_week, year)
                    VALUES (?, ?, ?, ?)
                """, (class_id, last_course, week_number, year))
            self.db.conn.commit()
            self.unsaved_changes = False
            messagebox.showinfo("Success", "Schedule saved successfully!")
        except Exception as e:
            logging.error(f"Error saving schedule: {e}")
            messagebox.showerror("Error", f"Failed to save schedule: {e}")
            self.db.conn.rollback()

    def _create_cell_menu(self):
        self.cell_menu = tk.Menu(self.main_frame, tearoff=0)
        self.cell_menu.add_command(label="Control", command=self._handle_control)
        self.cell_menu.add_command(label="Custom Content", command=self._handle_custom_content)
        self.cell_menu.add_separator()
        self.cell_menu.add_command(label="Switch Content With...", command=self._handle_switch_content)

    def _show_cell_menu(self, event, row, col):
        if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
            self.current_cell = (row, col)
            text_widget, _, class_label = self.cells[(row, col)]
            current_class = class_label.cget('text')
            other_appearances = self._find_other_appearances(row, col, current_class)
            self.cell_menu.entryconfig("Switch Content With...", state='normal' if other_appearances else 'disabled')
            self.cell_menu.post(event.x_root, event.y_root)

    def _find_other_appearances(self, current_row, current_col, class_name):
        appearances = []
        for (row, col), cell in self.cells.items():
            if isinstance(cell, tuple) and (row, col) != (current_row, current_col):
                _, _, class_label = cell
                if class_label and class_label.cget('text') == class_name:
                    appearances.append((row, col))
        return appearances

    def _handle_switch_content(self):
        if hasattr(self, 'current_cell'):
            current_row, current_col = self.current_cell
            if (current_row, current_col) in self.cells:
                current_cell = self.cells[(current_row, current_col)]
                if isinstance(current_cell, tuple):
                    text_widget, _, class_label = current_cell
                    current_class = class_label.cget('text')
                    other_appearances = self._find_other_appearances(current_row, current_col, current_class)
                    if other_appearances:
                        self._show_switch_dialog(other_appearances, current_class)

    def _show_switch_dialog(self, other_appearances, class_name):
        switch_window = tk.Toplevel(self.main_frame)
        switch_window.title(f"Switch Content - {class_name}")
        switch_window.geometry("400x300")
        frame = ttk.Frame(switch_window, padding="10")
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text=f"Select appearance to switch content with:", font=("Arial", 11, "bold")).pack(pady=(0, 10))
        listbox = tk.Listbox(frame, width=50, height=10)
        listbox.pack(fill='both', expand=True)
        for row, col in other_appearances:
            text_widget, _, _ = self.cells[(row, col)]
            content = text_widget.get('1.0', tk.END).strip() if text_widget.winfo_ismapped() else "Empty"
            day = self.columns[col - 1]
            time_slot = self._get_time_slot_text(row)
            listbox.insert(tk.END, f"{day} - {time_slot}: {content}")
        def switch_content():
            selection = listbox.curselection()
            if selection:
                target_row, target_col = other_appearances[selection[0]]
                current_text_widget, _, _ = self.cells[self.current_cell]
                current_content = current_text_widget.get('1.0', tk.END).strip() if current_text_widget.winfo_ismapped() else ""
                target_text_widget, target_placeholder, _ = self.cells[(target_row, target_col)]
                target_content = target_text_widget.get('1.0', tk.END).strip() if target_text_widget.winfo_ismapped() else ""
                self._update_cell_content(self.current_cell[0], self.current_cell[1], target_content)
                self._update_cell_content(target_row, target_col, current_content)
                self.unsaved_changes = True
                switch_window.destroy()
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Switch", command=switch_content).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=switch_window.destroy).pack(side='left')

    def _update_cell_content(self, row, col, content):
        if (row, col) in self.cells and isinstance(self.cells[(row, col)], tuple):
            text_widget, placeholder, _ = self.cells[(row, col)]
            if text_widget:
                text_widget.delete('1.0', tk.END)
                if content:
                    text_widget.insert('1.0', content)
                    text_widget.pack(fill='both', expand=True)
                    placeholder.pack_forget()
                else:
                    text_widget.pack_forget()
                    placeholder.pack(fill='both', expand=True)

    def _get_time_slot_text(self, row):
        if row <= len(self.morning_slots) + 1:
            return self.morning_slots[row - 2]
        elif row == len(self.morning_slots) + 2:
            return "Pause Déjeuner"
        else:
            afternoon_index = row - len(self.morning_slots) - 3
            return self.afternoon_slots[afternoon_index]

    def print_to_pdf(self):
        try:
            logging.info("Starting PDF generation...")
            data = []
            selected_week = self.week_selector.get()
            title = f"{selected_week}"
            data.append([title])
            headers = ["Horaire"] + self.columns
            data.append(headers)
            logging.info(f"Added headers: {headers}")
            grid_mapping = {}
            current_grid_row = 2
            for idx, slot in enumerate(self.morning_slots):
                grid_mapping[current_grid_row] = idx
                current_grid_row += 1
            current_grid_row += 1
            for idx, slot in enumerate(self.afternoon_slots, start=len(self.morning_slots)+1):
                grid_mapping[current_grid_row] = idx
                current_grid_row += 1
            schedule_state = []
            for slot in self.morning_slots:
                schedule_state.append([slot])
            schedule_state.append(["12:30 - 14:30"])
            for slot in self.afternoon_slots:
                schedule_state.append([slot])
            logging.info(f"Initial schedule state created with {len(schedule_state)} rows")
            for col_idx, day in enumerate(self.columns, start=1):
                logging.info(f"Processing day: {day} at column {col_idx}")
                is_vacation_day = False
                vacation_text = None
                for vac_range, vac_frame in self.vacation_cells.items():
                    if col_idx >= vac_range[0] and col_idx <= vac_range[1]:
                        is_vacation_day = True
                        if vac_frame and vac_frame.winfo_children():
                            vacation_text = vac_frame.winfo_children()[0].cget('text')
                        break
                for row_idx in range(len(schedule_state)):
                    if is_vacation_day:
                        if row_idx == 0:
                            schedule_state[row_idx].append({
                                'text': vacation_text or "Vacation",
                                'type': 'vacation',
                                'merge': len(schedule_state)
                            })
                        else:
                            schedule_state[row_idx].append("")
                    else:
                        if row_idx == len(self.morning_slots):
                            schedule_state[row_idx].append("Pause Déjeuner")
                        else:
                            grid_row = next((grid_row for grid_row, idx in grid_mapping.items() if idx == row_idx), None)
                            if grid_row is not None:
                                cell = self.cells.get((grid_row, col_idx))
                                content = self._get_cell_content(cell) if cell else ""
                                schedule_state[row_idx].append(content)
                            else:
                                schedule_state[row_idx].append("")
            data.extend(schedule_state)
            logging.info(f"Final data structure has {len(data)} rows")
            for idx, row in enumerate(data):
                logging.info(f"Row {idx}: {row}")
            if len(data) < 2:
                raise ValueError("Not enough data to generate PDF")
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"cahier_texte_week_{int(self.week_selector.get().split('Semaine ')[1].split(' -')[0])}.pdf"
            )
            if filename:
                generate_pdf(data, filename)
                messagebox.showinfo("Success", "PDF generated successfully!")
        except Exception as e:
            logging.error(f"Error in print_to_pdf: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")





    def print_to_pdf_grouped(self):
        try:
            logging.info("Starting grouped PDF generation...")

            # Parse the selected week and obtain the week's start date.
            selected_week = self.week_selector.get()
            week_start = datetime.strptime(selected_week.split("du ")[1].split(" au")[0], "%d/%m/%Y")
            # Get a mapping of day names (from self.columns) to dates.
            week_dates = get_week_dates(week_start, self.columns)

            # Build a grid mapping for the schedule_state.
            grid_mapping = {}
            current_grid_row = 2
            for idx, slot in enumerate(self.morning_slots):
                grid_mapping[current_grid_row] = idx
                current_grid_row += 1
            # Skip one row for the lunch separator.
            current_grid_row += 1
            for idx, slot in enumerate(self.afternoon_slots, start=len(self.morning_slots) + 1):
                grid_mapping[current_grid_row] = idx
                current_grid_row += 1

            # Build the initial schedule_state grid.
            schedule_state = []
            for slot in self.morning_slots:
                schedule_state.append([slot])
            schedule_state.append(["12:30 - 14:30"])  # Lunch row
            for slot in self.afternoon_slots:
                schedule_state.append([slot])
            logging.info("Initial schedule state created with {} rows".format(len(schedule_state)))

            # Append cell content for each day column.
            for col_idx, day in enumerate(self.columns, start=1):
                logging.info("Processing day: {} at column {}".format(day, col_idx))
                is_vacation_day = False
                vacation_text = None
                for vac_range, vac_frame in self.vacation_cells.items():
                    if col_idx >= vac_range[0] and col_idx <= vac_range[1]:
                        is_vacation_day = True
                        if vac_frame and vac_frame.winfo_children():
                            vacation_text = vac_frame.winfo_children()[0].cget('text')
                        break
                for row_idx in range(len(schedule_state)):
                    if is_vacation_day:
                        # For vacation days, we want to still include the session.
                        # For the first row of the day (usually the first session),
                        # try to preserve the original class name.
                        if row_idx == 0:
                            # Try to get the normal cell content (if any) from the grid.
                            grid_row = next((gr for gr, idx in grid_mapping.items() if idx == row_idx), None)
                            normal_content = ""
                            if grid_row is not None:
                                cell = self.cells.get((grid_row, col_idx))
                                normal_content = self._get_cell_content(cell) if cell else ""
                            # If normal content exists, extract the class name (first line).
                            if normal_content:
                                orig_class = normal_content.split("\n", 1)[0].strip()
                            else:
                                orig_class = "Unknown"
                            # Store a dictionary that preserves the original class.
                            schedule_state[row_idx].append({
                                'class': orig_class,
                                'text': vacation_text or "Vacation",
                                'type': 'vacation',
                                'merge': len(schedule_state)
                            })
                        else:
                            # For other rows on a vacation day, leave the cell empty.
                            schedule_state[row_idx].append("")
                    else:
                        # For non-vacation days.
                        if row_idx == len(self.morning_slots):
                            schedule_state[row_idx].append("Pause Déjeuner")
                        else:
                            grid_row = next((gr for gr, idx in grid_mapping.items() if idx == row_idx), None)
                            if grid_row is not None:
                                cell = self.cells.get((grid_row, col_idx))
                                content = self._get_cell_content(cell) if cell else ""
                                schedule_state[row_idx].append(content)
                            else:
                                schedule_state[row_idx].append("")
            logging.info("Final schedule state has {} rows".format(len(schedule_state)))

            # ---- Build the data dictionary for the PDF ----
            # Desired format:
            # {
            #    class_name: [ 
            #         { "date": ..., "time": ..., "content": ..., "observation": ... },
            #         ...
            #    ],
            #    ...
            # }
            pdf_data = {}
            for row in schedule_state:
                time_slot = row[0]
                # Skip the lunch row.
                if time_slot == "12:30 - 14:30":
                    continue
                # Process each day's cell (columns start at index 1).
                for col in range(1, len(row)):
                    cell_val = row[col]
                    if not cell_val:
                        continue
                    day_name = self.columns[col - 1]
                    date_str = week_dates.get(day_name, day_name)
                    
                    # If the cell is a dictionary indicating an event…
                    if isinstance(cell_val, dict) and cell_val.get('type') in ['vacation', 'holiday', 'absence']:
                        # Use the preserved original class if available.
                        group_key = cell_val.get('class', cell_val.get('type').title())
                        entry = {
                            "date": date_str,
                            "time": time_slot,
                            "content": "",  # content is empty because the session was overridden
                            "observation": cell_val.get('text', cell_val.get('type'))
                        }
                        if group_key not in pdf_data:
                            pdf_data[group_key] = []
                        pdf_data[group_key].append(entry)
                    else:
                        # Normal cell: assume the text is "ClassName\nAdditional details..."
                        parts = cell_val.split("\n", 1)
                        group_key = parts[0].strip()
                        content = parts[1].strip() if len(parts) > 1 else ""
                        entry = {
                            "date": date_str,
                            "time": time_slot,
                            "content": content,
                            "observation": ""
                        }
                        if group_key not in pdf_data:
                            pdf_data[group_key] = []
                        pdf_data[group_key].append(entry)
            logging.info("PDF data grouped by class/event: {}".format(pdf_data))

            # Check if there is any data to print.
            if not pdf_data:
                messagebox.showerror("Error", "No schedule entries found to generate grouped PDF.")
                return

            # Ask the user for the save location.
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile="cahier_texte_week_{}_grouped.pdf".format(
                    int(self.week_selector.get().split("Semaine ")[1].split(" -")[0])
                )
            )
            if filename:
                generate_pdf_grouped(pdf_data, filename)
                messagebox.showinfo("Success", "Grouped PDF generated successfully!")
        except Exception as e:
            logging.error("Error in print_to_pdf_grouped: " + str(e), exc_info=True)
            messagebox.showerror("Error", "Failed to generate grouped PDF: " + str(e))











    def _get_cell_content(self, cell):
        try:
            if cell is None:
                return ""
            if isinstance(cell, tuple):
                text_widget, _, class_label = cell
                if text_widget and text_widget.winfo_ismapped():
                    content = text_widget.get('1.0', tk.END).strip()
                    class_text = class_label.cget('text') if class_label else ""
                    return f"{class_text}\n{content}" if content else class_text
                else:
                    return class_label.cget('text') if class_label else ""
            elif hasattr(cell, 'winfo_children') and cell.winfo_children():
                return cell.winfo_children()[0].cget('text')
            return ""
        except Exception as e:
            logging.error(f"Error getting cell content: {str(e)}")
            return ""

    def _get_time_slot_id(self, time_slot):
        return self.db.get_time_slot_id(time_slot)

    def _on_closing(self):
        try:
            if messagebox.askokcancel("Quit", "Do you want to save before quitting?"):
                self.save_schedule()
            self.db.close()
            self.Cahier_texte_window.destroy()
        except Exception as e:
            logging.error(f"Error during application closing: {e}")
            self.Cahier_texte_window.destroy()
