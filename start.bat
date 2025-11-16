@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   School Schedule Management System
echo ============================================
echo.

REM Create directories if they don't exist
if not exist "data" (
    echo Creating data directory...
    mkdir data
)

if not exist "logs" (
    echo Creating logs directory...
    mkdir logs
)

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo.
echo Checking required packages...
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: tkinter is not installed
    echo Please reinstall Python and ensure "tcl/tk and IDLE" is checked
    echo.
    pause
    exit /b 1
)

echo.
echo Verifying project structure...
if not exist "main.py" (
    echo ERROR: main.py not found
    echo Please ensure you are in the correct directory
    echo.
    pause
    exit /b 1
)

if not exist "core" (
    echo ERROR: core directory not found
    echo Please ensure all project files are extracted
    echo.
    pause
    exit /b 1
)

echo.
echo Starting application...
echo If this is your first run, the database will be created automatically.
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo   ERROR: Application failed to start
    echo ============================================
    echo.
    echo Check the error message above.
    echo.
    echo Common solutions:
    echo 1. Install dependencies: pip install -r requirements.txt
    echo 2. Check Python version: python --version (must be 3.8+)
    echo 3. Run as Administrator if you see permission errors
    echo.
    echo For detailed help, see WINDOWS_SETUP.md
    echo.
    pause
)
