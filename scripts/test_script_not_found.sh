#!/bin/sh
# Тест: script_not_found
cd "$(dirname "$0")/.."
python3 src/main.py --script examples/nope.txt
