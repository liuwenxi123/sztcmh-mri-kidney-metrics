from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class RegionMetrics:
    mean: Optional[float]
    volume: int


@dataclass(slots=True)
class KidneyMetricSummary:
    all_region: RegionMetrics
    left_region: RegionMetrics
    right_region: RegionMetrics


@dataclass(slots=True)
class MiddleSliceMetricSummary:
    all_mean: Optional[float]
    left_mean: Optional[float]
    right_mean: Optional[float]
