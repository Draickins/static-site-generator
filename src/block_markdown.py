from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            filtered_blocks.append(stripped_block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    is_ulist = True
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            is_ulist = False
            break
    if is_ulist:
        return BlockType.UNORDERED_LIST

    if lines[0].startswith("1. "):
        is_olist = True
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                is_olist = False
                break
        if is_olist:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return children


def paragraph_to_html_node(block):
    content = " ".join(block.split('\n'))
    children = text_to_children(content)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == '#':
        level += 1
    text = block[level:].lstrip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block[3:-3]
    if text.startswith('\n'):
        text = text[1:]
    code_child = LeafNode("code", text)
    return ParentNode("pre", [code_child])


def quote_to_html_node(block):
    lines = block.split('\n')
    cleaned_lines = [line.lstrip('> ').strip() for line in lines]
    content = " ".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def olist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item.split(". ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", children)
