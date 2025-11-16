import os
import sys

# Get the base directory (webapp root)
# This works for both regular execution and when frozen with PyInstaller
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR]:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")

# Database path in data directory
DB_PATH = os.path.join(DATA_DIR, 'cahier_texte.db')

# Print configuration on import (helpful for debugging)
if __name__ != '__main__':
    print(f"[Config] BASE_DIR: {BASE_DIR}")
    print(f"[Config] DATA_DIR: {DATA_DIR}")
    print(f"[Config] DB_PATH: {DB_PATH}")
