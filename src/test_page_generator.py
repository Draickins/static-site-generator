import unittest
from page_generator import extract_title

class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# This is the main title

This is some paragraph text.

## This is a subtitle
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is the main title")

    def test_extract_title_no_h1(self):
        markdown = """
This is some text but there is no H1 header.
## This is an H2
"""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_with_extra_whitespace(self):
        markdown = "#   A title with spaces   "
        title = extract_title(markdown)
        self.assertEqual(title, "A title with spaces")

if __name__ == '__main__':
    unittest.main()
