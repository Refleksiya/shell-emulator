@echo off
REM Test: script_error
cd /d "%~dp0.."
python src\main.py --vfs examples\my_vfs.zip --script examples\error.txt
