"""
OptionsWidget - Settings/color-customisation panel.
Allows the user to change 6 key UI colors, reset to defaults, and close.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QColorDialog
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

from .color_manager import ColorManager


# Human-readable labels for each color key
_COLOR_LABELS = {
    "header_bg":        "Header Background",
    "sidebar_bg":       "Sidebar Background",
    "accent_primary":   "Primary Accent (Buttons / Highlights)",
    "card_border":      "Dashboard Card Border",
    "taskboard_accent": "Task Board Accent",
    "content_bg":       "Content Area Background",
}


class OptionsWidget(QWidget):
    """Settings panel with 6 color pickers, reset, and close."""

    def __init__(self, close_callback=None, parent=None):
        super().__init__(parent)
        self.color_manager = ColorManager()
        self.close_callback = close_callback
        self._pickers: dict[str, QPushButton] = {}
        self._build_ui()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 30, 30, 30)
        outer.setSpacing(20)

        # Title
        title = QLabel("⚙️  Overseer Settings — Colour Customisation")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e293b;")
        outer.addWidget(title)

        subtitle = QLabel("Click a colour swatch to change it. Changes are saved automatically.")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #64748b;")
        outer.addWidget(subtitle)

        # Color picker grid
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; }"
        )
        grid_layout = QGridLayout(card)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(14)

        for row, (key, label) in enumerate(_COLOR_LABELS.items()):
            lbl = QLabel(label)
            lbl.setFont(QFont("Arial", 10))
            lbl.setStyleSheet("border: none; color: #334155;")
            grid_layout.addWidget(lbl, row, 0)

            picker_btn = QPushButton()
            picker_btn.setFixedSize(120, 32)
            current_color = self.color_manager.get(key)
            self._apply_picker_style(picker_btn, current_color)
            picker_btn.clicked.connect(lambda _, k=key: self._pick_color(k))
            grid_layout.addWidget(picker_btn, row, 1, Qt.AlignmentFlag.AlignLeft)
            self._pickers[key] = picker_btn

        outer.addWidget(card)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        reset_btn = QPushButton("↺  Reset to Defaults")
        reset_btn.setMinimumHeight(38)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        reset_btn.clicked.connect(self._reset_defaults)
        btn_row.addWidget(reset_btn)

        close_btn = QPushButton("✕  Close Settings")
        close_btn.setMinimumHeight(38)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #2c3e50; }
        """)
        close_btn.clicked.connect(self._close_settings)
        btn_row.addWidget(close_btn)

        btn_row.addStretch()
        outer.addLayout(btn_row)
        outer.addStretch()

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------

    def _pick_color(self, key: str) -> None:
        """Open a colour dialog and save the chosen colour."""
        current = self.color_manager.get(key)
        color = QColorDialog.getColor(QColor(current), self, f"Choose colour — {_COLOR_LABELS[key]}")
        if color.isValid():
            hex_val = color.name()
            self.color_manager.set(key, hex_val)
            self._apply_picker_style(self._pickers[key], hex_val)

    def _reset_defaults(self) -> None:
        """Restore factory defaults and refresh all swatches."""
        self.color_manager.reset_to_defaults()
        for key, btn in self._pickers.items():
            self._apply_picker_style(btn, self.color_manager.get(key))

    def _close_settings(self) -> None:
        """Invoke the close callback (provided by the main window)."""
        if self.close_callback:
            self.close_callback()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_picker_style(btn: QPushButton, hex_color: str) -> None:
        """Style *btn* as a solid colour swatch with a contrasting label."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            text_color = "#000000" if luminance > 128 else "#ffffff"
        except Exception:
            text_color = "#ffffff"

        btn.setText(hex_color.upper())
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                color: {text_color};
                font-weight: bold;
                border: 1px solid #94a3b8;
                border-radius: 4px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                border: 2px solid #1e293b;
            }}
        """)
