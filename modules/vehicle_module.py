"""
Vehicle Module
Manages fuel logging, km tracking, and maintenance
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class VehicleModule(QWidget):
    """Vehicle Module - Vehicle and fuel tracking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Vehicle & KM Management")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Tab widget
        tabs = QTabWidget()

        # Fuel log tab
        fuel_layout = QVBoxLayout()
        fuel_controls = QHBoxLayout()
        
        fuel_btn = QPushButton("⛽ Log Fuel")
        fuel_btn.setMinimumHeight(35)
        fuel_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        fuel_btn.clicked.connect(self.log_fuel)
        fuel_controls.addWidget(fuel_btn)
        fuel_controls.addStretch()
        fuel_layout.addLayout(fuel_controls)

        self.fuel_table = QTableWidget()
        self.fuel_table.setColumnCount(5)
        self.fuel_table.setHorizontalHeaderLabels(["Date", "Liters", "Cost", "KM", "Notes"])
        self.fuel_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.fuel_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        fuel_layout.addWidget(self.fuel_table)
        fuel_widget = QWidget()
        fuel_widget.setLayout(fuel_layout)
        tabs.addTab(fuel_widget, "Fuel Log")

        # KM tracking tab
        km_layout = QVBoxLayout()
        km_controls = QHBoxLayout()
        
        km_btn = QPushButton("📍 Log KM")
        km_btn.setMinimumHeight(35)
        km_btn.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #2980b9; }"
        )
        km_btn.clicked.connect(self.log_km)
        km_controls.addWidget(km_btn)
        km_controls.addStretch()
        km_layout.addLayout(km_controls)

        self.km_table = QTableWidget()
        self.km_table.setColumnCount(4)
        self.km_table.setHorizontalHeaderLabels(["Date", "Start KM", "End KM", "Total KM"])
        self.km_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.km_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        km_layout.addWidget(self.km_table)
        km_widget = QWidget()
        km_widget.setLayout(km_layout)
        tabs.addTab(km_widget, "KM Tracking")

        # Maintenance tab
        maint_layout = QVBoxLayout()
        maint_controls = QHBoxLayout()
        
        maint_btn = QPushButton("🔧 Log Maintenance")
        maint_btn.setMinimumHeight(35)
        maint_btn.setStyleSheet(
            "QPushButton { background-color: #e74c3c; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #c0392b; }"
        )
        maint_btn.clicked.connect(self.log_maintenance)
        maint_controls.addWidget(maint_btn)
        maint_controls.addStretch()
        maint_layout.addLayout(maint_controls)

        self.maint_table = QTableWidget()
        self.maint_table.setColumnCount(5)
        self.maint_table.setHorizontalHeaderLabels(["Date", "Service", "Cost", "KM", "Next Due"])
        self.maint_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.maint_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        maint_layout.addWidget(self.maint_table)
        maint_widget = QWidget()
        maint_widget.setLayout(maint_layout)
        tabs.addTab(maint_widget, "Maintenance")

        layout.addWidget(tabs)

        self.fuel_data = []
        self.km_data = []
        self.maint_data = []
    
    def load_data(self):
        """Load vehicle data from Google Sheets"""
        try:
            self.fuel_data = self.connector.get_all_data("Dm_maps")
            self.display_fuel_log()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load vehicle data: {str(e)}")
    
    def display_fuel_log(self):
        """Display fuel log"""
        self.fuel_table.setRowCount(len(self.fuel_data))
        for row, entry in enumerate(self.fuel_data):
            self.fuel_table.setItem(row, 0, QTableWidgetItem(entry.get("Date", "")))
            self.fuel_table.setItem(row, 1, QTableWidgetItem(entry.get("Liters", "")))
            self.fuel_table.setItem(row, 2, QTableWidgetItem(entry.get("Cost", "")))
            self.fuel_table.setItem(row, 3, QTableWidgetItem(entry.get("KM", "")))
            self.fuel_table.setItem(row, 4, QTableWidgetItem(entry.get("Notes", "")))
    
    def log_fuel(self):
        """Log fuel entry"""
        QMessageBox.information(self, "Log Fuel", "Fuel entry form would open here.")
    
    def log_km(self):
        """Log KM entry"""
        QMessageBox.information(self, "Log KM", "KM entry form would open here.")
    
    def log_maintenance(self):
        """Log maintenance entry"""
        QMessageBox.information(self, "Log Maintenance", "Maintenance entry form would open here.")
