import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
  def test_props_to_html_two_props(self):
    node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(
      node.props_to_html(),
      ' href="https://www.google.com" target="_blank"',
    )

# HTMLNode tests

  def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

  def test_props_to_html_empty_dict(self):
      node = HTMLNode(props={})
      self.assertEqual(node.props_to_html(), "")

# LeafNode tests

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

  def test_to_html_with_multiple_children(self):
     child_node1 = LeafNode("b", "Bold text")
     child_node2 = LeafNode(None, "Normal text")
     child_node3 = LeafNode("i", "italic text")
     child_node4 = LeafNode(None, "Normal text")
     parent_node = ParentNode("p", [
        child_node1,
        child_node2,
        child_node3,
        child_node4,
     ])
     self.assertEqual(
        parent_node.to_html(), 
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
      )
     
  def test_to_html_with_no_children(self):
    child_node = LeafNode("span", None)
    parent_node = ParentNode("div", [child_node])
    with self.assertRaises(ValueError):
       parent_node.to_html()