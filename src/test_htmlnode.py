import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):



    def test_props_to_html(self):
        node = HTMLNode("p", "ewan", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })

        html = node.props_to_html()

        self.assertEqual(html, ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "ewan", None, None)

        html = node.props_to_html()

        self.assertEqual("", "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode("p", "ewan", None, {})
        
        html = node.props_to_html()

        self.assertEqual("", "")
        self.assertEqual(node.props, {})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
