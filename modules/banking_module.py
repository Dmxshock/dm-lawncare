"""
Banking Module
Manages financial transactions and account tracking
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from modules.sheets_connector import get_connector


class BankingModule(QWidget):
    """Banking Module - Financial transactions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = get_connector()
        self.init_ui()
        self.load_transactions()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Banking & Transactions")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b;")
        layout.addWidget(header)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        add_btn = QPushButton("➕ Add Transaction")
        add_btn.setMinimumHeight(35)
        add_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #219653; }"
        )
        add_btn.clicked.connect(self.add_transaction)
        controls_layout.addWidget(add_btn)

        type_label = QLabel("Type:")
        controls_layout.addWidget(type_label)
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Income", "Expense"])
        self.type_filter.currentTextChanged.connect(self.filter_transactions)
        controls_layout.addWidget(self.type_filter)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Summary cards
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)

        # Income card
        income_card = QLabel()
        income_card.setStyleSheet(
            "background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 4px;"
        )
        income_card.setText("💰 Total Income: Loading...")
        income_card.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.income_label = income_card
        summary_layout.addWidget(income_card)

        # Expense card
        expense_card = QLabel()
        expense_card.setStyleSheet(
            "background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 4px;"
        )
        expense_card.setText("📉 Total Expenses: Loading...")
        expense_card.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.expense_label = expense_card
        summary_layout.addWidget(expense_card)

        # Balance card
        balance_card = QLabel()
        balance_card.setStyleSheet(
            "background-color: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 4px;"
        )
        balance_card.setText("📊 Balance: Loading...")
        balance_card.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.balance_label = balance_card
        summary_layout.addWidget(balance_card)

        layout.addLayout(summary_layout)

        # Transactions table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Date", "Description", "Type", "Amount", "Category", "Actions"
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

        self.transactions_data = []
    
    def load_transactions(self):
        """Load transactions from Google Sheets"""
        try:
            self.transactions_data = self.connector.get_all_data("Dm_general_journals")
            self.update_summary()
            self.display_transactions(self.transactions_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load transactions: {str(e)}")
    
    def update_summary(self):
        """Update financial summary"""
        income = 0
        expenses = 0
        
        for trans in self.transactions_data:
            try:
                amount = float(trans.get("Amount", 0))
                if trans.get("Type", "").lower() == "income":
                    income += amount
                else:
                    expenses += amount
            except:
                pass
        
        balance = income - expenses
        self.income_label.setText(f"💰 Total Income: ${income:,.2f}")
        self.expense_label.setText(f"📉 Total Expenses: ${expenses:,.2f}")
        self.balance_label.setText(f"📊 Balance: ${balance:,.2f}")
    
    def display_transactions(self, transactions):
        """Display transactions in table"""
        self.table.setRowCount(len(transactions))
        
        for row, trans in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(trans.get("Date", "")))
            self.table.setItem(row, 1, QTableWidgetItem(trans.get("Description", "")))
            
            trans_type = trans.get("Type", "")
            type_item = QTableWidgetItem(trans_type)
            if trans_type.lower() == "income":
                type_item.setStyleSheet("background-color: #d4edda; color: #155724;")
            else:
                type_item.setStyleSheet("background-color: #f8d7da; color: #721c24;")
            self.table.setItem(row, 2, type_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(f"${trans.get('Amount', '')}" ))
            self.table.setItem(row, 4, QTableWidgetItem(trans.get("Category", "")))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet(
                "QPushButton { background-color: #e74c3c; color: white; border: none; border-radius: 3px; }"
            )
            self.table.setCellWidget(row, 5, delete_btn)
    
    def filter_transactions(self):
        """Filter transactions by type"""
        trans_type = self.type_filter.currentText()
        if trans_type == "All":
            self.display_transactions(self.transactions_data)
        else:
            filtered = [t for t in self.transactions_data if t.get("Type", "").lower() == trans_type.lower()]
            self.display_transactions(filtered)
    
    def add_transaction(self):
        """Add new transaction"""
        QMessageBox.information(self, "New Transaction", "Transaction form would open here.")
