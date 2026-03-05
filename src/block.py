from enum import Enum

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
  if (
    block.startswith("# ") or
    block.startswith("## ") or
    block.startswith("### ") or
    block.startswith("#### ") or
    block.startswith("##### ") or
    block.startswith("###### ")
    ):
    return BlockType.HEADING
  if block.startswith("```"):
    block_lines = block.split("\n")
    if block_lines[-1] == "```":
      return BlockType.CODE
  if block.startswith(">"):
    is_quote_block = True
    block_lines = block.split("\n")
    for line in block_lines:
      if not line.startswith(">"):
        is_quote_block = False
    if is_quote_block:
      return BlockType.QUOTE
  if block.startswith("- "):
    is_unordered_list_block = True
    block_lines = block.split("\n")
    for line in block_lines:
      if not line.startswith("- "):
        is_unordered_list_block = False
    if is_unordered_list_block:
      return BlockType.UNORDERED_LIST
  if block.startswith("1. "):
    is_ordered_list_block = True
    block_lines = block.split("\n")
    for i in range(0, len(block_lines)):
      if not block_lines[i].startswith(f"{str(i + 1)}. "):
        is_ordered_list_block = False
    if is_ordered_list_block:
      return BlockType.ORDERED_LIST
  return BlockType.PARAGRAPH