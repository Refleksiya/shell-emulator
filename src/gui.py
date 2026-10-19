"""Графический интерфейс эмулятора на tkinter."""

import tkinter as tk
from tkinter import scrolledtext

from shell import ShellError

PROMPT = "$ "


class App:
    """Окно эмулятора: поле вывода и строка ввода."""

    def __init__(self, shell):
        """Создаёт окно, в заголовке которого указано имя VFS."""
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — {shell.vfs_name}")
        self.output = scrolledtext.ScrolledText(self.root)
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def print(self, text):
        """Добавляет строку текста в поле вывода."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def on_enter(self, event):
        """Обрабатывает нажатие Enter в строке ввода."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print(PROMPT + line)
        self.run_line(line)

    def run_line(self, line):
        """Выполняет строку и выводит результат или ошибку."""
        try:
            result = self.shell.execute(line)
        except ShellError as error:
            result = f"Ошибка: {error}"
        if result:
            self.print(result)
        if not self.shell.running:
            self.root.destroy()

    def start(self):
        """Запускает главный цикл окна."""
        self.root.mainloop()
