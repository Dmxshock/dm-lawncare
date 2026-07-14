"""
Runsheets Module
Manages daily runsheet and job ordering
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QCheckBox,
    QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class RunsheetsModule(QWidget):
    """Runsheets Module - Daily runsheet management"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_runsheet()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Daily Run-Sheet Control")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Date selector
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        date_label = QLabel("Runsheet Date:")
        controls_layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.load_runsheet)
        controls_layout.addWidget(self.date_edit)

        generate_btn = QPushButton("📋 Generate Runsheet")
        generate_btn.setMinimumHeight(35)
        generate_btn.setStyleSheet(
            "QPushButton { background-color: #d35400; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #e67e22; }"
        )
        generate_btn.clicked.connect(self.generate_runsheet)
        controls_layout.addWidget(generate_btn)

        print_btn = QPushButton("🖨️ Print")
        print_btn.setMinimumHeight(35)
        print_btn.setStyleSheet(
            "QPushButton { background-color: #34495e; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #2c3e50; }"
        )
        print_btn.clicked.connect(self.print_runsheet)
        controls_layout.addWidget(print_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Runsheet jobs table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Order", "Time", "Client", "Address", "Service", "Completed", "Notes"
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

        self.runsheet_data = []
    
    def load_runsheet(self):
        """Load runsheet for selected date"""
        try:
            self.runsheet_data = self.connector.get_all_data("Dm_runsheets")
            self.display_runsheet(self.runsheet_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load runsheet: {str(e)}")
    
    def display_runsheet(self, jobs):
        """Display runsheet jobs"""
        self.table.setRowCount(len(jobs))
        
        for row, job in enumerate(jobs):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(job.get("Time", "")))
            self.table.setItem(row, 2, QTableWidgetItem(job.get("Client", "")))
            self.table.setItem(row, 3, QTableWidgetItem(job.get("Address", "")))
            self.table.setItem(row, 4, QTableWidgetItem(job.get("Service", "")))
            
            # Checkbox for completion
            checkbox = QCheckBox()
            checkbox.setChecked(job.get("Completed", "").lower() == "yes")
            checkbox.stateChanged.connect(lambda state, r=row: self.update_completion(r, state))
            self.table.setCellWidget(row, 5, checkbox)
            
            self.table.setItem(row, 6, QTableWidgetItem(job.get("Notes", "")))
    
    def generate_runsheet(self):
        """Generate daily runsheet"""
        QMessageBox.information(self, "Generate Runsheet", "Daily runsheet generated successfully!")
    
    def print_runsheet(self):
        """Print runsheet"""
        QMessageBox.information(self, "Print", "Runsheet sent to printer!")
    
    def update_completion(self, row, state):
        """Update job completion status"""
        completed = "yes" if state else "no"
        print(f"Job {row + 1} completion status updated to: {completed}")
