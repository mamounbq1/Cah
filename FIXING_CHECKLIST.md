# ✅ Comprehensive Fixing Checklist

## 🎯 How to Use This Checklist

1. Work through items in order (they're prioritized)
2. Check off ✅ items as you complete them
3. Test after each section
4. Document any issues found
5. Commit changes frequently

---

## 🚨 PHASE 1: EMERGENCY FIXES (DO FIRST!)

### A. Fix Import Errors (BLOCKING - 30 min)

- [ ] **Create `course_dist` package**
  ```bash
  cd /home/user/webapp
  mkdir -p course_dist
  touch course_dist/__init__.py
  ```

- [ ] **Move files to package** (Choose one approach):
  
  **Option A - Move files** (Recommended):
  - [ ] Move `db_manager.py` to `course_dist/`
  - [ ] Move `constants.py` to `course_dist/`
  - [ ] Move `pdf_generator.py` to `course_dist/`
  - [ ] Move `course_distribution.py` to `course_dist/`
  - [ ] Move `SavedSchedulesFrame.py` to `course_dist/`
  - [ ] Keep a copy of `cahier_texte.py` (imported in main)
  
  **Option B - Fix all imports** (Faster):
  - [ ] Update `main.py` imports (lines 12, 14, 15)
  - [ ] Update `home.py` imports (line 4)
  - [ ] Update `cahier_texte.py` imports (lines 7-13)
  - [ ] Update `cahier_texte2.py` imports (lines 7, 8, 12)
  - [ ] Update `course_distribution.py` imports (lines 5, 7)
  - [ ] Update `schedule_grid.py` imports (line 2)

- [ ] **Test application starts**
  ```bash
  python3 main.py
  ```

**Expected Result**: Application window opens (even if login fails)

---

### B. Fix Security Issues (CRITICAL - 15 min)

- [ ] **Remove hardcoded credentials** (`home.py` lines 58-59)
  ```python
  # Replace:
  login = 'admin'
  password = 'admin'
  
  # With:
  login = self.login_entry.get().strip()
  password = self.password_entry.get().strip()
  ```

- [ ] **Test login flow**
  - [ ] Try invalid credentials (should reject)
  - [ ] Try valid credentials (admin/admin from DB)
  - [ ] Try empty fields (should show error)

**Expected Result**: Login requires actual credentials from database

---

### C. Fix Database Issues (HIGH - 30 min)

- [ ] **Add `updated_at` column** (Update `db_manager.py`)
  ```python
  def upgrade_schedule_entries_table(self):
      """Add updated_at column if it doesn't exist"""
      try:
          self.cursor.execute("PRAGMA table_info(schedule_entries)")
          columns = [col[1] for col in self.cursor.fetchall()]
          
          if 'updated_at' not in columns:
              self.cursor.execute("""
                  ALTER TABLE schedule_entries 
                  ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
              """)
              self.conn.commit()
              logging.info("Added updated_at column")
      except sqlite3.Error as e:
          logging.error(f"Error upgrading table: {e}")
  ```

- [ ] **Call upgrade in `setup_database()`** (after line 159)

- [ ] **Add UNIQUE constraint** (Update `db_manager.py`)
  ```python
  # In setup_database(), modify schedule_entries table:
  """CREATE TABLE IF NOT EXISTS schedule_entries (
      entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
      class_id INTEGER,
      day_id INTEGER,
      time_slot_id INTEGER, 
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(day_id, time_slot_id),  -- ADD THIS LINE
      FOREIGN KEY (class_id) REFERENCES classes (id),
      FOREIGN KEY (day_id) REFERENCES days (day_id),
      FOREIGN KEY (time_slot_id) REFERENCES time_slots (slot_id)
  )"""
  ```

- [ ] **Backup existing database**
  ```bash
  cp cahier_texte.db cahier_texte.db.backup
  # OR
  cp data/cahier_texte.db data/cahier_texte.db.backup
  ```

- [ ] **Test database operations**
  - [ ] Add schedule entry
  - [ ] Update schedule entry
  - [ ] Delete schedule entry
  - [ ] Check logs for errors

**Expected Result**: Schedule operations complete without errors

---

### D. Standardize Database Path (MEDIUM - 15 min)

- [ ] **Ensure data directory exists**
  ```bash
  mkdir -p data
  ```

- [ ] **Move database if needed**
  ```bash
  if [ -f cahier_texte.db ] && [ ! -f data/cahier_texte.db ]; then
      mv cahier_texte.db data/
  fi
  ```

- [ ] **Update hardcoded paths**:
  - [ ] `cahier_texte.py` line 29: Use `from config import DB_PATH`
  - [ ] Check all files for "cahier_texte.db" and replace with `DB_PATH`

- [ ] **Verify config.py is correct**
  ```python
  import os
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  DB_PATH = os.path.join(BASE_DIR, 'data', 'cahier_texte.db')
  ```

**Expected Result**: Application uses consistent database path

---

## ⚡ PHASE 2: FIX CRITICAL BUGS (30-60 min)

### E. Fix Code Bugs

- [ ] **Fix duplicate dictionary keys** (`constants.py`)
  ```python
  # Remove duplicate entries at lines 19-23
  # Keep only one definition per key
  ```

- [ ] **Fix incorrect row calculation** (`schadual.py`)
  ```python
  # Lines 210-213 and 250-253
  MORNING_SLOT_COUNT = len(self.morning_slots)
  SEPARATOR_ROWS = 1
  
  if row <= MORNING_SLOT_COUNT:
      time_slot = self.morning_slots[row - 1]
  else:
      afternoon_index = row - MORNING_SLOT_COUNT - SEPARATOR_ROWS - 1
      time_slot = self.afternoon_slots[afternoon_index]
  ```

- [ ] **Test schedule grid**
  - [ ] Click morning slot cells
  - [ ] Click afternoon slot cells
  - [ ] Verify correct time slot selected

**Expected Result**: Schedule cell clicks select correct time slots

---

### F. Error Handling Improvements

- [ ] **Add try-catch in main initialization**
- [ ] **Add validation in form inputs**
- [ ] **Add user-friendly error messages**
- [ ] **Log all exceptions properly**

**Test Cases**:
- [ ] Invalid date input
- [ ] Empty form submission
- [ ] Database connection failure
- [ ] File I/O errors

**Expected Result**: Errors are caught and displayed appropriately

---

## 🔐 PHASE 3: SECURITY HARDENING (1-2 hours)

### G. Password Security

- [ ] **Install bcrypt**
  ```bash
  pip install bcrypt
  ```

- [ ] **Add password hashing** (Update `db_manager.py`)
  ```python
  import bcrypt
  
  def hash_password(self, password: str) -> str:
      """Hash password using bcrypt"""
      salt = bcrypt.gensalt()
      return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
  
  def verify_password(self, password: str, hashed: str) -> bool:
      """Verify password against hash"""
      return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
  ```

- [ ] **Update `create_default_admin()`**
  ```python
  hashed_pw = self.hash_password('admin')
  self.cursor.execute("""
      INSERT INTO enseignants (nom, matiere, login, password) 
      VALUES ('admin', 'admin', 'admin', ?)
  """, (hashed_pw,))
  ```

- [ ] **Update `get_user()` method**
  ```python
  def get_user(self, login, password):
      self.cursor.execute("SELECT * FROM enseignants WHERE login=?", (login,))
      user = self.cursor.fetchone()
      if user and self.verify_password(password, user[4]):  # user[4] is password
          return user
      return None
  ```

- [ ] **Migrate existing passwords**
  ```bash
  # Create a migration script or manually reset passwords
  ```

**Expected Result**: Passwords are hashed in database

---

### H. Input Validation

- [ ] **Create validation module** (`validators.py`)
  ```python
  import re
  from datetime import datetime
  
  class Validator:
      @staticmethod
      def validate_date(date_str):
          """Validate date format YYYY-MM-DD"""
          try:
              datetime.strptime(date_str, '%Y-%m-%d')
              return True, None
          except ValueError:
              return False, "Format de date invalide"
      
      @staticmethod
      def validate_text(text, min_len=1, max_len=1000):
          """Validate text length"""
          if len(text) < min_len:
              return False, f"Texte trop court (minimum {min_len})"
          if len(text) > max_len:
              return False, f"Texte trop long (maximum {max_len})"
          return True, None
      
      @staticmethod
      def validate_email(email):
          """Validate email format"""
          pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
          if re.match(pattern, email):
              return True, None
          return False, "Format d'email invalide"
  ```

- [ ] **Add validation to forms**
  - [ ] Login form
  - [ ] Date pickers
  - [ ] Text inputs
  - [ ] Excel import

**Expected Result**: Invalid inputs are rejected with clear messages

---

## 🧹 PHASE 4: CODE CLEANUP (2-4 hours)

### I. Remove Unused Files

- [ ] **Identify test files to remove or move**
  - [ ] `test.py` (has generate_pdf_grouped, might be needed)
  - [ ] `test1.py` (782 lines - review before deleting)
  - [ ] `test3.py` (347 lines - review before deleting)

- [ ] **Check for duplicate functionality**
  - [ ] `cahier_texte.py` vs `cahier_texte2.py` (compare and consolidate)

- [ ] **Remove unused imports**
  ```bash
  # Use a tool like autoflake
  pip install autoflake
  autoflake --remove-all-unused-imports --in-place --recursive .
  ```

**Expected Result**: Clean codebase without clutter

---

### J. Add Documentation

- [ ] **Create README.md**
  ```markdown
  # School Schedule Management System
  
  ## Installation
  ## Usage
  ## Features
  ## Requirements
  ## Troubleshooting
  ```

- [ ] **Add docstrings to functions**
  ```python
  def save_schedule(self, week_number: int, schedule_data: List[Tuple]) -> bool:
      """
      Save schedule for a specific week.
      
      Args:
          week_number: ISO week number (1-53)
          schedule_data: List of (row, col, content) tuples
      
      Returns:
          True if successful, False otherwise
      
      Raises:
          sqlite3.Error: If database operation fails
      """
  ```

- [ ] **Document database schema**
  - [ ] Create ER diagram
  - [ ] Document table relationships
  - [ ] Add comments to complex queries

**Expected Result**: Code is well-documented

---

### K. Code Quality Improvements

- [ ] **Add type hints**
  ```python
  from typing import List, Dict, Tuple, Optional
  ```

- [ ] **Follow PEP 8**
  ```bash
  pip install black flake8
  black *.py
  flake8 --max-line-length=120 *.py
  ```

- [ ] **Extract magic numbers**
  ```python
  # Before:
  if row <= 4:
  
  # After:
  MORNING_ROWS = 4
  if row <= MORNING_ROWS:
  ```

- [ ] **Break up large functions**
  - [ ] `cahier_texte.py` has very long functions
  - [ ] Split into smaller, testable units

**Expected Result**: Code follows best practices

---

## 🧪 PHASE 5: TESTING (4-8 hours)

### L. Manual Testing

- [ ] **Test Login Flow**
  - [ ] Valid login
  - [ ] Invalid login
  - [ ] Empty fields
  - [ ] Database error

- [ ] **Test Schedule Management**
  - [ ] Create entry
  - [ ] Update entry
  - [ ] Delete entry
  - [ ] Load saved schedule
  - [ ] Navigate weeks

- [ ] **Test Course Distribution**
  - [ ] Distribute courses
  - [ ] Handle vacations
  - [ ] Handle holidays
  - [ ] Save distribution

- [ ] **Test Excel Import**
  - [ ] Valid file
  - [ ] Invalid file
  - [ ] Large file
  - [ ] Duplicate data

- [ ] **Test PDF Generation**
  - [ ] Single page
  - [ ] Multiple pages
  - [ ] Empty schedule
  - [ ] Special characters

- [ ] **Test Calendar Features**
  - [ ] Add vacation
  - [ ] Add holiday
  - [ ] Add absence
  - [ ] Delete events
  - [ ] View events

**Expected Result**: All features work as expected

---

### M. Automated Testing (Optional but Recommended)

- [ ] **Setup pytest**
  ```bash
  pip install pytest pytest-cov
  mkdir tests
  ```

- [ ] **Write unit tests**
  ```python
  # tests/test_db_manager.py
  def test_create_default_admin():
      db = DatabaseManager(':memory:')
      # Test admin creation
  
  def test_save_schedule():
      # Test schedule saving
  ```

- [ ] **Write integration tests**
  ```python
  # tests/test_integration.py
  def test_full_schedule_workflow():
      # Test complete workflow
  ```

- [ ] **Run tests**
  ```bash
  pytest -v --cov=.
  ```

**Expected Result**: >70% code coverage

---

## 📦 PHASE 6: DEPLOYMENT PREP (2-4 hours)

### N. Documentation

- [ ] **Create user manual** (French)
- [ ] **Create developer guide**
- [ ] **Create installation guide**
- [ ] **Create troubleshooting guide**
- [ ] **Document API/database**

---

### O. Deployment Checklist

- [ ] **Create setup script**
  ```bash
  #!/bin/bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python3 main.py
  ```

- [ ] **Create installer** (optional)
  ```bash
  # Using PyInstaller
  pip install pyinstaller
  pyinstaller --onefile --windowed main.py
  ```

- [ ] **Test on clean environment**
- [ ] **Create backup procedures**
- [ ] **Setup logging rotation**
- [ ] **Create update procedure**

**Expected Result**: Application can be deployed easily

---

## 📊 PROGRESS TRACKING

### Overall Progress

```
Phase 1: Emergency Fixes     [          ] 0/4   (0%)
Phase 2: Critical Bugs       [          ] 0/2   (0%)
Phase 3: Security Hardening  [          ] 0/2   (0%)
Phase 4: Code Cleanup        [          ] 0/4   (0%)
Phase 5: Testing            [          ] 0/2   (0%)
Phase 6: Deployment         [          ] 0/2   (0%)
───────────────────────────────────────────────
Total Progress:             [          ] 0/16  (0%)
```

### Time Estimates

| Phase | Estimated Time | Actual Time |
|-------|---------------|-------------|
| Phase 1 | 1.5 hours | _____ |
| Phase 2 | 1 hour | _____ |
| Phase 3 | 2 hours | _____ |
| Phase 4 | 3 hours | _____ |
| Phase 5 | 6 hours | _____ |
| Phase 6 | 3 hours | _____ |
| **Total** | **16.5 hours** | **_____** |

---

## 🎯 Definition of Done

A task is complete when:

1. ✅ Code changes implemented
2. ✅ Code reviewed (self or peer)
3. ✅ Tests pass (manual or automated)
4. ✅ Documentation updated
5. ✅ Changes committed to git
6. ✅ No new bugs introduced

---

## 📝 Notes Section

Use this space to track issues, decisions, or observations:

```
Date: ___________
Issue: ___________
Resolution: ___________

Date: ___________
Issue: ___________
Resolution: ___________
```

---

**Last Updated**: 2025-11-15  
**Version**: 1.0  
**Status**: Ready to use
