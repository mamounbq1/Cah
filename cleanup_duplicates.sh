#!/bin/bash
# Script to remove duplicate and unnecessary files

cd /home/user/webapp

echo "============================================"
echo "FILE CLEANUP - Removing Duplicates"
echo "============================================"
echo ""

# Counter
removed=0

echo "📦 Removing CORE duplicates..."
for file in config.py constants.py db_manager.py theme_manager.py; do
    if [ -f "$file" ]; then
        echo "  ✓ Removing $file (exists in core/)"
        rm "$file"
        ((removed++))
    fi
done

echo ""
echo "🎨 Removing UI duplicates..."
for file in SavedSchedulesFrame.py cahier_texte.py home.py loading_window.py schadual.py schedule_grid.py tap_manager.py top_frame.py; do
    if [ -f "$file" ]; then
        echo "  ✓ Removing $file (exists in ui/)"
        rm "$file"
        ((removed++))
    fi
done

echo ""
echo "⚙️  Removing SERVICES duplicates..."
for file in absences.py add_entry.py classes.py course_distribution.py holiday.py import_excel.py modules.py pdf_generator.py vacances.py; do
    if [ -f "$file" ]; then
        echo "  ✓ Removing $file (exists in services/)"
        rm "$file"
        ((removed++))
    fi
done

echo ""
echo "🧪 Removing TEST files..."
for file in test.py test1.py test3.py cahier_texte2.py; do
    if [ -f "$file" ]; then
        echo "  ✓ Removing $file (old test file)"
        rm "$file"
        ((removed++))
    fi
done

echo ""
echo "📝 Removing OLD LOG files..."
for file in cahier_texte.log; do
    if [ -f "$file" ]; then
        echo "  ✓ Removing $file (old log file)"
        rm "$file"
        ((removed++))
    fi
done

echo ""
echo "============================================"
echo "CLEANUP COMPLETE"
echo "============================================"
echo "Files removed: $removed"
echo ""
echo "Files KEPT in root:"
echo "  ✓ main.py (entry point)"
echo "  ✓ run.sh (startup script)"
echo "  ✓ fix_imports.py (utility tool)"
echo "  ✓ requirements.txt (dependencies)"
echo "  ✓ *.md (documentation files)"
echo ""
echo "Organized structure:"
echo "  ✓ core/ - Core functionality"
echo "  ✓ ui/ - User interface"
echo "  ✓ services/ - Business logic"
echo "  ✓ data/ - Database"
echo "  ✓ logs/ - Application logs"
echo ""
