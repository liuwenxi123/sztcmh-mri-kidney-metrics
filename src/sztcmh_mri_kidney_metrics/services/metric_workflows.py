from __future__ import annotations

from pathlib import Path

import nibabel as nib

from sztcmh_mri_kidney_metrics.domain.kidney_metrics import calculate_kidney_metrics, calculate_middle_slice_metrics


def collect_nifti_files(directory: str) -> list[Path]:
    base = Path(directory)
    return sorted([path for path in base.iterdir() if path.suffix == '.nii' or path.name.endswith('.nii.gz')])


def load_nifti_array(path: str):
    return nib.load(path).get_fdata()


def strip_nifti_suffix(filename: str) -> str:
    if filename.endswith('.nii.gz'):
        return filename[:-7]
    if filename.endswith('.nii'):
        return filename[:-4]
    return filename


def pair_nifti_files(image_dir: str, label_dir: str) -> list[tuple[Path, Path]]:
    image_files = collect_nifti_files(image_dir)
    label_files = collect_nifti_files(label_dir)
    if len(image_files) != len(label_files):
        raise ValueError('Image and label file counts do not match.')
    return list(zip(image_files, label_files))


def calculate_single_pair_metrics(image_path: str, label_path: str):
    return calculate_kidney_metrics(load_nifti_array(image_path), load_nifti_array(label_path))


def calculate_batch_metric_rows(image_dir: str, label_dir: str) -> list[dict]:
    rows: list[dict] = []
    for image_path, label_path in pair_nifti_files(image_dir, label_dir):
        summary = calculate_single_pair_metrics(str(image_path), str(label_path))
        rows.append({'PatientID': strip_nifti_suffix(image_path.name), 'All Mean': summary.all_region.mean, 'Left Mean': summary.left_region.mean, 'Right Mean': summary.right_region.mean, 'All Volume': summary.all_region.volume, 'Left Volume': summary.left_region.volume, 'Right Volume': summary.right_region.volume})
    return rows


def calculate_batch_middle_slice_rows(image_dir: str, label_dir: str) -> list[dict]:
    rows: list[dict] = []
    for image_path, label_path in pair_nifti_files(image_dir, label_dir):
        summary = calculate_middle_slice_metrics(load_nifti_array(str(image_path)), load_nifti_array(str(label_path)))
        rows.append({'PatientID': strip_nifti_suffix(image_path.name), 'All Mean': summary.all_mean, 'Left Mean': summary.left_mean, 'Right Mean': summary.right_mean})
    return rows
