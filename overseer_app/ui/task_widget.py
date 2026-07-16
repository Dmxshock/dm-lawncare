"""
TaskItemWidget - Interactive task row with an action button.
Refactored from app_gui.py TaskItemWidget class.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont


class TaskItemWidget(QWidget):
    """Interactive task row with an action button for the Task Board."""

    def __init__(self, task_text: str, button_text: str, callback, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel(task_text)
        self.label.setFont(QFont("Arial", 10))
        self.label.setStyleSheet("color: #1e293b;")

        self.btn = QPushButton(button_text)
        self.btn.setFixedSize(140, 26)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                border-radius: 3px;
                border: none;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.btn.clicked.connect(callback)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.btn)
