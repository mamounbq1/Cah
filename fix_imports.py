#!/usr/bin/env python3
"""
Script to fix imports in reorganized project
"""
import os
import re

# Mapping of old imports to new imports
IMPORT_MAPPINGS = {
    'from course_dist.db_manager import': 'from core.db_manager import',
    'from course_dist.constants import': 'from core.constants import',
    'from course_dist.course_distribution import': 'from services.course_distribution import',
    'from course_dist.pdf_generator import': 'from services.pdf_generator import',
    'from course_dist.SavedSchedulesFrame import': 'from ui.SavedSchedulesFrame import',
    'from course_dist.cahier_texte import': 'from ui.cahier_texte import',
    'from db_manager import': 'from core.db_manager import',
    'from constants import': 'from core.constants import',
    'from theme_manager import': 'from core.theme_manager import',
    'from config import': 'from core.config import',
    'from pdf_generator import': 'from services.pdf_generator import',
    'from course_distribution import': 'from services.course_distribution import',
    'import db_manager': 'from core import db_manager',
    'import constants': 'from core import constants',
    'import theme_manager': 'from core import theme_manager',
    'import config': 'from core import config',
}

def fix_file_imports(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        for old_import, new_import in IMPORT_MAPPINGS.items():
            content = content.replace(old_import, new_import)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error fixing {filepath}: {e}")
        return False

def main():
    """Main function"""
    print("Fixing imports in project files...")
    
    directories = ['ui', 'services', 'core']
    fixed_count = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    filepath = os.path.join(root, file)
                    if fix_file_imports(filepath):
                        fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
