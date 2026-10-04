"""Собирает ZIP-архивы VFS из папок vfs_src в папку build.

Архивы не хранятся в репозитории, их создаёт этот скрипт.
"""

import pathlib
import zipfile

SOURCE_DIR = pathlib.Path("vfs_src")
BUILD_DIR = pathlib.Path("build")


def pack(folder):
    """Упаковывает одну папку в ZIP-архив."""
    archive_path = BUILD_DIR / f"{folder.name}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for item in sorted(folder.rglob("*")):
            archive.write(item, item.relative_to(folder).as_posix())
    print(f"создан {archive_path}")


def main():
    """Собирает архивы для всех папок внутри vfs_src."""
    BUILD_DIR.mkdir(exist_ok=True)
    for folder in sorted(SOURCE_DIR.iterdir()):
        if folder.is_dir():
            pack(folder)


if __name__ == "__main__":
    main()
