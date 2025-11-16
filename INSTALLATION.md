# 📦 Installation Guide

## ✅ Prerequisites

### Required Software
- **Python 3.8+** - Programming language
- **pip** - Python package manager
- **tkinter** - GUI framework (usually included with Python)

### System Requirements
- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 2GB
- **Disk Space**: 500MB free space
- **Display**: Minimum 1024x768 resolution

---

## 🚀 Quick Installation

### Step 1: Verify Python Installation
```bash
python3 --version
# Should show Python 3.8 or higher
```

### Step 2: Install Dependencies
```bash
cd /home/user/webapp
pip3 install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python3 -c "import tkinter, reportlab, pandas, tkcalendar; print('All dependencies installed!')"
```

### Step 4: Run the Application
```bash
./run.sh
# OR
python3 main.py
```

---

## 📚 Detailed Installation

### For Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt-get update

# Install Python 3 and pip
sudo apt-get install python3 python3-pip

# Install tkinter (if not already installed)
sudo apt-get install python3-tk

# Install Python dependencies
pip3 install -r requirements.txt

# Run the application
./run.sh
```

### For macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3

# tkinter is usually included with Python on macOS

# Install Python dependencies
pip3 install -r requirements.txt

# Run the application
./run.sh
```

### For Windows

1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - **Important**: Check "Add Python to PATH" during installation

2. **Open Command Prompt** (cmd.exe):
```cmd
# Navigate to project directory
cd C:\path\to\webapp

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🔧 Troubleshooting

### Issue: "tkinter not found"

**Linux**:
```bash
sudo apt-get install python3-tk
```

**macOS**:
```bash
brew install python-tk@3.11  # Replace 3.11 with your Python version
```

**Windows**:
- Reinstall Python from python.org
- Ensure "tcl/tk and IDLE" is checked during installation

---

### Issue: "ModuleNotFoundError: No module named 'reportlab'"

```bash
pip3 install reportlab
```

---

### Issue: "Cannot connect to database"

1. Check if `data/` directory exists:
```bash
ls -la data/
```

2. If not, create it:
```bash
mkdir -p data
```

3. Check database permissions:
```bash
chmod 644 data/cahier_texte.db  # If file exists
```

4. Delete and recreate database (⚠️ **This will delete all data**):
```bash
rm data/cahier_texte.db
python3 main.py  # Will create new database
```

---

### Issue: "Permission denied" on run.sh

```bash
chmod +x run.sh
./run.sh
```

---

## 📋 Dependency Details

### Core Dependencies (Required)

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.8+ | Runtime |
| tkinter | Built-in | GUI framework |
| reportlab | 3.6.0+ | PDF generation |
| pandas | 1.5.0+ | Data processing |
| tkcalendar | 1.6.0+ | Calendar widgets |
| Pillow | 9.0.0+ | Image processing |
| openpyxl | 3.0.0+ | Excel file handling |

### Optional Dependencies

| Package | Purpose |
|---------|---------|
| pytest | Unit testing |
| black | Code formatting |
| flake8 | Code linting |

---

## 🎯 Post-Installation Steps

### 1. First Run

```bash
./run.sh
```

The application will:
- Create necessary directories (`data/`, `logs/`)
- Initialize the database
- Create default admin user
- Open the login window

### 2. First Login

**Default Credentials**:
- **Username**: `admin`
- **Password**: `admin`

⚠️ **IMPORTANT**: Change the default password immediately!

### 3. Verify Installation

Test these features:
- [ ] Login with default credentials
- [ ] Navigate to "Emploi du temps"
- [ ] Try to add a schedule entry
- [ ] Check if PDF export works
- [ ] Try importing an Excel file

---

## 🔐 Security Configuration (Recommended)

### Change Default Password

After first login:
1. Currently, you need to change it directly in the database
2. Future versions will have a password change interface

**Manual Password Change** (temporary solution):
```sql
sqlite3 data/cahier_texte.db
UPDATE enseignants SET password = 'new_password_here' WHERE login = 'admin';
.quit
```

⚠️ **Note**: Future versions will hash passwords for security

---

## 📁 Directory Structure After Installation

```
webapp/
├── main.py                 # Application entry point
├── run.sh                  # Startup script (Linux/macOS)
├── requirements.txt        # Python dependencies
│
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── constants.py        # Constants
│   ├── db_manager.py       # Database management
│   └── theme_manager.py    # UI theme
│
├── ui/                     # User interface
│   ├── __init__.py
│   ├── home.py             # Login/Home screens
│   ├── schadual.py         # Schedule management
│   ├── cahier_texte.py     # Textbook tracking
│   └── ...
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── course_distribution.py
│   ├── pdf_generator.py
│   ├── import_excel.py
│   └── ...
│
├── data/                   # Database and data files
│   └── cahier_texte.db     # SQLite database
│
├── logs/                   # Application logs
│   ├── error_*.log
│   └── debug_*.log
│
└── tests/                  # Unit tests (future)
    └── __init__.py
```

---

## 🆘 Getting Help

### Check Logs

If the application fails to start:
```bash
cat logs/error_$(date +%Y%m%d).log
cat logs/debug_$(date +%Y%m%d).log
```

### Common Solutions

1. **Import errors**: Reinstall dependencies
   ```bash
   pip3 install -r requirements.txt --force-reinstall
   ```

2. **Database errors**: Check permissions
   ```bash
   chmod -R 755 data/
   ```

3. **Display issues**: Check DISPLAY variable (Linux)
   ```bash
   echo $DISPLAY
   export DISPLAY=:0  # If empty
   ```

### Report Issues

If problems persist:
1. Check existing documentation
2. Review logs
3. Note error messages
4. Document steps to reproduce

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip3 list`)
- [ ] `data/` directory exists
- [ ] `logs/` directory exists
- [ ] Database file created (`data/cahier_texte.db`)
- [ ] Application starts without errors
- [ ] Login screen appears
- [ ] Can login with default credentials
- [ ] Home screen loads successfully
- [ ] Can navigate between screens

---

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Backup current database
cp data/cahier_texte.db data/cahier_texte.db.backup

# Pull latest changes (if using git)
git pull

# Update dependencies
pip3 install -r requirements.txt --upgrade

# Restart application
./run.sh
```

### Database Backup

**Manual Backup**:
```bash
cp data/cahier_texte.db data/backup_$(date +%Y%m%d).db
```

**Restore from Backup**:
```bash
cp data/backup_YYYYMMDD.db data/cahier_texte.db
```

---

**Installation Complete!** 🎉

If you encounter any issues, please check the troubleshooting section or review the application logs.
