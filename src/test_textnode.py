import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestTextNode(unittest.TestCase):

    def test_eq_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_node_is_image(self):
        node = TextNode("image", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        self.assertNotEqual(node.url, None)

    def test_url_node_is_link(self):
        node = TextNode("link", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        self.assertNotEqual(node.url, None)


    def test_eq_node_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertEqual(node, node2)

    def test_not_eq_node(self):
        node = TextNode("a", TextType.TEXT)
        node2 = TextNode("b", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_node_with_not_same_text(self):
        node = TextNode("a", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        node2 = TextNode("b", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        self.assertNotEqual(node, node2)

    def test_not_eq_node_with_not_same_type(self):
        node = TextNode("a", TextType.IMAGE, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        node2 = TextNode("a", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        self.assertNotEqual(node, node2)

    def test_not_eq_node_with_not_same_url(self):
        node = TextNode("a", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        node2 = TextNode("a", TextType.LINK, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee0")

        self.assertNotEqual(node, node2)

    def test_url_node_not_link_or_image(self):
        node = TextNode("image", TextType.ITALIC, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")

        self.assertNotEqual(node.url, None)

    def test_split_nodes_delimiter_more_than_one_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `bolded phrase` in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)

        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_with_bold_text(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_with_italic_text(self):
        node = TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_with_code_text(self):
        node = TextNode("This is text with a `code phrase` in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code phrase", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT)
        ])






if __name__ == "__main__":
    unittest.main()
