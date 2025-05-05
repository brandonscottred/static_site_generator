import unittest

from textnode import TextNode, TextType
from string_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link

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

if __name__ == "__main__":
    unittest.main()