from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_rows_to_excel(rows: list[dict], output_path: str) -> Path:
    frame = pd.DataFrame(rows)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_excel(path, index=False)
    return path
