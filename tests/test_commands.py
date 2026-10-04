"""Тесты команд ls и cd на загруженной VFS."""

import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from errors import ShellError  # noqa: E402
from shell import Shell  # noqa: E402


class TestCommands(unittest.TestCase):
    """Тесты работы команд с VFS."""

    def setUp(self):
        """Создаёт VFS из временного архива и загружает её."""
        self.folder = TemporaryDirectory()
        path = Path(self.folder.name) / "test.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("a.txt", "текст")
            archive.writestr("docs/b.txt", "текст")
        self.shell = Shell(path)
        self.shell.load()

    def tearDown(self):
        """Удаляет временную папку."""
        self.folder.cleanup()

    def test_ls_root(self):
        """ls показывает файлы и папки корня."""
        self.assertEqual(self.shell.execute("ls"), "a.txt  docs/")

    def test_ls_path(self):
        """ls показывает содержимое указанного каталога."""
        self.assertEqual(self.shell.execute("ls docs"), "b.txt")

    def test_ls_missing(self):
        """ls по несуществующему пути — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("ls nope")

    def test_cd_and_prompt(self):
        """cd меняет текущий каталог и приглашение."""
        self.shell.execute("cd docs")
        self.assertEqual(self.shell.prompt(), "/docs$ ")

    def test_cd_back(self):
        """cd .. возвращает в корень."""
        self.shell.execute("cd docs")
        self.shell.execute("cd ..")
        self.assertEqual(self.shell.prompt(), "/$ ")

    def test_cd_to_file(self):
        """cd в файл — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("cd a.txt")


if __name__ == "__main__":
    unittest.main()
