#!/bin/sh
# Тест: script_exit
cd "$(dirname "$0")/.."
python3 src/main.py --script examples/exit.txt
