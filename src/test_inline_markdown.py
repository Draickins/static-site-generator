import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_node_not_text_type(self):
        nodes = [TextNode("Already bold", TextType.BOLD)]
        expected = [TextNode("Already bold", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), expected)

    def test_text_node_no_delimiter(self):
        nodes = [TextNode("Just plain text", TextType.TEXT)]
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_simple_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_text(self):
        node = TextNode("This is **bolded** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_text(self):
        node = TextNode("This is *italicized* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_empty_alt(self):
        text = "![](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_link_not_image(self):
        text = "This is a [link](link.com) and an ![image](image.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "link.com")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png) in the middle.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" in the middle.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![alt text](url.jpg) followed by text", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "url.jpg"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "Text followed by ![alt text](url.jpg)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "url.jpg"),
            ],
            new_nodes,
        )

    def test_split_only_image(self):
        node = TextNode("![sole image](only.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("sole image", TextType.IMAGE, "only.png")], new_nodes
        )

    def test_split_no_images(self):
        original_node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([original_node])
        self.assertListEqual([original_node], new_nodes)

    def test_split_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)

    def test_split_non_text_node(self):
        original_node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_image([original_node])
        self.assertListEqual([original_node], new_nodes)


    def test_split_image_no_alt_text(self):
        node = TextNode("Image with no alt text ![](no_alt.png) here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with no alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "no_alt.png"),
                TextNode(" here.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_empty_url(self):
        node = TextNode("![image]() is an image with empty URL", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, ""),
                TextNode(" is an image with empty URL", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com) in the middle.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in the middle.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[anchor text](url.com) followed by text", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("anchor text", TextType.LINK, "url.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Text followed by [anchor text](url.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("anchor text", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode("[sole link](only.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("sole link", TextType.LINK, "only.com")], new_nodes
        )

    def test_split_no_links(self):
        original_node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([original_node])
        self.assertListEqual([original_node], new_nodes)

    def test_split_empty_text_node_for_link(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_split_link_no_anchor_text(self):
        node = TextNode("Link with no anchor [](no_anchor.com) here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with no anchor ", TextType.TEXT),
                TextNode("", TextType.LINK, "no_anchor.com"),
                TextNode(" here.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_empty_url(self):
        node = TextNode("[link]() is a link with empty URL", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, ""),
                TextNode(" is a link with empty URL", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_full_conversion_example(self):
        text = "My favorite space opera is **Star Wars**, *especially* the original trilogy. You can `print('Hello there')` and see a picture of ![General Kenobi](https://example.com/kenobi.jpg) or visit the [official site](https://www.starwars.com/)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("My favorite space opera is ", TextType.TEXT),
            TextNode("Star Wars", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("especially", TextType.ITALIC),
            TextNode(" the original trilogy. You can ", TextType.TEXT),
            TextNode("print('Hello there')", TextType.CODE),
            TextNode(" and see a picture of ", TextType.TEXT),
            TextNode("General Kenobi", TextType.IMAGE, "https://example.com/kenobi.jpg"),
            TextNode(" or visit the ", TextType.TEXT),
            TextNode("official site", TextType.LINK, "https://www.starwars.com/"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_various_formats_interspersed(self):
        text = "A **bold** statement, followed by *italicized* thoughts and `technical_jargon`."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement, followed by ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" thoughts and ", TextType.TEXT),
            TextNode("technical_jargon", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_images_and_links_only(self):
        text = "![A cat](https://example.com/cat.png)[A dog](https://example.com/dog.html)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("A cat", TextType.IMAGE, "https://example.com/cat.png"),
            TextNode("A dog", TextType.LINK, "https://example.com/dog.html"),
        ]
        self.assertListEqual(nodes, expected)

    def test_simple_unformatted_sentence(self):
        text = "This is a sentence without any special formatting."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is a sentence without any special formatting.", TextType.TEXT)]
        self.assertListEqual(nodes, expected)

    def test_empty_string_input(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [])

    def test_error_on_unclosed_markdown(self):
        text = "This sentence has `an unclosed code block"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
