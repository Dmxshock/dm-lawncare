"""
Inventory Module
Manages tools and stock levels
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class InventoryModule(QWidget):
    """Inventory Module - Tools and stock management"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_inventory()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Inventory & Tools")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        add_btn = QPushButton("➕ Add Item")
        add_btn.setMinimumHeight(35)
        add_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        add_btn.clicked.connect(self.add_item)
        controls_layout.addWidget(add_btn)

        low_stock_btn = QPushButton("⚠️ Low Stock")
        low_stock_btn.setMinimumHeight(35)
        low_stock_btn.setStyleSheet(
            "QPushButton { background-color: #e74c3c; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #c0392b; }"
        )
        low_stock_btn.clicked.connect(self.show_low_stock)
        controls_layout.addWidget(low_stock_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Inventory table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Item", "Category", "Quantity", "Min Level", "Status", "Actions"
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

        self.inventory_data = []
    
    def load_inventory(self):
        """Load inventory from Google Sheets"""
        try:
            self.inventory_data = self.connector.get_all_data("Dm_inventory")
            self.display_inventory(self.inventory_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load inventory: {str(e)}")
    
    def display_inventory(self, items):
        """Display inventory in table"""
        self.table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item.get("Item", "")))
            self.table.setItem(row, 1, QTableWidgetItem(item.get("Category", "")))
            
            qty = item.get("Quantity", "0")
            min_level = item.get("Min Level", "5")
            
            self.table.setItem(row, 2, QTableWidgetItem(qty))
            self.table.setItem(row, 3, QTableWidgetItem(min_level))
            
            # Status
            try:
                qty_int = int(qty)
                min_int = int(min_level)
                status_item = QTableWidgetItem()
                if qty_int < min_int:
                    status_item.setText("⚠️ Low Stock")
                    status_item.setStyleSheet("background-color: #f8d7da; color: #721c24;")
                else:
                    status_item.setText("✓ In Stock")
                    status_item.setStyleSheet("background-color: #d4edda; color: #155724;")
                self.table.setItem(row, 4, status_item)
            except:
                self.table.setItem(row, 4, QTableWidgetItem("N/A"))
            
            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(80)
            edit_btn.setStyleSheet(
                "QPushButton { background-color: #3498db; color: white; border: none; border-radius: 3px; }"
            )
            self.table.setCellWidget(row, 5, edit_btn)
    
    def add_item(self):
        """Add new inventory item"""
        QMessageBox.information(self, "New Item", "Item entry form would open here.")
    
    def show_low_stock(self):
        """Show low stock items"""
        low_stock = []
        for item in self.inventory_data:
            try:
                qty = int(item.get("Quantity", 0))
                min_level = int(item.get("Min Level", 5))
                if qty < min_level:
                    low_stock.append(f"• {item.get('Item', '')}: {qty} (Min: {min_level})")
            except:
                pass
        
        if low_stock:
            message = "Low Stock Items:\n" + "\n".join(low_stock)
        else:
            message = "All items have adequate stock!"
        
        QMessageBox.information(self, "Low Stock Alert", message)
