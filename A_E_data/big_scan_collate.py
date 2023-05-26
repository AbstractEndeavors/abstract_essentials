import os
import ast
import inspect
from typing import get_type_hints
import difflib
import shutil

def get_functions(file_path):
    with open(file_path, 'r') as file:
        source = file.read()
        
    tree = ast.parse(source)
    functions = {node.name: source[node.lineno - 1:node.end_lineno] for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    return functions

def compare_functions(func1, func2):
  try:
    tree1 = ast.parse(func1)
    tree2 = ast.parse(func2)
    input([tree1,tree2])
    variables1 = [n.id for n in ast.walk(tree1) if isinstance(n, ast.Name)]
    variables2 = [n.id for n in ast.walk(tree2) if isinstance(n, ast.Name)]
    variables_score = 3 if set(variables1) == set(variables2) else 0
    lines_score = 3 if len(func1.splitlines()) == len(func2.splitlines()) else 0
    length_score = 3 if abs(len(func1) - len(func2)) / max(len(func1), len(func2)) <= 0.1 else (2 if abs(len(func1) - len(func2)) / max(len(func1), len(func2)) <= 0.15 else 0)
    nested_score = 3 if not any(isinstance(n, ast.FunctionDef) for n in ast.walk(tree1) and n in ast.walk(tree2)) else 0
    sig1 = inspect.signature(eval(func1))
    sig2 = inspect.signature(eval(func2))
    type_hints1 = get_type_hints(eval(func1))
    type_hints2 = get_type_hints(eval(func2))
    signature_score = 3 if sig1.parameters == sig2.parameters and type_hints1 == type_hints2 else 0

    return variables_score + lines_score + length_score + nested_score + signature_score
  except:
    print(func1,func2)
    return 0
def refactor_function(func_name, module_path):
  print(func_name)
  with open(module_path, 'r+') as file:
        content = file.read()
        new_content = content.replace(
            f'def {func_name}',
            f'from utilities import {func_name}'
        )
        file.seek(0)
        file.write(new_content)
        file.truncate()

def refactor_module(module_path, utility_path):
    utility_functions = get_functions(utility_path)
    module_functions = get_functions(module_path)
    
    for name, func in module_functions.items():
        if name in utility_functions:
            score = compare_functions(func, utility_functions[name])
            if score >= 9:
                refactor_function(name, module_path)

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
# Specify the folder path you want to scan
folder_path = '/home/hmmm/Documents/python_scripts/modules/abstract_essentials'
utility_path = '/home/hmmm/Documents/python_scripts/modules/abstract_essentials/abstract_utilities/abstract_utilities/functions.py'

# Copy the entire parent directory
shutil.copytree(folder_path, '/home/hmmm/Documents/python_scripts/modules/abstract_backup')

# Get the directory map
directory_map = get_directory_map(folder_path)
input(directory_map)
# Get shared functions
shared_functions = get_shared_functions(directory_map)
input(shared_functions)
# Iterate over each file and refactor it
for root, data in directory_map.items():
    for file, functions in data['file_functions'].items():
        file_path = os.path.join(root, file)
        refactor_module(file_path, utility_path)
