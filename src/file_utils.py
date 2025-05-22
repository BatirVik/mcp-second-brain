from pathlib import Path

from src.types import StrPath


def get_dir_files_recursive(dir: StrPath) -> list[Path]:
    return [item for item in Path(dir).rglob("*") if item.is_file()]
