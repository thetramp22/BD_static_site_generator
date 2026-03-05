import unittest
from block import *

class TestBlock(unittest.TestCase):
  def test_block_to_block_type_heading(self):
    block = "### Heading3"
    result = block_to_block_type(block)
    self.assertEqual(BlockType.HEADING, result)

  def test_block_to_block_type_wrong_heading(self):
    block = "####### invalid heading should return paragraph"
    result = block_to_block_type(block)
    self.assertEqual(BlockType.PARAGRAPH, result)

  def test_block_to_block_type_code(self):
    block = """```
here is some code
here is more code
here is the last code
```"""
    result = block_to_block_type(block)
    self.assertEqual(BlockType.CODE, result)

  def test_block_to_block_type_quote(self):
    block = """>here is some quote
>here is more quote
>here is the last quote"""
    result = block_to_block_type(block)
    self.assertEqual(BlockType.QUOTE, result)

  def test_block_to_block_type_unordered_list(self):
    block = """- here is some list
- here is more list
- here is the last list"""
    result = block_to_block_type(block)
    self.assertEqual(BlockType.UNORDERED_LIST, result)

  def test_block_to_block_type_ordered_list(self):
    block = """1. here is some list
2. here is more list
3. here is the last list"""
    result = block_to_block_type(block)
    self.assertEqual(BlockType.ORDERED_LIST, result)

if __name__ == "__main__":
  unittest.main()