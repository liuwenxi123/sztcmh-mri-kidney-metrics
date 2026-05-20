from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RenameOperation:
    source: Path
    destination: Path


def build_rename_plan(directory: str, original_key: str, rename_key: str) -> list[RenameOperation]:
    base = Path(directory)
    plan: list[RenameOperation] = []
    for path in sorted(base.iterdir()):
        if path.is_file() and original_key in path.name:
            plan.append(RenameOperation(source=path, destination=path.with_name(path.name.replace(original_key, rename_key))))
    return plan


def apply_rename_plan(plan: list[RenameOperation]) -> list[RenameOperation]:
    for operation in plan:
        operation.source.rename(operation.destination)
    return plan
