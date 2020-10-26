@echo off
cd /d "%~dp0"
set PATH=%SystemRoot%\System32
set PYTHONDONTWRITEBYTECODE=1
bin\python.exe src\main.py
echo.
pause
