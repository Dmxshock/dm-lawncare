"""
main.py — Entry point for Overseer APP.
Section 1: UI Shell

Run:
    python main.py
or on Windows:
    run_debug.bat
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import LawnCarePortal


def main():
    """Launch the Overseer APP."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = LawnCarePortal()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
