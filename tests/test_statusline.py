import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import statusline  # noqa: E402


class Render(unittest.TestCase):
    def test_below_threshold(self):
        self.assertEqual(statusline.render(49, 50), "context 49%")

    def test_at_threshold(self):
        self.assertIn(statusline.NUDGE, statusline.render(50, 50))

    def test_above_threshold(self):
        line = statusline.render(80, 50)
        self.assertTrue(line.startswith("context 80%"))
        self.assertIn(statusline.NUDGE, line)

    def test_unknown(self):
        self.assertEqual(statusline.render(None, 50), "context –")

    def test_no_threshold_no_nudge(self):
        self.assertEqual(statusline.render(99, None), "context 99%")


class UsedPercentage(unittest.TestCase):
    def test_rounds(self):
        self.assertEqual(statusline.used_percentage('{"context_window":{"used_percentage":62.4}}'), 62)
        self.assertEqual(statusline.used_percentage('{"context_window":{"used_percentage":62.6}}'), 63)

    def test_unknown_input(self):
        for raw in ["", "not json", "[]", "null", "{}", '{"context_window":null}', '{"context_window":{}}',
                    '{"context_window":{"used_percentage":null}}', '{"context_window":{"used_percentage":"x"}}',
                    '{"context_window":{"used_percentage":true}}', '{"context_window":{"used_percentage":NaN}}']:
            with self.subTest(raw=raw):
                self.assertIsNone(statusline.used_percentage(raw))


class Threshold(unittest.TestCase):
    def test_real_criteria(self):
        self.assertIsInstance(statusline.fill_threshold(), int)

    def test_parses_bullet(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "criteria.md"
            path.write_text("- **Hand off** ... or context fill, as the user reports it, reaches **35%** *(provisional)*")
            self.assertEqual(statusline.fill_threshold(path), 35)

    def test_parse_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "criteria.md"
            path.write_text("nothing here")
            self.assertIsNone(statusline.fill_threshold(path))
            self.assertIsNone(statusline.fill_threshold(pathlib.Path(tmp) / "missing.md"))


if __name__ == "__main__":
    unittest.main()
