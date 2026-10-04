@echo off
REM Test: script_not_found
cd /d "%~dp0.."
python src\main.py --script examples\nope.txt
