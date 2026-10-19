#!/bin/sh
# Тест: неверный формат VFS
cd "$(dirname "$0")/.."
python3 src/main.py --vfs README.md
