# 🚀 Quick Fix Guide - Critical Issues

## 🔴 BLOCKING ISSUE #1: Missing `course_dist` Module

### Problem
Application crashes immediately on startup with:
```
ModuleNotFoundError: No module named 'course_dist'
```

### Quick Fix Solution

**Option A: Create Package Structure (Recommended)**
```bash
# 1. Create the package directory
mkdir course_dist
touch course_dist/__init__.py

# 2. Move required files into the package
mv db_manager.py course_dist/
mv constants.py course_dist/
mv pdf_generator.py course_dist/
mv course_distribution.py course_dist/
mv SavedSchedulesFrame.py course_dist/
mv cahier_texte.py course_dist/
```

**Option B: Fix Imports (Quick Temporary Fix)**

Replace all imports in affected files:
```python
# BEFORE:
from course_dist.db_manager import DatabaseManager
from course_dist.constants import MORNING_SLOTS, AFTERNOON_SLOTS

# AFTER:
from db_manager import DatabaseManager
from constants import MORNING_SLOTS, AFTERNOON_SLOTS
```

**Files to update**:
- `main.py`
- `home.py`
- `cahier_texte2.py`
- `schedule_grid.py`

---

## 🔴 CRITICAL ISSUE #2: Hardcoded Login

### Problem
Authentication is completely bypassed:
```python
# home.py, lines 58-59
login = 'admin'  # HARDCODED!
password = 'admin'  # HARDCODED!
```

### Quick Fix
```python
# home.py - Replace lines 54-59 with:
def check_login(self):
    """Handle user login."""
    login = self.login_entry.get().strip()
    password = self.password_entry.get().strip()
    
    if not login or not password:
        self.show_error("Veuillez remplir tous les champs")
        return
    
    try:
        enseignant = self.db_manager.get_user(login, password)
        
        if enseignant:
            home_frame = self.controller.frames["HomeFrame"]
            home_frame.set_user(enseignant)
            self.controller.show_frame("HomeFrame")
        else:
            self.show_error("Identifiants incorrects")
    
    except sqlite3.Error as e:
        logging.error(f"Database error during login: {e}")
        self.show_error("Erreur de connexion à la base de données")
    except Exception as e:
        logging.error(f"Unexpected login error: {e}")
        self.show_error("Une erreur inattendue est survenue.")
```

---

## 🔴 CRITICAL ISSUE #3: Missing Database Column

### Problem
```python
# schadual.py tries to update non-existent column
UPDATE schedule_entries 
SET class_id = (SELECT id FROM classes WHERE name = ?),
    updated_at = CURRENT_TIMESTAMP  # ❌ Column doesn't exist!
```

### Quick Fix
Add migration to `db_manager.py`:

```python
def upgrade_schedule_entries_table(self):
    """Add updated_at column if it doesn't exist"""
    try:
        # Check if column exists
        self.cursor.execute("PRAGMA table_info(schedule_entries)")
        columns = [col[1] for col in self.cursor.fetchall()]
        
        if 'updated_at' not in columns:
            self.cursor.execute("""
                ALTER TABLE schedule_entries 
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
            self.conn.commit()
            logging.info("Added updated_at column to schedule_entries")
    except sqlite3.Error as e:
        logging.error(f"Error upgrading schedule_entries: {e}")
```

Call this in `setup_database()`:
```python
def setup_database(self):
    # ... existing code ...
    self.conn.commit()
    logging.info("Database tables set up successfully.")
    
    # Add this line:
    self.upgrade_schedule_entries_table()
    
    self.create_default_admin()
    self.initialize_time_slots()
```

---

## 🟡 HIGH PRIORITY ISSUE #4: Database Path Confusion

### Problem
Multiple database paths:
- `config.py`: `data/cahier_texte.db`
- Root directory: `cahier_texte.db`
- Hardcoded: `"data/cahier_texte.db"`

### Quick Fix
Standardize all references:

```python
# 1. Ensure data directory exists
import os
os.makedirs('data', exist_ok=True)

# 2. Move existing database
if os.path.exists('cahier_texte.db'):
    import shutil
    shutil.move('cahier_texte.db', 'data/cahier_texte.db')

# 3. Update all hardcoded paths
# In cahier_texte.py line 29:
# BEFORE:
self.course_distributor = CourseDistributionManager("data/cahier_texte.db")
# AFTER:
from config import DB_PATH
self.course_distributor = CourseDistributionManager(DB_PATH)
```

---

## 🟡 HIGH PRIORITY ISSUE #5: Duplicate Dictionary Keys

### Problem
```python
# constants.py - Duplicate keys in COLORS dict
COLORS = {
    'holiday_bg': '#FFB6C1',
    'absence_bg': '#FFE4E1',
    'vacation_bg': '#FFE4E1',
    # ... more colors ...
    'holiday_bg': '#FFB6C1',   # DUPLICATE!
    'absence_bg': '#FFE4E1',   # DUPLICATE!
    'vacation_bg': '#FFCCBC',  # DIFFERENT VALUE!
}
```

### Quick Fix
Remove duplicates and consolidate:

```python
# constants.py - Replace COLORS dict with:
COLORS = {
    'header_bg': '#2C3E50',
    'header_fg': 'white',
    'time_bg': '#34495E',
    'time_fg': 'white',
    'cell_bg': 'white',
    'cell_fg': '#2C3E50',
    'empty_fg': '#95A5A6',
    'hover_bg': '#ECF0F1',
    'hover_empty_fg': '#7F8C8D',
    'placeholder_bg': '#F0F0F0',
    'holiday_bg': '#FFB6C1',        # Light pink for holidays
    'absence_bg': '#FFE4E1',        # Light red for absences
    'vacation_bg': '#FFCCBC',       # Light orange for vacations
    'no_more_courses_bg': '#FFF3CD',
    'distribution_error_bg': '#F8D7DA',
    'default_bg': '#FFFFFF'
}
```

---

## 🟡 ISSUE #6: Missing Unique Constraint

### Problem
Code tries to use `ON CONFLICT` without proper constraint:
```python
# schadual.py
INSERT INTO schedule_entries (class_id, day_id, time_slot_id)
...
ON CONFLICT(day_id, time_slot_id) DO UPDATE SET
```

### Quick Fix
Add migration to create unique constraint:

```python
def add_schedule_entries_constraint(self):
    """Add unique constraint to schedule_entries"""
    try:
        # Create new table with constraint
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule_entries_new (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                day_id INTEGER,
                time_slot_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(day_id, time_slot_id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (day_id) REFERENCES days (day_id),
                FOREIGN KEY (time_slot_id) REFERENCES time_slots (slot_id)
            )
        """)
        
        # Copy data
        self.cursor.execute("""
            INSERT OR IGNORE INTO schedule_entries_new 
            SELECT entry_id, class_id, day_id, time_slot_id, 
                   created_at, created_at as updated_at
            FROM schedule_entries
        """)
        
        # Drop old table and rename new one
        self.cursor.execute("DROP TABLE IF EXISTS schedule_entries")
        self.cursor.execute("ALTER TABLE schedule_entries_new RENAME TO schedule_entries")
        
        self.conn.commit()
        logging.info("Added unique constraint to schedule_entries")
    except sqlite3.Error as e:
        logging.error(f"Error adding constraint: {e}")
        self.conn.rollback()
```

---

## 🟢 MEDIUM PRIORITY ISSUE #7: Incorrect Row Calculation

### Problem
```python
# schadual.py - Wrong afternoon slot calculation
if row <= 4:
    time_slot = self.morning_slots[row - 1]
else:
    time_slot = self.afternoon_slots[row - 6]  # ❌ Should account for separator
```

### Quick Fix
```python
# Calculate based on total morning slots and separator
MORNING_SLOT_COUNT = len(self.morning_slots)  # 4
SEPARATOR_ROWS = 1

if row <= MORNING_SLOT_COUNT:
    time_slot = self.morning_slots[row - 1]
else:
    # Account for separator row
    afternoon_index = row - MORNING_SLOT_COUNT - SEPARATOR_ROWS - 1
    time_slot = self.afternoon_slots[afternoon_index]
```

---

## 📋 Step-by-Step Fix Priority

### Phase 1: Make Application Runnable (30 minutes)
1. ✅ Fix import errors (course_dist)
2. ✅ Fix hardcoded login
3. ✅ Create requirements.txt
4. ✅ Standardize database path

### Phase 2: Fix Database Issues (1 hour)
5. ✅ Add updated_at column
6. ✅ Add unique constraint
7. ✅ Fix duplicate colors
8. ✅ Test database operations

### Phase 3: Fix Logic Errors (1 hour)
9. ✅ Fix row calculation
10. ✅ Test schedule operations
11. ✅ Verify PDF generation

### Phase 4: Security & Validation (2 hours)
12. ✅ Add password hashing
13. ✅ Add input validation
14. ✅ Add error handling
15. ✅ Test user login flow

---

## 🧪 Testing Checklist

After fixes, test these scenarios:

### Login Flow
- [ ] Valid credentials login
- [ ] Invalid credentials rejected
- [ ] Empty fields validation
- [ ] Database connection error handling

### Schedule Management
- [ ] Create schedule entry
- [ ] Update existing entry
- [ ] Delete entry
- [ ] Load saved schedule
- [ ] Navigate between weeks

### Course Distribution
- [ ] Distribute courses for week
- [ ] Handle vacation periods
- [ ] Handle holidays
- [ ] Handle absences
- [ ] Save distribution

### PDF Generation
- [ ] Generate single-page PDF
- [ ] Generate split PDF (large schedule)
- [ ] Handle empty schedule
- [ ] Handle vacation/holiday cells

### Data Import
- [ ] Import Excel file
- [ ] Handle invalid file
- [ ] Handle duplicate entries
- [ ] Display imported data

---

## 🆘 Emergency Rollback

If fixes cause issues, rollback steps:

1. **Restore from git**:
```bash
git stash
git reset --hard HEAD
```

2. **Restore database**:
```bash
cp data/cahier_texte.db.backup data/cahier_texte.db
```

3. **Clear Python cache**:
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📞 Support

If you encounter issues during fixes:

1. Check logs in `logs/` directory
2. Review `PROJECT_ANALYSIS.md` for detailed explanations
3. Test in isolation (create test database)
4. Document any new issues found

---

**Last Updated**: 2025-11-15  
**Version**: 1.0
