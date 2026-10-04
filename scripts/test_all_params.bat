@echo off
REM Test: all_params
cd /d "%~dp0.."
python src\main.py --vfs examples\my_vfs.zip --script examples\ok.txt
