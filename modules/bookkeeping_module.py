"""
Bookkeeping Module
Manages expenses and category tracking
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class BookkeepingModule(QWidget):
    """Bookkeeping Module - Expense tracking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_expenses()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Book Keeping & Expenses")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        add_btn = QPushButton("➕ Add Expense")
        add_btn.setMinimumHeight(35)
        add_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        add_btn.clicked.connect(self.add_expense)
        controls_layout.addWidget(add_btn)

        summary_btn = QPushButton("📊 Summary")
        summary_btn.setMinimumHeight(35)
        summary_btn.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #2980b9; }"
        )
        summary_btn.clicked.connect(self.show_summary)
        controls_layout.addWidget(summary_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Expenses table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Date", "Description", "Category", "Amount", "Tax", "Total"
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

        self.expenses_data = []
    
    def load_expenses(self):
        """Load expenses from Google Sheets"""
        try:
            self.expenses_data = self.connector.get_all_data("Dm_general_journals")
            # Filter for expenses only
            expenses = [e for e in self.expenses_data if e.get("Type", "").lower() == "expense"]
            self.display_expenses(expenses)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load expenses: {str(e)}")
    
    def display_expenses(self, expenses):
        """Display expenses in table"""
        self.table.setRowCount(len(expenses))
        
        for row, expense in enumerate(expenses):
            self.table.setItem(row, 0, QTableWidgetItem(expense.get("Date", "")))
            self.table.setItem(row, 1, QTableWidgetItem(expense.get("Description", "")))
            self.table.setItem(row, 2, QTableWidgetItem(expense.get("Category", "")))
            
            try:
                amount = float(expense.get("Amount", 0))
                tax = amount * 0.1  # 10% tax
                total = amount + tax
                self.table.setItem(row, 3, QTableWidgetItem(f"${amount:.2f}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"${tax:.2f}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"${total:.2f}"))
            except:
                pass
    
    def add_expense(self):
        """Add new expense"""
        QMessageBox.information(self, "New Expense", "Expense entry form would open here.")
    
    def show_summary(self):
        """Show expense summary"""
        total = 0
        by_category = {}
        
        for expense in self.expenses_data:
            if expense.get("Type", "").lower() == "expense":
                try:
                    amount = float(expense.get("Amount", 0))
                    total += amount
                    category = expense.get("Category", "Other")
                    by_category[category] = by_category.get(category, 0) + amount
                except:
                    pass
        
        summary_text = f"Total Expenses: ${total:.2f}\n\nBy Category:\n"
        for category, amount in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            summary_text += f"  {category}: ${amount:.2f}\n"
        
        QMessageBox.information(self, "Expense Summary", summary_text)
