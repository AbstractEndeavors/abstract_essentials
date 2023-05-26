import os
import ast

def get_functions(file_path):
    functions = []

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return functions

def get_shared_functions(directory_map):
    shared_functions = {}

    for directory, data in directory_map.items():
        file_functions = data['file_functions']

        for file, functions in file_functions.items():
            for function in functions:
                if function in shared_functions:
                    shared_functions[function].append((file, directory))
                else:
                    shared_functions[function] = [(file, directory)]

    return shared_functions

def get_directory_map(folder_path):
    directory_map = {}

    for root, dirs, files in os.walk(folder_path):
        file_sizes = []
        folder_sizes = []
        num_items = 0
        file_functions = {}

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_sizes.append(os.path.getsize(file_path))
                functions = get_functions(file_path)
                file_functions[file] = functions
                num_items += 1

        folder_sizes = [os.path.getsize(os.path.join(root, folder)) for folder in dirs]
        num_items += len(dirs)

        directory_map[root] = {
            'file_size': sum(file_sizes),
            'folder_size': sum(folder_sizes),
            'num_items': num_items,
            'file_functions': file_functions
        }

    return directory_map

# Specify the folder path you want to scan
folder_path = '/home/hmmm/Documents/python_scripts/modules/'

directory_map = get_directory_map(folder_path)
input(directory_map)
# Get shared functions
shared_functions = get_shared_functions(directory_map)
input(shared_functions)
# Print shared functions
for function, files in shared_functions.items():
    print(f"Function: {function}")
    print("Files:")
    for file, directory in files:
        print(f"  - {file} ({directory})")
    print('---')
