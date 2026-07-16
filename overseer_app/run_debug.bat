@echo off
echo Starting Overseer APP (Debug Mode)...
echo.
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start. Ensure PyQt6 is installed:
    echo   pip install PyQt6
    pause
)
