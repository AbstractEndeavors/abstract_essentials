"""
read_write_utils.py

This module, 'read_write_utils.py', provides utility functions for reading and writing to files.
These include functions to:

Usage:
    import abstract_utilities.read_write_utils as read_write_utils

1. Write content to a file.
2. Read content from a file.
3. Check if a string has a file extension.
4. Read from or write to a file depending on the number of arguments.
5. Create a file if it does not exist, then read from it.

Each function includes a docstring to further explain its purpose, input parameters, and return values.
"""
import os
def write_to_file(filepath: str, contents: str = '') -> str:
    """
    Write contents to a file. If the file does not exist, it is created.
    
    Args:
        filepath: The path of the file to write to.
        contents: The content to write to the file.
        
    Returns:
        The contents that were written to the file.
    """
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(contents)
    return contents

def read_from_file(filepath: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        filepath: The path of the file to read from.
        
    Returns:
        The contents of the file.
    """
    with open(filepath, 'r', encoding='UTF-8') as f:
        return f.read()

def is_file_extension(obj: str) -> bool:
    """
    Check if a string has a file extension.
    
    Args:
        obj: The string to check.
        
    Returns:
        True if the string has a file extension, False otherwise.
    """
    return len(obj) >= 4 and '.' in obj[-4:-3]

def read_or_write(path: str, contents: str = None) -> str:
    """
    Read from or write to a file depending on the number of arguments.
    
    Args:
        path: The path of the file to read from or write to.
        contents: The content to write to the file. If this argument is not provided, the function will read from the file instead.
        
    Returns:
        The contents of the file.
    """
    if contents is None:
        return read_from_file(path)
    else:
        if is_file_extension(contents):
            contents, path = path, contents
        return write_to_file(path, contents)
    
def create_and_read_file(filepath: str, contents: str = '') -> str:
    """
    Create a file if it does not exist, then read from it.
    
    Args:
        filepath: The path of the file to create and read from.
        contents: The content to write to the file if it does not exist.
        
    Returns:
        The contents of the file.
    """
    # If the file does not exist, write the contents to it
    if not os.path.isfile(filepath):
        write_to_file(filepath, contents)
    return read_from_file(filepath)
