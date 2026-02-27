from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type is not TextType.TEXT:
      new_nodes.append(node)
    else:
      split_node = node.text.split(delimiter)
      if len(split_node) % 2 != 1:
        raise Exception("invalid markdown syntax")
      for i in range(0, len(split_node)):
        if i % 2 == 0:
          new_nodes.append(TextNode(split_node[i], TextType.TEXT))
        else:
          new_nodes.append(TextNode(split_node[i], text_type))
  return new_nodes
