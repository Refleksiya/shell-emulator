"""Точка входа: разбор параметров и запуск эмулятора."""

import argparse

from gui import App
from shell import Shell


def parse_args():
    """Читает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args()


def main():
    """Создаёт оболочку с параметрами и открывает окно."""
    args = parse_args()
    App(Shell(args.vfs), args.script).start()


if __name__ == "__main__":
    main()
