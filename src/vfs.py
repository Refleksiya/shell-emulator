"""Виртуальная файловая система в памяти (источник — ZIP-архив)."""

import base64
import zipfile

from errors import ShellError

ROOT_NAME = "/"


class Node:
    """Узел VFS: папка (children) или файл (data в base64)."""

    def __init__(self, name, is_dir, data=""):
        """Создаёт узел с именем name."""
        self.name = name
        self.is_dir = is_dir
        self.data = data
        self.children = {}


def make_dirs(root, parts):
    """Создаёт цепочку папок по списку имён и возвращает последнюю."""
    node = root
    for part in parts:
        if part not in node.children:
            node.children[part] = Node(part, True)
        node = node.children[part]
    return node


def split_path(name):
    """Делит путь из архива на список имён без пустых частей."""
    return [part for part in name.split("/") if part]


def load_vfs(path):
    """Загружает VFS из ZIP-архива в память. Содержимое файлов
    хранится в виде base64, сам архив не изменяется."""
    try:
        archive = zipfile.ZipFile(path)
    except FileNotFoundError:
        raise ShellError(f"VFS не найдена: {path}")
    except zipfile.BadZipFile:
        raise ShellError(f"неверный формат VFS, нужен ZIP: {path}")
    root = Node(ROOT_NAME, True)
    with archive:
        for info in archive.infolist():
            parts = split_path(info.filename)
            if not parts:
                continue
            if info.is_dir():
                make_dirs(root, parts)
            else:
                folder = make_dirs(root, parts[:-1])
                data = base64.b64encode(archive.read(info)).decode()
                folder.children[parts[-1]] = Node(parts[-1], False, data)
    return root


def copy_node(node, name):
    """Создаёт копию узла VFS с новым именем."""
    copy = Node(name, node.is_dir, node.data)
    for child in node.children.values():
        copy.children[child.name] = copy_node(child, child.name)
    return copy


def walk_path(cwd, path):
    """Собирает список имён итогового пути с учётом . и .."""
    parts = [] if path.startswith("/") else list(cwd)
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return parts


def resolve(root, cwd, path):
    """Находит узел по пути. Возвращает пару (узел, список имён)."""
    parts = walk_path(cwd, path)
    node = root
    for part in parts:
        if not node.is_dir or part not in node.children:
            raise ShellError(f"нет такого файла или каталога: {path}")
        node = node.children[part]
    return node, parts
