from __future__ import annotations

from pathlib import Path

import nibabel as nib

from sztcmh_mri_kidney_metrics.domain.vmre_sadc import calculate_thresholded_metrics
from sztcmh_mri_kidney_metrics.services.metric_workflows import collect_nifti_files, strip_nifti_suffix


def calculate_single_threshold_metrics(vmre_path: str, label_path: str, sadc_path: str, threshold: float) -> dict:
    vmre = nib.load(vmre_path).get_fdata()
    label = nib.load(label_path).get_fdata()
    sadc = nib.load(sadc_path).get_fdata()
    summary = calculate_thresholded_metrics(vmre, label, sadc, threshold)
    return {'Image_File': strip_nifti_suffix(Path(vmre_path).name), 'origin_vMRE': summary.origin_vmre_mean, 'origin_sADC': summary.origin_sadc_mean, 'new_vMRE': summary.filtered_vmre_mean, 'new_sADC': summary.filtered_sadc_mean, 'origin_count': summary.original_count, 'filtered_count': summary.filtered_count, 'removed_count': summary.removed_count}


def calculate_directory_threshold_metrics(vmre_dir: str, label_dir: str, sadc_dir: str, threshold: float) -> list[dict]:
    vmre_files = collect_nifti_files(vmre_dir)
    label_files = collect_nifti_files(label_dir)
    sadc_files = collect_nifti_files(sadc_dir)
    if not (len(vmre_files) == len(label_files) == len(sadc_files)):
        raise ValueError('vMRE, label, and sADC file counts do not match.')
    return [calculate_single_threshold_metrics(str(vmre_path), str(label_path), str(sadc_path), threshold) for vmre_path, label_path, sadc_path in zip(vmre_files, label_files, sadc_files)]
