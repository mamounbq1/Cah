#!/bin/bash
# Startup script for School Schedule Management System

echo "===================================="
echo "School Schedule Management System"
echo "===================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if required packages are installed
echo ""
echo "Checking dependencies..."

python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: tkinter is not installed"
    echo "   Install with: sudo apt-get install python3-tk"
    exit 1
fi
echo "✓ tkinter installed"

python3 -c "import reportlab" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: reportlab not installed (required for PDF generation)"
    echo "   Install with: pip3 install reportlab"
fi

python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: pandas not installed (required for Excel import)"
    echo "   Install with: pip3 install pandas openpyxl"
fi

python3 -c "import tkcalendar" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: tkcalendar not installed (required for calendar features)"
    echo "   Install with: pip3 install tkcalendar"
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo ""
    echo "Creating data directory..."
    mkdir -p data
fi

# Check if logs directory exists
if [ ! -d "logs" ]; then
    echo "Creating logs directory..."
    mkdir -p logs
fi

echo ""
echo "===================================="
echo "Starting application..."
echo "===================================="
echo ""
echo "Default login credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "⚠️  Please change the default password after first login!"
echo ""

# Start the application
cd "$(dirname "$0")"
python3 main.py

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ Application exited with error code: $EXIT_CODE"
    echo "Check logs/error_*.log for details"
    exit $EXIT_CODE
fi
