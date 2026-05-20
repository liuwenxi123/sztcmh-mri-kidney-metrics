import os
import sys
import unittest

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.domain.vmre_sadc import calculate_thresholded_metrics


class VmreSadcTests(unittest.TestCase):
    def test_threshold_filtering_removes_low_vmre_points(self):
        vmre = np.array([[[1.0, 4.0], [0.0, 6.0]]])
        label = np.array([[[1, 1], [0, 1]]])
        sadc = np.array([[[10.0, 20.0], [0.0, 30.0]]])

        result = calculate_thresholded_metrics(vmre, label, sadc, threshold=4.0)

        self.assertEqual(result.original_count, 3)
        self.assertEqual(result.filtered_count, 1)
        self.assertAlmostEqual(result.origin_vmre_mean, 11 / 3)
        self.assertAlmostEqual(result.origin_sadc_mean, 20.0)
        self.assertAlmostEqual(result.filtered_vmre_mean, 6.0)
        self.assertAlmostEqual(result.filtered_sadc_mean, 30.0)


if __name__ == "__main__":
    unittest.main()

