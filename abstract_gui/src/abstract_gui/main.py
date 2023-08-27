import os
import sys
import importlib.util

excluded_files = ['__pycache__', 'main.py', '__init__.py']
excluded_directories = ['__pycache__']

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_filtered_files(directory):
    modules = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item not in excluded_files:
            if item_path.endswith('.py'):
                modules.append(import_module_from_file(item_path))
        elif os.path.isdir(item_path) and item not in excluded_directories:
            modules.extend(get_filtered_files(item_path))
    return modules

def main():
    print("Hello, this is abstract_gui.")
    # You can import and use other modules or functions of abstract_utilities here.
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)

    # Add the abstract_gui module's parent directory to the Python system path
    module_directory = os.path.join(directory_path, 'src')
    sys.path.append(module_directory)

    # Import the entire abstract_gui module
    from abstract_gui import *

    # Now you can use functions or classes from the abstract_gui module directly
    # For example:
    # gui_instance = abstract_gui.AbstractGUI()
    # gui_instance.show()

if __name__ == "__main__":
    main()
