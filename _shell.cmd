@echo off

:: Make sure that CWD is this directory
cd /d "%~dp0"

:: Decrease the chances of "DLL hell" by reducing PATH to the minimum
set PATH=%SystemRoot%\System32

:: App starts fast enough without, so no need to clutter the src folder
set PYTHONDONTWRITEBYTECODE=1

:: Run main.py with enclosed python.exe (Python 3.7.4-x64)
bin\python.exe src\main.py

echo.
pause
