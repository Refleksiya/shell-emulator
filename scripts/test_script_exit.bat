@echo off
REM Test: script_exit
cd /d "%~dp0.."
python src\main.py --script examples\exit.txt
