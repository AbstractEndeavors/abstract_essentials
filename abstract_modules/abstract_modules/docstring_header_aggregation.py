import os
import importlib
import inspect

def gather_header_docs(folder_path):
    header_docs = ""

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]  # Remove the ".py" extension
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, "__doc__"):
                    docstring = inspect.getdoc(obj)
                    if docstring:
                        header_docs += f"{name}:\n{docstring}\n\n"

    return header_docs

# Usage example
folder_path = "/path/to/your/folder"  # Replace with the path to your folder
header_docs = gather_header_docs(folder_path)
print(header_docs)
