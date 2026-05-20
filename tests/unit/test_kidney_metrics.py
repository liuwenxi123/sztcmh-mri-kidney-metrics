import os
import sys
import unittest

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sztcmh_mri_kidney_metrics.domain.kidney_metrics import (
    calculate_kidney_metrics,
    calculate_middle_slice_metrics,
)


class KidneyMetricsTests(unittest.TestCase):
    def test_calculate_kidney_metrics_returns_all_left_right_values(self):
        image = np.arange(1, 17, dtype=float).reshape(4, 2, 2)
        label = np.zeros((4, 2, 2), dtype=int)
        label[0, 0, 0] = 1
        label[1, 1, 1] = 1
        label[2, 0, 0] = 1
        label[3, 1, 1] = 1

        result = calculate_kidney_metrics(image, label)

        self.assertEqual(result.all_region.volume, 4)
        self.assertAlmostEqual(result.all_region.mean, 8.5)
        self.assertEqual(result.left_region.volume, 2)
        self.assertAlmostEqual(result.left_region.mean, 4.5)
        self.assertEqual(result.right_region.volume, 2)
        self.assertAlmostEqual(result.right_region.mean, 12.5)

    def test_calculate_middle_slice_metrics_uses_legacy_window_selection(self):
        image = np.ones((4, 2, 5), dtype=float)
        image[:, :, 2] = 3.0
        image[:, :, 3] = 5.0
        label = np.zeros((4, 2, 5), dtype=int)
        label[:, :, 1:4] = 1

        result = calculate_middle_slice_metrics(image, label)

        self.assertAlmostEqual(result.all_mean, 2.0)
        self.assertAlmostEqual(result.left_mean, 2.0)
        self.assertAlmostEqual(result.right_mean, 2.0)

    def test_shape_mismatch_raises_value_error(self):
        image = np.ones((2, 2, 2), dtype=float)
        label = np.ones((2, 2, 3), dtype=int)

        with self.assertRaises(ValueError):
            calculate_kidney_metrics(image, label)


if __name__ == "__main__":
    unittest.main()

