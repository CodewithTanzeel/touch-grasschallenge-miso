@echo off
setlocal enabledelayedexpansion

echo === Touch Grass Desktop Companion Installer ===
echo Windows Batch Installer
echo.

cd /d "%~dp0"

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found! Please install Python 3.10+ and try again.
    echo.
    echo Install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found.
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

pip install --upgrade pip
pip install -r requirements.txt

REM Download required models
echo Downloading open-weight model...
python scripts/download_models.py

REM Make the companion executable
echo Setting up scripts...
echo @echo off > run.bat
echo cd /d "%%~dp0" >> run.bat
echo call venv\Scripts\activate.bat >> run.bat
echo python main.py >> run.bat

echo.
echo Installation complete!
echo Run the companion with: run.bat
echo Or double-click the "run.bat" file to start the companion.
echo.
pause