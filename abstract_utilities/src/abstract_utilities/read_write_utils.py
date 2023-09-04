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
import os

# File and Directory Operations
os.rename(src, dst)            # Rename a file or directory
os.remove(path)               # Remove a file
os.unlink(path)               # Alias for os.remove()
os.rmdir(path)                # Remove an empty directory
os.makedirs(path)             # Create directories recursively
os.makedirs(path, exist_ok=True)  # Create directories, ignore if exists
os.mkdir(path)                # Create a single directory
os.listdir(path)              # List files and directories in a path
os.chdir(path)                # Change current working directory
os.getcwd()                   # Get current working directory
os.stat(path)                 # Get file/directory information
os.lstat(path)                # Get symbolic link information
os.symlink(src, dst)          # Create a symbolic link
os.readlink(path)             # Read the target of a symbolic link
os.getcwd()                   # Get current working directory
os.chdir(path)                # Change current working directory

# File and Directory Information
os.path.exists(path)          # Check if a path exists
os.path.isfile(path)          # Check if a path points to a file
os.path.isdir(path)           # Check if a path points to a directory
os.path.islink(path)          # Check if a path points to a symbolic link
os.path.abspath(path)         # Get the absolute path of a file/directory
os.path.basename(path)        # Get the base name of a path
os.path.dirname(path)         # Get the directory name of a path
os.path.join(path1, path2, ...)  # Join path components into a single path

# File Permissions
os.chmod(path, mode)          # Change file permissions
os.access(path, mode)         # Check if a file is accessible with given mode

# File Times
os.path.getatime(path)        # Get last access time of a file
os.path.getmtime(path)        # Get last modification time of a file
os.path.getctime(path)        # Get creation time of a file
os.utime(path, times)         # Set access and modification times

# Working with Paths
os.path.split(path)           # Split a path into (head, tail)
os.path.splitext(path)        # Split a path into (root, ext)
os.path.normpath(path)        # Normalize a path (e.g., convert slashes)

# Other
os.path.samefile(path1, path2)  # Check if two paths refer to the same file

# Directory Traversal
for root, dirs, files in os.walk(top, topdown=True):
    # Traverse a directory tree, yielding root, dirs, and files lists

# Temporary Files and Directories
import tempfile
tempfile.mkstemp()            # Create a temporary file
tempfile.mkdtemp()            # Create a temporary directory
tempfile.TemporaryFile()      # Create a temporary file object

# Environment Variables
os.environ                    # Dictionary of environment variables
os.environ['VAR_NAME']        # Access an environment variable
os.environ.get('VAR_NAME')    # Access an environment variable (with default)

# Path Manipulation
os.path.abspath(path)         # Convert relative path to absolute path
os.path.join(path1, path2, ...)  # Join paths together
os.path.split(path)           # Split a path into directory and filename
os.path.dirname(path)         # Get the directory part of a path
os.path.basename(path)        # Get the filename part of a path
os.path.exists(path)          # Check if a path exists
os.path.isfile(path)          # Check if a path points to a file
os.path.isdir(path)           # Check if a path points to a directory

# File Permissions
os.chmod(path, mode)          # Change file permissions

# Miscellaneous
os.getpid()                   # Get the current process ID
os.getlogin()                 # Get the name of the logged-in user

"""
import os
def write_to_file(*args, file_path: str = None, contents: any = None, **kwargs):
    """
    Write contents to a file. If the file does not exist, it is created.

    Args:
        filepath: The path of the file to write to.
        contents: The content to write to the file.
        
    Returns:
        The contents that were written to the file.
    """
    if kwargs:
        if 'filepath' in kwargs.keys():
            file_path = kwargs['filepath']
    if not args:
        if file_path is None or contents is None:
            print("Missing file path or contents.")
            return
    elif len(args) > 1:
        print("Too many arguments.")
        return
    else:
        if file_path is None:
            path, file = os.path.split(args[0])
            _, ext = os.path.splitext(file)
            if os.path.isdir(path) and ext:
                file_path = args[0]
            else:
                contents = args[0]
        elif contents is None:
            contents = args[0]
        else:
            print("Redundant arguments.")
            return

    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(contents)

    return contents


def read_from_file(*args, file_path:str=None, **kwargs) -> str:
    """
    Read the contents of a file.
    
    Args:
        filepath: The path of the file to read from.
        
    Returns:
        The contents of the file.
    """
    if kwargs:
        if len(kwargs)>1:
            print("Too many arguments.")
            return
        if 'filepath' in kwargs.keys():
            file_path = kwargs['filepath']
        elif file_path is None:
            file_path = list(kwargs.values())[0]
    if args:
        if len(args)>1:
            print("Too many arguments.")
            return
        if file_path is None:
            file_path = args[0] 
    if file_path is None:
        path, file = os.path.split(args[0])
        _, ext = os.path.splitext(file)
        if os.path.isdir(path) and ext:
            file_path = args[0]
        else:
            contents = args[0]
    if not os.path.isfile(file_path):
        print("invalid file path.")
        return 
    with open(file_path, 'r', encoding='UTF-8') as f:
        return f.read()
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
def is_file_extension(obj: str) -> bool:
    """
    Check if a string has a file extension.
    
    Args:
        obj: The string to check.
        
    Returns:
        True if the string has a file extension, False otherwise.
    """
    return len(obj) >= 4 and '.' in obj[-4:-3]

def create_and_read_file(*args, file_path: str = None, contents: str = '', **kwargs) -> str:
    """
    Create a file if it does not exist, then read from it.
    
    Args:
        file_path: The path of the file to create and read from.
        contents: The content to write to the file if it does not exist.
        
    Returns:
        The contents of the file.
    """
    if kwargs:
        if 'file_path' in kwargs:
            file_path = kwargs['file_path']
    if not args:
        if file_path is None or contents is None:
            print("Missing file path or contents.")
            return
    elif len(args) > 2:
        print("Too many arguments.")
        return
    else:
        if file_path is None:
            path, file = os.path.split(args[0])
            _, ext = os.path.splitext(file)
            if os.path.isdir(path) and ext:
                file_path = args[0]
            else:
                contents = args[0]
        elif contents is None:
            contents = args[1]
    
    # If the file does not exist, write the contents to it
    if not os.path.isfile(file_path):
        write_to_file(file_path, contents)
    
    return read_from_file(file_path)

def delete_file(file_path:str):
    if os.path.isfile(file_path):
        os.remove(file_path)

