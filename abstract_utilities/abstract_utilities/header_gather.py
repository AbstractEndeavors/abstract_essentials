import os
import importlib
import inspect
from read_write_utils import *
def gather_header_docs(folder_path):
    header_docs = ""

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py"):
            print(file_name)
            try:
                header_docs += read_from_file(file_name).split('"""')[1].split('"""')[0]
                
            except:
                print()
    print(header_docs)

# Usage example
folder_path = os.getcwd() # Replace with the path to your folder
header_docs = gather_header_docs(folder_path)
print(header_docs)
