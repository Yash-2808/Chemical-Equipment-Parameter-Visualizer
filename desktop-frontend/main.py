import sys
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFileDialog,
    QMessageBox, QTabWidget, QComboBox, QTextEdit, QHeaderView,
    QSplitter, QFrame, QGridLayout, QScrollArea, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

# Modern color scheme
COLORS = {
    'primary': '#2563eb',
    'primary_dark': '#1e40af',
    'primary_light': '#3b82f6',
    'secondary': '#10b981',
    'accent': '#f59e0b',
    'danger': '#ef4444',
    'success': '#10b981',
    'warning': '#f59e0b',
    'info': '#06b6d4',
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_tertiary': '#f1f5f9',
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'text_muted': '#94a3b8',
    'border': '#e2e8f0',
    'border_light': '#f1f5f9',
    'shadow': 'rgba(0, 0, 0, 0.1)',
}

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def get_datasets(self):
        try:
            response = requests.get(f"{self.base_url}/datasets/")
            return response.json()
        except Exception as e:
            return None
    
    def get_dataset_detail(self, dataset_id):
        try:
            response = requests.get(f"{self.base_url}/datasets/{dataset_id}/")
            return response.json()
        except Exception as e:
            return None
    
    def get_dataset_equipment(self, dataset_id):
        try:
            response = requests.get(f"{self.base_url}/datasets/{dataset_id}/equipment/")
            return response.json()
        except Exception as e:
            return None
    
    def get_dataset_summary(self, dataset_id):
        try:
            response = requests.get(f"{self.base_url}/datasets/{dataset_id}/summary/")
            return response.json()
        except Exception as e:
            return None
    
    def upload_csv(self, file_path, dataset_name=None):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {}
                if dataset_name:
                    data['dataset_name'] = dataset_name
                
                response = requests.post(f"{self.base_url}/datasets/upload_csv/", 
                                       files=files, data=data)
                return response.json()
        except Exception as e:
            return None
    
    def get_analytics(self):
        try:
            response = requests.get(f"{self.base_url}/analytics/")
            return response.json()
        except Exception as e:
            return None

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)
        self.setParent(parent)
        
        # Modern styling for matplotlib
        fig.patch.set_facecolor('white')
        self.axes.set_facecolor('#f8fafc')
        self.axes.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_color('#e2e8f0')
        self.axes.spines['bottom'].set_color('#e2e8f0')

def apply_modern_style(widget):
    """Apply modern styling to widgets"""
    if isinstance(widget, QPushButton):
        widget.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {COLORS['primary_light']}, stop:1 {COLORS['primary']});
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: {COLORS['primary_dark']};
                transform: translateY(0px);
            }}
        """)
    elif isinstance(widget, QLabel):
        if widget.objectName() == 'title':
            widget.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_primary']};
                    font-size: 24px;
                    font-weight: 700;
                    padding: 16px 0px;
                }}
            """)
        elif widget.objectName() == 'subtitle':
            widget.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_secondary']};
                    font-size: 16px;
                    font-weight: 600;
                    padding: 8px 0px;
                }}
            """)
        else:
            widget.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_primary']};
                    font-size: 14px;
                    padding: 4px 0px;
                }}
            """)
    elif isinstance(widget, QTableWidget):
        widget.setStyleSheet(f"""
            QTableWidget {{
                background: {COLORS['bg_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                gridline-color: {COLORS['border_light']};
                selection-background-color: {COLORS['primary']};
                selection-color: white;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            QTableWidget::item:selected {{
                background: {COLORS['primary']};
                color: white;
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {COLORS['bg_secondary']}, stop:1 {COLORS['bg_tertiary']});
                color: {COLORS['text_primary']};
                padding: 12px;
                border: none;
                border-right: 1px solid {COLORS['border']};
                border-bottom: 1px solid {COLORS['border']};
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 12px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 12px;
                border-right: none;
            }}
        """)
    elif isinstance(widget, QFrame):
        if widget.objectName() == 'card':
            widget.setStyleSheet(f"""
                QFrame {{
                    background: {COLORS['bg_primary']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 16px;
                    padding: 16px;
                    margin: 8px;
                }}
            """)
        elif widget.objectName() == 'container':
            widget.setStyleSheet(f"""
                QFrame {{
                    background: {COLORS['bg_secondary']};
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 12px;
                    padding: 20px;
                    margin: 4px;
                }}
            """)

class DatasetListWidget(QWidget):
    dataset_selected = pyqtSignal(dict)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with modern styling
        header_frame = QFrame()
        header_frame.setObjectName('container')
        header_layout = QVBoxLayout()
        
        header = QLabel("Equipment Datasets")
        header.setObjectName('title')
        header_layout.addWidget(header)
        
        # Buttons with modern styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.upload_btn = QPushButton("📁 Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_datasets)
        
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()
        
        header_layout.addLayout(button_layout)
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # Table with modern styling
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "File", "Upload Date", "Equipment Count", "Avg Flowrate", "Avg Pressure"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        # Apply modern styling to all widgets
        apply_modern_style(header)
        apply_modern_style(self.upload_btn)
        apply_modern_style(self.refresh_btn)
        apply_modern_style(self.table)
        apply_modern_style(header_frame)
    
    def load_datasets(self):
        try:
            data = self.api_client.get_datasets()
            if data and 'results' in data:
                datasets = data['results']
            elif data:
                datasets = data
            else:
                datasets = []
            
            self.table.setRowCount(len(datasets))
            
            for row, dataset in enumerate(datasets):
                self.table.setItem(row, 0, QTableWidgetItem(dataset.get('name', '')))
                self.table.setItem(row, 1, QTableWidgetItem(dataset.get('file_name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(dataset.get('upload_date', '')))
                self.table.setItem(row, 3, QTableWidgetItem(str(dataset.get('equipment_count', dataset.get('total_count', 0)))))
                self.table.setItem(row, 4, QTableWidgetItem(f"{dataset.get('avg_flowrate', 0):.2f}" if dataset.get('avg_flowrate') else 'N/A'))
                self.table.setItem(row, 5, QTableWidgetItem(f"{dataset.get('avg_pressure', 0):.2f}" if dataset.get('avg_pressure') else 'N/A'))
                
                # Store dataset ID as hidden data
                self.table.item(row, 0).setData(Qt.UserRole, dataset['id'])
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load datasets: {str(e)}")
    
    def on_selection_changed(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            dataset_id = selected_items[0].data(Qt.UserRole)
            dataset_detail = self.api_client.get_dataset_detail(dataset_id)
            if dataset_detail:
                self.dataset_selected.emit(dataset_detail)
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                result = self.api_client.upload_csv(file_path)
                if result:
                    QMessageBox.information(self, "Success", "CSV uploaded successfully!")
                    self.load_datasets()
                else:
                    QMessageBox.warning(self, "Error", "Failed to upload CSV")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Upload failed: {str(e)}")

class DatasetDetailWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header with back button
        header_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back to Datasets")
        self.back_btn.clicked.connect(self.go_back)
        self.title_label = QLabel("Dataset Details")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Summary tab
        self.summary_widget = QWidget()
        self.summary_layout = QVBoxLayout()
        self.summary_widget.setLayout(self.summary_layout)
        self.tab_widget.addTab(self.summary_widget, "Summary")
        
        # Charts tab
        self.charts_widget = QWidget()
        self.charts_layout = QVBoxLayout()
        self.charts_widget.setLayout(self.charts_layout)
        self.tab_widget.addTab(self.charts_widget, "Charts")
        
        # Equipment table tab
        self.table_widget = QWidget()
        self.table_layout = QVBoxLayout()
        self.table_widget.setLayout(self.table_layout)
        self.tab_widget.addTab(self.table_widget, "Equipment Data")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_dataset(self, dataset):
        self.current_dataset = dataset
        self.title_label.setText(f"Dataset: {dataset.get('name', 'Unknown')}")
        
        # Load summary
        self.load_summary()
        
        # Load charts
        self.load_charts()
        
        # Load equipment table
        self.load_equipment_table()
    
    def load_summary(self):
        # Clear existing widgets
        for i in reversed(range(self.summary_layout.count())):
            child = self.summary_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Summary info
        summary_group = QFrame()
        summary_group.setFrameStyle(QFrame.Box)
        summary_layout = QVBoxLayout()
        
        summary_layout.addWidget(QLabel(f"<b>Name:</b> {self.current_dataset.get('name', 'N/A')}"))
        summary_layout.addWidget(QLabel(f"<b>Upload Date:</b> {self.current_dataset.get('upload_date', 'N/A')}"))
        summary_layout.addWidget(QLabel(f"<b>Total Equipment:</b> {self.current_dataset.get('total_count', 'N/A')}"))
        summary_layout.addWidget(QLabel(f"<b>Avg Flowrate:</b> {self.current_dataset.get('avg_flowrate', 'N/A')}"))
        summary_layout.addWidget(QLabel(f"<b>Avg Pressure:</b> {self.current_dataset.get('avg_pressure', 'N/A')}"))
        summary_layout.addWidget(QLabel(f"<b>Avg Temperature:</b> {self.current_dataset.get('avg_temperature', 'N/A')}"))
        
        summary_group.setLayout(summary_layout)
        self.summary_layout.addWidget(summary_group)
        
        # Type distribution
        if 'type_distribution' in self.current_dataset:
            type_dist_group = QFrame()
            type_dist_group.setFrameStyle(QFrame.Box)
            type_dist_layout = QVBoxLayout()
            type_dist_layout.addWidget(QLabel("<b>Equipment Type Distribution:</b>"))
            
            for eq_type, count in self.current_dataset['type_distribution'].items():
                type_dist_layout.addWidget(QLabel(f"  {eq_type}: {count}"))
            
            type_dist_group.setLayout(type_dist_layout)
            self.summary_layout.addWidget(type_dist_group)
    
    def load_charts(self):
        # Clear existing widgets
        for i in reversed(range(self.charts_layout.count())):
            child = self.charts_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get detailed summary for charts
        dataset_id = self.current_dataset['id']
        summary = self.api_client.get_dataset_summary(dataset_id)
        
        if summary and 'type_distribution' in summary:
            # Type distribution pie chart
            canvas1 = MatplotlibCanvas(self, width=6, height=5)
            types = list(summary['type_distribution'].keys())
            counts = list(summary['type_distribution'].values())
            
            # Modern color palette
            colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
                      '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16']
            
            wedges, texts, autotexts = canvas1.axes.pie(
                counts, labels=types, autopct='%1.1f%%', startangle=90,
                colors=colors[:len(types)], wedgeprops=dict(width=0.3),
                textprops=dict(fontsize=11, fontweight='500')
            )
            
            # Enhance text styling
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            canvas1.axes.set_title(f'Equipment Type Distribution - {dataset.name}', 
                                   fontsize=16, fontweight='600', color=COLORS['text_primary'], 
                                   pad=20)
            self.charts_layout.addWidget(canvas1)
            
            # Parameter comparison bar chart
            if 'statistics' in summary:
                canvas2 = MatplotlibCanvas(self, width=6, height=5)
                stats = summary['statistics']
                
                categories = ['Flowrate', 'Pressure', 'Temperature']
                averages = [stats['flowrate']['avg'], stats['pressure']['avg'], stats['temperature']['avg']]
                minimums = [stats['flowrate']['min'], stats['pressure']['min'], stats['temperature']['min']]
                maximums = [stats['flowrate']['max'], stats['pressure']['max'], stats['temperature']['max']]
                
                x = range(len(categories))
                width = 0.25
                
                # Modern colors for bars
                bar_colors = ['#ef4444', '#2563eb', '#10b981']
                
                canvas2.axes.bar([i - width for i in x], minimums, width, 
                                label='Minimum', color=bar_colors[0], alpha=0.8)
                canvas2.axes.bar(x, averages, width, 
                                label='Average', color=bar_colors[1], alpha=0.8)
                canvas2.axes.bar([i + width for i in x], maximums, width, 
                                label='Maximum', color=bar_colors[2], alpha=0.8)
                
                canvas2.axes.set_xlabel('Parameters', fontsize=12, fontweight='500', color=COLORS['text_primary'])
                canvas2.axes.set_ylabel('Values', fontsize=12, fontweight='500', color=COLORS['text_primary'])
                canvas2.axes.set_title('Parameter Comparison', fontsize=16, fontweight='600', 
                                       color=COLORS['text_primary'], pad=20)
                canvas2.axes.set_xticks(x)
                canvas2.axes.set_xticklabels(categories, fontsize=11)
                canvas2.axes.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
                
                self.charts_layout.addWidget(canvas2)
    
    def load_equipment_table(self):
        # Clear existing widgets
        for i in reversed(range(self.table_layout.count())):
            child = self.table_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get equipment data
        dataset_id = self.current_dataset['id']
        equipment_data = self.api_client.get_dataset_equipment(dataset_id)
        
        if equipment_data:
            if 'results' in equipment_data:
                equipment = equipment_data['results']
            else:
                equipment = equipment_data
            
            # Create table
            table = QTableWidget()
            table.setRowCount(len(equipment))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Name", "Type", "Flowrate", "Pressure", "Temperature"])
            
            for row, item in enumerate(equipment):
                table.setItem(row, 0, QTableWidgetItem(item.get('name', '')))
                table.setItem(row, 1, QTableWidgetItem(item.get('type', '')))
                table.setItem(row, 2, QTableWidgetItem(f"{item.get('flowrate', 0):.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"{item.get('pressure', 0):.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{item.get('temperature', 0):.2f}"))
            
            table.horizontalHeader().setStretchLastSection(True)
            table.resizeColumnsToContents()
            
            self.table_layout.addWidget(QLabel("Equipment Details:"))
            self.table_layout.addWidget(table)
    
    def go_back(self):
        # This will be handled by the main window
        self.parent().parent().show_dataset_list()

class AnalyticsWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_analytics()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Global Analytics")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(header)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Analytics")
        self.refresh_btn.clicked.connect(self.load_analytics)
        layout.addWidget(self.refresh_btn)
        
        # Content area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.content_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def load_analytics(self):
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        try:
            data = self.api_client.get_analytics()
            if not data:
                QMessageBox.warning(self, "Error", "Failed to load analytics")
                return
            
            # Overview cards
            overview_group = QFrame()
            overview_group.setFrameStyle(QFrame.Box)
            overview_layout = QGridLayout()
            
            overview_layout.addWidget(QLabel("<b>Total Datasets:</b>"), 0, 0)
            overview_layout.addWidget(QLabel(str(data.get('overview', {}).get('total_datasets', 0))), 0, 1)
            overview_layout.addWidget(QLabel("<b>Total Equipment:</b>"), 1, 0)
            overview_layout.addWidget(QLabel(str(data.get('overview', {}).get('total_equipment', 0))), 1, 1)

            overview_group.setLayout(overview_layout)
            self.content_layout.addWidget(overview_group)

            # Type distribution chart
            if 'overview' in data and 'type_distribution' in data['overview']:
                canvas = MatplotlibCanvas(self, width=6, height=4)
                types = list(data['overview']['type_distribution'].keys())
                counts = list(data['overview']['type_distribution'].values())

                # Modern color palette
                colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
                          '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16']

                wedges, texts, autotexts = canvas.axes.pie(
                    counts, labels=types, autopct='%1.1f%%', startangle=90,
                    colors=colors[:len(types)], wedgeprops=dict(width=0.3),
                    textprops=dict(fontsize=11, fontweight='500')
                )

                # Enhance text styling
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(10)

                canvas.axes.set_title('Overall Equipment Type Distribution', 
                                      fontsize=16, fontweight='600', color=COLORS['text_primary'], 
                                      pad=20)
                self.content_layout.addWidget(canvas)

            # Recent datasets
            if 'recent_datasets' in data:
                recent_group = QFrame()
                recent_group.setFrameStyle(QFrame.Box)
                recent_layout = QVBoxLayout()
                recent_layout.addWidget(QLabel("<b>Recent Datasets:</b>"))
                
                for dataset in data['recent_datasets']:
                    dataset_info = QLabel(f"• {dataset.get('name', 'N/A')} - {dataset.get('equipment_count', 0)} equipment")
                    recent_layout.addWidget(dataset_info)
                
                recent_group.setLayout(recent_layout)
                self.content_layout.addWidget(recent_group)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load analytics: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set modern application style
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {COLORS['bg_secondary']}, stop:1 {COLORS['bg_tertiary']});
            }}
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Navigation header
        nav_frame = QFrame()
        nav_frame.setObjectName('container')
        nav_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title)
        
        # Navigation buttons
        nav_button_layout = QHBoxLayout()
        nav_button_layout.setSpacing(15)
        
        self.dataset_list_btn = QPushButton("📊 Datasets")
        self.dataset_list_btn.clicked.connect(self.show_dataset_list)
        
        self.analytics_btn = QPushButton("📈 Analytics")
        self.analytics_btn.clicked.connect(self.show_analytics)
        
        nav_button_layout.addWidget(self.dataset_list_btn)
        nav_button_layout.addWidget(self.analytics_btn)
        nav_button_layout.addStretch()
        
        nav_layout.addLayout(nav_button_layout)
        nav_frame.setLayout(nav_layout)
        main_layout.addWidget(nav_frame)
        
        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background: {COLORS['bg_primary']};
                border-radius: 16px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        
        # Dataset list widget
        self.dataset_list_widget = DatasetListWidget(self.api_client)
        self.dataset_list_widget.dataset_selected.connect(self.show_dataset_detail)
        self.content_stack.addWidget(self.dataset_list_widget)
        
        # Dataset detail widget
        self.dataset_detail_widget = DatasetDetailWidget(self.api_client)
        self.content_stack.addWidget(self.dataset_detail_widget)
        
        # Analytics widget
        self.analytics_widget = AnalyticsWidget(self.api_client)
        self.content_stack.addWidget(self.analytics_widget)
        
        main_layout.addWidget(self.content_stack)
        central_widget.setLayout(main_layout)
        
        # Apply modern styling
        apply_modern_style(title)
        apply_modern_style(self.dataset_list_btn)
        apply_modern_style(self.analytics_btn)
        apply_modern_style(nav_frame)
        
        # Show dataset list by default
        self.show_dataset_list()
    
    def show_dataset_list(self):
        self.content_stack.setCurrentWidget(self.dataset_list_widget)
        self.dataset_list_widget.load_datasets()
    
    def show_dataset_detail(self, dataset):
        self.dataset_detail_widget.load_dataset(dataset)
        self.content_stack.setCurrentWidget(self.dataset_detail_widget)
    
    def show_analytics(self):
        self.analytics_widget.load_analytics()
        self.content_stack.setCurrentWidget(self.analytics_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
