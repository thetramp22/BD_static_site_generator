from enum import Enum

class TextType(Enum):
  TEXT = "text"
  BOLD = "**Bold text**"
  ITALIC = "_Italic text_"
  CODE = "`Code text`"
  LINK = "[anchor text](url)"
  IMAGE = "![alt text](url)"

class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, other):
    pass

  def __repr__(self):
    pass