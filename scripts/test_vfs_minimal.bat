@echo off
REM Test VFS: minimal
cd /d "%~dp0.."
python scripts\make_vfs.py
python src\main.py --vfs build\minimal.zip --script examples\stage3.txt
