#!/bin/sh
# Тест команд этапа 4
cd "$(dirname "$0")/.."
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/deep.zip --script examples/stage4.txt
