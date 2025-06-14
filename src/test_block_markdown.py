import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_extra_newlines_are_ignored(self):
        md = """
First block, standing tall.


Second block, after a fall.



Third block, answers the call.
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "First block, standing tall.",
                "Second block, after a fall.",
                "Third block, answers the call.",
            ]
        )

    def test_leading_and_trailing_whitespace(self):
        md = """
  A block that starts with spaces.

A block that ends with spaces.

  A block with both.
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "A block that starts with spaces.",
                "A block that ends with spaces.",
                "A block with both.",
            ]
        )

    def test_single_block_document(self):
        md = "### Just a single heading, nothing more."
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "### Just a single heading, nothing more."
            ]
        )

    def test_empty_string_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, [])

    def test_whitespace_only_input(self):
        md = "   \n\n   \n\n  "
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_not_heading(self):
        self.assertEqual(block_to_block_type("####### Not a Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ncode\nlines\n```"), BlockType.CODE)

    def test_not_code(self):
        self.assertEqual(block_to_block_type("```code"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)

    def test_not_quote(self):
        self.assertEqual(block_to_block_type("> line 1\nline 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

    def test_not_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1\n- item 2"), BlockType.UNORDERED_LIST) # This is valid
        self.assertEqual(block_to_block_type("* item 1\nitem 2"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\n2.item 2"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Another paragraph\nwith two lines."), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
