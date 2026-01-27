# Project Structure

This document outlines the organized structure of the Chemical Equipment Parameter Visualizer project.

## 📁 Root Directory Structure

```
chemical-equipment-parameter-visualizer/
├── 📄 README.md                 # Main project documentation
├── 📄 .gitignore               # Git ignore file
├── 📄 requirements.txt         # Python dependencies
├── 📁 backend/                 # Django REST API backend
├── 📁 web-frontend/            # React web application
├── 📁 desktop-frontend/        # PyQt5 desktop application
├── 📁 data/                   # Data files and datasets
├── 📁 docs/                   # Documentation
├── 📁 scripts/                 # Utility scripts
└── 📁 exports/                 # Generated exports (PDFs, etc.)
```

## 🔧 Backend Structure (`backend/`)

```
backend/
├── 📁 backend/                 # Django project settings
│   ├── 📄 __init__.py
│   ├── 📄 settings.py           # Django configuration
│   ├── 📄 urls.py              # URL routing
│   ├── 📄 wsgi.py              # WSGI configuration
│   └── 📄 asgi.py              # ASGI configuration
├── 📁 equipment/              # Main Django app
│   ├── 📄 __init__.py
│   ├── 📄 admin.py              # Django admin configuration
│   ├── 📄 apps.py              # App configuration
│   ├── 📄 models.py            # Database models
│   ├── 📄 serializers.py        # DRF serializers
│   ├── 📄 views.py              # API views
│   ├── 📄 urls.py              # App URL routing
│   ├── 📄 utils.py              # Utility functions
│   ├── 📄 authentication.py     # Authentication logic
│   ├── 📁 migrations/          # Database migrations
│   └── 📁 management/          # Django management commands
├── 📁 static/                  # Static files
├── 📁 media/                   # Media uploads
├── 📄 manage.py                # Django management script
└── 📄 db.sqlite3               # SQLite database (development)
```

## 🌐 Web Frontend Structure (`web-frontend/`)

```
web-frontend/
├── 📄 package.json             # Node.js dependencies
├── 📄 package-lock.json        # Dependency lock file
├── 📄 .gitignore              # Git ignore for frontend
├── 📄 README.md               # Frontend documentation
├── 📁 public/                 # Static assets
│   ├── 📄 index.html          # Main HTML template
│   ├── 📄 favicon.ico         # Favicon
│   ├── 📄 logo192.png         # Logo
│   ├── 📄 logo512.png         # Logo
│   └── 📄 manifest.json        # PWA manifest
├── 📁 src/                    # Source code
│   ├── 📄 index.js            # Application entry point
│   ├── 📄 App.js              # Main App component
│   ├── 📄 index.css           # Global styles
│   ├── 📁 components/         # React components
│   │   ├── 📄 DatasetList.js
│   │   ├── 📄 DatasetDetail.js
│   │   ├── 📄 CSVUpload.js
│   │   ├── 📄 Analytics.js
│   │   └── 📄 Login.js
│   ├── 📁 services/           # API services
│   │   └── 📄 api.js
│   └── 📁 styles/             # CSS stylesheets
│       └── 📄 App.css
└── 📁 build/                  # Production build output
```

## 🖥️ Desktop Frontend Structure (`desktop-frontend/`)

```
desktop-frontend/
├── 📄 main.py                 # Main application entry point
├── 📄 requirements.txt         # Python dependencies (if separate)
└── 📁 assets/                 # Desktop app assets (if any)
```

## 📊 Data Structure (`data/`)

```
data/
├── 📁 csv/                    # CSV dataset files
│   ├── 📄 sample_equipment_data.csv
│   ├── 📄 chemical_plant_alpha.csv
│   ├── 📄 industrial_pumps_data.csv
│   ├── 📄 petrochemical_complex.csv
│   ├── 📄 pharmaceutical_facility.csv
│   └── 📄 refinery_operations.csv
└── 📁 exports/                # Generated exports
    ├── 📄 *.pdf               # Generated PDF reports
    └── 📄 *.csv               # Exported data files
```

## 📚 Documentation Structure (`docs/`)

```
docs/
├── 📄 PROJECT_STRUCTURE.md     # This file
├── 📄 README.md               # Main documentation
├── 📄 test_report.pdf          # Sample generated report
├── 📁 api/                    # API documentation
├── 📁 deployment/             # Deployment guides
└── 📁 development/           # Development documentation
```

## 🔧 Scripts Structure (`scripts/`)

```
scripts/
├── 📄 start.bat               # Quick start script
├── 📄 setup.sh               # Environment setup (Linux/Mac)
└── 📄 deploy.sh              # Deployment script
```

## 🎯 File Organization Principles

1. **Separation of Concerns**: Each module has its own directory
2. **Logical Grouping**: Related files are grouped together
3. **Clear Naming**: Directory and file names are descriptive
4. **Scalability**: Structure supports future growth
5. **Documentation**: Each major component has documentation

## 📝 Notes

- The `exports/` directory is for generated content (PDFs, exported CSVs)
- Static files for production builds are handled by build processes
- Database files are excluded from version control
- Configuration files are kept at appropriate levels

This structure ensures maintainability, scalability, and clear organization for the entire project.
