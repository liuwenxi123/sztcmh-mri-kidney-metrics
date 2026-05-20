from __future__ import annotations

from typing import Optional

import numpy as np

from sztcmh_mri_kidney_metrics.models.metrics import KidneyMetricSummary, MiddleSliceMetricSummary, RegionMetrics


def _safe_mean(values: np.ndarray) -> Optional[float]:
    if values.size == 0:
        return None
    return float(np.mean(values))


def _ensure_matching_shape(image_data: np.ndarray, label_data: np.ndarray) -> None:
    if image_data.shape != label_data.shape:
        raise ValueError("Image and label dimensions do not match.")


def _region_metrics(image_data: np.ndarray, mask: np.ndarray) -> RegionMetrics:
    values = image_data[mask > 0]
    return RegionMetrics(mean=_safe_mean(values), volume=int(np.sum(mask > 0)))


def calculate_kidney_metrics(image_data: np.ndarray, label_data: np.ndarray) -> KidneyMetricSummary:
    _ensure_matching_shape(image_data, label_data)
    midline_index = image_data.shape[0] // 2
    return KidneyMetricSummary(
        all_region=_region_metrics(image_data, label_data),
        left_region=_region_metrics(image_data[:midline_index, :, :], label_data[:midline_index, :, :]),
        right_region=_region_metrics(image_data[midline_index:, :, :], label_data[midline_index:, :, :]),
    )


def _find_slice_bounds(mask: np.ndarray) -> tuple[Optional[int], Optional[int]]:
    first = None
    last = None
    for index in range(mask.shape[2]):
        if np.any(mask[:, :, index] > 0):
            if first is None:
                first = index
            last = index
    return first, last


def _legacy_middle_slice(first: Optional[int], last: Optional[int]) -> slice:
    if first is None or last is None:
        return slice(0, 0)
    middle = (first + last) / 2
    return slice(int(middle - 1), int(middle + 1))


def calculate_middle_slice_metrics(image_data: np.ndarray, label_data: np.ndarray) -> MiddleSliceMetricSummary:
    _ensure_matching_shape(image_data, label_data)
    midline_index = image_data.shape[0] // 2
    all_slice = _legacy_middle_slice(*_find_slice_bounds(label_data))
    left_slice = _legacy_middle_slice(*_find_slice_bounds(label_data[:midline_index, :, :]))
    right_slice = _legacy_middle_slice(*_find_slice_bounds(label_data[midline_index:, :, :]))

    all_values = image_data[:, :, all_slice][label_data[:, :, all_slice] > 0]
    left_values = image_data[:midline_index, :, left_slice][label_data[:midline_index, :, left_slice] > 0]
    right_values = image_data[midline_index:, :, right_slice][label_data[midline_index:, :, right_slice] > 0]
    return MiddleSliceMetricSummary(
        all_mean=_safe_mean(all_values),
        left_mean=_safe_mean(left_values),
        right_mean=_safe_mean(right_values),
    )
