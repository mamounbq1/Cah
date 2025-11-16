# 🪟 Windows Setup Guide

## ⚠️ Error: "Le chemin d'accès spécifié est introuvable"

This error means "The specified path cannot be found" in French. Here's how to fix it:

---

## 🔧 Quick Fix Steps

### Step 1: Ensure Directory Structure Exists

Open **Command Prompt** (cmd.exe) or **PowerShell** as Administrator:

```cmd
cd "C:\Users\DELL\Desktop\MAE 2026\Cah-main"
```

### Step 2: Create Required Directories

```cmd
mkdir data
mkdir logs
```

### Step 3: Check if Database Exists

```cmd
dir data
```

If `cahier_texte.db` is missing, the application will create it on first run.

### Step 4: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

If you get an error about pip not found:
```cmd
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

```cmd
python main.py
```

---

## 📋 Complete Windows Installation

### 1. Install Python

1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Also check "Install tcl/tk and IDLE"
4. Click "Install Now"

### 2. Verify Python Installation

Open Command Prompt and type:
```cmd
python --version
```

Should show Python 3.8 or higher.

### 3. Navigate to Project Directory

```cmd
cd "C:\Users\DELL\Desktop\MAE 2026\Cah-main"
```

**Note**: Use quotes if path contains spaces.

### 4. Create Project Structure

```cmd
mkdir data
mkdir logs
```

### 5. Install Dependencies

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run Application

```cmd
python main.py
```

---

## 🐛 Troubleshooting Windows-Specific Issues

### Issue 1: "python is not recognized"

**Solution**:
1. Add Python to PATH manually:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\Users\DELL\AppData\Local\Programs\Python\Python3XX` (replace XX with your version)
   - Add: `C:\Users\DELL\AppData\Local\Programs\Python\Python3XX\Scripts`
   - Click OK, restart Command Prompt

### Issue 2: "tkinter not found"

**Solution**:
- Reinstall Python from python.org
- During installation, click "Modify"
- Ensure "tcl/tk and IDLE" is checked
- Click "Install"

### Issue 3: Path with Spaces or Special Characters

**Solution**:
Always use quotes around paths:
```cmd
cd "C:\Users\DELL\Desktop\MAE 2026\Cah-main"
python main.py
```

### Issue 4: French Encoding Error

**Solution**:
Run with UTF-8 encoding:
```cmd
chcp 65001
python main.py
```

### Issue 5: "Access Denied" or Permission Error

**Solution**:
Run Command Prompt as Administrator:
1. Press Windows key
2. Type "cmd"
3. Right-click "Command Prompt"
4. Select "Run as administrator"

---

## 🚀 Create Windows Startup Script

Create a file called `start.bat` in the project directory:

```batch
@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   School Schedule Management System
echo ============================================
echo.

REM Create directories if they don't exist
if not exist "data" mkdir data
if not exist "logs" mkdir logs

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Starting application...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error message above
    pause
)
```

### How to Use start.bat:

1. Create the file `start.bat` in your project folder
2. Double-click `start.bat` to run the application
3. No need to open Command Prompt manually

---

## 📁 Verify Directory Structure

Your directory should look like this:

```
C:\Users\DELL\Desktop\MAE 2026\Cah-main\
├── main.py
├── requirements.txt
├── start.bat                  (create this)
│
├── core\
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── db_manager.py
│   └── theme_manager.py
│
├── ui\
│   ├── __init__.py
│   ├── home.py
│   ├── schadual.py
│   └── ...
│
├── services\
│   ├── __init__.py
│   ├── pdf_generator.py
│   └── ...
│
├── data\                      (create this)
│   └── cahier_texte.db        (will be auto-created)
│
└── logs\                      (create this)
    └── (log files)
```

---

## ✅ Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] Project downloaded and extracted
- [ ] `data\` directory created
- [ ] `logs\` directory created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No spaces in file names causing issues

---

## 🎯 First Run Instructions

1. **Open Command Prompt** in project directory:
   ```cmd
   cd "C:\Users\DELL\Desktop\MAE 2026\Cah-main"
   ```

2. **Create directories**:
   ```cmd
   mkdir data
   mkdir logs
   ```

3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run application**:
   ```cmd
   python main.py
   ```

5. **Login with default credentials**:
   - Username: `admin`
   - Password: `admin`

---

## 🔍 If Still Not Working

### Check These:

1. **Python Version**:
   ```cmd
   python --version
   ```
   Must be 3.8 or higher

2. **Pip Version**:
   ```cmd
   pip --version
   ```

3. **Check if tkinter is installed**:
   ```cmd
   python -c "import tkinter; print('tkinter OK')"
   ```

4. **Check project files**:
   ```cmd
   dir main.py
   dir core
   dir ui
   dir services
   ```

5. **View error details**:
   ```cmd
   python main.py > error.txt 2>&1
   type error.txt
   ```

---

## 📞 Common Error Messages and Solutions

| Error Message | Solution |
|--------------|----------|
| `Le chemin d'accès spécifié est introuvable` | Create `data\` and `logs\` directories |
| `python is not recognized` | Add Python to PATH |
| `No module named 'tkinter'` | Reinstall Python with tcl/tk |
| `No module named 'reportlab'` | Run `pip install -r requirements.txt` |
| `Access is denied` | Run as Administrator |
| `[WinError 3]` | Check path spelling and use quotes |

---

## 🎉 Success!

If the application starts successfully, you should see:
1. A window titled "School Schedule Management System"
2. A login screen with username and password fields
3. No error messages in the console

**Default Login**:
- Username: `admin`
- Password: `admin`

---

Need more help? Check the error messages in the Command Prompt window or create the `start.bat` file for easier troubleshooting.
