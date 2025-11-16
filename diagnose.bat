@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   System Diagnostics
echo ============================================
echo.

echo [1/8] Checking current directory...
cd
echo.

echo [2/8] Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo SOLUTION: Install Python from https://www.python.org/downloads/
) else (
    echo OK: Python is installed
)
echo.

echo [3/8] Checking pip installation...
pip --version 2>nul
if %errorlevel% neq 0 (
    echo WARNING: pip not found
    echo SOLUTION: Reinstall Python with pip enabled
) else (
    echo OK: pip is installed
)
echo.

echo [4/8] Checking tkinter...
python -c "import tkinter; print('OK: tkinter is installed')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: tkinter not found
    echo SOLUTION: Reinstall Python and check "tcl/tk and IDLE"
)
echo.

echo [5/8] Checking project files...
if exist "main.py" (
    echo OK: main.py found
) else (
    echo ERROR: main.py not found
)

if exist "core" (
    echo OK: core directory found
) else (
    echo ERROR: core directory not found
)

if exist "ui" (
    echo OK: ui directory found
) else (
    echo ERROR: ui directory not found
)

if exist "services" (
    echo OK: services directory found
) else (
    echo ERROR: services directory not found
)
echo.

echo [6/8] Checking/Creating data directory...
if not exist "data" (
    echo Creating data directory...
    mkdir data
    echo OK: data directory created
) else (
    echo OK: data directory exists
)
echo.

echo [7/8] Checking/Creating logs directory...
if not exist "logs" (
    echo Creating logs directory...
    mkdir logs
    echo OK: logs directory created
) else (
    echo OK: logs directory exists
)
echo.

echo [8/8] Checking Python dependencies...
python -c "import reportlab; print('OK: reportlab installed')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: reportlab not installed
    echo SOLUTION: Run: pip install -r requirements.txt
)

python -c "import pandas; print('OK: pandas installed')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: pandas not installed
    echo SOLUTION: Run: pip install -r requirements.txt
)

python -c "import tkcalendar; print('OK: tkcalendar installed')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: tkcalendar not installed
    echo SOLUTION: Run: pip install -r requirements.txt
)

python -c "import openpyxl; print('OK: openpyxl installed')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: openpyxl not installed
    echo SOLUTION: Run: pip install -r requirements.txt
)
echo.

echo ============================================
echo   Diagnostics Complete
echo ============================================
echo.
echo If any ERRORs were found above, fix them before running the application.
echo If WARNINGs about dependencies, run: pip install -r requirements.txt
echo.
echo To start the application, run: start.bat
echo Or run directly: python main.py
echo.
pause
