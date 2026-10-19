"""Тесты команд ls и cd на загруженной VFS."""

import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from errors import ShellError
from shell import Shell


class TestCommands(unittest.TestCase):
    """Тесты работы команд с VFS."""

    def setUp(self):
        """Создаёт VFS из временного архива и загружает её."""
        self.folder = TemporaryDirectory()
        path = Path(self.folder.name) / "test.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("a.txt", "текст")
            archive.writestr("docs/b.txt", "текст")
            archive.writestr("docs/sub/c.txt", "текст")
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
        self.assertEqual(self.shell.execute("ls docs"), "b.txt  sub/")

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


class TestChanges(TestCommands):
    """Тесты команд rm и cp, изменяющих VFS в памяти."""

    def test_rm_file(self):
        """rm удаляет файл."""
        self.shell.execute("rm a.txt")
        self.assertEqual(self.shell.execute("ls"), "docs/")

    def test_rm_dir_without_flag(self):
        """rm каталога без -r — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("rm docs")

    def test_rm_dir(self):
        """rm -r удаляет каталог со всем содержимым."""
        self.shell.execute("rm -r docs")
        self.assertEqual(self.shell.execute("ls"), "a.txt")

    def test_cp_file(self):
        """cp создаёт копию файла под новым именем."""
        self.shell.execute("cp a.txt copy.txt")
        self.assertEqual(self.shell.execute("ls"), "a.txt  copy.txt  docs/")

    def test_cp_into_dir(self):
        """cp в каталог сохраняет имя файла."""
        self.shell.execute("cp a.txt docs")
        self.assertEqual(self.shell.execute("ls docs"), "a.txt  b.txt  sub/")

    def test_cp_dir(self):
        """cp -r копирует каталог целиком."""
        self.shell.execute("cp -r docs backup")
        self.assertEqual(self.shell.execute("ls backup"), "b.txt  sub/")

    def test_cp_dir_without_flag(self):
        """cp каталога без -r — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("cp docs backup")

    def test_source_file_not_changed(self):
        """Исходный архив не меняется: удаление только в памяти."""
        self.shell.execute("rm a.txt")
        other = Shell(self.shell.vfs_path)
        other.load()
        self.assertEqual(other.execute("ls"), "a.txt  docs/")


if __name__ == "__main__":
    unittest.main()
