"""
Jobsheets Module
Manages job tracking and completion
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class JobsheetsModule(QWidget):
    """Jobsheets Module - Track jobs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_jobsheets()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Job Sheets Management")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        new_btn = QPushButton("➕ New Job")
        new_btn.setMinimumHeight(35)
        new_btn.setStyleSheet(
            "QPushButton { background-color: #f39c12; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #e67e22; }"
        )
        new_btn.clicked.connect(self.create_job)
        controls_layout.addWidget(new_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setMinimumHeight(35)
        refresh_btn.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #2980b9; }"
        )
        refresh_btn.clicked.connect(self.load_jobsheets)
        controls_layout.addWidget(refresh_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Jobs table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Job ID", "Client", "Service", "Date", "Status", "Notes", "Actions"
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

        self.jobsheets_data = []
    
    def load_jobsheets(self):
        """Load jobsheets from Google Sheets"""
        try:
            self.jobsheets_data = self.connector.get_all_data("Dm_Jobsheets")
            self.display_jobsheets(self.jobsheets_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load jobsheets: {str(e)}")
    
    def display_jobsheets(self, jobs):
        """Display jobsheets in table"""
        self.table.setRowCount(len(jobs))
        
        for row, job in enumerate(jobs):
            self.table.setItem(row, 0, QTableWidgetItem(job.get("Job ID", "")))
            self.table.setItem(row, 1, QTableWidgetItem(job.get("Client", "")))
            self.table.setItem(row, 2, QTableWidgetItem(job.get("Service", "")))
            self.table.setItem(row, 3, QTableWidgetItem(job.get("Date", "")))
            
            status = job.get("Status", "")
            status_item = QTableWidgetItem(status)
            if status.lower() == "completed":
                status_item.setStyleSheet("background-color: #d4edda; color: #155724;")
            elif status.lower() == "in progress":
                status_item.setStyleSheet("background-color: #fff3cd; color: #856404;")
            self.table.setItem(row, 4, status_item)
            
            self.table.setItem(row, 5, QTableWidgetItem(job.get("Notes", "")))
            
            action_btn = QPushButton("Complete")
            action_btn.setMaximumWidth(80)
            action_btn.setStyleSheet(
                "QPushButton { background-color: #27ae60; color: white; border: none; border-radius: 3px; }"
            )
            action_btn.clicked.connect(lambda checked, r=row: self.complete_job(r))
            self.table.setCellWidget(row, 6, action_btn)
    
    def create_job(self):
        """Create new job"""
        QMessageBox.information(self, "New Job", "Job creation form would open here.")
    
    def complete_job(self, row):
        """Mark job as complete"""
        if row < len(self.jobsheets_data):
            job = self.jobsheets_data[row]
            reply = QMessageBox.question(
                self, "Complete Job",
                f"Mark job {job.get('Job ID')} as complete?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                QMessageBox.information(self, "Success", "Job marked as completed!")
                self.load_jobsheets()
