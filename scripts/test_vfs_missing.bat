@echo off
REM Test: VFS not found
cd /d "%~dp0.."
python src\main.py --vfs build\nope.zip
