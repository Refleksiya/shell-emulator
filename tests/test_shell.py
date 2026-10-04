"""Тесты логики эмулятора."""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from shell import (  # noqa: E402
    Shell, ShellError, parse, read_script, vfs_name_from_path,
)

DATA = Path(__file__).parent / "data"


class TestParse(unittest.TestCase):
    """Тесты парсера."""

    def test_split(self):
        """Строка делится на слова, кавычки учитываются."""
        self.assertEqual(parse('ls "my dir"'), ["ls", "my dir"])

    def test_env_var(self):
        """Переменная окружения раскрывается."""
        os.environ["TEST_VAR"] = "hello"
        self.assertEqual(parse("ls $TEST_VAR"), ["ls", "hello"])

    def test_bad_quote(self):
        """Незакрытая кавычка — ошибка."""
        with self.assertRaises(ShellError):
            parse('ls "abc')

    def test_comment(self):
        """Всё после # отбрасывается."""
        self.assertEqual(parse("ls a # коммент"), ["ls", "a"])


class TestConfig(unittest.TestCase):
    """Тесты параметров и стартового скрипта."""

    def test_vfs_name_default(self):
        """Без пути имя VFS по умолчанию."""
        self.assertEqual(vfs_name_from_path(None), "vfs")

    def test_vfs_name_from_path(self):
        """Имя VFS берётся из пути."""
        self.assertEqual(vfs_name_from_path("a/b/my.zip"), "my.zip")

    def test_read_script(self):
        """Комментарии и пустые строки пропускаются."""
        lines = read_script(DATA / "script.txt")
        self.assertEqual(lines, [(2, "ls -l"), (4, "cd home")])

    def test_script_not_found(self):
        """Несуществующий скрипт — ошибка."""
        with self.assertRaises(ShellError):
            read_script(DATA / "nope.txt")


class TestShell(unittest.TestCase):
    """Тесты команд."""

    def setUp(self):
        """Создаёт новую оболочку перед каждым тестом."""
        self.shell = Shell()

    def test_ls_stub(self):
        """ls выводит своё имя и аргументы."""
        self.assertEqual(self.shell.execute("ls -l"), "ls, аргументы: ['-l']")

    def test_cd_stub(self):
        """cd выводит своё имя и аргументы."""
        self.assertEqual(self.shell.execute("cd a"), "cd, аргументы: ['a']")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("cd a b")

    def test_unknown_command(self):
        """Неизвестная команда — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("foo")

    def test_empty_line(self):
        """Пустая строка ничего не выводит."""
        self.assertEqual(self.shell.execute("   "), "")

    def test_exit(self):
        """exit останавливает оболочку."""
        self.shell.execute("exit")
        self.assertFalse(self.shell.running)

    def test_exit_with_args(self):
        """exit с аргументами — ошибка."""
        with self.assertRaises(ShellError):
            self.shell.execute("exit 1")


if __name__ == "__main__":
    unittest.main()
