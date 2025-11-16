import os

# Get the base directory (webapp root)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Database path in data directory
DB_PATH = os.path.join(BASE_DIR, 'data', 'cahier_texte.db')
