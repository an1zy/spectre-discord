@echo off
chcp 65001 > nul
title SPECTRE // Discord Activity Engine
cd /d "%~dp0"

python -c "import rich" >nul 2>&1
if %errorlevel% neq 0 (
    echo [SPECTRE] Installing required dependencies (rich)...
    pip install -r requirements.txt
)

python main.py
pause
