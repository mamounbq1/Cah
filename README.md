# 🏫 Cahier de Texte - School Schedule Management System

## 📋 Project Overview

**Cahier de Texte** is a comprehensive desktop application designed for managing school schedules, teacher assignments, student absences, vacations, and course distributions. Built with Python 3 and Tkinter, it provides an intuitive interface for educational institutions.

### 🎯 Key Features

- 📅 **Schedule Management**: Create, edit, and manage weekly class schedules
- 👨‍🏫 **Teacher Portal**: Teacher login and assignment management
- 📊 **Course Distribution**: Automatic course distribution across weeks
- 🏖️ **Calendar Integration**: Manage vacations, holidays, and absences
- 📄 **PDF Export**: Generate professional PDF reports of schedules
- 📥 **Excel Import**: Import data from Excel spreadsheets
- 🎨 **Modern UI**: Clean, themed interface with French localization

---

## ⚠️ IMPORTANT NOTICE

**This project is currently under development and requires critical fixes before use.**

### 🚨 Known Issues

1. **Application won't start** - Missing `course_dist` package
2. **Security vulnerabilities** - Hardcoded credentials and plain-text passwords
3. **Database inconsistencies** - Missing columns and constraints
4. Several other bugs documented in analysis files

**Please review the analysis documents before using this application.**

---

## 📚 Documentation Files

This repository includes comprehensive analysis and fixing documentation:

### 📊 Analysis Documents

1. **`PROJECT_ANALYSIS.md`** (19 KB)
   - Complete bug analysis with 10 critical/major issues
   - 15+ improvement recommendations
   - Security vulnerability assessment
   - Code quality analysis
   - Performance optimization suggestions

2. **`PROJECT_SUMMARY.md`** (11 KB)
   - Executive summary and key findings
   - Architecture overview and component breakdown
   - Database schema documentation
   - Bug summary by severity
   - Improvement priority matrix
   - Code metrics and complexity analysis
   - Deployment readiness assessment

3. **`QUICK_FIX_GUIDE.md`** (10 KB)
   - Step-by-step fixes for critical issues
   - Code examples for each fix
   - Testing checklist
   - Emergency rollback procedures
   - Quick reference for developers

4. **`FIXING_CHECKLIST.md`** (14 KB)
   - Comprehensive checkbox-based fixing guide
   - 6 phases with time estimates
   - Progress tracking section
   - Definition of done criteria
   - Notes section for tracking work

### 📝 Quick Start

For developers fixing the application:

```bash
# 1. Read the analysis first
cat PROJECT_SUMMARY.md

# 2. Follow the quick fix guide
cat QUICK_FIX_GUIDE.md

# 3. Use the checklist while working
open FIXING_CHECKLIST.md

# 4. Refer to detailed analysis as needed
cat PROJECT_ANALYSIS.md
```

---

## 🚀 Installation (After Fixes)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite3 (usually included with Python)

### Setup Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd webapp

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python3 -c "from db_manager import DatabaseManager; db = DatabaseManager()"

# 5. Run the application
python3 main.py
```

### First-Time Login

**Default credentials**:
- Username: `admin`
- Password: `admin`

⚠️ **Important**: Change the default password immediately after first login!

---

## 📦 Dependencies

```txt
Python >= 3.8
tkinter (usually built-in)
reportlab >= 3.6.0
pandas >= 1.5.0
tkcalendar >= 1.6.0
pillow >= 9.0.0
openpyxl >= 3.0.0
```

See `requirements.txt` for complete list.

---

## 🏗️ Project Structure

```
webapp/
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
│
├── 📊 Analysis Documents
│   ├── PROJECT_ANALYSIS.md    # Comprehensive bug analysis
│   ├── PROJECT_SUMMARY.md     # Executive summary
│   ├── QUICK_FIX_GUIDE.md     # Quick fix instructions
│   └── FIXING_CHECKLIST.md    # Fixing checklist
│
├── 🎨 UI Components
│   ├── home.py                # Login and home screens
│   ├── schadual.py            # Schedule management
│   ├── cahier_texte.py        # Textbook/course tracking
│   ├── theme_manager.py       # UI theme management
│   └── top_frame.py           # Top navigation
│
├── 🗄️ Database
│   ├── db_manager.py          # Database operations
│   └── data/
│       └── cahier_texte.db    # SQLite database
│
├── 🔧 Services
│   ├── course_distribution.py # Course distribution logic
│   ├── pdf_generator.py       # PDF generation
│   ├── import_excel.py        # Excel import functionality
│   └── constants.py           # Application constants
│
├── 📅 Calendar Features
│   ├── vacances.py            # Vacation management
│   ├── holiday.py             # Holiday management
│   └── absences.py            # Absence tracking
│
└── 📝 Logs
    └── logs/                  # Application logs
```

---

## 🐛 Bug Reporting

### Known Issues

**Critical (Blocking)**:
1. Missing `course_dist` package prevents application startup
2. Hardcoded authentication credentials
3. Missing database columns

**High Priority**:
4. Database path inconsistencies
5. Incorrect schedule row calculations
6. SQL injection vulnerabilities in some queries

**Medium Priority**:
7. Duplicate dictionary keys
8. Incomplete error handling
9. No input validation

For complete bug list, see `PROJECT_ANALYSIS.md`

### Reporting New Issues

When reporting bugs, please include:

1. **Description**: What went wrong?
2. **Steps to Reproduce**: How to recreate the issue?
3. **Expected Behavior**: What should happen?
4. **Actual Behavior**: What actually happened?
5. **Environment**: OS, Python version, etc.
6. **Logs**: Relevant log entries from `logs/` directory

---

## 🔐 Security Considerations

### Current Security Issues

⚠️ **WARNING**: This application has known security vulnerabilities:

1. **Hardcoded Credentials**: Authentication is currently bypassed
2. **Plain-Text Passwords**: Passwords stored without hashing
3. **Limited Input Validation**: Potential for SQL injection
4. **No Role-Based Access**: Single admin user only

**DO NOT use in production until these issues are resolved!**

### Security Roadmap

- [ ] Implement password hashing (bcrypt/argon2)
- [ ] Remove hardcoded credentials
- [ ] Add comprehensive input validation
- [ ] Implement role-based access control (RBAC)
- [ ] Add session management
- [ ] Implement audit logging
- [ ] Add data encryption for sensitive fields

See `PROJECT_ANALYSIS.md` Section "Security Recommendations" for details.

---

## 🧪 Testing

### Current Status

❌ **No automated tests currently exist**

### Testing Roadmap

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **UI Tests**: Test user interface workflows
4. **Performance Tests**: Test with large datasets
5. **Security Tests**: Penetration testing

### Manual Testing

See `FIXING_CHECKLIST.md` Phase 5 for comprehensive manual testing checklist.

---

## 📈 Roadmap

### Phase 1: Emergency Fixes (Week 1)
- [ ] Fix import errors
- [ ] Remove security vulnerabilities
- [ ] Add missing database elements
- [ ] Standardize database paths

### Phase 2: Stabilization (Week 2-3)
- [ ] Comprehensive error handling
- [ ] Input validation
- [ ] Database backup functionality
- [ ] Fix all high-priority bugs

### Phase 3: Security & Polish (Week 3-4)
- [ ] Password hashing
- [ ] User roles and permissions
- [ ] UI/UX improvements
- [ ] Performance optimization

### Phase 4: Testing & Deployment (Week 5-6)
- [ ] Comprehensive testing
- [ ] Load testing
- [ ] Security audit
- [ ] Deployment preparation
- [ ] User documentation

---

## 🤝 Contributing

### Development Workflow

1. **Read Documentation**: Start with analysis documents
2. **Follow Checklist**: Use `FIXING_CHECKLIST.md`
3. **Test Thoroughly**: Manual and automated testing
4. **Document Changes**: Update relevant documentation
5. **Commit Often**: Small, focused commits

### Code Standards

- Follow PEP 8 style guide
- Add type hints to functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation

### Git Workflow

```bash
# Create feature branch
git checkout -b fix/issue-name

# Make changes
# Test changes
# Commit changes
git commit -m "Fix: Description of fix"

# Push changes
git push origin fix/issue-name

# Create pull request
```

---

## 📞 Support & Contact

### Getting Help

1. **Documentation**: Check analysis documents first
2. **Logs**: Review `logs/` directory for errors
3. **Issues**: Search existing issues before creating new ones
4. **Discussion**: Use project discussions for questions

### Useful Resources

- **Python Documentation**: https://docs.python.org/3/
- **Tkinter Tutorial**: https://docs.python.org/3/library/tkinter.html
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **ReportLab User Guide**: https://www.reportlab.com/docs/reportlab-userguide.pdf

---

## 📄 License

[Add license information here]

---

## 🙏 Acknowledgments

- Built with Python and Tkinter
- PDF generation powered by ReportLab
- Calendar widgets by tkcalendar
- Data processing with pandas

---

## 📊 Project Stats

- **Total Python Files**: 29
- **Total Lines of Code**: ~8,500
- **Database Tables**: 14
- **Test Coverage**: 0% (to be improved)
- **Documentation**: Comprehensive analysis completed

---

## 🔄 Version History

### Version 1.0 (Current - Under Development)
- Initial codebase
- Comprehensive bug analysis completed
- Documentation created
- ⚠️ Not production-ready

### Planned Releases
- **v1.1**: Critical bug fixes
- **v1.2**: Security improvements
- **v1.3**: Stabilization and testing
- **v2.0**: Production-ready release

---

## 🎯 Quick Links

- 📊 [Full Bug Analysis](PROJECT_ANALYSIS.md)
- 📝 [Executive Summary](PROJECT_SUMMARY.md)
- 🔧 [Quick Fix Guide](QUICK_FIX_GUIDE.md)
- ✅ [Fixing Checklist](FIXING_CHECKLIST.md)

---

**Last Updated**: 2025-11-15  
**Status**: Under Development - Not Production Ready  
**Maintainer**: [Your Name/Team]  
**Analysis By**: Claude AI Code Assistant
