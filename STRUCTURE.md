# 📐 Project Structure Documentation

## 🎯 Overview

This document describes the reorganized structure of the School Schedule Management System after refactoring.

---

## 📊 Directory Tree

```
webapp/
│
├── 📄 main.py                      # Application entry point
├── 🚀 run.sh                       # Startup script (Linux/macOS)
├── 📋 requirements.txt             # Python dependencies
│
├── 📚 Documentation Files
│   ├── README.md                   # Main documentation
│   ├── INSTALLATION.md             # Installation guide
│   ├── STRUCTURE.md                # This file
│   ├── PROJECT_ANALYSIS.md         # Bug analysis
│   ├── PROJECT_SUMMARY.md          # Executive summary
│   ├── QUICK_FIX_GUIDE.md          # Quick fixes
│   └── FIXING_CHECKLIST.md         # Fix checklist
│
├── 🔧 core/                        # Core functionality
│   ├── __init__.py
│   ├── config.py                   # Global configuration
│   ├── constants.py                # Application constants
│   ├── db_manager.py               # Database operations
│   └── theme_manager.py            # UI theme management
│
├── 🎨 ui/                          # User interface components
│   ├── __init__.py
│   ├── home.py                     # Login & home screens
│   ├── schadual.py                 # Schedule management
│   ├── cahier_texte.py             # Textbook/course tracking
│   ├── SavedSchedulesFrame.py      # Saved schedules view
│   ├── schedule_grid.py            # Schedule grid widget
│   ├── tap_manager.py              # Tab management
│   ├── top_frame.py                # Top navigation
│   └── loading_window.py           # Loading screen
│
├── ⚙️ services/                    # Business logic & services
│   ├── __init__.py
│   ├── course_distribution.py      # Course distribution logic
│   ├── pdf_generator.py            # PDF generation
│   ├── test.py                     # PDF grouping (grouped export)
│   ├── import_excel.py             # Excel import functionality
│   ├── vacances.py                 # Vacation management
│   ├── holiday.py                  # Holiday management
│   ├── absences.py                 # Absence tracking
│   ├── modules.py                  # Module management
│   ├── classes.py                  # Class management
│   └── add_entry.py                # Add entry functionality
│
├── 🔨 utils/                       # Utility functions (future)
│   └── __init__.py
│
├── 🗄️ data/                        # Database & data files
│   ├── cahier_texte.db             # SQLite database
│   └── Classeur1.xlsx              # Sample Excel file
│
├── 📝 logs/                        # Application logs
│   ├── error_YYYYMMDD.log          # Error logs
│   └── debug_YYYYMMDD.log          # Debug logs
│
├── 🧪 tests/                       # Unit tests (to be implemented)
│   └── __init__.py
│
└── 🗑️ Old Files (for reference)
    ├── cahier_texte.log
    ├── cahier_texte2.py            # Duplicate (deprecated)
    ├── test1.py                    # Test file (to be removed)
    └── test3.py                    # Test file (to be removed)
```

---

## 📦 Package Descriptions

### 1. `core/` - Core Functionality

**Purpose**: Contains fundamental application components used across the entire system.

| File | Description | Key Functions |
|------|-------------|---------------|
| `config.py` | Global configuration | `BASE_DIR`, `DB_PATH` |
| `constants.py` | Application constants | `COLORS`, `MORNING_SLOTS`, `AFTERNOON_SLOTS`, `DAYS` |
| `db_manager.py` | Database operations | `DatabaseManager` class, CRUD operations |
| `theme_manager.py` | UI theme | `ThemeManager.setup_theme()` |

**Dependencies**: None (only Python standard library)

---

### 2. `ui/` - User Interface

**Purpose**: All graphical user interface components and screens.

| File | Description | Main Classes |
|------|-------------|--------------|
| `home.py` | Login & dashboard | `LoginFrame`, `HomeFrame` |
| `schadual.py` | Schedule view/edit | `EmploiDuTempsApp` |
| `cahier_texte.py` | Course textbook | `CahierTextFrame` |
| `SavedSchedulesFrame.py` | Saved schedules | `SavedSchedulesFrame` |
| `schedule_grid.py` | Schedule grid widget | Grid rendering logic |
| `tap_manager.py` | Tab management | `TabManagerFrame` |
| `top_frame.py` | Navigation bar | `TopFrame` |
| `loading_window.py` | Loading screen | `LoadingContext` |

**Dependencies**: 
- `core.*` (config, db_manager, theme_manager, constants)
- `services.*` (for business logic)

---

### 3. `services/` - Business Logic

**Purpose**: Business logic, data processing, and external services.

| File | Description | Key Functions |
|------|-------------|---------------|
| `course_distribution.py` | Course distribution | `CourseDistributionManager` |
| `pdf_generator.py` | PDF export | `generate_pdf()` |
| `test.py` | Grouped PDF export | `generate_pdf_grouped()` |
| `import_excel.py` | Excel import | `ExcelImporterFrame` |
| `vacances.py` | Vacation management | CRUD for vacations |
| `holiday.py` | Holiday management | CRUD for holidays |
| `absences.py` | Absence tracking | CRUD for absences |
| `modules.py` | Module management | Module operations |
| `classes.py` | Class management | Class operations |
| `add_entry.py` | Entry addition | Add new entries |

**Dependencies**: 
- `core.*` (config, db_manager, constants)
- External: `reportlab`, `pandas`, `openpyxl`

---

### 4. `utils/` - Utilities (Future)

**Purpose**: Utility functions and helpers.

**Planned Content**:
- Input validators
- Date/time helpers
- String formatters
- File I/O helpers

---

### 5. `data/` - Data Storage

**Purpose**: Persistent data storage.

| Item | Type | Description |
|------|------|-------------|
| `cahier_texte.db` | SQLite | Main database |
| `*.xlsx` | Excel | Sample/import files |
| `backup_*.db` | SQLite | Database backups |

---

### 6. `logs/` - Application Logs

**Purpose**: Application logging and debugging.

| Log File | Content |
|----------|---------|
| `error_YYYYMMDD.log` | Error-level logs |
| `debug_YYYYMMDD.log` | Debug-level logs |

**Rotation**: Daily (by date)

---

## 🔗 Import Relationships

### Import Hierarchy

```
main.py
├── core.theme_manager
├── core.db_manager
├── core.config
│
├── ui.home
│   ├── core.db_manager
│   └── core.theme_manager
│
├── ui.schadual
│   ├── core.config
│   ├── core.theme_manager
│   └── services.pdf_generator
│
├── ui.cahier_texte
│   ├── core.db_manager
│   ├── core.constants
│   ├── services.course_distribution
│   └── services.pdf_generator
│
└── services.*
    ├── core.config
    ├── core.db_manager
    └── core.constants
```

### Key Import Rules

1. **`core/`** modules have no internal dependencies
2. **`ui/`** modules import from `core/` and `services/`
3. **`services/`** modules import from `core/` only
4. **No circular imports** allowed
5. **All imports are absolute** (not relative)

---

## 📊 Database Schema

Located in: `data/cahier_texte.db`

### Core Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `enseignants` | Teachers | id, nom, matiere, login, password |
| `classes` | Classes | id, name, level, school_year |
| `days` | Days of week | day_id, name |
| `time_slots` | Time periods | slot_id, start_time, end_time |
| `schedule_entries` | Schedule | entry_id, class_id, day_id, time_slot_id |
| `vacances` | Vacations | id, start_date, end_date, label |
| `jours_feries` | Holidays | id, date, label |
| `absences` | Absences | id, date, motif |

See `core/db_manager.py` for complete schema.

---

## 🚀 Application Flow

### Startup Sequence

```
1. main.py executed
   ↓
2. Import all modules
   ↓
3. Initialize MainApp (tk.Tk)
   ↓
4. Setup logging (logs/ directory)
   ↓
5. Setup theme (ThemeManager)
   ↓
6. Setup window (geometry, style)
   ↓
7. Initialize all frames
   ├── LoginFrame
   ├── HomeFrame
   ├── EmploiDuTempsApp
   ├── TabManagerFrame
   ├── SavedSchedulesFrame
   ├── CahierTextFrame
   └── ExcelImporterFrame
   ↓
8. Initialize DatabaseManager
   ├── Connect to database
   ├── Create tables if needed
   ├── Create default admin user
   └── Initialize time slots
   ↓
9. Show LoginFrame
   ↓
10. Start main event loop
```

### User Flow

```
Login Screen (LoginFrame)
├─[Success]→ Home Screen (HomeFrame)
│            ├─[➕ Ajouter une entrée]→ CahierTextFrame
│            ├─[🖨️ Imprimer l'état]→ SavedSchedulesFrame
│            ├─[📥 Importer contenu]→ ExcelImporterFrame
│            ├─[⚙️ Ajouter contraintes]→ TabManagerFrame
│            ├─[📅 Emploi du temps]→ EmploiDuTempsApp
│            └─[📚 Distribuer cours]→ CahierTextFrame
│
└─[Failure]→ Error message, retry
```

---

## 🔧 Configuration

### Global Configuration (`core/config.py`)

```python
BASE_DIR = <project_root>
DB_PATH = <project_root>/data/cahier_texte.db
```

### Application Constants (`core/constants.py`)

- **Colors**: UI color scheme
- **Time Slots**: Morning/afternoon periods
- **Days**: Days of the week (French)
- **Functions**: Date/time utilities

---

## 🧹 Cleanup Status

### ✅ Completed
- [x] Reorganized file structure
- [x] Fixed all imports
- [x] Removed hardcoded credentials
- [x] Fixed database issues
- [x] Created documentation

### 🔄 In Progress
- [ ] Remove old/duplicate files
- [ ] Add unit tests
- [ ] Improve error handling

### 📅 Planned
- [ ] Add input validation
- [ ] Implement password hashing
- [ ] Add user roles
- [ ] Create web interface

---

## 📝 Naming Conventions

### Files
- **Lowercase with underscores**: `db_manager.py`, `theme_manager.py`
- **PascalCase for classes**: `DatabaseManager`, `ThemeManager`
- **Clear, descriptive names**: Not `utils.py`, but `database_utils.py`

### Directories
- **Lowercase**: `core/`, `ui/`, `services/`
- **Descriptive**: Not `src/`, but `core/`
- **No abbreviations**: Not `svc/`, but `services/`

### Python Code
- **Classes**: `PascalCase` (e.g., `DatabaseManager`)
- **Functions**: `snake_case` (e.g., `get_user()`)
- **Constants**: `UPPER_CASE` (e.g., `DB_PATH`)
- **Private**: `_leading_underscore` (e.g., `_setup_environment()`)

---

## 🔒 Security Notes

### Current State
- ✅ Imports are fixed
- ✅ Hardcoded credentials removed
- ✅ Database path centralized
- ⚠️ Passwords not hashed (TODO)
- ⚠️ No input validation (TODO)
- ⚠️ No role-based access (TODO)

### Recommendations
1. Implement password hashing (bcrypt)
2. Add input sanitization
3. Implement RBAC
4. Add audit logging
5. Encrypt sensitive data

---

## 📊 Statistics

- **Total Files**: 29 Python files
- **Lines of Code**: ~8,500
- **Core Modules**: 4
- **UI Components**: 8
- **Services**: 9
- **Documentation Files**: 7
- **Test Coverage**: 0% (to be improved)

---

## 🆘 Common Tasks

### Adding a New UI Component

1. Create file in `ui/` directory
2. Import from `core.*` as needed
3. Register in `main.py` `frame_classes` dict
4. Add navigation from `HomeFrame`

### Adding a New Service

1. Create file in `services/` directory
2. Import from `core.*` as needed
3. Use `DatabaseManager` for data access
4. Call from UI components

### Modifying Database Schema

1. Update `core/db_manager.py` `setup_database()`
2. Create migration function if needed
3. Test with fresh database
4. Document changes

---

**Last Updated**: 2025-11-16  
**Version**: 2.0 (Reorganized)  
**Status**: Production-Ready Structure
