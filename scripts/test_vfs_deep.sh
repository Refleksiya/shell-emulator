#!/bin/sh
# Тест VFS: deep
cd "$(dirname "$0")/.."
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/deep.zip --script examples/stage3.txt
