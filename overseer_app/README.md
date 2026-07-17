# Overseer APP — Section 1: UI Shell

PC management portal for DmLawnCare, built with **PyQt6**.

## Requirements

```
pip install PyQt6
```

## How to Run

**Windows:**
```
cd overseer_app
run_debug.bat
```

**Linux / macOS:**
```
cd overseer_app
python3 main.py
# or
bash run_debug.sh
```

## Section 1 — Features Delivered

| Area | Feature |
|---|---|
| Header (fixed top) | ⚙️ App title, 📅 date, 🕐 real-time clock (1 s), 🔔 next alarm |
| Left sidebar | 16 coloured navigation tabs + ⚙️ Settings gear at bottom |
| Dashboard tab | 4 metric cards, ⚠️ Task Action Board, 📋 Runsheet Control |
| Settings panel | 6 colour pickers, reset to defaults, close button |
| Persistence | Colour choices saved to `config/settings.json` |

## File Structure

```
overseer_app/
├── main.py                   Entry point
├── ui/
│   ├── __init__.py
│   ├── main_window.py        LawnCarePortal (main window)
│   ├── nav_button.py         NavButton sidebar widget
│   ├── dashboard_widget.py   DashboardWidget metric card
│   ├── task_widget.py        TaskItemWidget interactive row
│   ├── options.py            OptionsWidget settings panel
│   └── color_manager.py      ColorManager JSON persistence
├── config/
│   ├── defaults.json         Factory colour defaults
│   └── settings.json         User colour overrides (auto-saved)
├── run_debug.bat             Windows launcher
├── run_debug.sh              Linux/macOS launcher
└── README.md                 This file
```

## 16 Navigation Tabs

| # | Tab | Colour |
|---|---|---|
| 1 | 🏠 Dashboard | Green |
| 2 | 👥 Clients | Blue |
| 3 | 📄 Workbook | Blue |
| 4 | 📄 Quotes | Orange |
| 5 | 📅 Bookings | Red |
| 6 | 🗂️ Invoices | Light Blue |
| 7 | 📊 Jobsheets | Yellow |
| 8 | ⏰ Timesheets | Gold |
| 9 | 🚗 Vehicle | Pink |
| 10 | 🏦 Banking | Light Blue |
| 11 | 📚 Bookkeeping | Purple |
| 12 | 🔧 Inventory | Teal |
| 13 | 📅 Calendar | Dark Blue |
| 14 | ✉️ Communications | Green |
| 15 | 🌐 Website | Orange |
| 16 | 📱 Mobile | Purple |

## Roadmap

- **Section 2** — Repository Layer (Google Sheets API)
- **Section 3** — ID Tracker Box
- **Section 4** — Tab Modules (one at a time)
- **Section 5** — Integrations (Weebly, Apps Sheet, Banking)
- **Section 6** — Deployment & Packaging
