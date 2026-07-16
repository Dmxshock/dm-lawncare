"""
NavButton - Colored sidebar navigation button widget.
Refactored from app_gui.py NavButton class.
"""

from PyQt6.QtWidgets import QPushButton


class NavButton(QPushButton):
    """Custom navigation button for the colored left sidebar."""

    def __init__(self, text: str, color: str = "#27ae60", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(40)
        self.color = color
        self.update_style(False)

    def update_style(self, checked: bool) -> None:
        """Apply active or inactive stylesheet based on selection state."""
        if checked:
            self.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 10px;
                    border: none;
                    color: white;
                    background-color: {self.color};
                    font-weight: bold;
                    border-radius: 4px;
                    margin: 2px;
                    border: 2px solid white;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 10px;
                    border: none;
                    color: white;
                    background-color: {self.color};
                    font-weight: bold;
                    border-radius: 4px;
                    margin: 2px;
                }}
                QPushButton:hover {{
                    background-color: {self._brighten(self.color)};
                }}
            """)

    @staticmethod
    def _brighten(hex_color: str) -> str:
        """Return a slightly brighter version of *hex_color* for hover effect."""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            r = min(255, r + 25)
            g = min(255, g + 25)
            b = min(255, b + 25)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color
