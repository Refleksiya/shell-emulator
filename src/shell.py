"""Логика эмулятора: разбор строки и выполнение команд."""

import os
import shlex

from errors import ShellError
from vfs import Node, ROOT_NAME, load_vfs

DEFAULT_VFS_NAME = "vfs"
MAX_CD_ARGS = 1
COMMENT = "#"


def parse(line):
    """Раскрывает переменные окружения ($HOME и т.п.) и делит строку
    на слова с учётом кавычек. Всё после # считается комментарием."""
    line = os.path.expandvars(line)
    try:
        return shlex.split(line, comments=True)
    except ValueError:
        raise ShellError("ошибка разбора: незакрытая кавычка")


def vfs_name_from_path(path):
    """Возвращает имя VFS по пути (имя файла или папки)."""
    if not path:
        return DEFAULT_VFS_NAME
    return os.path.basename(os.path.normpath(path))


def read_script(path):
    """Читает стартовый скрипт. Возвращает список пар
    (номер строки, строка) без пустых строк и комментариев."""
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.read().splitlines()
    except OSError:
        raise ShellError(f"не удалось открыть скрипт: {path}")
    result = []
    for number, line in enumerate(lines, start=1):
        text = line.strip()
        if text and not text.startswith(COMMENT):
            result.append((number, text))
    return result


class Shell:
    """Эмулятор оболочки: хранит состояние и выполняет команды."""

    def __init__(self, vfs_path=None):
        """Создаёт оболочку. vfs_path — путь к VFS (может быть None)."""
        self.vfs_path = vfs_path
        self.vfs_name = vfs_name_from_path(vfs_path)
        self.root = Node(ROOT_NAME, True)
        self.cwd = []
        self.running = True
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

    def load(self):
        """Загружает VFS в память. Возвращает сообщение о результате."""
        if not self.vfs_path:
            return "VFS не задана, используется пустой каталог"
        self.root = load_vfs(self.vfs_path)
        return f"VFS загружена: {self.vfs_path}"

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
