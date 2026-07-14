"""
Timesheets Module
Manages hours worked and wage calculations
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QSpinBox,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class TimesheetsModule(QWidget):
    """Timesheets Module - Hours and wage tracking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_timesheets()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Timesheets & Wages")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        new_entry_btn = QPushButton("➕ New Entry")
        new_entry_btn.setMinimumHeight(35)
        new_entry_btn.setStyleSheet(
            "QPushButton { background-color: #f39c12; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #e67e22; }"
        )
        new_entry_btn.clicked.connect(self.add_entry)
        controls_layout.addWidget(new_entry_btn)

        calculate_btn = QPushButton("🧮 Calculate Wages")
        calculate_btn.setMinimumHeight(35)
        calculate_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        calculate_btn.clicked.connect(self.calculate_wages)
        controls_layout.addWidget(calculate_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Timesheets table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Employee", "Date", "Hours", "Rate/Hour", "Total", "Notes", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
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
        layout.addWidget(self.table)

        self.timesheets_data = []
    
    def load_timesheets(self):
        """Load timesheets from Google Sheets"""
        try:
            self.timesheets_data = self.connector.get_all_data("Dm_timesheets")
            self.display_timesheets(self.timesheets_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load timesheets: {str(e)}")
    
    def display_timesheets(self, timesheets):
        """Display timesheets in table"""
        self.table.setRowCount(len(timesheets))
        
        for row, sheet in enumerate(timesheets):
            self.table.setItem(row, 0, QTableWidgetItem(sheet.get("Employee", "")))
            self.table.setItem(row, 1, QTableWidgetItem(sheet.get("Date", "")))
            self.table.setItem(row, 2, QTableWidgetItem(sheet.get("Hours", "")))
            self.table.setItem(row, 3, QTableWidgetItem(sheet.get("Rate", "")))
            
            # Calculate total
            try:
                hours = float(sheet.get("Hours", 0))
                rate = float(sheet.get("Rate", 0))
                total = hours * rate
                self.table.setItem(row, 4, QTableWidgetItem(f"${total:.2f}"))
            except:
                self.table.setItem(row, 4, QTableWidgetItem("$0.00"))
            
            self.table.setItem(row, 5, QTableWidgetItem(sheet.get("Notes", "")))
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(80)
            edit_btn.setStyleSheet(
                "QPushButton { background-color: #3498db; color: white; border: none; border-radius: 3px; }"
            )
            self.table.setCellWidget(row, 6, edit_btn)
    
    def add_entry(self):
        """Add new timesheet entry"""
        QMessageBox.information(self, "New Entry", "Timesheet entry form would open here.")
    
    def calculate_wages(self):
        """Calculate total wages"""
        total = 0
        for sheet in self.timesheets_data:
            try:
                hours = float(sheet.get("Hours", 0))
                rate = float(sheet.get("Rate", 0))
                total += hours * rate
            except:
                pass
        QMessageBox.information(self, "Total Wages", f"Total wages: ${total:.2f}")
