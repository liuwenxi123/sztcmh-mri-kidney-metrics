from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class VmreSadcThresholdSummary:
    origin_vmre_mean: Optional[float]
    origin_sadc_mean: Optional[float]
    filtered_vmre_mean: Optional[float]
    filtered_sadc_mean: Optional[float]
    original_count: int
    filtered_count: int
    removed_count: int
