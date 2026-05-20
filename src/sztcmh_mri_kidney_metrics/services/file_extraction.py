from __future__ import annotations

import shutil
from enum import Enum
from pathlib import Path


class ExtractionMode(str, Enum):
    DIRECT = "direct"
    FIRST_LEVEL = "first_level"
    SECOND_LEVEL = "second_level"


def _iter_matching_files(source_dir: Path, nested_key: str, filename_key: str, mode: ExtractionMode):
    if mode is ExtractionMode.DIRECT:
        for path in source_dir.iterdir():
            if path.is_file() and filename_key in path.name:
                yield path
        return

    if mode is ExtractionMode.FIRST_LEVEL:
        for child in source_dir.iterdir():
            if child.is_dir():
                for path in child.iterdir():
                    if path.is_file() and filename_key in path.name:
                        yield path
        return

    if mode is ExtractionMode.SECOND_LEVEL:
        for child in source_dir.iterdir():
            if child.is_dir():
                nested = child / nested_key
                if nested.exists() and nested.is_dir():
                    for path in nested.iterdir():
                        if path.is_file() and filename_key in path.name:
                            yield path


def extract_matching_files(source_dir: str, destination_dir: str, nested_key: str, filename_key: str, mode: ExtractionMode) -> list[Path]:
    source = Path(source_dir)
    target = Path(destination_dir)
    target.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for path in _iter_matching_files(source, nested_key, filename_key, mode):
        destination = target / path.name
        shutil.copy2(path, destination)
        copied.append(destination)
    return copied
