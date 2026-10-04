#!/bin/sh
# Тест VFS: minimal
cd "$(dirname "$0")/.."
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/minimal.zip --script examples/stage3.txt
