import unittest
from green_analyzer.benchmark import compare_functions


class BenchmarkTests(unittest.TestCase):
    def test_equivalent_outputs(self):
        r = compare_functions(sorted, sorted, ([3, 1, 2],), repeats=2)
        self.assertTrue(r["outputs_equivalent"])
        self.assertIsNotNone(r["baseline"])

    def test_mismatch_not_timed(self):
        r = compare_functions(sorted, list, ([3, 1, 2],), repeats=2)
        self.assertFalse(r["outputs_equivalent"])
        self.assertIsNone(r["baseline"])


if __name__ == "__main__":
    unittest.main()
