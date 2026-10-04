@echo off
REM Test VFS: deep
cd /d "%~dp0.."
python scripts\make_vfs.py
python src\main.py --vfs build\deep.zip --script examples\stage3.txt
