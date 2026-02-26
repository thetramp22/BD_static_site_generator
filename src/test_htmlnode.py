import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
  def test_props_to_html_two_props(self):
    node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(
      node.props_to_html(),
      ' href="https://www.google.com" target="_blank"',
    )

  def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

  def test_props_to_html_empty_dict(self):
      node = HTMLNode(props={})
      self.assertEqual(node.props_to_html(), "")

  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a(self):
     node = LeafNode("a", "click here", props={"href": "https://www.google.com"})
     self.assertEqual(node.to_html(), '<a href="https://www.google.com">click here</a>')

  def test_leaf_to_html_no_tag(self):
     node = LeafNode(None, "just this")
     self.assertEqual(node.to_html(), "just this")

  def test_leaf_to_html_no_value(self):
     node = LeafNode("p", None)
     with self.assertRaises(ValueError):
        node.to_html()