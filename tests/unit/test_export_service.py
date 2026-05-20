import os
import sys
import tempfile
import unittest

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.services.export_service import export_rows_to_excel


class ExportServiceTests(unittest.TestCase):
    def test_export_rows_to_excel_writes_expected_columns(self):
        with tempfile.TemporaryDirectory() as work_dir:
            output = os.path.join(work_dir, "result.xlsx")
            rows = [{"PatientID": "case-001", "All Mean": 1.23, "Left Mean": 2.34}]

            export_rows_to_excel(rows, output)

            frame = pd.read_excel(output)
            self.assertEqual(list(frame.columns), ["PatientID", "All Mean", "Left Mean"])
            self.assertEqual(frame.iloc[0]["PatientID"], "case-001")


if __name__ == "__main__":
    unittest.main()

