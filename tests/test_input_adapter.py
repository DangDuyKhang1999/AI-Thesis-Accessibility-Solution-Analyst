import unittest

from accessibility_analyst.input_adapter import InputAdapter, UnsupportedInputError


class InputAdapterTests(unittest.TestCase):
    def test_accepts_image_as_one_page(self):
        document = InputAdapter().from_bytes(b"png", "sample.png", "image/png")
        self.assertEqual(len(document.pages), 1)
        self.assertEqual(document.pages[0].mime_type, "image/png")

    def test_rejects_unknown_input(self):
        with self.assertRaises(UnsupportedInputError):
            InputAdapter().from_bytes(b"data", "sample.txt", "text/plain")


if __name__ == "__main__":
    unittest.main()
