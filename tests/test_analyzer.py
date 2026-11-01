import unittest
from green_analyzer.analyzer import analyze_source


class AnalyzerTests(unittest.TestCase):
    def test_nested_loop(self):
        self.assertTrue(any(f.rule_id == "GCA001" for f in analyze_source("for x in a:\n for y in b:\n  pass")))

    def test_membership(self):
        self.assertTrue(any(f.rule_id == "GCA002" for f in analyze_source("for x in a:\n if x in items: pass")))

    def test_syntax_error(self):
        with self.assertRaises(ValueError):
            analyze_source("def broken(:\n pass")


if __name__ == "__main__":
    unittest.main()
