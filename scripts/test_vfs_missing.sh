#!/bin/sh
# Тест: VFS не найдена
cd "$(dirname "$0")/.."
python3 src/main.py --vfs build/nope.zip
