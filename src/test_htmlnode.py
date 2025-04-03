import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        node = HTMLNode("a", "click me", None, {"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
    
    def test_props_with_multiple_attributes(self):
        node = HTMLNode(
            "a", 
            "click me", 
            None, 
            {"href": "https://www.example.com", "target": "_blank", "class": "link"}
        )
        props_html = node.props_to_html()
        self.assertIn(' href="https://www.example.com"', props_html)
        self.assertIn(' target="_blank"', props_html)
        self.assertIn(' class="link"', props_html)

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "Hello, world!", None, None)
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()
