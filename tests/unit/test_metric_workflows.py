import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.services.metric_workflows import (
    collect_nifti_files,
    pair_nifti_files,
)


class MetricWorkflowTests(unittest.TestCase):
    def test_collect_nifti_files_ignores_non_nifti_files(self):
        with tempfile.TemporaryDirectory() as work_dir:
            base = Path(work_dir)
            (base / "a.nii").write_text("a", encoding="utf-8")
            (base / "b.nii.gz").write_text("b", encoding="utf-8")
            (base / "desktop.ini").write_text("system", encoding="utf-8")

            result = collect_nifti_files(work_dir)

            self.assertEqual([path.name for path in result], ["a.nii", "b.nii.gz"])

    def test_pair_nifti_files_matches_by_patient_key_and_ignores_extra_labels(self):
        with tempfile.TemporaryDirectory() as image_dir, tempfile.TemporaryDirectory() as label_dir:
            image_base = Path(image_dir)
            label_base = Path(label_dir)
            (image_base / "005-stiff_map.nii").write_text("a", encoding="utf-8")
            (image_base / "013_stiff_map.nii").write_text("b", encoding="utf-8")
            (label_base / "005_DWI_kidney.nii").write_text("c", encoding="utf-8")
            (label_base / "013_DWI_kidney.nii").write_text("d", encoding="utf-8")
            (label_base / "999_DWI_kidney.nii").write_text("e", encoding="utf-8")

            pairs = pair_nifti_files(image_dir, label_dir)

            self.assertEqual(
                [(image.name, label.name) for image, label in pairs],
                [
                    ("005-stiff_map.nii", "005_DWI_kidney.nii"),
                    ("013_stiff_map.nii", "013_DWI_kidney.nii"),
                ],
            )


if __name__ == "__main__":
    unittest.main()
