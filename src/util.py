from textnode import *
import re
from block import *
from htmlnode import *
import os
from pathlib import Path

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

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  new_children = []
  for block in blocks:
    block_type = block_to_block_type(block)
    if block_type == BlockType.CODE:
      converted_block = markdown_syntax_to_html_syntax(block)
      code_block_node = text_node_to_html_node(TextNode(converted_block, TextType.CODE))
      block_node = ParentNode("pre", [code_block_node])
    else:
      children = text_to_childern(block)
      block_node = create_block_html_node(block_type, children)
      if block_node.tag == "h":
        block_node.tag += set_heading_type(markdown)
    new_children.append(block_node)
  return ParentNode("div", new_children, )

# this function needs to convert  markdown syntax to html syntax before calling text_to_textnodes
def text_to_childern(text):
  converted_text = markdown_syntax_to_html_syntax(text)
  textnodes = text_to_textnodes(converted_text)
  htmlnodes = []
  for textnode in textnodes:
    htmlnode = text_node_to_html_node(textnode)
    htmlnodes.append(htmlnode)
  return htmlnodes

def create_block_html_node(block_type, children):
  match block_type:
    case BlockType.QUOTE:
      return ParentNode("blockquote", children)
    case BlockType.UNORDERED_LIST:
      return ParentNode("ul", children)
    case BlockType.ORDERED_LIST:      
      return ParentNode("ol", children)
    case BlockType.CODE:
      return ParentNode("code", children)
    case BlockType.HEADING:
      return ParentNode("h", children)
    case BlockType.PARAGRAPH:
      return ParentNode("p", children)

def markdown_syntax_to_html_syntax(markdown):
  block_type = block_to_block_type(markdown)
  match block_type:
    case BlockType.QUOTE:
      lines = markdown.split("\n")
      new_lines = []
      for line in lines:
        markdown_removed = line[2:]
        new_lines.append(markdown_removed)
      new_block = " ".join(new_lines)
      return new_block
    case BlockType.UNORDERED_LIST:
      lines = markdown.split("\n")
      new_lines = []
      for line in lines:
        markdown_removed = line[2:]
        html_added = "<li>" + markdown_removed + "</li>"
        new_lines.append(html_added)
      new_block = "".join(new_lines)
      return new_block
    case BlockType.ORDERED_LIST:
      lines = markdown.split("\n")
      new_lines = []
      for line in lines:
        markdown_removed = line[3:]
        html_added = "<li>" + markdown_removed + "</li>"
        new_lines.append(html_added)
      new_block = "".join(new_lines)
      return new_block
    case BlockType.HEADING:
      heading_parts = markdown.split(" ", maxsplit=1)
      return heading_parts[1]
    case BlockType.PARAGRAPH:
      return markdown.replace("\n", " ")
    case BlockType.CODE:
      lines = markdown.split("\n")
      new_block = "\n".join(lines[1:-1])
      new_block += "\n"
      return new_block
    
def set_heading_type(markdown):
      heading_parts = markdown.split(" ", maxsplit=1)
      heading_syntax = heading_parts[0]
      heading_type = str(len(heading_syntax))
      return heading_type

def extract_title(markdown):
  lines = markdown.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[2:].strip()
  raise Exception("no title found")

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  with open(from_path) as f:
    markdown = f.read()
  with open(template_path) as g:
    template = g.read()
  content = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)
  document = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
  dest_dir_path = os.path.dirname(dest_path)
  if dest_dir_path != "":
    os.makedirs(dest_dir_path, exist_ok=True)
  with open(dest_path, "w") as f:
    f.write(document)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  dir_contents = os.listdir(dir_path_content)
  for item in dir_contents:
    item_path = os.path.join(dir_path_content, item)
    if os.path.isfile(item_path):
      dest_item_path = Path(os.path.join(dest_dir_path, item)).with_suffix(".html")
      generate_page(item_path, template_path, dest_item_path)
    else:
      new_dir_path_content = item_path
      new_dest_dir_path = os.path.join(dest_dir_path, item)
      generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)