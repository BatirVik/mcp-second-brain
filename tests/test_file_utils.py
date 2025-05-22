from pathlib import Path

from src.file_utils import get_dir_files_recursive

STATIC = Path(__file__).parent / "static"


def test_get_dir_files_recursive():
    paths = get_dir_files_recursive(STATIC)
    assert set(paths) == {
        STATIC / "h1.txt",
        STATIC / "folder" / "h2.txt",
        STATIC / "folder" / "h3.txt",
    }
