from __future__ import annotations

from typing import Optional

import numpy as np

from sztcmh_mri_kidney_metrics.models.vmre import VmreSadcThresholdSummary


def _safe_mean(values: np.ndarray) -> Optional[float]:
    if values.size == 0:
        return None
    return float(np.mean(values))


def calculate_thresholded_metrics(vmre_image: np.ndarray, label_image: np.ndarray, sadc_image: np.ndarray, threshold: float) -> VmreSadcThresholdSummary:
    if vmre_image.shape != label_image.shape or vmre_image.shape != sadc_image.shape:
        raise ValueError("vMRE, label, and sADC dimensions do not match.")

    label_positions = np.nonzero(label_image)
    original_vmre = vmre_image[label_positions]
    original_sadc = sadc_image[label_positions]

    remove_positions = np.where(original_vmre <= threshold)
    filtered_label = np.array(label_image, copy=True)
    filtered_label[
        label_positions[0][remove_positions],
        label_positions[1][remove_positions],
        label_positions[2][remove_positions],
    ] = 0

    filtered_vmre = vmre_image[filtered_label.nonzero()]
    filtered_sadc = sadc_image[filtered_label.nonzero()]
    original_count = int(original_vmre.size)
    filtered_count = int(filtered_vmre.size)

    return VmreSadcThresholdSummary(
        origin_vmre_mean=_safe_mean(original_vmre),
        origin_sadc_mean=_safe_mean(original_sadc),
        filtered_vmre_mean=_safe_mean(filtered_vmre),
        filtered_sadc_mean=_safe_mean(filtered_sadc),
        original_count=original_count,
        filtered_count=filtered_count,
        removed_count=original_count - filtered_count,
    )
