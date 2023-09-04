"""
path_utils.py

This module provides a collection of utility functions related to file and directory path management. 
Its features include, but are not limited to:

Usage:
    import abstract_utilities.path_utils as path_utils

- Determining appropriate file path separators based on the operating system.
- Joining paths using the correct file path separator.
- Fetching the current working directory and user's home folder.
- Checking if a path corresponds to a file or directory and if they exist.
- Fetching file sizes and determining the size of directories.
- Creating multiple nested directories if they do not exist.
- Retrieving creation time of files.
- Converting sizes to GB with options for truncation.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import os
import platform
from pathlib import Path
def get_os_info():
    """
    Get Operating System Information

    This function retrieves information about the current operating system, including its name and bit size.

    Returns:
    - os_info (dict): A dictionary containing the operating system information.
                      Keys:
                      - "operating_system" (str): The name of the operating system (e.g., "Windows", "Linux", "Darwin").
                      - "bit_size" (str): The bit size of the operating system (e.g., "32bit", "64bit").

    Example:
    os_info = get_os_info()
    print("Operating System:", os_info["operating_system"])
    print("Bit Size:", os_info["bit_size"])
    """
    os_name = platform.system()
    bit_size = platform.architecture()[0]
    return {"operating_system": os_name, "bit_size": bit_size}
def get_dirs(path):
    """
    Get List of Immediate Subdirectories in a Path

    This function uses the os.walk method to traverse through a directory tree and returns a list of immediate subdirectories
    within the specified path.

    Parameters:
    - path (str): The path for which subdirectories need to be retrieved.

    Returns:
    - subdirectories (list): A list of immediate subdirectories within the specified path.

    Example:
    subdirs = get_dirs("/path/to/directory")
    print("Immediate Subdirectories:", subdirs)
    """
    from os import walk
    for (dirpath, dirnames, filenames) in walk(path):
        return dirnames
def sanitize_filename(name: str):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
    name (str): Filename to sanitize.
    
    Returns:
    str: Sanitized filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)
def get_directory(file_path: str) -> str:
    """
    Extracts and returns the directory path from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The directory path extracted from the file path.
    """
    return file_path[:-len(get_base_name(file_path))]

def get_base_name(file_path: str) -> str:
    """
    Extracts and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file.
    """
    return os.path.basename(file_path)
def split_text(string: str) -> tuple:
    """
    Splits a string into its base name and extension and returns them as a tuple.

    Args:
        string (str): A string to be split, typically representing a file name.

    Returns:
        tuple: A tuple containing the base name and extension of the input string.
    """
    return os.path.splitext(string)
def get_ext(file_path: str) -> str:
    """
    Retrieves and returns the extension of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The extension of the file (including the dot).
    """
    return split_text(get_base_name(file_path))[1]
def get_file_name(file_path: str) -> str:
    """
    Retrieves and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file (without extension).
    """
    return split_text(get_base_name(file_path))[0]
def get_slash():
    """
    Returns the appropriate file path separator depending on the current operating system.
    """
    slash = '/'  # Assume a Unix-like system by default
    if slash not in get_current_path():
        slash = '\\'  # Use backslash for Windows systems
    return slash

def simple_path_join(path_A:str, path_B:str):
    """
    Join two paths using the appropriate file path separator.

    Args:
        path_A (str): The first path to join.
        path_B (str): The second path to join.
    
    Returns:
        str: The joined path.
    """
    return os.path.join(str(path_A), str(path_B))

def path_join(path_A, path_B=None):
    """
    Joins two paths or a list of paths using the appropriate file path separator.

    Args:
        path_A (str or list): The first path or list of paths to join.
        path_B (str, optional): The second path to join. Defaults to None.
    
    Returns:
        str: The joined path.
    """
    if path_B is not None:  # If path_B is provided, join path_A and path_B
        return simple_path_join(path_A, path_B)
    if isinstance(path_A, list):  # If path_A is a list, join all paths in the list
        path = path_A[0]
        for k in range(1, len(path_A)):
            path = simple_path_join(path, path_A[k])
        return path

def if_not_last_child_join(path:str,child:str):
    """
    Adds a child path to the given path if it's not already present at the end.

    Args:
        path (str): The parent path.
        child (str): The child path to add.
    
    Returns:
        str: The updated path.
    """
    if path.endswith(child):
        return path
    return simple_path_join(path, child)

def get_current_path():
    """
    Returns the current working directory.
    
    Returns:
        str: The current working directory.
    """
    return os.getcwd()

def get_home_folder():
    """
    Returns the path to the home directory of the current user.
    
    Returns:
        str: The path to the home directory.
    """
    return os.path.expanduser("~")

def is_file(path: str) -> bool:
    """Checks if the provided path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)

def update_global_variable(name: str, value) -> None:
    """Updates the global variable with the provided name and value.

    Args:
        name (str): The name of the global variable.
        value: The value to assign to the global variable.

    Returns:
        None
    """
    globals()[name] = value

def list_directory_contents(path: str) -> list:
    """Returns a list of directory contents or a list with a single file, if the path is a file.

    Args:
        path (str): The path of the directory or file.

    Returns:
        list: A list of directory contents or a list with a single file path.
    """
    if is_file(path):
        return [path]
    elif is_valid_path(path):
        return os.listdir(path)
    return [path]

def trunc(a: float, x: int) -> float:
    """
    Truncates a float number to a specific number of decimal places.

    Args:
        a (float): The number to truncate.
        x (int): The number of decimal places to retain.

    Returns:
        float: The truncated float number.
    """
    temp = str(a)
    for i in range(len(temp)):
        if temp[i] == '.':
            try:
                return float(temp[:i+x+1])
            except:
                return float(temp)
    return float(temp)

def mkGb(k) -> float:
    """
    Converts a value to Gigabytes (GB).

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB.
    """
    return float(float(k)*(10**9))

def mkGbTrunk(k) -> float:
    """
    Converts a value to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(k), 5)

def mkGbTrunFroPathTot(k) -> float:
    """
    Fetches the file size from a path, converts it to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (str): The file path.

    Returns:
        float: The file size converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(s.path.getsize(k)), 5)


def get_abs_name_of_this() -> Path:
    """
    Returns the absolute name of the current module.

    Returns:
        Path: The absolute name of the current module.
    """
    return Path(__name__).absolute()

def createFolds(ls: list) -> None:
    """
    Creates multiple directories.

    Args:
        ls (list): The list of directory paths to create.
    """
    for k in range(len(ls)):
        mkdirs(ls[k])

def mkdirs(path: str) -> str:
    """
    Creates a directory and any necessary intermediate directories.

    Args:
        path (str): The directory path to create.

    Returns:
        str: The created directory path.
    """
    os.makedirs(path, exist_ok=True)
    return path

def file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at the specified path.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def file_exists(file_path: str) -> bool:
    """
    Checks if a file exists at the specified path.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def dir_exists(path: str) -> bool:
    """
    Checks if a directory exists at the specified path.

    Args:
        path (str): The path to the directory.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(path)
def file_size(path:str):
    if is_file(path):
        return os.path.getsize(path)
    return 0
def get_file_create_time(path):
    return os.path.getctime(path)
def get_size(path: str) -> int:
    """
    Calculates the size of a file or a directory.

    Args:
        path (str): The path of the file or directory.

    Returns:
        int: The size of the file or directory in bytes.
    """
    total_size = file_size(path)
    if dir_exists(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                total_size += file_size(simple_path_join(dirpath, file))
    return total_size

def get_total_size(folder_path: str) -> int:
    """
    Calculates the total size of a directory and its subdirectories.

    Args:
        folder_path (str): The path of the directory.

    Returns:
        int: The total size of the directory and its subdirectories in bytes.
    """
    total_size = 0
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            total_size += get_size(item_path)
    return total_size
