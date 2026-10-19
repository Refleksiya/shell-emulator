"""Тесты виртуальной файловой системы."""

import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from errors import ShellError
from vfs import load_vfs, resolve


def make_zip(folder):
    """Создаёт тестовый ZIP-архив и возвращает путь к нему."""
    path = Path(folder) / "test.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("a.txt", "привет")
        archive.writestr("docs/b.txt", "текст")
        archive.writestr("docs/sub/c.txt", "ещё текст")
    return path


class TestVfs(unittest.TestCase):
    """Тесты загрузки VFS и поиска путей."""

    def setUp(self):
        """Создаёт временный архив и загружает его."""
        self.folder = TemporaryDirectory()
        self.root = load_vfs(make_zip(self.folder.name))

    def tearDown(self):
        """Удаляет временную папку."""
        self.folder.cleanup()

    def test_files_loaded(self):
        """В корне появились файл и папка."""
        self.assertEqual(sorted(self.root.children), ["a.txt", "docs"])

    def test_nested_file(self):
        """Файл третьего уровня доступен по пути."""
        node, _ = resolve(self.root, [], "docs/sub/c.txt")
        self.assertFalse(node.is_dir)

    def test_parent_path(self):
        """Путь с .. поднимается на уровень выше."""
        node, parts = resolve(self.root, ["docs", "sub"], "../b.txt")
        self.assertEqual(parts, ["docs", "b.txt"])
        self.assertEqual(node.name, "b.txt")

    def test_base64(self):
        """Содержимое файла хранится в base64."""
        node, _ = resolve(self.root, [], "a.txt")
        self.assertEqual(node.data, "0L/RgNC40LLQtdGC")

    def test_missing_path(self):
        """Несуществующий путь — ошибка."""
        with self.assertRaises(ShellError):
            resolve(self.root, [], "nope.txt")

    def test_vfs_not_found(self):
        """Отсутствующий архив — ошибка."""
        with self.assertRaises(ShellError):
            load_vfs(Path(self.folder.name) / "nope.zip")

    def test_bad_format(self):
        """Файл не ZIP — ошибка."""
        bad = Path(self.folder.name) / "bad.zip"
        bad.write_text("это не архив", encoding="utf-8")
        with self.assertRaises(ShellError):
            load_vfs(bad)


if __name__ == "__main__":
    unittest.main()
