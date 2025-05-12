import unittest

from textnode import TextNode, TextType
from string_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks, BlockType, block_to_block_type

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_with_code_delimiter(self):
        node = TextNode("This is text with a `codeblock` word", TextType.TEXT)
        actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("codeblock", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]

        self.assertEqual(actual_nodes, expected_nodes)
    
    def test_split_with_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        actual_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]

        self.assertEqual(actual_nodes, expected_nodes)

class TestImagesLinksExtraction(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
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
    
    def test_split_links(self):
        node = TextNode(
            "Check out this [great resource](https://example.com) and also visit [another site](https://test.org) for more info.",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("great resource", TextType.LINK, "https://example.com"),
                TextNode(" and also visit ", TextType.TEXT),
                TextNode("another site", TextType.LINK, "https://test.org"),
                TextNode(" for more info.", TextType.TEXT),                
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_edge_cases(self):
    # Test with multiple consecutive newlines and extra whitespace
        md = """
    
First block with  **bold text**
    
    

Second block with
multiple lines
and _italic_ text


- List item 1
- List item 2   
    """
    
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with  **bold text**",
                "Second block with\nmultiple lines\nand _italic_ text",
                "- List item 1\n- List item 2"
            ]
        )

class TestBlockTypes(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
        
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading level 1"), BlockType.heading)
        self.assertEqual(block_to_block_type("## Heading level 2"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Heading level 6"), BlockType.heading)
        
        self.assertEqual(block_to_block_type("#Heading with no space"), BlockType.paragraph)
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.paragraph)
        
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode goes here\n```"), BlockType.code)
        self.assertEqual(block_to_block_type("```\nmulti-line\ncode\nblock\n```"), BlockType.code)
        self.assertEqual(block_to_block_type("```only opening backticks"), BlockType.paragraph)
        
    def test_quote(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.quote)
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2\n>Line 3"), BlockType.quote)
        self.assertEqual(block_to_block_type(">Line 1\nLine 2 not starting with >"), BlockType.paragraph)

if __name__ == "__main__":
    unittest.main()