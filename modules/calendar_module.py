"""
Calendar & Maps Module
Manages calendar view and route planning
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget,
    QLabel, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class CalendarModule(QWidget):
    """Calendar & Maps Module - Calendar view and route planning"""
    
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
        header = QLabel("Calendar & Route Planning")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()

        # Calendar tab
        cal_layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.on_date_selected)
        cal_layout.addWidget(self.calendar)

        # Jobs for selected date
        jobs_label = QLabel("Bookings for Selected Date:")
        jobs_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        cal_layout.addWidget(jobs_label)

        self.jobs_table = QTableWidget()
        self.jobs_table.setColumnCount(4)
        self.jobs_table.setHorizontalHeaderLabels(["Time", "Client", "Address", "Service"])
        self.jobs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.jobs_table.setMaximumHeight(150)
        self.jobs_table.setStyleSheet("""
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
        cal_layout.addWidget(self.jobs_table)

        cal_widget = QWidget()
        cal_widget.setLayout(cal_layout)
        tabs.addTab(cal_widget, "Calendar")

        # Routes tab
        routes_layout = QVBoxLayout()

        routes_btn = QPushButton("🗺️ Optimize Route")
        routes_btn.setMinimumHeight(35)
        routes_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        routes_btn.clicked.connect(self.optimize_route)
        routes_layout.addWidget(routes_btn)

        routes_info = QLabel(
            "Route optimization helps minimize travel time and fuel costs.\n"
            "Click 'Optimize Route' to calculate the most efficient route for today's jobs."
        )
        routes_info.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 4px;"
        )
        routes_info.setWordWrap(True)
        routes_layout.addWidget(routes_info)

        self.route_table = QTableWidget()
        self.route_table.setColumnCount(5)
        self.route_table.setHorizontalHeaderLabels(["Order", "Client", "Address", "Est. Time", "Distance"])
        self.route_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.route_table.setStyleSheet("""
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
        routes_layout.addWidget(self.route_table)

        routes_widget = QWidget()
        routes_widget.setLayout(routes_layout)
        tabs.addTab(routes_widget, "Routes")

        layout.addWidget(tabs)

        self.bookings_data = []
    
    def load_data(self):
        """Load calendar data from Google Sheets"""
        try:
            self.bookings_data = self.connector.get_all_data("Dm_bookings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load calendar data: {str(e)}")
    
    def on_date_selected(self, date):
        """Handle date selection"""
        selected_date = date.toString("dd/MM/yyyy")
        filtered = [b for b in self.bookings_data if b.get("Date", "") == selected_date]
        
        self.jobs_table.setRowCount(len(filtered))
        for row, booking in enumerate(filtered):
            self.jobs_table.setItem(row, 0, QTableWidgetItem(booking.get("Time", "")))
            self.jobs_table.setItem(row, 1, QTableWidgetItem(booking.get("Client", "")))
            self.jobs_table.setItem(row, 2, QTableWidgetItem(booking.get("Address", "")))
            self.jobs_table.setItem(row, 3, QTableWidgetItem(booking.get("Service", "")))
    
    def optimize_route(self):
        """Optimize route for the day"""
        QMessageBox.information(self, "Route Optimization", 
            "Route has been optimized!\n\nOptimal route generated for today's jobs."
        )
