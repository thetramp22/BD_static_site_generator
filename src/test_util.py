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

  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
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
      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
    )

  def test_text_to_textnodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    self.assertEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      new_nodes
    )

  def test_text_to_textnodes_unordered(self):
    text = "This is _text_ with [links](https://boot.dev), ![images](https://i.imgur.com/fJRm4Vk.jpeg), and **elements** in `random` order."
    new_nodes = text_to_textnodes(text)
    self.assertEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.ITALIC),
        TextNode(" with ", TextType.TEXT),
        TextNode("links", TextType.LINK, "https://boot.dev"),
        TextNode(", ", TextType.TEXT),
        TextNode("images", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(", and ", TextType.TEXT),
        TextNode("elements", TextType.BOLD),
        TextNode(" in ", TextType.TEXT),
        TextNode("random", TextType.CODE),
        TextNode(" order.", TextType.TEXT)
      ],
      new_nodes
    )

  def test_text_to_textnodes_not_starting_with_text(self):
    text = "**This text** doesn't start with `text`"
    new_nodes = text_to_textnodes(text)
    self.assertEqual(
      [
        TextNode("This text", TextType.BOLD),
        TextNode(" doesn't start with ", TextType.TEXT),
        TextNode("text", TextType.CODE)
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

  def text_mardown_to_blocks_extra_newlines(self):
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

# markdown_to_html_node and it's helper functions

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

  def test_unordered_list(self):
    md = """
This is an unordered list:

- first item
- second item
- third item 

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is an unordered list:</p><ul><li>first item</li><li>second item</li><li>third item</li></ul></div>",
    )

  def test_ordered_list(self):
    md = """
This is an ordered list:

1. first item
2. second item
3. third item 

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is an ordered list:</p><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>",
    )

# extract title

  def test_extract_title(self):
    md = "# My Title"
    result = extract_title(md)
    self.assertEqual(result, "My Title")

  def test_extract_title_no_title(self):
    md = "This is not a Title"
    with self.assertRaises(Exception):
      extract_title(md)

if __name__ == "__main__":
  unittest.main()