# Chemical Equipment Parameter Visualizer

A modern hybrid web and desktop application for visualizing and analyzing chemical equipment parameters from CSV data.

## 🎯 Project Overview

This application provides a comprehensive solution for chemical equipment data management with professional visualization and analytics. Users can upload CSV files containing equipment data and access detailed insights through both web and desktop interfaces. The system features a Django REST API backend, React web frontend with modern UI, and PyQt5 desktop application with enhanced visualizations.

## ✨ Key Features

### 🚀 Core Functionality
- **CSV Upload**: Drag-and-drop CSV file upload with validation
- **Data Processing**: Automatic parsing and analysis with Pandas
- **Modern Visualizations**: Interactive charts and graphs
- **Analytics Dashboard**: Comprehensive statistics and insights
- **Data History**: Store and manage last 5 uploaded datasets
- **PDF Reports**: Generate detailed reports with charts

### 🎨 Enhanced UI/UX
- **Modern Design**: Professional gradient-based interfaces
- **Responsive Layout**: Works seamlessly on all screen sizes
- **Smooth Animations**: Micro-interactions and transitions
- **Consistent Branding**: Unified design across platforms
- **Intuitive Navigation**: User-friendly interface elements

### 🔧 Technical Features
- **Hybrid Architecture**: Single backend serving multiple frontends
- **REST API**: Comprehensive API with full CRUD operations
- **Authentication**: Simple API key-based security
- **Error Handling**: Robust error management and user feedback
- **Performance**: Optimized data loading and rendering

## 🛠️ Technology Stack

### Backend
- **Python Django 4.2.7**: Web framework and REST API
- **Django REST Framework**: API serialization and routing
- **Pandas 1.5.3**: Data processing and CSV handling
- **SQLite**: Database for storing datasets and equipment data
- **ReportLab**: Professional PDF report generation
- **Matplotlib**: Chart generation for desktop app

### Web Frontend
- **React.js**: Modern JavaScript framework
- **Chart.js**: Interactive data visualization
- **Axios**: HTTP client for API communication
- **CSS3**: Modern styling with CSS variables and animations
- **Responsive Design**: Mobile-first approach

### Desktop Frontend
- **PyQt5**: Cross-platform desktop application framework
- **Matplotlib**: High-quality data visualization
- **Requests**: HTTP client for API communication
- **Modern Styling**: Custom widget styling with gradients

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django backend
│   ├── backend/               # Django project settings
│   ├── equipment/             # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views with actions
│   │   ├── serializers.py     # Data serializers
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py           # Django admin interface
│   │   ├── authentication.py  # API authentication
│   │   └── utils.py           # PDF generation utilities
│   ├── manage.py              # Django management script
│   └── db.sqlite3            # SQLite database
├── web-frontend/              # React web application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── DatasetList.js
│   │   │   ├── DatasetDetail.js
│   │   │   ├── CSVUpload.js
│   │   │   └── Analytics.js
│   │   ├── services/          # API service layer
│   │   ├── App.js             # Main application component
│   │   └── App.css            # Modern CSS styling
│   └── package.json           # Node.js dependencies
├── desktop-frontend/          # PyQt5 desktop application
│   └── main.py                # Desktop application with modern UI
├── sample_equipment_data.csv  # Sample data for testing
├── requirements.txt           # Python dependencies
├── start.bat                 # Easy startup script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip (Python package manager)
- npm (Node.js package manager)

### 🎯 Easy Startup (Recommended)
```bash
# Run the startup script
start.bat
```

### 🔧 Manual Setup

#### Backend Setup
1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

#### Web Frontend Setup
1. **Navigate to web frontend:**
   ```bash
   cd web-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React server:**
   ```bash
   npm start
   ```

#### Desktop Application
```bash
cd desktop-frontend
python main.py
```

## 📱 Application Access

- **Backend API**: http://localhost:8000/api/
- **Web Frontend**: http://localhost:3000 (or next available port)
- **Desktop App**: Native application window

## 📊 CSV File Format

The application expects CSV files with these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Equipment Name | Equipment identifier | Pump A |
| Type | Equipment category | Pump |
| Flowrate | Flow rate value | 150.5 |
| Pressure | Pressure value | 2.3 |
| Temperature | Temperature value | 75.2 |

**Sample CSV:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,150.5,2.3,75.2
Heat Exchanger B,Heat Exchanger,89.3,1.8,120.5
Valve C,Valve,45.7,3.1,85.3
```

## 🎮 Usage Guide

### Web Application
1. **Upload Data**: Click "Upload CSV" and drag/drop or select a file
2. **View Datasets**: Browse uploaded datasets with modern card layout
3. **Analyze Data**: Click any dataset to see:
   - Interactive charts (pie charts, bar charts)
   - Summary statistics with cards
   - Detailed equipment table
   - Type distribution analysis
4. **Generate Reports**: Download PDF reports with embedded charts

### Desktop Application
1. **Launch**: Run the desktop application for native experience
2. **Navigate**: Use modern navigation with emoji icons
3. **Upload Data**: Use the "📁 Upload CSV" button
4. **View Analytics**: Switch between tabs for different views
5. **Export**: Generate PDF reports with professional charts

## 🔌 API Endpoints

### Datasets
- `GET /api/datasets/` - List datasets (limited to 5)
- `POST /api/datasets/upload_csv/` - Upload CSV file
- `GET /api/datasets/{id}/` - Get dataset details
- `GET /api/datasets/{id}/equipment/` - Get equipment for dataset
- `GET /api/datasets/{id}/summary/` - Get summary statistics
- `GET /api/datasets/{id}/generate_pdf_report/` - Generate PDF report
- `GET /api/datasets/{id}/generate_charts_pdf/` - Generate charts PDF

### Equipment & Analytics
- `GET /api/equipment/` - List equipment with filtering
- `GET /api/analytics/` - Global analytics overview

### Authentication
Include API key header for enhanced security:
```http
X-API-Key: demo-api-key-12345
```

## 🎨 UI/UX Features

### Web Application
- **Modern Header**: Gradient background with glassmorphism navigation
- **Card-Based Layout**: Hover animations and smooth transitions
- **Interactive Charts**: Beautiful visualizations with Chart.js
- **Responsive Design**: Mobile-first responsive layout
- **Loading States**: Animated spinners and skeleton screens
- **Error Handling**: User-friendly error messages with retry options

### Desktop Application
- **Modern Widgets**: Gradient buttons and styled components
- **Enhanced Charts**: Donut pie charts and colored bar charts
- **Professional Layout**: Clean navigation with emoji icons
- **Native Feel**: Platform-consistent UI elements
- **Large Window**: 1400x900 for optimal viewing

## 🔧 Configuration

### Backend Settings (`backend/backend/settings.py`)
- `DEBUG`: Development/production mode
- `ALLOWED_HOSTS`: Allowed hostnames
- `CORS_ALLOWED_ORIGINS`: Cross-origin settings
- `SIMPLE_API_KEY`: Authentication key
- File upload limits: 10MB max, CSV only

### File Upload
- **Maximum Size**: 10MB
- **Supported Formats**: CSV only
- **Required Columns**: Equipment Name, Type, Flowrate, Pressure, Temperature
- **Validation**: Automatic column validation and error reporting

## 📦 Sample Data

The included `sample_equipment_data.csv` contains 30 equipment records across 10 types:
- Pumps (3 items)
- Heat Exchangers (3 items)
- Valves (3 items)
- Compressors (3 items)
- Reactors (3 items)
- Filters (3 items)
- Tanks (3 items)
- Distillation Columns (3 items)
- Mixers (3 items)
- Dryers (3 items)

Realistic parameter values for testing all features.

## 🐛 Troubleshooting

### Common Issues & Solutions

**"Failed to fetch dataset details"**
- ✅ Fixed: Updated queryset method to allow detail views
- Clear browser cache (Ctrl+Shift+R)
- Restart Django server if needed

**CORS Errors**
- Verify CORS settings include your frontend port
- Restart Django server after changing settings
- Check browser console for specific errors

**File Upload Issues**
- Verify CSV format matches required columns
- Check file size (max 10MB)
- Ensure file is properly formatted CSV

**Desktop App Issues**
- Install PyQt5: `pip install PyQt5`
- Check if Django server is running
- Verify network connectivity to localhost:8000

### Debug Tips
- **Browser Console**: Check for JavaScript errors (F12 → Console)
- **Network Tab**: Inspect API requests and responses
- **Django Logs**: Monitor server output for errors
- **Direct API Testing**: Use curl or Postman to test endpoints

## 🚀 Deployment

### Backend Production
1. **Environment Variables**:
   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS=yourdomain.com
   export SECRET_KEY=your-secret-key
   ```

2. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Production Server**: Use Gunicorn or uWSGI

### Web Frontend Production
```bash
npm run build
# Deploy the build/ directory to web server
```

### Desktop Application
- Use PyInstaller to create executables
- Create installers for different platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Ensure code quality and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎯 Project Status: ✅ Complete

The Chemical Equipment Parameter Visualizer is fully functional with:
- ✅ All core features implemented
- ✅ Modern UI/UX design
- ✅ Both web and desktop frontends
- ✅ Comprehensive API
- ✅ PDF report generation
- ✅ Sample data and documentation
- ✅ Error handling and validation
- ✅ Production-ready codebase

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review API documentation at `/api/` endpoints
- Test with the provided sample data
- Ensure all prerequisites are installed
