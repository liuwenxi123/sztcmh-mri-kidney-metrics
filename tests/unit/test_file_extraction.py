import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.services.file_extraction import ExtractionMode, extract_matching_files


class FileExtractionTests(unittest.TestCase):
    def test_extract_matching_files_from_second_level_folder(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            nested = Path(source_dir) / "case01" / "MRE1"
            nested.mkdir(parents=True)
            file_path = nested / "kidney_mask.nii.gz"
            file_path.write_text("demo", encoding="utf-8")

            copied = extract_matching_files(
                source_dir=source_dir,
                destination_dir=target_dir,
                nested_key="MRE1",
                filename_key="kidney",
                mode=ExtractionMode.SECOND_LEVEL,
            )

            self.assertEqual(len(copied), 1)
            self.assertTrue((Path(target_dir) / "kidney_mask.nii.gz").exists())


if __name__ == "__main__":
    unittest.main()
