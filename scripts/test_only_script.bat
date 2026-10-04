@echo off
REM Test: only_script
cd /d "%~dp0.."
python src\main.py --script examples\ok.txt
