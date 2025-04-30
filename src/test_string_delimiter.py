import unittest

from textnode import TextNode, TextType
from string_delimiter import split_nodes_delimiter

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

if __name__ == "__main__":
    unittest.main()