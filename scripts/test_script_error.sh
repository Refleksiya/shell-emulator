#!/bin/sh
# Тест: script_error
cd "$(dirname "$0")/.."
python3 src/main.py --vfs examples/my_vfs.zip --script examples/error.txt
