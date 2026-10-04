#!/bin/sh
# Тест VFS: small
cd "$(dirname "$0")/.."
python3 scripts/make_vfs.py
python3 src/main.py --vfs build/small.zip --script examples/stage3.txt
