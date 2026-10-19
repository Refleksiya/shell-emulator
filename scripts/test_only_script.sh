#!/bin/sh
# Тест: only_script
cd "$(dirname "$0")/.."
python3 src/main.py --script examples/ok.txt
