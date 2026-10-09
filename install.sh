#!/bin/bash

# Touch Grass Desktop Companion Installer
# Cross-platform setup for Windows, Mac, and Linux
# Designed for low-resource systems (i7-6600U, 8GB RAM)

set -e

cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Touch Grass Desktop Companion Installer ===${NC}"

# Determine the user context and paths
if [[ "$EUID" -eq 0 ]]; then
    echo -e "${RED}Do NOT run as root! Running as non-root user.${NC}"
    exit 1
fi

# Use python3 or python3.10+ (avoid python command on Windows) if available
PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" &> /dev/null; then
    echo -e "${RED}Python3 not found! Please install Python 3.10+ and try again.${NC}"
    exit 1
fi

echo -e "${YELLOW}Python found: ${PYTHON}$NC"

# Create a virtual environment
VENV_DIR="${PWD}/venv"
echo -e "${YELLOW}Creating virtual environment...${NC}"

# Try pyvenv first (should be present on most Python installations)
if ! command -v "$PYTHON" -m venv "$VENV_DIR"; then
    echo -e "${YELLOW}pyvenv not available, trying with python3.10 if available...${NC}"
    # Try with python3.10 explicitly
    PYTHON=${PYTHON:-python3.10}
    if ! command -v "$PYTHON" -m venv "$VENV_DIR"; then
        echo -e "${RED}Failed to create virtual environment!${NC}"
        exit 1
    fi
fi

# Activate the virtual environment and install dependencies
echo -e "${YELLOW}Activating virtual environment and installing dependencies...${NC}"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt

# Download required models
echo -e "${YELLOW}Downloading open-weight model...${NC}"
python scripts/download_models.py

# Make the companion executable
echo -e "${YELLOW}Setting up scripts...${NC}"
cat <<'EOF' > run.sh
#!/usr/bin/env bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
EOF
chmod +x run.sh

cat <<'EOF' > run.bat
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
EOF
chmod +x run.bat

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}Run the companion with: ./run.sh (Linux/macOS) or run.bat (Windows)${NC}"
echo -e "${YELLOW}Or double-click the 'run.bat' or 'run.sh' files to start the companion.${NC}"
echo -e "${YELLOW}You can also set MISO_CHARACTER=your_character to use a different companion.${NC}"