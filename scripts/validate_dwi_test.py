from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sztcmh_mri_kidney_metrics.services.metric_workflows import collect_nifti_files


def main(target_dir: str) -> int:
    target = Path(target_dir)
    if not target.exists():
        raise SystemExit(f'Target path does not exist: {target}')
    summary = {'target': str(target), 'children': sorted([child.name for child in target.iterdir()])[:50], 'nifti_files_in_root': [path.name for path in collect_nifti_files(str(target))] if target.is_dir() else []}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
