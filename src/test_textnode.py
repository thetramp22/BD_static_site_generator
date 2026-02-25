import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_text_not_eq(self):
    node = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is a different text node", TextType.TEXT)
    self.assertNotEqual(node, node2)

  def test_text_type_not_eq(self):
    node = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is a text node", TextType.LINK)
    self.assertNotEqual(node, node2)

  def test_url_not_eq(self):
    node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
    self.assertNotEqual(node, node2)

if __name__ == "__main__":
  unittest.main()