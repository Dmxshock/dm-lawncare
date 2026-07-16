"""
DashboardWidget - Metric card widget for the Home Dashboard.
Refactored from app_gui.py DashboardWidget class.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QFont


class DashboardWidget(QFrame):
    """Dynamic operational counter & data block card."""

    def __init__(self, title: str, content_lines: list, accent_color: str = "#27ae60", parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-left: 5px solid {accent_color};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #475569; border: none;")
        layout.addWidget(title_lbl)

        for line in content_lines:
            line_lbl = QLabel(line)
            line_lbl.setFont(QFont("Arial", 10))
            line_lbl.setStyleSheet("color: #1e293b; border: none;")
            line_lbl.setWordWrap(True)
            layout.addWidget(line_lbl)

        layout.addStretch()
