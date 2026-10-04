@echo off
REM Test stage 5 commands
cd /d "%~dp0.."
python scripts\make_vfs.py
python src\main.py --vfs build\deep.zip --script examples\stage5.txt
