"""
Invoices Module
Manages invoice generation, tracking, and payment status
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class InvoicesModule(QWidget):
    """Invoices Module - Manage invoices"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_invoices()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Invoice Management")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        create_btn = QPushButton("➕ Create Invoice")
        create_btn.setMinimumHeight(35)
        create_btn.setStyleSheet(
            "QPushButton { background-color: #8e44ad; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #7d3c98; }"
        )
        create_btn.clicked.connect(self.create_invoice)
        controls_layout.addWidget(create_btn)

        # Filter by status
        filter_label = QLabel("Filter:")
        controls_layout.addWidget(filter_label)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Paid", "Unpaid", "Overdue"])
        self.status_filter.currentTextChanged.connect(self.filter_invoices)
        controls_layout.addWidget(self.status_filter)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Invoices table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Invoice ID", "Client", "Amount", "Date", "Due Date", "Status", "Actions"
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

        self.invoices_data = []
    
    def load_invoices(self):
        """Load invoices from Google Sheets"""
        try:
            self.invoices_data = self.connector.get_all_data("Dm_invoices")
            self.display_invoices(self.invoices_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load invoices: {str(e)}")
    
    def display_invoices(self, invoices):
        """Display invoices in table"""
        self.table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(invoice.get("Invoice ID", "")))
            self.table.setItem(row, 1, QTableWidgetItem(invoice.get("Client", "")))
            self.table.setItem(row, 2, QTableWidgetItem(invoice.get("Amount", "")))
            self.table.setItem(row, 3, QTableWidgetItem(invoice.get("Date", "")))
            self.table.setItem(row, 4, QTableWidgetItem(invoice.get("Due Date", "")))
            
            status = invoice.get("Status", "")
            status_item = QTableWidgetItem(status)
            
            # Color code status
            if status.lower() == "paid":
                status_item.setStyleSheet("background-color: #d4edda; color: #155724;")
            elif status.lower() == "unpaid":
                status_item.setStyleSheet("background-color: #f8d7da; color: #721c24;")
            elif status.lower() == "overdue":
                status_item.setStyleSheet("background-color: #f5c6cb; color: #721c24; font-weight: bold;")
            
            self.table.setItem(row, 5, status_item)
            
            action_btn = QPushButton("View")
            action_btn.setMaximumWidth(80)
            action_btn.setStyleSheet(
                "QPushButton { background-color: #27ae60; color: white; border: none; border-radius: 3px; }"
            )
            action_btn.clicked.connect(lambda checked, r=row: self.view_invoice(r))
            self.table.setCellWidget(row, 6, action_btn)
    
    def filter_invoices(self):
        """Filter invoices by status"""
        status_filter = self.status_filter.currentText()
        if status_filter == "All":
            self.display_invoices(self.invoices_data)
        else:
            filtered = [i for i in self.invoices_data if i.get("Status", "").lower() == status_filter.lower()]
            self.display_invoices(filtered)
    
    def create_invoice(self):
        """Create new invoice"""
        QMessageBox.information(self, "New Invoice", "Invoice creation form would open here.")
    
    def view_invoice(self, row):
        """View invoice details"""
        if row < len(self.invoices_data):
            invoice = self.invoices_data[row]
            QMessageBox.information(self, "Invoice Details",
                f"Invoice ID: {invoice.get('Invoice ID', '')}\n"
                f"Client: {invoice.get('Client', '')}\n"
                f"Amount: ${invoice.get('Amount', '')}\n"
                f"Date: {invoice.get('Date', '')}\n"
                f"Due Date: {invoice.get('Due Date', '')}\n"
                f"Status: {invoice.get('Status', '')}"
            )
