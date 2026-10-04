@echo off
REM Test VFS: small
cd /d "%~dp0.."
python scripts\make_vfs.py
python src\main.py --vfs build\small.zip --script examples\stage3.txt
