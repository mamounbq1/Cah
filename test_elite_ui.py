#!/usr/bin/env python3
"""
Quick test script to view the Elite Enterprise Dashboard
"""
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.elite_theme import EliteTheme
from ui.elite_dashboard import EliteEnterpriseDashboard

def main():
    """Test the elite dashboard"""
    root = tk.Tk()
    root.title("Elite Enterprise Dashboard - Test")
    root.geometry("1400x900")
    
    # Setup elite theme
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('clam')
    EliteTheme.setup_styles(style)
    
    # Create dashboard
    dashboard = EliteEnterpriseDashboard(root, root)
    dashboard.pack(fill='both', expand=True)
    
    print("✅ Elite Dashboard loaded successfully!")
    print("🎨 Premium theme applied")
    print("📊 KPI widgets active")
    print("⚡ Quick actions ready")
    
    root.mainloop()

if __name__ == "__main__":
    main()
