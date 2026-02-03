@echo off
:: Navigate to the folder where this batch file is located
cd /d "%~dp0"

:: Check if the virtual environment exists
if not exist ".venv" (
    echo [!] Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [!] Installing dependencies...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: Run your main script
echo [!] Launching program...
python main.py

pause