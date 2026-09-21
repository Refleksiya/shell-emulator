"""Логика эмулятора: разбор строки и выполнение команд."""

import os
import shlex

DEFAULT_VFS_NAME = "vfs"
MAX_CD_ARGS = 1


class ShellError(Exception):
    """Ошибка выполнения команды (выводится пользователю)."""


def parse(line):
    """Раскрывает переменные окружения ($HOME и т.п.) и делит строку
    на слова с учётом кавычек."""
    line = os.path.expandvars(line)
    try:
        return shlex.split(line)
    except ValueError:
        raise ShellError("ошибка разбора: незакрытая кавычка")


class Shell:
    """Эмулятор оболочки: хранит состояние и выполняет команды."""

    def __init__(self, vfs_name=DEFAULT_VFS_NAME):
        """Создаёт оболочку с заданным именем VFS."""
        self.vfs_name = vfs_name
        self.running = True
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

    def execute(self, line):
        """Выполняет одну строку и возвращает текст вывода."""
        words = parse(line)
        if not words:
            return ""
        name, args = words[0], words[1:]
        if name not in self.commands:
            raise ShellError(f"{name}: команда не найдена")
        return self.commands[name](args)

    def cmd_ls(self, args):
        """Заглушка ls: выводит имя команды и аргументы."""
        return f"ls, аргументы: {args}"

    def cmd_cd(self, args):
        """Заглушка cd: выводит имя команды и аргументы."""
        if len(args) > MAX_CD_ARGS:
            raise ShellError("cd: слишком много аргументов")
        return f"cd, аргументы: {args}"

    def cmd_exit(self, args):
        """Завершает работу эмулятора."""
        if args:
            raise ShellError("exit: команда не принимает аргументы")
        self.running = False
        return ""
