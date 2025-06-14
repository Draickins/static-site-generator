import os
import shutil
import sys

from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Deleting {dir_path_docs} directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print(f"Copying static files to {dir_path_docs} directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print("Generating pages from content directory...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_docs,
        basepath,
    )

    print("Site generation complete!")

if __name__ == "__main__":
    main()
