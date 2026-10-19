#!/bin/sh
# Тест: only_vfs
cd "$(dirname "$0")/.."
python3 src/main.py --vfs examples/my_vfs.zip
