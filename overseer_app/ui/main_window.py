"""
main_window.py - LawnCarePortal main application window.
Section 1: UI Shell — header, sidebar, dashboard, settings panel.
Refactored from app_gui.py and enhanced with real-time clock, colour
management, and a modular file layout.
"""

import sys
import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel, QGridLayout, QFrame,
    QStackedWidget, QSizePolicy, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from .nav_button import NavButton
from .dashboard_widget import DashboardWidget
from .task_widget import TaskItemWidget
from .options import OptionsWidget
from .color_manager import ColorManager


# ---------------------------------------------------------------------------
# Tab metadata  (name, sheet_source, sidebar_colour)
# ---------------------------------------------------------------------------
TABS_META = [
    ("🏠 Dashboard",         "Local_Cache",              "#27ae60"),
    ("👥 Clients",           "Dm_client_accounts",       "#2980b9"),
    ("📄 Workbook",          "Dm_workbook",               "#2980b9"),
    ("📄 Quotes",            "Dm_quotes",                "#e67e22"),
    ("📅 Bookings",          "Dm_bookings",              "#e74c3c"),
    ("🗂️ Invoices",          "Dm_invoices",              "#3498db"),
    ("📊 Jobsheets",         "Dm_Jobsheets",             "#f39c12"),
    ("⏰ Timesheets",        "Dm_timesheets",            "#f1c40f"),
    ("🚗 Vehicle",           "Dm_vehicle",               "#e91e63"),
    ("🏦 Banking",           "Dm_banking",               "#3498db"),
    ("📚 Bookkeeping",       "Dm_book_keeping",          "#9b59b6"),
    ("🔧 Inventory",         "Dm_inventory",             "#1abc9c"),
    ("📅 Calendar",          "Dm_calendar",              "#2196f3"),
    ("✉️ Communications",    "Dm_emails",                "#27ae60"),
    ("🌐 Website",           "Dm_website",               "#ff9800"),
    ("📱 Mobile",            "Dm_mobile",                "#9c27b0"),
]


class LawnCarePortal(QMainWindow):
    """Main DmOverseer Application Window — Section 1 UI Shell."""

    def __init__(self):
        super().__init__()
        self.color_manager = ColorManager()

        self.setWindowTitle("⚙️  Overseer APP — DmLawnCare Portal")
        self.resize(1380, 900)

        # ------------------------------------------------------------------
        # Root widget
        # ------------------------------------------------------------------
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ------------------------------------------------------------------
        # Header bar (fixed top)
        # ------------------------------------------------------------------
        self.header_frame = self._build_header()
        root_layout.addWidget(self.header_frame)

        # ------------------------------------------------------------------
        # Main body: sidebar + content
        # ------------------------------------------------------------------
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Left sidebar
        self.sidebar = self._build_sidebar()
        body_layout.addWidget(self.sidebar)

        # Content area
        self.content_area = QWidget()
        self.content_area.setStyleSheet(
            f"background-color: {self.color_manager.get('content_bg')};"
        )
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        self.tab_stack = QStackedWidget()
        content_layout.addWidget(self.tab_stack)
        body_layout.addWidget(self.content_area)

        root_layout.addWidget(body)

        # ------------------------------------------------------------------
        # Build internal state then construct tab pages
        # ------------------------------------------------------------------
        self.btn_group: list[NavButton] = []
        self.options_index: int | None = None

        self._populate_sidebar_buttons()
        self._build_tab_pages()
        self._build_options_page()

        self.switch_tab(0)

        # ------------------------------------------------------------------
        # Real-time clock timer
        # ------------------------------------------------------------------
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)
        self._update_clock()

    # ======================================================================
    # Header
    # ======================================================================

    def _build_header(self) -> QFrame:
        """Create the fixed top header bar."""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(
            f"QFrame {{ background-color: {self.color_manager.get('header_bg')}; }}"
        )

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(20)

        # App title
        title_lbl = QLabel("⚙️  Overseer APP")
        title_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #ecf0f1; border: none;")
        layout.addWidget(title_lbl)

        layout.addStretch()

        # Date display
        self.date_lbl = QLabel()
        self.date_lbl.setFont(QFont("Arial", 10))
        self.date_lbl.setStyleSheet("color: #bdc3c7; border: none;")
        self._refresh_date()
        layout.addWidget(self.date_lbl)

        # Separator
        sep = QLabel("|")
        sep.setStyleSheet("color: #5d6d7e; border: none;")
        layout.addWidget(sep)

        # Clock
        self.clock_lbl = QLabel()
        self.clock_lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.clock_lbl.setFixedWidth(80)
        self.clock_lbl.setStyleSheet("color: #ecf0f1; border: none;")
        layout.addWidget(self.clock_lbl)

        # Separator
        sep2 = QLabel("|")
        sep2.setStyleSheet("color: #5d6d7e; border: none;")
        layout.addWidget(sep2)

        # Next alarm (fixed right)
        self.alarm_lbl = QLabel("🔔  Next alarm: 08:30 AM")
        self.alarm_lbl.setFont(QFont("Arial", 10))
        self.alarm_lbl.setStyleSheet("color: #f39c12; border: none;")
        layout.addWidget(self.alarm_lbl)

        return header

    # ======================================================================
    # Sidebar
    # ======================================================================

    def _build_sidebar(self) -> QFrame:
        """Create the fixed left sidebar frame (buttons added separately)."""
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(
            f"#Sidebar {{ background-color: {self.color_manager.get('sidebar_bg')}; }}"
        )

        # Wrap inside a scroll area so it degrades gracefully on small screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        self.sidebar_layout = QVBoxLayout(inner)
        self.sidebar_layout.setContentsMargins(0, 15, 0, 5)
        self.sidebar_layout.setSpacing(2)

        scroll.setWidget(inner)

        outer_layout = QVBoxLayout(sidebar)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(scroll)

        # Gear / Settings button pinned at the bottom of sidebar
        self.settings_btn = QPushButton("⚙️  Settings")
        self.settings_btn.setMinimumHeight(42)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                border: none;
                color: #ecf0f1;
                background-color: #1a252f;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #273746; }
        """)
        self.settings_btn.clicked.connect(self.show_options_page)
        outer_layout.addWidget(self.settings_btn)

        return sidebar

    def _populate_sidebar_buttons(self) -> None:
        """Add one NavButton per tab to the sidebar layout."""
        for index, (name, _, color) in enumerate(TABS_META):
            btn = NavButton(name, color)
            btn.clicked.connect(lambda _checked, idx=index: self.switch_tab(idx))
            self.sidebar_layout.addWidget(btn)
            self.btn_group.append(btn)

        self.sidebar_layout.addStretch()

    # ======================================================================
    # Tab pages
    # ======================================================================

    def _build_tab_pages(self) -> None:
        """Build all 16 tab pages and add them to the stack."""
        # TAB 0: Dashboard (full home view)
        self.tab_stack.addWidget(self._build_dashboard_tab())

        # TABs 1-15: placeholder pages (populated in future sections)
        placeholder_labels = [name for name, _, _ in TABS_META[1:]]
        for name in placeholder_labels:
            self.tab_stack.addWidget(self._make_placeholder(name))

    def _build_dashboard_tab(self) -> QWidget:
        """Build the full Dashboard / Home tab."""
        tab = QWidget()
        tab.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Section heading
        heading = QLabel("DmOverseer — Business Management Command Centre")
        heading.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        heading.setStyleSheet("color: #1e293b; padding-bottom: 4px;")
        layout.addWidget(heading)

        # ---- Metrics row (4 cards) ----------------------------------------
        metrics_scroll = QScrollArea()
        metrics_scroll.setWidgetResizable(True)
        metrics_scroll.setFixedHeight(185)
        metrics_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        metrics_content = QWidget()
        metrics_grid = QGridLayout(metrics_content)
        metrics_grid.setSpacing(15)
        metrics_grid.setContentsMargins(0, 0, 5, 0)

        metrics_grid.addWidget(DashboardWidget(
            title="👥 Client Accounts",
            content_lines=[
                "• <b>New Clients:</b> 3 Action Required",
                "• <b>Total Clients:</b> 142 Accounts Logged",
            ],
            accent_color="#2980b9",
        ), 0, 0)

        metrics_grid.addWidget(DashboardWidget(
            title="📄 Quotes Pipeline",
            content_lines=[
                "• <b>Total Quotes Generated:</b> 18",
                "• <b>Ready to Accept/Book:</b> 4 Confirmed",
            ],
            accent_color="#e67e22",
        ), 0, 1)

        metrics_grid.addWidget(DashboardWidget(
            title="📅 Next Scheduled Booking",
            content_lines=[
                "• <b>Tomorrow 8:30 AM:</b> J. Smith",
                "• <b>Location:</b> 24 Harrison St, Frankston",
            ],
            accent_color="#27ae60",
        ), 0, 2)

        metrics_grid.addWidget(DashboardWidget(
            title="💰 Invoice Summary",
            content_lines=[
                "• <b>Generated:</b> 89  |  • <b>Paid:</b> 74",
                "• <b>Unpaid (A/R):</b> 15 Outstanding",
            ],
            accent_color="#8e44ad",
        ), 0, 3)

        metrics_scroll.setWidget(metrics_content)
        layout.addWidget(metrics_scroll)

        # ---- Bottom split: runsheet + task board --------------------------
        bottom_split = QHBoxLayout()
        bottom_split.setSpacing(15)

        # Runsheet card
        runsheet_card = QFrame()
        runsheet_card.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; "
            "border-left: 5px solid #d35400; border-radius: 6px; }"
        )
        rs_layout = QVBoxLayout(runsheet_card)
        rs_layout.setContentsMargins(15, 15, 15, 15)
        rs_layout.setSpacing(8)

        rs_title = QLabel("📋 Daily Run-Sheet Control")
        rs_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        rs_title.setStyleSheet("color: #475569; border: none;")
        rs_layout.addWidget(rs_title)

        rs_info = QLabel(
            "• <b>Next Run:</b> 09/07/2026<br/>"
            "• <b>Jobs Scheduled:</b> 5 Allocated Runs<br/><br/>"
            "<i>Tracks: Journeys, timesheets, vehicles, expenses, "
            "and updates journal automatically.</i>"
        )
        rs_info.setFont(QFont("Arial", 10))
        rs_info.setStyleSheet("color: #1e293b; border: none;")
        rs_info.setWordWrap(True)
        rs_layout.addWidget(rs_info)

        gen_rs_btn = QPushButton("Generate Daily Runsheet Fields")
        gen_rs_btn.setMinimumHeight(35)
        gen_rs_btn.setStyleSheet(
            "QPushButton { background-color: #d35400; color: white; font-weight: bold; "
            "border: none; border-radius: 4px; } "
            "QPushButton:hover { background-color: #e67e22; }"
        )
        gen_rs_btn.clicked.connect(self._trigger_runsheet_pipeline)
        rs_layout.addWidget(gen_rs_btn)
        rs_layout.addStretch()

        bottom_split.addWidget(runsheet_card, 1)

        # Task board card
        task_card = QFrame()
        task_card.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; "
            "border-left: 5px solid #f1c40f; border-radius: 6px; }"
        )
        task_layout = QVBoxLayout(task_card)
        task_layout.setContentsMargins(15, 15, 15, 15)
        task_layout.setSpacing(8)

        task_title = QLabel("⚠️ Overseer Action & Task Board")
        task_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        task_title.setStyleSheet("color: #475569; border: none;")
        task_layout.addWidget(task_title)

        task_sub = QLabel(
            "Items requiring manually initiated template reminders or job validation checks:"
        )
        task_sub.setFont(QFont("Arial", 9))
        task_sub.setStyleSheet("color: #64748b; border: none;")
        task_layout.addWidget(task_sub)

        self.task_list_widget = QListWidget()
        self.task_list_widget.setStyleSheet(
            "QListWidget { border: 1px solid #e2e8f0; border-radius: 4px; background: #f8fafc; }"
        )
        task_layout.addWidget(self.task_list_widget)

        # Seed initial task items
        self._add_task(
            "M. Lawson (Completed 3 weeks ago) - 4-Week Return Due",
            "Send Return Template",
            self._task_return_reminder,
        )
        self._add_task(
            "Quote #3402 (R. Davies) - Client accepted online portal",
            "Book & Assign Job ID",
            self._task_booking_pipeline,
        )
        self._add_task(
            "Job ID #9082 - Incomplete work reported (Rain delay)",
            "Update Jobsheet Log",
            self._task_jobsheet_update,
        )
        self._add_task(
            "Invoice #8812 - Marked paid via bank sheet sync",
            "Clear from A/R Logs",
            self._task_clear_ar,
        )

        bottom_split.addWidget(task_card, 2)
        layout.addLayout(bottom_split)

        return tab

    def _make_placeholder(self, name: str) -> QWidget:
        """Return a generic placeholder widget for tabs not yet built."""
        widget = QWidget()
        lyt = QVBoxLayout(widget)
        lyt.setContentsMargins(20, 20, 20, 20)

        title = QLabel(f"<h2>{name}</h2>")
        title.setStyleSheet("color: #2c3e50;")
        lyt.addWidget(title)

        info = QLabel(
            f"<b>{name}</b> module coming in a future section.<br/>"
            "This tab will be fully populated once Section 1 is confirmed working."
        )
        info.setStyleSheet(
            "background-color: #f8fafc; border: 1px solid #e2e8f0; "
            "padding: 15px; border-radius: 4px; color: #475569;"
        )
        info.setWordWrap(True)
        lyt.addWidget(info)
        lyt.addStretch()

        return widget

    # ======================================================================
    # Options page
    # ======================================================================

    def _build_options_page(self) -> None:
        """Add the settings/options page to the tab stack."""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        self.options_widget = OptionsWidget(close_callback=self._close_options)
        page_layout.addWidget(self.options_widget)

        self.options_index = self.tab_stack.addWidget(page)

    def show_options_page(self) -> None:
        """Switch to the settings page and deselect sidebar buttons."""
        if self.options_index is not None:
            self.tab_stack.setCurrentIndex(self.options_index)
            for btn in self.btn_group:
                btn.setChecked(False)
                btn.update_style(False)

    def _close_options(self) -> None:
        """Return to the Dashboard (tab 0) from settings."""
        self.switch_tab(0)

    # ======================================================================
    # Navigation
    # ======================================================================

    def switch_tab(self, index: int) -> None:
        """Activate tab *index* and update sidebar highlight."""
        self.tab_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.btn_group):
            active = (i == index)
            btn.setChecked(active)
            btn.update_style(active)

    # ======================================================================
    # Clock helpers
    # ======================================================================

    def _update_clock(self) -> None:
        now = datetime.datetime.now()
        self.clock_lbl.setText(f"🕐 {now.strftime('%I:%M:%S %p')}")

    def _refresh_date(self) -> None:
        today = datetime.date.today()
        self.date_lbl.setText(f"📅 {today.strftime('%A, %d %B %Y')}")

    # ======================================================================
    # Task board helpers
    # ======================================================================

    def _add_task(self, text: str, button_label: str, callback) -> None:
        """Inject a TaskItemWidget row into the task list."""
        item = QListWidgetItem(self.task_list_widget)
        widget = TaskItemWidget(text, button_label, lambda _item=item: callback(_item))
        item.setSizeHint(widget.sizeHint())
        self.task_list_widget.addItem(item)
        self.task_list_widget.setItemWidget(item, widget)

    # ======================================================================
    # Task callbacks
    # ======================================================================

    def _task_return_reminder(self, list_item: QListWidgetItem) -> None:
        """Send a 4-week return reminder template."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Review Reminder Template")
        msg.setText(
            "<b>Lawn Care Reminder Template:</b><br><br>"
            "<i>'Hi M. Lawson, it has been 3 weeks since your last lawn service. "
            "Your lawn is due for maintenance next week. Let us know if your preferred "
            "day and time remain the same so we can secure your booking slot!'</i>"
        )
        msg.setInformativeText("Dispatch this communication log via Dm_emails?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if msg.exec() == QMessageBox.StandardButton.Yes:
            print("[Task Action] Template approved. Logging communication to Dm_emails...")
            self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def _task_booking_pipeline(self, list_item: QListWidgetItem) -> None:
        """Open the booking confirmation review panel."""
        client_name = "R. Davies"
        requested_date = "15/07/2026"
        requested_time = "10:00 AM"
        suburb = "Frankston"
        services = "Lawn Mowing & Edging (Large Yard)"
        estimated_quote_total = "$85.00"

        review_box = QMessageBox(self)
        review_box.setWindowTitle("Overseer Quote & Booking Review Engine")
        review_box.setIcon(QMessageBox.Icon.Information)
        review_box.setText(
            f"<h3>Incoming Web Booking & Quote Request</h3>"
            f"<b>Client:</b> {client_name}<br>"
            f"<b>Location:</b> {suburb}<br>"
            f"<b>Requested Slot:</b> {requested_date} at {requested_time}<br>"
            f"<b>Job Details:</b> {services} — <b>Value:</b> {estimated_quote_total}<br><br>"
            f"⚠️ <b>Area Optimisation:</b> 2 other jobs in <u>{suburb}</u> on this date. "
            f"Grouping saves ~12 km in travel."
        )
        review_box.setInformativeText(
            "Confirmed arrival window with client? 'Accept' will lock the appointment, "
            "generate a Job ID, and email the client."
        )
        accept_btn = review_box.addButton("Accept & Confirm Booking", QMessageBox.ButtonRole.AcceptRole)
        review_box.addButton("Call Client / Change Time", QMessageBox.ButtonRole.ActionRole)
        review_box.addButton("Keep Pending", QMessageBox.ButtonRole.RejectRole)
        review_box.exec()

        if review_box.clickedButton() == accept_btn:
            year = datetime.datetime.now().strftime("%Y")
            job_id = f"LAWN-{year}-042"
            print(f"[Engine] Booking confirmed — Job ID: {job_id}")
            self.task_list_widget.takeItem(self.task_list_widget.row(list_item))
            success = QMessageBox(self)
            success.setWindowTitle("Booking Secured")
            success.setText(
                f"🎉 Job <b>{job_id}</b> lodged in Google Calendar and synced to sheets."
            )
            success.exec()

    def _task_jobsheet_update(self, list_item: QListWidgetItem) -> None:
        """Append weather/delay notes to the jobsheet."""
        print("[Task Action] Appending weather/delay notes to Dm_Jobsheets...")
        self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def _task_clear_ar(self, list_item: QListWidgetItem) -> None:
        """Clear the invoice from accounts receivable."""
        print("[Task Action] Moving invoice from Outstanding to Paid columns...")
        self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def _trigger_runsheet_pipeline(self) -> None:
        """Trigger daily runsheet generation."""
        print("[Engine Pipeline] Processing daily runsheet field layout updates...")
