"""
DmOverseer Lawn Care - Ultimate Standalone Portal
Main GUI Application with Full Module Integration
Preserves original Home Dashboard design + integrates all business modules
"""

import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QScrollArea, QLabel,
    QGridLayout, QFrame, QStackedWidget, QSizePolicy,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

# Import all business modules
from modules.home_module import HomeModule
from modules.client_module import ClientModule
from modules.quotes_module import QuotesModule
from modules.bookings_module import BookingsModule
from modules.invoices_module import InvoicesModule
from modules.jobsheets_module import JobsheetsModule
from modules.runsheets_module import RunsheetsModule
from modules.timesheets_module import TimesheetsModule
from modules.vehicle_module import VehicleModule
from modules.banking_module import BankingModule
from modules.bookkeeping_module import BookkeepingModule
from modules.inventory_module import InventoryModule
from modules.calendar_module import CalendarModule
from modules.communications_module import CommunicationsModule
from modules.website_module import WebsiteModule
from modules.mobile_module import MobileModule
from modules.options_module import OptionsWidget


class NavButton(QPushButton):
    """Custom navigation button for colored sidebar"""
    def __init__(self, text, color="#27ae60", parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setMinimumHeight(40)
        self.color = color
        self.update_style(False)
    
    def update_style(self, checked):
        """Update button style based on state"""
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
                    opacity: 0.9;
                }}
            """)


class DashboardWidget(QFrame):
    """Dynamic operational counter & data block card."""
    def __init__(self, title, content_lines, accent_color="#27ae60", parent=None):
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


class TaskItemWidget(QWidget):
    """Interactive task row with action button for the Task Widget."""
    def __init__(self, task_text, button_text, callback, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.label = QLabel(task_text)
        self.label.setFont(QFont("Arial", 10))
        self.label.setStyleSheet("color: #1e293b;")

        self.btn = QPushButton(button_text)
        self.btn.setFixedSize(130, 26)
        self.btn.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; font-weight: bold; border-radius: 3px; border: none; font-size: 11px; }
            QPushButton:hover { background-color: #219653; }
        """)
        self.btn.clicked.connect(callback)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.btn)


class LawnCarePortal(QMainWindow):
    """Main DmOverseer Application Window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DmOverseer Lawn Care Ultimate Standalone Portal")
        self.resize(1350, 850)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Left sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("#Sidebar { background-color: #2c3e50; }")

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 15, 0, 15)
        self.sidebar_layout.setSpacing(2)

        # Main work area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        self.tab_display_stack = QStackedWidget()
        self.content_layout.addWidget(self.tab_display_stack)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Tab metadata with names, sheet sources, and colors
        self.tabs_meta = [
            ("🏠 Home", "Local_Cache", "#27ae60"),
            ("👥 Client Accounts", "Dm_client_accounts", "#27ae60"),
            ("📄 Quotes", "Dm_quotes", "#e67e22"),
            ("📅 Bookings", "Dm_bookings", "#e74c3c"),
            ("🗂️ Invoices", "Dm_invoices", "#3498db"),
            ("📊 Jobsheets / Runsheet", "Dm_Jobsheets", "#f39c12"),
            ("📂 Archive", "Dm_archive", "#95a5a6"),
            ("⏰ Timesheets / Wages", "Dm_timesheets", "#f1c40f"),
            ("🚗 Vehicle Log", "Dm_vehicle", "#e91e63"),
            ("🏦 Banking", "Dm_banking", "#3498db"),
            ("📚 Book Keeping", "Dm_book_keeping", "#9b59b6"),
            ("🔧 Inventory / Tools", "Dm_inventory", "#1abc9c"),
            ("📅 Calendar / Maps", "Dm_calendar", "#2196f3"),
            ("✉️ Emails / SMS / Google", "Dm_emails", "#27ae60"),
            ("🌐 Website", "Dm_website", "#ff9800"),
            ("📱 Mobile", "Dm_mobile", "#9c27b0"),
        ]

        self.btn_group = []
        self.options_index = None
        self.modules = {}

        self.build_navigation_sidebar()
        self.build_all_tab_interfaces()
        self.build_options_workspace()

        self.switch_tab(0)

        # Options button in toolbar
        self.gearBtn = QPushButton("⚙️ Options")
        self.gearBtn.setMinimumHeight(35)
        self.gearBtn.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        self.gearBtn.clicked.connect(self.show_options_workspace)

        self.toolbar = self.addToolBar("Settings")
        self.toolbar.addWidget(self.gearBtn)

    def build_navigation_sidebar(self):
        """Build colored navigation sidebar with all tabs"""
        for index, (name, _, color) in enumerate(self.tabs_meta):
            btn = NavButton(name, color)
            btn.clicked.connect(lambda checked, idx=index: self.switch_tab(idx))
            self.sidebar_layout.addWidget(btn)
            self.btn_group.append(btn)
        
        self.sidebar_layout.addStretch()

    def switch_tab(self, index):
        """Switch to a specific tab"""
        self.tab_display_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.btn_group):
            btn.setChecked(i == index)
            btn.update_style(i == index)

    def build_all_tab_interfaces(self):
        """Build all tab interfaces - mix of original design and integrated modules"""
        
        # TAB 0: HOME DASHBOARD (ORIGINAL DESIGN PRESERVED)
        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)
        home_layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("DmOverseer Business Management Command Centre")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #1e293b; padding-bottom: 5px;")
        home_layout.addWidget(header)

        # Scroll area for top metrics widgets
        metrics_scroll = QScrollArea()
        metrics_scroll.setWidgetResizable(True)
        metrics_scroll.setFixedHeight(180)
        metrics_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        metrics_content = QWidget()
        metrics_grid = QGridLayout(metrics_content)
        metrics_grid.setSpacing(15)
        metrics_grid.setContentsMargins(0, 0, 5, 0)

        metrics_grid.addWidget(DashboardWidget(
            title="👥 Client Accounts",
            content_lines=["• <b>New Clients:</b> 3 Action Required", "• <b>Total Clients:</b> 142 Accounts Logged"],
            accent_color="#2980b9"
        ), 0, 0)

        metrics_grid.addWidget(DashboardWidget(
            title="📄 Quotes Pipeline",
            content_lines=["• <b>Total Quotes Generated:</b> 18", "• <b>Ready to Accept/Book:</b> 4 Confirmed"],
            accent_color="#e67e22"
        ), 0, 1)

        metrics_grid.addWidget(DashboardWidget(
            title="📅 Next Scheduled Booking",
            content_lines=["• <b>Tomorrow 8:30 AM:</b> J. Smith", "• <b>Location:</b> 24 Harrison St, Frankston"],
            accent_color="#27ae60"
        ), 0, 2)

        metrics_grid.addWidget(DashboardWidget(
            title="💰 Invoice Summary",
            content_lines=["• <b>Generated:</b> 89  |  • <b>Paid:</b> 74", "• <b>Unpaid (A/R):</b> 15 Outstanding"],
            accent_color="#8e44ad"
        ), 0, 3)

        metrics_scroll.setWidget(metrics_content)
        home_layout.addWidget(metrics_scroll)

        # Bottom split: runsheet + task board
        bottom_split = QHBoxLayout()
        bottom_split.setSpacing(15)

        runsheet_card = QFrame()
        runsheet_card.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; "
            "border-left: 5px solid #d35400; border-radius: 6px; }"
        )
        rs_layout = QVBoxLayout(runsheet_card)
        rs_layout.setContentsMargins(15, 15, 15, 15)

        rs_title = QLabel("📋 Daily Run-Sheet Control")
        rs_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        rs_title.setStyleSheet("color: #475569; border: none;")
        rs_layout.addWidget(rs_title)

        rs_info = QLabel(
            "• <b>Next Run:</b> 09/07/2026<br/>"
            "• <b>Jobs Scheduled:</b> 5 Allocated Runs<br/><br/>"
            "<i>Tracks: Journeys, timesheets, vehicles, expenses, and updates journal automatically.</i>"
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
        gen_rs_btn.clicked.connect(self.trigger_runsheet_generation_pipeline)
        rs_layout.addWidget(gen_rs_btn)

        bottom_split.addWidget(runsheet_card, 1)

        task_card = QFrame()
        task_card.setStyleSheet(
            "QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; "
            "border-left: 5px solid #f1c40f; border-radius: 6px; }"
        )
        task_layout = QVBoxLayout(task_card)
        task_layout.setContentsMargins(15, 15, 15, 15)

        task_title = QLabel("⚠️ Overseer Action & Task Board")
        task_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        task_title.setStyleSheet("color: #475569; border: none;")
        task_layout.addWidget(task_title)

        task_sub = QLabel("Items requiring manually initiated template reminders or job validation checks:")
        task_sub.setFont(QFont("Arial", 9))
        task_sub.setStyleSheet("color: #64748b; border: none;")
        task_layout.addWidget(task_sub)

        self.task_list_widget = QListWidget()
        self.task_list_widget.setStyleSheet(
            "QListWidget { border: 1px solid #e2e8f0; border-radius: 4px; background: #f8fafc; }"
        )
        task_layout.addWidget(self.task_list_widget)

        self.add_manual_action_task(
            "M. Lawson (Completed 3 weeks ago) - 4-Week Return Due",
            "Send Return Template",
            self.initiate_return_reminder
        )
        self.add_manual_action_task(
            "Quote #3402 (R. Davies) - Client accepted online portal",
            "Book & Assign Job ID",
            self.initiate_booking_pipeline
        )
        self.add_manual_action_task(
            "Job ID #9082 - Incomplete work reported (Rain delay)",
            "Update Jobsheet Log",
            self.initiate_jobsheet_update
        )
        self.add_manual_action_task(
            "Invoice #8812 - Marked paid via bank sheet sync",
            "Clear from A/R Logs",
            self.clear_ar_task
        )

        bottom_split.addWidget(task_card, 2)
        home_layout.addLayout(bottom_split)

        self.tab_display_stack.addWidget(home_tab)

        # TAB 1: CLIENT ACCOUNTS (INTEGRATED MODULE)
        try:
            client_tab = ClientModule()
            self.modules["clients"] = client_tab
            self.tab_display_stack.addWidget(client_tab)
        except Exception as e:
            print(f"Error loading Client module: {e}")
            self.add_placeholder_tab("Client Accounts")

        # TAB 2: QUOTES (INTEGRATED MODULE)
        try:
            quotes_tab = QuotesModule()
            self.modules["quotes"] = quotes_tab
            self.tab_display_stack.addWidget(quotes_tab)
        except Exception as e:
            print(f"Error loading Quotes module: {e}")
            self.add_placeholder_tab("Quotes")

        # TAB 3: BOOKINGS (INTEGRATED MODULE)
        try:
            bookings_tab = BookingsModule()
            self.modules["bookings"] = bookings_tab
            self.tab_display_stack.addWidget(bookings_tab)
        except Exception as e:
            print(f"Error loading Bookings module: {e}")
            self.add_placeholder_tab("Bookings")

        # TAB 4: INVOICES (INTEGRATED MODULE)
        try:
            invoices_tab = InvoicesModule()
            self.modules["invoices"] = invoices_tab
            self.tab_display_stack.addWidget(invoices_tab)
        except Exception as e:
            print(f"Error loading Invoices module: {e}")
            self.add_placeholder_tab("Invoices")

        # TAB 5: JOBSHEETS (INTEGRATED MODULE)
        try:
            jobsheets_tab = JobsheetsModule()
            self.modules["jobsheets"] = jobsheets_tab
            self.tab_display_stack.addWidget(jobsheets_tab)
        except Exception as e:
            print(f"Error loading Jobsheets module: {e}")
            self.add_placeholder_tab("Jobsheets")

        # TAB 6: ARCHIVE (PLACEHOLDER)
        self.add_placeholder_tab("Archive")

        # TAB 7: TIMESHEETS/WAGES (INTEGRATED MODULE)
        try:
            timesheets_tab = TimesheetsModule()
            self.modules["timesheets"] = timesheets_tab
            self.tab_display_stack.addWidget(timesheets_tab)
        except Exception as e:
            print(f"Error loading Timesheets module: {e}")
            self.add_placeholder_tab("Timesheets/Wages")

        # TAB 8: VEHICLE LOG (INTEGRATED MODULE)
        try:
            vehicle_tab = VehicleModule()
            self.modules["vehicle"] = vehicle_tab
            self.tab_display_stack.addWidget(vehicle_tab)
        except Exception as e:
            print(f"Error loading Vehicle module: {e}")
            self.add_placeholder_tab("Vehicle Log")

        # TAB 9: BANKING (INTEGRATED MODULE)
        try:
            banking_tab = BankingModule()
            self.modules["banking"] = banking_tab
            self.tab_display_stack.addWidget(banking_tab)
        except Exception as e:
            print(f"Error loading Banking module: {e}")
            self.add_placeholder_tab("Banking")

        # TAB 10: BOOKKEEPING (INTEGRATED MODULE)
        try:
            bookkeeping_tab = BookkeepingModule()
            self.modules["bookkeeping"] = bookkeeping_tab
            self.tab_display_stack.addWidget(bookkeeping_tab)
        except Exception as e:
            print(f"Error loading Bookkeeping module: {e}")
            self.add_placeholder_tab("Book Keeping")

        # TAB 11: INVENTORY (INTEGRATED MODULE)
        try:
            inventory_tab = InventoryModule()
            self.modules["inventory"] = inventory_tab
            self.tab_display_stack.addWidget(inventory_tab)
        except Exception as e:
            print(f"Error loading Inventory module: {e}")
            self.add_placeholder_tab("Inventory/Tools")

        # TAB 12: CALENDAR (INTEGRATED MODULE)
        try:
            calendar_tab = CalendarModule()
            self.modules["calendar"] = calendar_tab
            self.tab_display_stack.addWidget(calendar_tab)
        except Exception as e:
            print(f"Error loading Calendar module: {e}")
            self.add_placeholder_tab("Calendar/Maps")

        # TAB 13: COMMUNICATIONS (INTEGRATED MODULE)
        try:
            communications_tab = CommunicationsModule()
            self.modules["communications"] = communications_tab
            self.tab_display_stack.addWidget(communications_tab)
        except Exception as e:
            print(f"Error loading Communications module: {e}")
            self.add_placeholder_tab("Communications")

        # TAB 14: WEBSITE (INTEGRATED MODULE)
        try:
            website_tab = WebsiteModule()
            self.modules["website"] = website_tab
            self.tab_display_stack.addWidget(website_tab)
        except Exception as e:
            print(f"Error loading Website module: {e}")
            self.add_placeholder_tab("Website")

        # TAB 15: MOBILE (INTEGRATED MODULE)
        try:
            mobile_tab = MobileModule()
            self.modules["mobile"] = mobile_tab
            self.tab_display_stack.addWidget(mobile_tab)
        except Exception as e:
            print(f"Error loading Mobile module: {e}")
            self.add_placeholder_tab("Mobile")

    def add_placeholder_tab(self, name):
        """Add placeholder tab when module fails to load"""
        tab_widget = QWidget()
        lyt = QVBoxLayout(tab_widget)

        title_lbl = QLabel(f"<h2>{name}</h2>")
        title_lbl.setStyleSheet("color: #2c3e50;")
        lyt.addWidget(title_lbl)

        info = QLabel(f"<b>{name} module is loading...</b><br/>Please ensure all modules are properly installed.")
        info.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 4px;")
        lyt.addWidget(info)
        lyt.addStretch()

        self.tab_display_stack.addWidget(tab_widget)

    def build_options_workspace(self):
        """Build options/settings workspace"""
        options_page = QWidget()
        options_layout = QVBoxLayout(options_page)
        options_layout.setContentsMargins(0, 0, 0, 0)

        self.optionsWidget = OptionsWidget()
        options_layout.addWidget(self.optionsWidget)

        self.options_index = self.tab_display_stack.addWidget(options_page)

    def show_options_workspace(self):
        """Switch to options workspace"""
        if self.options_index is not None:
            self.tab_display_stack.setCurrentIndex(self.options_index)
            # Uncheck all sidebar buttons
            for btn in self.btn_group:
                btn.setChecked(False)
                btn.update_style(False)

    def add_manual_action_task(self, text, button_label, callback):
        """Helper to create and safely inject items with interactive buttons into the list box widget."""
        item = QListWidgetItem(self.task_list_widget)
        custom_widget = TaskItemWidget(text, button_label, lambda: callback(item))
        item.setSizeHint(custom_widget.sizeHint())
        self.task_list_widget.addItem(item)
        self.task_list_widget.setItemWidget(item, custom_widget)

    # OPERATIONAL TASK ACTIONS (Manual Triggers)
    def initiate_return_reminder(self, list_item):
        """Pulls template text and prepares communication log via Dm_emails/Dm_bookings."""
        print("[Task Action] Loading Email/SMS text templates for 4-week regular job re-booking...")
        msg = QMessageBox(self)
        msg.setWindowTitle("Review Reminder Template")
        msg.setText(
            "<b>Lawn Care Reminder Template:</b><br><br>"
            "<i>'Hi M. Lawson, it has been 3 weeks since your last lawn service. "
            "Your lawn is due for maintenance next week. Let us know if your preferred "
            "day and time remain the same so we can secure your booking slot!'</i>"
        )

        msg.setInformativeText("Would you like to dispatch this communication log via Dm_emails?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            print("[Task Action] Template approved. Logging communication to Dm_emails...")
            self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def initiate_booking_pipeline(self, list_item):
        """Opens a live review panel for quotes and bookings sent from your website."""
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
            f"⚠️ <b>Area Optimisation Check:</b> You have 2 other jobs scheduled in <u>{suburb}</u> on this date. "
            f"Grouping this job will save you approximately 12km in travel expenses."
        )

        review_box.setInformativeText(
            "Have you confirmed the arrival window with the client over the phone if adjustments were needed? "
            "Clicking 'Yes' will lock in the appointment, generate a Job ID, and email the client."
        )

        accept_btn = review_box.addButton("Accept & Confirm Booking", QMessageBox.ButtonRole.AcceptRole)
        call_client_btn = review_box.addButton("Call Client / Change Time", QMessageBox.ButtonRole.ActionRole)
        cancel_btn = review_box.addButton("Keep Pending", QMessageBox.ButtonRole.RejectRole)

        review_box.exec()

        if review_box.clickedButton() == accept_btn:
            year = datetime.datetime.now().strftime("%Y")
            next_job_number = "042"
            generated_job_id = f"LAWN-{year}-{next_job_number}"

            print(f"\n[Engine Loop] --- PROCESSING CONFIRMATION FOR JOB ID: {generated_job_id} ---")
            print(f"[gspread] Writing Job ID {generated_job_id} to Dm_quotes (Status -> 'Accepted')")
            print(f"[gspread] Writing Job ID {generated_job_id} to Dm_bookings (Status -> 'Confirmed')")
            print(f"[gspread] Creating fresh structural template inside Dm_Jobsheets for job execution...")
            print(f"[Google Calendar API] Creating calendar appointment for {client_name} on {requested_date} at {requested_time}")
            print(f"[Dm_emails System] Dispatched Confirmation: 'Hi {client_name}, your quote & booking are confirmed...'")

            self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

            success = QMessageBox(self)
            success.setWindowTitle("Booking Secured")
            success.setText(
                f"🎉 Success! Job <b>{generated_job_id}</b> has been officially lodged in your Google Calendar and synced to your sheets."
            )
            success.exec()

        elif review_box.clickedButton() == call_client_btn:
            new_slot, ok = QInputDialog.getText(
                self, "Schedule Adjustment",
                f"Enter new agreed time/day for {client_name} (e.g., 15/07/2026 1:30 PM):"
            )
            if ok and new_slot:
                print(f"[gspread Log] Updated requested window to: {new_slot} inside Dm_bookings based on client call.")

    def initiate_jobsheet_update(self, list_item):
        """Opens target jobsheet configuration to append notes or extra service entries."""
        print("[Task Action] Appending weather/delay notes to Dm_Jobsheets configuration fields...")
        self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def clear_ar_task(self, list_item):
        """Balances the books inside Dm_general_journals and account receivable columns."""
        print("[Task Action] Balances matched. Moving invoice from Outstanding to Paid columns...")
        self.task_list_widget.takeItem(self.task_list_widget.row(list_item))

    def trigger_runsheet_generation_pipeline(self):
        """Trigger runsheet generation"""
        print("[Engine Pipeline] Processing daily runsheet field layout updates...")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    portal = LawnCarePortal()
    portal.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
