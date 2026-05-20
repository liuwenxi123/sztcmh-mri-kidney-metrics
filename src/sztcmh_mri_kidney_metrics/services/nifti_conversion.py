from __future__ import annotations

from pathlib import Path

import nibabel as nib


def convert_directory_to_gz(directory: str) -> list[Path]:
    converted: list[Path] = []
    for path in Path(directory).iterdir():
        if path.is_file() and path.name.endswith('.nii'):
            image = nib.load(str(path))
            destination = path.with_name(path.name.replace('.nii', '.nii.gz'))
            nib.save(image, str(destination))
            path.unlink()
            converted.append(destination)
    return converted


def convert_directory_from_gz(directory: str) -> list[Path]:
    converted: list[Path] = []
    for path in Path(directory).iterdir():
        if path.is_file() and path.name.endswith('.nii.gz'):
            image = nib.load(str(path))
            destination = path.with_suffix('')
            nib.save(nib.Nifti1Image(image.get_fdata(), image.affine), str(destination))
            path.unlink()
            converted.append(destination)
    return converted
