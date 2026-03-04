from textnode import *
import re

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

def extract_markdown_images(text):
  images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return images


def extract_markdown_links(text):  
  links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return links

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:    
    if node.text_type is not TextType.TEXT:
      new_nodes.append(node)
    else:
      images = extract_markdown_images(node.text)
      if images == ():
        new_nodes.append(node)
      else:
        current_text = node.text
        for image in images:
          image_alt, image_link = image
          sections = current_text.split(f"![{image_alt}]({image_link})", 1)
          if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
          new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
          current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
  return new_nodes
        

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type is not TextType.TEXT:
      new_nodes.append(node)
    else:
      links = extract_markdown_links(node.text)
      if links == ():
        new_nodes.append(node)
      else:
        current_text = node.text
        for link in links:
          link_text, link_url = link
          sections = current_text.split(f"[{link_text}]({link_url})", 1)
          if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
          new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
          current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
  return new_nodes

def text_to_textnodes(text):
  textnode_to_process = TextNode(text, TextType.TEXT)
  split_bold = split_nodes_delimiter([textnode_to_process], '**', TextType.BOLD)
  split_italic = split_nodes_delimiter(split_bold, '_', TextType.ITALIC)
  split_code = split_nodes_delimiter(split_italic, '`', TextType.CODE)
  split_image = split_nodes_image(split_code)
  result = split_nodes_link(split_image)
  return result

def markdown_to_blocks(markdown):
  blocks = []
  mardown_sections = markdown.split("\n\n")
  for section in mardown_sections:
    stripped_section = section.strip()
    if stripped_section != "":
      blocks.append(stripped_section)
  return blocks