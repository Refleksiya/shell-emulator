@echo off
REM Test: only_vfs
cd /d "%~dp0.."
python src\main.py --vfs examples\my_vfs.zip
