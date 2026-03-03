import unittest
from textnode import TextNode, TextType
from util import *

class TestUtil(unittest.TestCase):
  def test_split_nodes_delimiter_bold(self):
    markdown = "This is text with a **bolded phrase** in the middle"
    node = TextNode(markdown, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertEqual(
      new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),
      ]
    )

  def test_split_nodes_delimiter_code(self):
    markdown = "This is text with a `code phrase` in the middle"
    node = TextNode(markdown, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(
      new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code phrase", TextType.CODE),
        TextNode(" in the middle", TextType.TEXT),
      ]
    )

  def test_split_nodes_delimiter_italic(self):
    markdown = "This is text with a _italic phrase_ in the middle"
    node = TextNode(markdown, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    self.assertEqual(
      new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("italic phrase", TextType.ITALIC),
        TextNode(" in the middle", TextType.TEXT),
      ]
    )

  def test_split_nodes_delimiter_no_closing_delimiter(self):
    markdown = "This is text with a _italic phrase in the middle"
    node = TextNode(markdown, TextType.TEXT)
    with self.assertRaises(Exception):
      split_nodes_delimiter([node], "_", TextType.ITALIC)

  def test_split_nodes_delimiter_not_type_text(self):
    node = TextNode("Not a TypeText.TEXT node", TextType.BOLD)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(new_nodes, [node])

  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://www.fake.com)"
    )
    self.assertListEqual([("link", "https://www.fake.com")], matches)

if __name__ == "__main__":
  unittest.main()