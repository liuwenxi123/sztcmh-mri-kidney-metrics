import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.services.rename_service import apply_rename_plan, build_rename_plan


class RenameServiceTests(unittest.TestCase):
    def test_build_and_apply_rename_plan(self):
        with tempfile.TemporaryDirectory() as work_dir:
            path = Path(work_dir) / "case_old_name.nii.gz"
            path.write_text("demo", encoding="utf-8")

            plan = build_rename_plan(work_dir, "old", "new")
            apply_rename_plan(plan)

            self.assertEqual(len(plan), 1)
            self.assertFalse(path.exists())
            self.assertTrue((Path(work_dir) / "case_new_name.nii.gz").exists())


if __name__ == "__main__":
    unittest.main()
