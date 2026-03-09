import os
import shutil
from util import generate_pages_recursive
import sys

docs_filepath = "./docs"
static_filepath = "./static"
basepath = "/"

if len(sys.argv) > 1:
    basepath = sys.argv[1]

def main():
  if os.path.exists(docs_filepath):
    shutil.rmtree(docs_filepath)
    os.mkdir(docs_filepath)
  else:    
    os.mkdir(docs_filepath)
  copy_folder_contents(static_filepath, docs_filepath)
  generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def copy_folder_contents(source, destination):
  folder_contents = os.listdir(source)
  for item in folder_contents:
    item_filepath = os.path.join(source, item)
    if os.path.isfile(item_filepath):
      destination_filepath = os.path.join(destination, item)
      shutil.copy(item_filepath, destination_filepath)
    else:
      new_destination = os.path.join(destination, item)
      os.mkdir(new_destination)
      copy_folder_contents(item_filepath, new_destination)

main()