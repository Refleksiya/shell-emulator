"""Точка входа: запуск эмулятора оболочки."""

from gui import App
from shell import Shell


def main():
    """Создаёт оболочку и открывает окно."""
    App(Shell()).start()


if __name__ == "__main__":
    main()
