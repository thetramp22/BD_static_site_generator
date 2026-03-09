import os
import shutil
from util import generate_pages_recursive

public_filepath = "./public"
static_filepath = "./static"

def main():
  if os.path.exists(public_filepath):
    shutil.rmtree(public_filepath)
    os.mkdir(public_filepath)
  else:    
    os.mkdir(public_filepath)
  copy_folder_contents(static_filepath, public_filepath)
  generate_pages_recursive("content", "template.html", "public")

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