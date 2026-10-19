"""Графический интерфейс эмулятора на tkinter."""

import tkinter as tk
from tkinter import scrolledtext

from errors import ShellError
from shell import read_script

PROMPT = "$ "
NOT_SET = "не задан"


class App:
    """Окно эмулятора: поле вывода и строка ввода."""

    def __init__(self, shell, script_path=None):
        """Создаёт окно, в заголовке которого указано имя VFS."""
        self.shell = shell
        self.script_path = script_path
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — {shell.vfs_name}")
        self.output = scrolledtext.ScrolledText(self.root)
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()
        self.print_params()
        self.load_vfs()

    def print(self, text):
        """Добавляет строку текста в поле вывода."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def print_params(self):
        """Отладочный вывод параметров запуска."""
        self.print("Параметры запуска:")
        self.print(f"  VFS: {self.shell.vfs_path or NOT_SET}")
        self.print(f"  Стартовый скрипт: {self.script_path or NOT_SET}")
        self.print("")

    def load_vfs(self):
        """Загружает VFS и печатает результат или ошибку."""
        try:
            self.print(self.shell.load())
        except ShellError as error:
            self.print(f"Ошибка: {error}")
        self.print("")

    def on_enter(self, event):
        """Обрабатывает нажатие Enter в строке ввода."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print(PROMPT + line)
        self.run_line(line)

    def run_line(self, line):
        """Выполняет строку, выводит результат или ошибку.
        Возвращает True, если ошибки не было."""
        try:
            result = self.shell.execute(line)
        except ShellError as error:
            self.print(f"Ошибка: {error}")
            return False
        if result:
            self.print(result)
        if not self.shell.running:
            self.root.destroy()
        return True

    def run_script(self):
        """Выполняет стартовый скрипт, показывая ввод и вывод.
        При первой ошибке скрипт останавливается."""
        try:
            lines = read_script(self.script_path)
        except ShellError as error:
            self.print(f"Ошибка: {error}")
            return
        for number, line in lines:
            self.print(PROMPT + line)
            if not self.run_line(line):
                self.print(f"Скрипт остановлен: ошибка в строке {number}")
                return
            if not self.shell.running:
                return

    def start(self):
        """Запускает скрипт (если задан) и главный цикл окна."""
        if self.script_path:
            self.root.after(0, self.run_script)
        self.root.mainloop()
