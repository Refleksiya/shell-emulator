@echo off
REM Test: wrong VFS format
cd /d "%~dp0.."
python src\main.py --vfs README.md
