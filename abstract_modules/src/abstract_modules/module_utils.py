import os
import ast
import re
import sys
import importlib
import inspect
from abstract_gui import get_browser
from abstract_utilities.json_utils import dump_to_file,create_and_read_json
import pkg_resources
def save_alias_map(data):
    """
    Save data to alias_map.json.
    
    Args:
        data (dict): The alias map data to save.
    """
    dump_to_file(file_path=os.path.join(os.path.dirname(__file__), 'alias_map.json'),json_data=data)
def load_alias_map():
    """
    Load data from alias_map.json.
    
    Returns:
        dict: The loaded alias map data.
    """
    return create_and_read_json(file_path=os.path.join(os.path.dirname(__file__), 'alias_map.json'),json_data={"ALIAS":{},"NEVER":[],"DEFAULT":[]})

def map_to_actual_name(module_name):
    ALIAS_MAP = load_alias_map()
    return ALIAS_MAP["ALIAS"].get(module_name, module_name)
def scan_folder_for_required_modules(folder_path=None,exclude:(str or list)=[],exclue_default_modules:bool=True):
    """
    Scan the specified folder for Python files and create a list of necessary Python modules.
    :param folder_path: The path of the folder to scan. If None, a folder will be picked using a GUI window.
    :return: A list of required Python modules based on all Python files found in the folder.
    """
    exclude=list(exclude)
    if folder_path is None:
        folder_path = get_browser(
            title="Please choose the destination for your import scripts to be analyzed",
            initial_folder=os.getcwd()
        )
    
    required_modules = set()

    def visit_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tree = ast.parse(file.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            required_modules.add(name.name)
                    elif isinstance(node, ast.ImportFrom):
                        module_parts = node.module.split('.')
                        if node.level > 0:
                            module_parts = ['.'.join(module_parts[:node.level])] + module_parts[node.level:]
                        module_name = '.'.join(module_parts)
                        for name in node.names:
                            required_modules.add(f'{module_name}.{name.name}')
        except SyntaxError:
            # Skip files with syntax errors
            pass

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                visit_file(file_path)
       
    # Update the required_modules to include submodules
    updated_required_modules = set()
    for module in required_modules:
        if module not in exclude:
            parts = module.split('.')
            for i in range(len(parts)):
                updated_required_modules.add('.'.join(parts[:i+1]))
    if exclue_default_modules:
        new_modules = []
        for each in updated_required_modules:
            if each not in sys.builtin_module_names:
                new_modules.append(each)
        updated_required_modules =new_modules
    required_list = list(updated_required_modules)
    return required_list
def get_installed_versions(install_requires):
    """
    Get the version numbers of the installed Python modules listed in 'install_requires'.
    :param install_requires: A list of Python module names with optional version constraints.
    :return: A tuple of (list of module names with their version numbers appended, list of ignored dependencies).
    """
    installed_versions = []
    ignored_dependencies = []  # to capture modules that are ignored

    for requirement in install_requires:
        module_name = map_to_actual_name(requirement.split('>=')[0].split('==')[0].strip())
        
        # Validate module_name and skip if not valid
        if not is_valid_package_name(module_name):
            continue

        try:
            version = pkg_resources.get_distribution(module_name).version
        except pkg_resources.DistributionNotFound:
            # Module not found, capture it and continue
            ignored_dependencies.append(module_name)
            continue

        # Append the version number to the module name in the required format
        if '>=' in requirement:
            installed_versions.append(f'{module_name}>={version}')
        elif '==' in requirement:
            installed_versions.append(f'{module_name}=={version}')
        else:
            installed_versions.append(f'{module_name}>={version}')

    return installed_versions, ignored_dependencies
def is_valid_package_name(package_name):
    """
    Check if a given package name is a valid Python package name.
    
    Args:
        package_name (str): Package name to be validated.
        
    Returns:
        bool: True if the package name is valid, False otherwise.
    """
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', package_name) is not None

def gather_header_docs(folder_path):
    """
    Gather header documentation from Python modules within a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing Python modules.
        
    Returns:
        str: Concatenated header documentation for classes with docstrings.
    """
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

