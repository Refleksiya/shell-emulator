"""Логика эмулятора: разбор строки и выполнение команд."""

import os
import shlex
import time

from errors import ShellError
from vfs import Node, ROOT_NAME, copy_node, load_vfs, resolve

DEFAULT_VFS_NAME = "vfs"
MAX_PATH_ARGS = 1
COMMENT = "#"
SYSTEM_NAME = "EmulatorOS"
SYSTEM_VERSION = "1.0"
MACHINE = "x86_64"
SECONDS_IN_MINUTE = 60
NAMES_SEPARATOR = "  "
RECURSIVE_FLAG = "-r"
CP_ARGS_COUNT = 2


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


def format_name(node):
    """Имя узла для вывода: у папки в конце добавляется слеш."""
    return node.name + "/" if node.is_dir else node.name


def one_path(args, command):
    """Возвращает путь из аргументов команды (не больше одного)."""
    if len(args) > MAX_PATH_ARGS:
        raise ShellError(f"{command}: слишком много аргументов")
    return args[0] if args else ""


def split_flag(args, flag):
    """Отделяет флаг от остальных аргументов."""
    return flag in args, [arg for arg in args if arg != flag]


def parent_path_of(path):
    """Возвращает путь к родительскому каталогу и имя в конце пути."""
    folder, _, name = path.rpartition("/")
    if not folder:
        folder = "/" if path.startswith("/") else "."
    return folder, name


class Shell:
    """Эмулятор оболочки: хранит состояние и выполняет команды."""

    def __init__(self, vfs_path=None):
        """Создаёт оболочку. vfs_path — путь к VFS (может быть None)."""
        self.vfs_path = vfs_path
        self.vfs_name = vfs_name_from_path(vfs_path)
        self.root = Node(ROOT_NAME, True)
        self.cwd = []
        self.running = True
        self.start_time = time.monotonic()
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "uname": self.cmd_uname,
            "echo": self.cmd_echo,
            "uptime": self.cmd_uptime,
            "rm": self.cmd_rm,
            "cp": self.cmd_cp,
            "exit": self.cmd_exit,
        }

    def prompt(self):
        """Приглашение к вводу с текущим каталогом."""
        return "/" + "/".join(self.cwd) + "$ "

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
        """Выводит содержимое каталога или имя файла."""
        path = one_path(args, "ls") or "."
        node, _ = resolve(self.root, self.cwd, path)
        if not node.is_dir:
            return node.name
        names = [format_name(child) for child in node.children.values()]
        return NAMES_SEPARATOR.join(sorted(names))

    def cmd_cd(self, args):
        """Переходит в каталог VFS."""
        path = one_path(args, "cd") or "/"
        node, parts = resolve(self.root, self.cwd, path)
        if not node.is_dir:
            raise ShellError(f"cd: не является каталогом: {path}")
        self.cwd = parts
        return ""

    def cmd_uname(self, args):
        """Выводит сведения о системе, с -a — подробные."""
        if not args:
            return SYSTEM_NAME
        if args == ["-a"]:
            return f"{SYSTEM_NAME} {self.vfs_name} {SYSTEM_VERSION} {MACHINE}"
        raise ShellError(f"uname: неизвестный аргумент: {args[0]}")

    def cmd_echo(self, args):
        """Выводит свои аргументы через пробел."""
        return " ".join(args)

    def cmd_uptime(self, args):
        """Выводит время работы эмулятора."""
        if args:
            raise ShellError("uptime: команда не принимает аргументы")
        seconds = int(time.monotonic() - self.start_time)
        minutes = seconds // SECONDS_IN_MINUTE
        return f"время работы: {minutes} мин {seconds % SECONDS_IN_MINUTE} с"

    def directory(self, path):
        """Находит каталог по пути."""
        node, _ = resolve(self.root, self.cwd, path)
        if not node.is_dir:
            raise ShellError(f"не является каталогом: {path}")
        return node

    def cmd_rm(self, args):
        """Удаляет файл или каталог (с -r) в памяти."""
        recursive, paths = split_flag(args, RECURSIVE_FLAG)
        path = one_path(paths, "rm")
        if not path:
            raise ShellError("rm: не указан путь")
        node, parts = resolve(self.root, self.cwd, path)
        if not parts:
            raise ShellError("rm: нельзя удалить корень VFS")
        if node.is_dir and not recursive:
            raise ShellError(f"rm: это каталог, нужен -r: {path}")
        folder, name = parent_path_of(path)
        del self.directory(folder).children[name or node.name]
        return ""

    def cmd_cp(self, args):
        """Копирует файл или каталог (с -r) внутри памяти."""
        recursive, paths = split_flag(args, RECURSIVE_FLAG)
        if len(paths) != CP_ARGS_COUNT:
            raise ShellError("cp: нужны источник и приёмник")
        source, _ = resolve(self.root, self.cwd, paths[0])
        if source.is_dir and not recursive:
            raise ShellError(f"cp: это каталог, нужен -r: {paths[0]}")
        folder, name = self.target_of(paths[1], source.name)
        folder.children[name] = copy_node(source, name)
        return ""

    def target_of(self, path, default_name):
        """Определяет каталог и имя, под которым сохранить копию."""
        if path.endswith("/"):
            return self.directory(path), default_name
        folder, name = parent_path_of(path)
        parent = self.directory(folder)
        child = parent.children.get(name)
        if child is not None and child.is_dir:
            return child, default_name
        return parent, name

    def cmd_exit(self, args):
        """Завершает работу эмулятора."""
        if args:
            raise ShellError("exit: команда не принимает аргументы")
        self.running = False
        return ""
