#!/bin/sh
# Тест: all_params
cd "$(dirname "$0")/.."
python3 src/main.py --vfs examples/my_vfs.zip --script examples/ok.txt
